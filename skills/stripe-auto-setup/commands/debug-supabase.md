# Debug Supabase Issues Command

You are helping debug common Supabase issues in a development project.

## Context

This command helps diagnose and fix common Supabase-related issues including:
- Edge Function deployment failures
- RLS (Row Level Security) policy errors
- Authentication problems
- Database connection issues
- Environment variable misconfigurations

## Diagnostic Steps

### STEP 1: Check Project Connection

```bash
# Verify Supabase CLI is installed
npx supabase --version

# Check if project is linked
npx supabase status

# If not linked, show how to link
echo "Not linked? Run:"
echo "npx supabase link --project-ref YOUR_PROJECT_REF"
```

**Common Issue**: "Cannot find project ref"
**Solution**: Extract from .env: `grep SUPABASE_URL .env`

### STEP 2: Verify Environment Variables

Check `.env` file for required variables:

```bash
# Required frontend variables
grep -E "VITE_SUPABASE_URL|VITE_SUPABASE_ANON_KEY" .env

# Check if values are set
if [ -z "$VITE_SUPABASE_URL" ]; then
  echo "❌ VITE_SUPABASE_URL is missing!"
fi
```

**Required Variables**:
- `VITE_SUPABASE_URL` - Your project URL
- `VITE_SUPABASE_ANON_KEY` - Public anon key
- Backend: Set via `npx supabase secrets set`

### STEP 3: Check Docker (for Edge Functions)

```bash
# Check if Docker is running
docker --version && docker ps

# If not running
echo "Docker not running. Start with:"
echo "open -a Docker  # macOS"
echo "# Wait 30 seconds, then retry"
```

### STEP 4: Test Edge Function Deployment

```bash
# List existing functions
npx supabase functions list

# Try deploying with debug
npx supabase functions deploy FUNCTION_NAME --debug

# Check logs
npx supabase functions logs FUNCTION_NAME --limit 50
```

**Common Errors**:

| Error | Cause | Fix |
|-------|-------|-----|
| `Docker is not running` | Docker not started | `open -a Docker` |
| `failed to read file` | Wrong working directory | Check you're in project root |
| `deployment status 500` | Vercel infrastructure | Check https://www.vercel-status.com |

### STEP 5: Check RLS Policies

```bash
# View current policies on a table
psql $DATABASE_URL -c "SELECT * FROM pg_policies WHERE tablename = 'YOUR_TABLE';"

# Or via Supabase SQL Editor:
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename = 'YOUR_TABLE';
```

**Common RLS Issues**:

1. **"new row violates row-level security policy"**
   - Cause: INSERT policy missing or too restrictive
   - Fix: Create policy or use SERVICE_ROLE_KEY

```sql
-- Temporary fix (for development only)
ALTER TABLE your_table DISABLE ROW LEVEL SECURITY;

-- Proper fix: Create policy
CREATE POLICY "Allow authenticated inserts"
ON your_table FOR INSERT
TO authenticated
WITH CHECK (true);
```

2. **"permission denied for table"**
   - Cause: Using anon key instead of service role key
   - Fix: Use `SUPABASE_SERVICE_ROLE_KEY` in Edge Functions

### STEP 6: Test Database Connection

Create test Edge Function:

```typescript
import { createClient } from 'npm:@supabase/supabase-js@2'

Deno.serve(async (req) => {
  try {
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    )

    // Test query
    const { data, error } = await supabase
      .from('YOUR_TABLE')
      .select('*')
      .limit(1)

    if (error) throw error

    return new Response(JSON.stringify({
      success: true,
      message: 'Database connection works!',
      data
    }))

  } catch (err) {
    return new Response(JSON.stringify({
      success: false,
      error: String(err)
    }), { status: 500 })
  }
})
```

### STEP 7: Check Secrets Configuration

```bash
# List all secrets (shows names only, not values)
npx supabase secrets list

# Set missing secrets
npx supabase secrets set SECRET_NAME=value

# Common secrets needed:
# - SUPABASE_SERVICE_ROLE_KEY
# - STRIPE_SECRET_KEY (if using Stripe)
# - OPENAI_API_KEY (if using AI)
```

### STEP 8: Verify CORS Configuration

Edge Functions need proper CORS headers:

```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, apikey, x-client-info',
  'Access-Control-Max-Age': '86400',
}

Deno.serve(async (req) => {
  // ALWAYS handle OPTIONS first
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders
    })
  }

  // Include CORS in ALL responses
  return new Response(JSON.stringify({ data }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  })
})
```

## Common Issue Checklist

Run through this checklist:

- [ ] Supabase project is linked (`npx supabase status`)
- [ ] Environment variables are set (`.env` file)
- [ ] Docker is running (`docker ps`)
- [ ] Secrets are configured (`npx supabase secrets list`)
- [ ] RLS policies allow your operation
- [ ] Using correct key (anon vs service_role)
- [ ] CORS headers are included
- [ ] Function is deployed (`npx supabase functions list`)

## Quick Fixes

### Reset Everything
```bash
# Re-link project
npx supabase link --project-ref PROJECT_REF

# Re-deploy function
npx supabase functions deploy FUNCTION_NAME

# Check logs
npx supabase functions logs FUNCTION_NAME
```

### Fresh Start
```bash
# Unlink and re-link
rm -rf .vercel supabase/.temp
npx supabase link --project-ref PROJECT_REF
npx supabase secrets list
npx supabase functions deploy FUNCTION_NAME
```

## Getting More Help

If issues persist:
1. Check Supabase status: https://status.supabase.com
2. View detailed logs: `npx supabase functions logs FUNCTION_NAME --follow`
3. Check Supabase docs: https://supabase.com/docs
4. Ask in Supabase Discord: https://discord.supabase.com

## Related Resources

- [SUPABASE_TROUBLESHOOTING_SKILL.md](../SUPABASE_TROUBLESHOOTING_SKILL.md) - Complete troubleshooting guide
- [/setup-stripe-checkout](./setup-stripe-checkout.md) - Stripe integration example
