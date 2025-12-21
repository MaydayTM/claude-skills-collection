# Stripe Checkout Setup Command

You are helping set up Stripe checkout integration with Supabase Edge Functions for a web application.

## Context
This command sets up a complete Stripe checkout flow including:
- Frontend checkout button integration
- Supabase Edge Functions for checkout session creation
- Stripe webhook handling for payment confirmation
- Database integration for payment tracking

## Required Information from User

Ask the user for these details BEFORE starting:

1. **Stripe Keys** (from https://dashboard.stripe.com/apikeys):
   - Publishable Key (pk_live_... or pk_test_...)
   - Secret Key (sk_live_... or sk_test_...)
   - Webhook Secret (whsec_...) - Get from https://dashboard.stripe.com/webhooks

2. **Supabase Project**:
   - Project URL (check .env file or ask user)
   - Anon Key (check .env file or ask user)
   - Confirm you can run `npx supabase status` successfully

3. **Product Details**:
   - What products/services are being sold?
   - Price IDs from Stripe (price_...)
   - Product names and descriptions

## Step-by-Step Implementation

### STEP 1: Verify Supabase Connection

```bash
# Check if already linked
npx supabase status

# If not linked, extract PROJECT_REF from .env
grep SUPABASE_URL .env | sed 's/.*https:\/\/\([^.]*\)\.supabase\.co.*/\1/'

# Link project
npx supabase link --project-ref PROJECT_REF
```

### STEP 2: Set Supabase Secrets

```bash
# Set all Stripe secrets in Supabase
npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...

# Add price IDs if needed
npx supabase secrets set STRIPE_PRICE_ID_PRODUCT_1=price_...

# Verify secrets are set
npx supabase secrets list
```

### STEP 3: Create Database Table for Payments

Create migration file:

```sql
-- Create stripe_payments table
CREATE TABLE IF NOT EXISTS stripe_payments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  stripe_session_id text UNIQUE NOT NULL,
  customer_email text,
  customer_name text,
  amount bigint, -- Amount in cents
  currency text DEFAULT 'eur',
  product_type text,
  product_name text,
  status text DEFAULT 'pending', -- pending, completed, failed
  metadata jsonb,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE stripe_payments ENABLE ROW LEVEL SECURITY;

-- Policy: Only authenticated users (admin) can view all payments
CREATE POLICY "Authenticated users can view payments"
  ON stripe_payments FOR SELECT
  TO authenticated
  USING (true);

-- Policy: Service role can insert/update (for Edge Functions)
CREATE POLICY "Service role can manage payments"
  ON stripe_payments FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

-- Indexes for performance
CREATE INDEX idx_stripe_payments_session ON stripe_payments(stripe_session_id);
CREATE INDEX idx_stripe_payments_email ON stripe_payments(customer_email);
CREATE INDEX idx_stripe_payments_status ON stripe_payments(status);
CREATE INDEX idx_stripe_payments_created ON stripe_payments(created_at DESC);
```

Save as `supabase/migrations/YYYYMMDDHHMMSS_add_stripe_payments.sql` and run:
```bash
npx supabase db push
```

### STEP 4: Create Edge Function - Checkout Session

Create `supabase/functions/create-checkout-session/index.ts`:

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'
import Stripe from 'npm:stripe@14'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, x-client-info',
}

