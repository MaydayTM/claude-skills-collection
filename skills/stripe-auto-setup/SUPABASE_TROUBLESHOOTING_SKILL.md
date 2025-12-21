# Supabase Edge Functions & Troubleshooting - Cloud Skill Guide

## Common Issues & Solutions

### 0. Setting Up Supabase for a New Project (AI Onboarding)

When an AI starts working on a new project with Supabase, it needs to establish the connection first. This is THE FIRST STEP before any Edge Function deployment or database work.

#### Quick Project Setup Checklist

```bash
# 1. Check if project is already linked
npx supabase status

# If not linked, you'll see: "Cannot find project ref. Have you run supabase init or link?"
```

#### Option A: Project Already Has Supabase (Most Common)

**When to use**: The project has a `supabase/` folder with Edge Functions or migrations.

```bash
# 1. Find the project reference
# Look in one of these locations:
cat supabase/.temp/project-ref       # First check here
grep SUPABASE_URL .env                # Or extract from URL
# URL format: https://PROJECT_REF.supabase.co

# 2. Link to existing project
npx supabase link --project-ref PROJECT_REF

# Example:
# npx supabase link --project-ref nizujczrkntoolnptxht

# 3. Verify connection
npx supabase status
npx supabase secrets list  # Should show project secrets
```

**How AI should find PROJECT_REF**:
```bash
# Method 1: Check .temp folder
if [ -f "supabase/.temp/project-ref" ]; then
  cat supabase/.temp/project-ref
fi

# Method 2: Extract from .env file
grep -o 'https://[^.]*\.supabase\.co' .env | sed 's/https:\/\/\([^.]*\)\.supabase\.co/\1/'

# Method 3: Check environment variables
env | grep SUPABASE_URL
```

**Environment Variables to Collect**:
```bash
# From .env or .env.local or .env.example
VITE_SUPABASE_URL=https://PROJECT_REF.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# PROJECT_REF example: nizujczrkntoolnptxht
# Extract it from the URL: https://[PROJECT_REF].supabase.co
```

#### Option B: Brand New Supabase Project

**When to use**: Starting from scratch, no Supabase setup yet.

```bash
# 1. Login to Supabase (opens browser)
npx supabase login

# 2. Initialize Supabase in project
npx supabase init

# This creates:
# supabase/
# ├── config.toml
# ├── functions/
# └── migrations/

# 3. Link to existing Supabase project OR create new one
# Option 3a: Link to existing project on Supabase dashboard
npx supabase link --project-ref PROJECT_REF

# Option 3b: Create new project (if you have none)
# Go to https://supabase.com/dashboard and create project manually
# Then link with: npx supabase link --project-ref NEW_PROJECT_REF

# 4. Pull existing schema (if project has data)
npx supabase db pull

# 5. Get your credentials from Supabase Dashboard
# https://supabase.com/dashboard/project/PROJECT_REF/settings/api
```

#### Finding Credentials for New Projects

**Where to find each credential:**

| Credential | Location | Usage |
|-----------|----------|-------|
| `PROJECT_REF` | Supabase Dashboard URL or `.env` file | `https://[PROJECT_REF].supabase.co` |
| `SUPABASE_URL` | Dashboard → Settings → API → Project URL | Frontend & Edge Functions |
| `SUPABASE_ANON_KEY` | Dashboard → Settings → API → Project API keys → `anon` `public` | Frontend (safe for browser) |
| `SUPABASE_SERVICE_ROLE_KEY` | Dashboard → Settings → API → Project API keys → `service_role` | Edge Functions only (admin access) |

**Steps for AI**:
1. Ask user: "I need access to your Supabase project. Can you provide the `SUPABASE_URL` from your `.env` file or Supabase Dashboard?"
2. Extract `PROJECT_REF` from URL
3. Run: `npx supabase link --project-ref PROJECT_REF`
4. Verify with: `npx supabase status`

#### AI Onboarding Script

```bash
#!/bin/bash
# Supabase AI Onboarding Script

echo "🔍 Checking Supabase project setup..."

# Check if supabase folder exists
if [ ! -d "supabase" ]; then
  echo "❌ No supabase/ folder found. Need to initialize."
  echo "Run: npx supabase init"
  exit 1
fi

# Check if already linked
if npx supabase status &>/dev/null; then
  echo "✅ Project already linked!"
  npx supabase status
  exit 0
fi

# Try to find project ref
PROJECT_REF=""

# Method 1: Check .temp folder
if [ -f "supabase/.temp/project-ref" ]; then
  PROJECT_REF=$(cat supabase/.temp/project-ref)
  echo "✅ Found PROJECT_REF in .temp: $PROJECT_REF"
fi

# Method 2: Check .env files
if [ -z "$PROJECT_REF" ]; then
  for env_file in .env .env.local .env.example; do
    if [ -f "$env_file" ]; then
      SUPABASE_URL=$(grep SUPABASE_URL "$env_file" | cut -d= -f2 | tr -d '"' | tr -d "'")
      if [ ! -z "$SUPABASE_URL" ]; then
        PROJECT_REF=$(echo "$SUPABASE_URL" | sed -n 's/.*https:\/\/\([^.]*\)\.supabase\.co.*/\1/p')
        echo "✅ Found PROJECT_REF in $env_file: $PROJECT_REF"
        break
      fi
    fi
  done
fi

# If found, link project
if [ ! -z "$PROJECT_REF" ]; then
  echo "🔗 Linking to project: $PROJECT_REF"
  npx supabase link --project-ref "$PROJECT_REF"

  echo "✅ Verifying connection..."
  npx supabase status

  echo "✅ Setup complete! You can now deploy Edge Functions."
else
  echo "❌ Could not find PROJECT_REF."
  echo "Please provide your SUPABASE_URL from .env or Supabase Dashboard."
  echo "Then run: npx supabase link --project-ref YOUR_PROJECT_REF"
fi
```

#### Common "Not Linked" Errors

| Error Message | Cause | Fix |
|--------------|-------|-----|
| `Cannot find project ref` | Project not linked | Run `npx supabase link --project-ref REF` |
| `Invalid project ref` | Wrong project reference | Check Dashboard URL or `.env` file |
| `You are not logged in` | Not authenticated | Run `npx supabase login` first |
| `Access denied for project` | No permissions | Check you're using correct Supabase account |
| `Project not found` | Typo in ref or project deleted | Verify ref in Supabase Dashboard |

#### Environment File Template for New Projects

Create this `.env.local` file structure:

```bash
# .env.local (DO NOT COMMIT - add to .gitignore)

# Supabase Configuration
VITE_SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here

# For Edge Functions (set via CLI, not in .env)
# npx supabase secrets set SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
# npx supabase secrets set OPENAI_API_KEY=sk-...
# npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
```

Create this `.env.example` file (safe to commit):

```bash
# .env.example (SAFE TO COMMIT - just template)

# Supabase Configuration
VITE_SUPABASE_URL=https://your-project-ref.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here

# Instructions:
# 1. Copy this file to .env.local
# 2. Fill in your actual values from Supabase Dashboard
# 3. Never commit .env.local to git
```

#### Verifying Setup

After linking, verify everything works:

```bash
# 1. Check link status
npx supabase status
# Should show: Status, API URL, GraphQL URL, etc.

# 2. List Edge Functions
npx supabase functions list

# 3. Check secrets
npx supabase secrets list

# 4. Test database connection
npx supabase db pull --dry-run

# 5. If all green, you're ready to deploy!
npx supabase functions deploy FUNCTION_NAME
```

#### Multi-Project Workflow

If working with multiple Supabase projects:

```bash
# Project 1
cd ~/projects/app1
npx supabase link --project-ref project1ref
npx supabase functions deploy my-function

# Project 2
cd ~/projects/app2
npx supabase link --project-ref project2ref
npx supabase functions deploy my-function

# Each project folder maintains its own link in supabase/.temp/
```

#### AI Decision Tree for Project Setup

```
START: AI begins work on new project
│
├─> Does supabase/ folder exist?
│   ├─> NO: Ask user to run `npx supabase init` or create project
│   └─> YES: Continue
│
├─> Run `npx supabase status`
│   ├─> SUCCESS: Already linked ✅ → Proceed with tasks
│   └─> FAIL: Not linked → Continue
│
├─> Search for PROJECT_REF
│   ├─> Check: supabase/.temp/project-ref
│   ├─> Check: .env files for SUPABASE_URL
│   └─> Check: README.md or docs
│
├─> Found PROJECT_REF?
│   ├─> YES: Run `npx supabase link --project-ref REF`
│   └─> NO: Ask user for SUPABASE_URL or PROJECT_REF
│
└─> Verify with `npx supabase status`
    ├─> SUCCESS: ✅ Ready to work
    └─> FAIL: Ask user to check credentials/permissions
```