Deno.serve(async (req: Request) => {
  // Handle CORS
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders })
  }

  const requestId = crypto.randomUUID()

  try {
    // Initialize Stripe
    const stripeKey = Deno.env.get('STRIPE_SECRET_KEY')
    if (!stripeKey) {
      throw new Error('STRIPE_SECRET_KEY not configured')
    }

    const stripe = new Stripe(stripeKey, {
      apiVersion: '2023-10-16',
      httpClient: Stripe.createFetchHttpClient(),
    })

    // Initialize Supabase
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
      { auth: { persistSession: false } }
    )

    // Parse request
    const { priceId, customerEmail, customerName, metadata } = await req.json()

    if (!priceId) {
      return new Response(
        JSON.stringify({ error: 'priceId is required', requestId }),
        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
      )
    }

    // Create Stripe checkout session
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card', 'bancontact', 'ideal'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'payment',
      success_url: `${req.headers.get('origin')}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${req.headers.get('origin')}/cancel`,
      customer_email: customerEmail,
      metadata: { ...metadata, requestId },
      allow_promotion_codes: true,
    })

    // Save to database
    const { error: dbError } = await supabase
      .from('stripe_payments')
      .insert({
        stripe_session_id: session.id,
        customer_email: customerEmail || 'unknown',
        customer_name: customerName,
        amount: session.amount_total,
        currency: 'eur',
        product_type: metadata?.product_type || 'unknown',
        product_name: metadata?.product_name || 'Unknown Product',
        status: 'pending',
        metadata: { price_id: priceId, ...metadata },
      })

    if (dbError) {
      console.error('[checkout] Database error:', { requestId, dbError })
      // Don't fail - checkout session is created
    }

    return new Response(
      JSON.stringify({ sessionId: session.id, url: session.url, requestId }),
      { status: 200, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (err) {
    console.error('[checkout] Error:', { requestId, error: String(err) })
    return new Response(
      JSON.stringify({ error: 'Internal error', requestId }),
      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

### STEP 5: Create Edge Function - Stripe Webhook

Create `supabase/functions/stripe-webhook/index.ts`:

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'
import Stripe from 'npm:stripe@14'

Deno.serve(async (req: Request) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()

  try {
    const stripeKey = Deno.env.get('STRIPE_SECRET_KEY')
    const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET')

    if (!stripeKey || !webhookSecret) {
      throw new Error('Stripe credentials not configured')
    }

    const stripe = new Stripe(stripeKey, {
      apiVersion: '2023-10-16',
      httpClient: Stripe.createFetchHttpClient(),
    })

    // Verify webhook signature
    const event = stripe.webhooks.constructEvent(body, signature!, webhookSecret)

    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
      { auth: { persistSession: false } }
    )

    // Handle events
    switch (event.type) {
      case 'checkout.session.completed': {
        const session = event.data.object as Stripe.Checkout.Session

        await supabase
          .from('stripe_payments')
          .update({
            status: 'completed',
            updated_at: new Date().toISOString(),
          })
          .eq('stripe_session_id', session.id)

        console.log('[webhook] Payment completed:', session.id)
        break
      }

      case 'payment_intent.payment_failed': {
        const paymentIntent = event.data.object as Stripe.PaymentIntent
        const sessionId = paymentIntent.metadata?.session_id

        if (sessionId) {
          await supabase
            .from('stripe_payments')
            .update({
              status: 'failed',
              updated_at: new Date().toISOString(),
            })
            .eq('stripe_session_id', sessionId)

          console.log('[webhook] Payment failed:', sessionId)
        }
        break
      }
    }

    return new Response(JSON.stringify({ received: true }), { status: 200 })

  } catch (err) {
    console.error('[webhook] Error:', String(err))
    return new Response(JSON.stringify({ error: String(err) }), { status: 400 })
  }
})
```

### STEP 6: Deploy Edge Functions

```bash
# Ensure Docker is running
open -a Docker

# Deploy both functions
npx supabase functions deploy create-checkout-session
npx supabase functions deploy stripe-webhook

# Verify deployment
npx supabase functions list
```

### STEP 7: Configure Stripe Webhook

1. Go to https://dashboard.stripe.com/webhooks
2. Click "Add endpoint"
3. **Endpoint URL**: `https://YOUR_PROJECT_REF.supabase.co/functions/v1/stripe-webhook`
4. **Events to send**:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Click "Add endpoint"
6. Copy the **Signing secret** (whsec_...)
7. Update Supabase secret: `npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_...`

### STEP 8: Frontend Integration

Create a hook `src/hooks/useStripeCheckout.ts`:

```typescript
import { useState } from 'react'

interface CheckoutOptions {
  priceId: string
  customerEmail?: string
  customerName?: string
  metadata?: Record<string, any>
}

export const useStripeCheckout = () => {
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const createCheckout = async (options: CheckoutOptions) => {
    setIsLoading(true)
    setError(null)

    try {
      const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
      const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

      const response = await fetch(`${supabaseUrl}/functions/v1/create-checkout-session`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${anonKey}`,
          'apikey': anonKey,
        },
        body: JSON.stringify(options),
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || 'Checkout failed')
      }

      const { url } = await response.json()
      window.location.href = url // Redirect to Stripe

    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong'
      setError(message)
      console.error('Checkout error:', err)
    } finally {
      setIsLoading(false)
    }
  }

  return { createCheckout, isLoading, error }
}
```

Usage in component:

```typescript
import { useStripeCheckout } from '../hooks/useStripeCheckout'