---

### 1. Edge Function Deployment Issues

#### Problem: "failed to read file: open supabase/functions/*/index.ts: no such file or directory"

**Root Cause**: Supabase CLI uses a different working directory than expected, especially on macOS.

**Solutions**:
```bash
# Option 1: Check current workdir in error message
# If it says "Using workdir /Users/username" instead of project root:
mkdir -p /Users/$(whoami)/supabase/functions/FUNCTION_NAME
cp PROJECT_ROOT/supabase/functions/FUNCTION_NAME/index.ts /Users/$(whoami)/supabase/functions/FUNCTION_NAME/

# Option 2: Remove macOS extended attributes (@ flag in ls -la)
xattr -c supabase/functions/FUNCTION_NAME/index.ts

# Option 3: Ensure you're in project root
cd $(git rev-parse --show-toplevel)
npx supabase functions deploy FUNCTION_NAME
```

**Prevention**:
- Always run Supabase CLI commands from project root
- Check `supabase/.temp/project-ref` exists in your project
- Verify Docker is running: `docker --version`

---

#### Problem: "WARNING: Docker is not running" or "error running container: exit 1"

**Solutions**:
```bash
# Start Docker Desktop
open -a Docker

# Verify Docker is running
docker --version
docker ps

# If Docker is running but still fails, restart Docker daemon
# Then retry deployment
```

---

#### Problem: "unexpected deploy status 500: Function deploy failed due to an internal error"

**Common Causes**:
1. **Docker not running** - Start Docker first
2. **File permission issues** - Run `xattr -c` on the file
3. **Invalid TypeScript/Deno code** - Check syntax errors
4. **Missing imports** - Verify all npm: or https: imports are correct
5. **Supabase API issues** - Check https://status.supabase.com

**Debug Steps**:
```bash
# 1. Test locally first
npx supabase functions serve FUNCTION_NAME --no-verify-jwt

# 2. Check for TypeScript errors
deno check supabase/functions/FUNCTION_NAME/index.ts

# 3. Deploy with debug flag
npx supabase functions deploy FUNCTION_NAME --debug

# 4. Check Supabase logs
npx supabase functions logs FUNCTION_NAME
```

---

### 2. Environment Variables & Secrets

#### Best Practices for Secrets Management

**DO**:
```bash
# Set secrets via CLI (encrypted, secure)
npx supabase secrets set API_KEY=value
npx supabase secrets set STRIPE_SECRET_KEY=sk_live_xxx

# List all secrets (only shows names & hashes, not values)
npx supabase secrets list

# Use secrets in Edge Functions
const apiKey = Deno.env.get('API_KEY')
```

**DON'T**:
```bash
# ❌ Never commit .env files with real secrets to git
# ❌ Never use VITE_ prefix for backend secrets
# ❌ Never hardcode secrets in Edge Function code
```

**Secret Types by Use Case**:

| Secret Type | Where to Store | Example |
|------------|---------------|---------|
| Frontend (browser-safe) | `.env` with `VITE_` prefix | `VITE_SUPABASE_ANON_KEY` |
| Backend (Edge Functions) | Supabase Secrets | `STRIPE_SECRET_KEY` |
| Local development only | `.env.local` (gitignored) | `LOCAL_DEV_KEY` |
| Vercel deployment | Vercel Environment Variables | All `VITE_*` vars |

---

### 3. CORS Issues

#### Problem: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Complete CORS Headers Template**:
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*', // Or specific domain in production
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, x-client-info',
  'Access-Control-Max-Age': '86400', // 24 hours
}

Deno.serve(async (req: Request) => {
  // ALWAYS handle OPTIONS first
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders,
    })
  }

  // Include CORS in ALL responses
  try {
    const data = { success: true }
    return new Response(JSON.stringify(data), {
      status: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
```

---

### 4. Database Connection Issues

#### Problem: "Failed to connect to database" in Edge Functions

**Solutions**:
```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

// ✅ CORRECT: Use environment variables
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, // For admin operations
  {
    auth: { persistSession: false }, // Important for Edge Functions
    global: { headers: { 'X-Client-Info': 'edge-function-name@1.0.0' } },
  }
)

// ❌ WRONG: Using anon key for admin operations
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_ANON_KEY')!, // Limited permissions
)
```

**When to use which key**:
- **ANON_KEY**: Public, row-level security enforced, for frontend
- **SERVICE_ROLE_KEY**: Admin access, bypasses RLS, for Edge Functions only

---

### 5. Stripe Integration Issues

#### Webhook Verification Fails

**Common Problem**: Signature verification fails

**Solution**:
```typescript
import Stripe from 'https://esm.sh/stripe@14.21.0'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient(), // Required for Deno
})

Deno.serve(async (req: Request) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text() // Important: Use .text() not .json()

  try {
    const event = stripe.webhooks.constructEvent(
      body, // Raw body as string
      signature!,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')!
    )

    // Process event...

  } catch (err) {
    console.error('Webhook signature verification failed:', err.message)
    return new Response(JSON.stringify({ error: 'Invalid signature' }), {
      status: 400,
    })
  }
})
```

**Webhook Configuration Checklist**:
1. ✅ Webhook URL: `https://PROJECT_REF.supabase.co/functions/v1/FUNCTION_NAME`
2. ✅ Events: `checkout.session.completed`, `payment_intent.succeeded`, `payment_intent.payment_failed`
3. ✅ Webhook secret stored in Supabase: `npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_xxx`
4. ✅ API version matches code (e.g., `2023-10-16`)

---

### 6. Import Issues

#### Problem: Module not found or import errors

**Modern Deno Imports (Recommended)**:
```typescript
// ✅ Use npm: specifier with version pinning
import { createClient } from 'npm:@supabase/supabase-js@2.45.3'
import Stripe from 'npm:stripe@14.21.0'

// ✅ Use esm.sh for packages not on npm
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
```

**Legacy Imports (Avoid)**:
```typescript
// ❌ Old style - being deprecated
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
```

**Import Resolution Issues**:
```bash
# Create deno.json in project root to configure imports
{
  "compilerOptions": {
    "allowJs": true,
    "lib": ["deno.window"],
    "strict": true
  },
  "imports": {
    "supabase": "npm:@supabase/supabase-js@2",
    "stripe": "npm:stripe@14"
  }
}
```

---

### 7. Logging & Debugging

#### Essential Logging Pattern

```typescript
Deno.serve(async (req: Request) => {
  const requestId = crypto.randomUUID()

  try {
    console.log('[FUNCTION_NAME] Request received', {
      requestId,
      method: req.method,
      url: req.url
    })

    const body = await req.json()
    console.log('[FUNCTION_NAME] Parsed body', { requestId, body })

    // Your logic here...

    console.log('[FUNCTION_NAME] Success', { requestId })
    return new Response(JSON.stringify({ ok: true, requestId }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    })

  } catch (err) {
    console.error('[FUNCTION_NAME] Error', {
      requestId,
      error: String(err),
      stack: (err as Error)?.stack
    })
    return new Response(JSON.stringify({ error: 'Internal error', requestId }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }
})
```

**View Logs**:
```bash
# Real-time logs
npx supabase functions logs FUNCTION_NAME --follow

# Recent logs
npx supabase functions logs FUNCTION_NAME --limit 100

# Filter by level
npx supabase functions logs FUNCTION_NAME --level error
```

---

### 8. Testing Edge Functions Locally

```bash
# Start local Supabase (requires Docker)
npx supabase start

# Serve function locally
npx supabase functions serve FUNCTION_NAME --no-verify-jwt

# Test with curl
curl -i --location --request POST 'http://localhost:54321/functions/v1/FUNCTION_NAME' \
  --header 'Authorization: Bearer ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"key":"value"}'

# Stop local Supabase
npx supabase stop
```

---

### 9. Row Level Security (RLS) Issues

#### Problem: "new row violates row-level security policy"

**Common Causes**:
1. RLS is enabled but no policies exist
2. Policy doesn't match the operation (INSERT vs UPDATE vs SELECT)
3. Using anon key instead of service role key in Edge Function