function ProductPage() {
  const { createCheckout, isLoading } = useStripeCheckout()

  const handleCheckout = () => {
    createCheckout({
      priceId: 'price_1234567890', // Your Stripe price ID
      customerEmail: 'user@example.com',
      metadata: {
        product_type: 'membership',
        product_name: 'Premium Membership',
      },
    })
  }

  return (
    <button onClick={handleCheckout} disabled={isLoading}>
      {isLoading ? 'Loading...' : 'Buy Now'}
    </button>
  )
}
```

### STEP 9: Environment Variables

Update `.env` file:

```bash
# Supabase (already exists)
VITE_SUPABASE_URL=https://PROJECT_REF.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key

# Stripe (FRONTEND - browser safe)
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_...

# Stripe Price IDs (browser safe)
VITE_STRIPE_PRICE_ID_PRODUCT_1=price_...
VITE_STRIPE_PRICE_ID_PRODUCT_2=price_...
```

**IMPORTANT**: Never put `STRIPE_SECRET_KEY` or `STRIPE_WEBHOOK_SECRET` in `.env` - these are set via Supabase secrets only!

### STEP 10: Testing

**Test Mode (recommended first):**
1. Use Stripe test keys (pk_test_... and sk_test_...)
2. Test card: `4242 4242 4242 4242`, any future expiry, any CVC
3. Test the full flow: checkout → payment → webhook → database update

**Production Mode:**
1. Switch to live keys (pk_live_... and sk_live_...)
2. Configure live webhook in Stripe Dashboard
3. Test with real card (use small amount first!)

### STEP 11: Verify Everything Works

**Checklist:**
- [ ] Supabase secrets configured (`npx supabase secrets list`)
- [ ] Edge Functions deployed (`npx supabase functions list`)
- [ ] Stripe webhook configured (check Stripe Dashboard)
- [ ] Database table created (`stripe_payments`)
- [ ] Frontend env vars set (`.env`)
- [ ] Test checkout creates Stripe session
- [ ] Test payment updates database
- [ ] Check Supabase logs: `npx supabase functions logs create-checkout-session`

## Common Issues & Solutions

### Issue: 401 Unauthorized when calling Edge Function
**Solution**: Add Authorization header with Supabase anon key:
```typescript
headers: {
  'Authorization': `Bearer ${anonKey}`,
  'apikey': anonKey,
}
```

### Issue: Webhook signature verification fails
**Solution**:
1. Use `await req.text()` NOT `req.json()` for webhook body
2. Verify `STRIPE_WEBHOOK_SECRET` is set correctly
3. Check webhook is sending to correct URL

### Issue: Database insert fails with RLS error
**Solution**: Edge Function should use `SUPABASE_SERVICE_ROLE_KEY` not `SUPABASE_ANON_KEY`

### Issue: Docker not running error during deployment
**Solution**: `open -a Docker` and wait 30 seconds before deploying

## Success Criteria

When complete, you should be able to:
1. ✅ Click checkout button on frontend
2. ✅ Get redirected to Stripe checkout page
3. ✅ Complete test payment
4. ✅ See payment record in `stripe_payments` table
5. ✅ Payment status updates to "completed" via webhook
6. ✅ No errors in Supabase Edge Function logs

## Next Steps After Setup

- Add email confirmation (using Resend or SendGrid)
- Create admin dashboard to view payments
- Add refund functionality
- Implement subscription billing (recurring payments)
- Add invoice generation

---

**IMPORTANT**: Always test thoroughly in test mode before going live with real payments!