**Solutions**:

```sql
-- Option 1: Disable RLS for specific table (not recommended for production)
ALTER TABLE table_name DISABLE ROW LEVEL SECURITY;

-- Option 2: Create proper policy
CREATE POLICY "Allow service role full access" ON table_name
  FOR ALL
  USING (auth.role() = 'service_role');

-- Option 3: Create specific policies
CREATE POLICY "Allow authenticated inserts" ON table_name
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow public reads" ON table_name
  FOR SELECT
  USING (true);
```

**In Edge Function**:
```typescript
// Use service role key to bypass RLS
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!, // Bypasses RLS
  { auth: { persistSession: false } }
)
```

---

### 10. Performance Optimization

#### Connection Pooling
```typescript
// ✅ Create client once outside handler
const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,
  { auth: { persistSession: false } }
)

Deno.serve(async (req: Request) => {
  // Use same client instance
  const { data, error } = await supabase.from('table').select()
  // ...
})
```

#### Reduce Cold Starts
```typescript
// Pre-initialize heavy dependencies
const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient(),
})

// Warm-up check
if (!Deno.env.get('STRIPE_SECRET_KEY')) {
  console.error('STRIPE_SECRET_KEY not set - function will fail')
}
```

---

### 11. Common Error Messages & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Docker is not running` | Docker Desktop stopped | `open -a Docker` |
| `failed to read file` | Wrong working directory | Copy files to `/Users/$(whoami)/supabase/functions/` |
| `CORS policy error` | Missing CORS headers | Add corsHeaders to all responses including OPTIONS |
| `Invalid JWT` | Using wrong key | Use SERVICE_ROLE_KEY for admin, ANON_KEY for client |
| `row-level security policy` | RLS blocking insert | Use SERVICE_ROLE_KEY or create policy |
| `Stripe signature verification failed` | Wrong body format | Use `await req.text()` not `req.json()` |
| `Module not found` | Import URL wrong | Use `npm:package@version` format |
| `Function timeout` | Long-running operation | Optimize queries or increase timeout |

---

### 12. Deployment Checklist

Before deploying Edge Functions:

```bash
# 1. Verify Docker is running
docker --version && docker ps

# 2. Test function locally
npx supabase functions serve FUNCTION_NAME --no-verify-jwt

# 3. Check for TypeScript errors
deno check supabase/functions/FUNCTION_NAME/index.ts

# 4. Verify all secrets are set
npx supabase secrets list

# 5. Deploy
npx supabase functions deploy FUNCTION_NAME

# 6. Test deployed function
curl -i --location --request POST \
  'https://PROJECT_REF.supabase.co/functions/v1/FUNCTION_NAME' \
  --header 'Authorization: Bearer ANON_KEY' \
  --header 'Content-Type: application/json' \
  --data '{"test":true}'

# 7. Monitor logs
npx supabase functions logs FUNCTION_NAME --follow
```

---

### 13. Useful Commands Reference

```bash
# Secrets Management
npx supabase secrets set KEY=value
npx supabase secrets list
npx supabase secrets unset KEY

# Function Management
npx supabase functions list
npx supabase functions deploy FUNCTION_NAME
npx supabase functions delete FUNCTION_NAME
npx supabase functions logs FUNCTION_NAME

# Local Development
npx supabase start
npx supabase stop
npx supabase status
npx supabase functions serve FUNCTION_NAME

# Database
npx supabase db pull
npx supabase db push
npx supabase db reset
npx supabase migration new MIGRATION_NAME

# Linking & Authentication
npx supabase link --project-ref PROJECT_REF
npx supabase login
```

---

### 14. Architecture Best Practices

#### Edge Function Structure
```
supabase/functions/
├── _shared/              # Shared utilities
│   ├── cors.ts          # CORS headers
│   ├── supabase.ts      # Supabase client factory
│   └── validation.ts    # Zod schemas
├── function-name/
│   └── index.ts         # Main handler
└── deno.json            # Import maps
```

#### Shared CORS Module
```typescript
// supabase/functions/_shared/cors.ts
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, x-client-info',
  'Access-Control-Max-Age': '86400',
}

export const handleCORS = (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders })
  }
  return null
}
```

#### Use in Edge Function
```typescript
import { corsHeaders, handleCORS } from '../_shared/cors.ts'

Deno.serve(async (req: Request) => {
  const corsResponse = handleCORS(req)
  if (corsResponse) return corsResponse

  // Your logic here
})
```

---

### 15. Troubleshooting Workflow

When encountering issues, follow this systematic approach:

```
1. Check Docker status
   └─> docker --version && docker ps
       └─> If not running: open -a Docker

2. Verify you're in project root
   └─> pwd
       └─> Should be: .../project-name
       └─> git rev-parse --show-toplevel

3. Check file exists and is readable
   └─> ls -la supabase/functions/FUNCTION_NAME/index.ts
       └─> If @ flag present: xattr -c FILE_PATH

4. Verify secrets are set
   └─> npx supabase secrets list
       └─> Set missing: npx supabase secrets set KEY=value

5. Test locally first
   └─> npx supabase functions serve FUNCTION_NAME
       └─> Fix any runtime errors

6. Deploy with debug
   └─> npx supabase functions deploy FUNCTION_NAME --debug
       └─> Check error messages carefully

7. Monitor logs after deploy
   └─> npx supabase functions logs FUNCTION_NAME --follow
       └─> Test endpoint and watch for errors

8. Test the endpoint
   └─> Use curl or Postman
       └─> Check response and logs
```

---

### 16. Security Hardening

```typescript
// Input Validation
import { z } from 'npm:zod@3'

const requestSchema = z.object({
  email: z.string().email(),
  amount: z.number().positive(),
  metadata: z.record(z.unknown()).optional(),
})

Deno.serve(async (req: Request) => {
  const body = await req.json()

  // Validate input
  const result = requestSchema.safeParse(body)
  if (!result.success) {
    return new Response(
      JSON.stringify({ error: 'Invalid input', details: result.error }),
      { status: 400, headers: corsHeaders }
    )
  }

  const { email, amount, metadata } = result.data
  // Safe to use validated data
})
```

```typescript
// Rate Limiting (manual implementation)
const rateLimits = new Map<string, { count: number; resetAt: number }>()

function checkRateLimit(ip: string, maxRequests = 10, windowMs = 60000): boolean {
  const now = Date.now()
  const limit = rateLimits.get(ip)

  if (!limit || now > limit.resetAt) {
    rateLimits.set(ip, { count: 1, resetAt: now + windowMs })
    return true
  }

  if (limit.count >= maxRequests) {
    return false
  }

  limit.count++
  return true
}

Deno.serve(async (req: Request) => {
  const ip = req.headers.get('x-forwarded-for') || 'unknown'

  if (!checkRateLimit(ip)) {
    return new Response(JSON.stringify({ error: 'Too many requests' }), {
      status: 429,
      headers: corsHeaders,
    })
  }

  // Process request...
})
```

---

## Quick Reference Card

**Most Common Issues:**
1. Docker not running → `open -a Docker`
2. Wrong working dir → Copy files to `/Users/$(whoami)/supabase/functions/`
3. CORS errors → Add corsHeaders to ALL responses
4. RLS blocking → Use SERVICE_ROLE_KEY
5. Webhook fails → Use `req.text()` not `req.json()`

**Must-Have in Every Edge Function:**
```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, x-client-info',
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders })
  }

  const requestId = crypto.randomUUID()

  try {
    // Your logic
    return new Response(JSON.stringify({ ok: true, requestId }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  } catch (err) {
    console.error('Error', { requestId, error: String(err) })
    return new Response(JSON.stringify({ error: 'Internal error', requestId }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    })
  }
})
```

---

## Final Tips

1. **Always use request IDs** for debugging
2. **Test locally before deploying**
3. **Monitor logs after deployment**
4. **Use TypeScript types** for better error catching
5. **Version pin all imports** (npm:package@1.2.3)
6. **Never commit secrets** to git
7. **Use SERVICE_ROLE_KEY** in Edge Functions for admin operations
8. **Always handle CORS OPTIONS** requests
9. **Validate all inputs** with Zod or similar
10. **Keep functions small and focused** - one responsibility per function

---

**This guide is based on real-world troubleshooting of Supabase Edge Functions deployment issues on macOS, Stripe integration, CORS problems, and general Supabase development patterns encountered in production environments.**
