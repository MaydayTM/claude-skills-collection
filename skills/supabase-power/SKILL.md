---
name: supabasepower
description: Use after feature design to generate Supabase migrations with RLS policies, supporting four ownership patterns with dev-first workflow
author: Mehdi Michiels
---

# SupabasePower Skill

## Overview

Generate battle-tested Supabase migrations from feature requirements. Supports four ownership patterns, generates migrations with commented-out RLS policies for fast development, provides pre-production validation checklists.

**Core principle:** Pre-flight check → Gather requirements → Generate migration → Validate before production.

**Announce at start:** "I'm using the supabasepower skill to generate your migration."

## When to Use This Skill

Use this skill when:
- You have feature requirements and need database structure
- You're starting a new Supabase feature with tables and auth
- You need RLS policies but want to develop without auth friction
- You're ready to add security to existing dev tables

**Don't use when:**
- Modifying existing migrations (this creates new ones)
- Building non-Supabase databases
- Schema already exists and just needs queries

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **0. Pre-flight** | Check Supabase CLI, verify project setup | Ready environment |
| **1. Gather** | Ask ownership pattern questions | Requirements clarity |
| **2. Generate** | Create migration with commented RLS | `.sql` file in migrations/ |
| **3. Validate** | Provide test checklist | TodoWrite todos |

## The Workflow

### Phase 0: Pre-flight Check

**Step 0.1: Check Supabase CLI installation**

```bash
# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
  echo "Supabase CLI not found."
fi
```

If CLI not found, use AskUserQuestion:

```javascript
{
  "question": "Supabase CLI is not installed. Would you like help installing it?",
  "header": "CLI Setup",
  "multiSelect": false,
  "options": [
    {
      "label": "Yes, help me install",
      "description": "I'll guide you through installing Supabase CLI for your system."
    },
    {
      "label": "I'll install it myself",
      "description": "Show me the installation docs and I'll do it."
    }
  ]
}
```

If "Yes, help me install", detect OS and provide installation commands:

```bash
# macOS
brew install supabase/tap/supabase

# Linux
curl -fsSL https://cli.supabase.com/install.sh | sh

# Windows (PowerShell)
scoop install supabase
```

**Step 0.2: Verify Supabase project**

```bash
# Check for Supabase project
if [ ! -f "supabase/config.toml" ]; then
  echo "No Supabase project initialized in this directory."
fi
```

If project not found, use AskUserQuestion:

```javascript
{
  "question": "No Supabase project found. Would you like to initialize one?",
  "header": "Project Init",
  "multiSelect": false,
  "options": [
    {
      "label": "Yes, initialize now",
      "description": "Run 'supabase init' to create project structure."
    },
    {
      "label": "I'm in the wrong directory",
      "description": "Let me navigate to my Supabase project first."
    }
  ]
}
```

If "Yes, initialize now":

```bash
supabase init
# This creates:
# - supabase/config.toml
# - supabase/migrations/
# - supabase/seed.sql
```

**Step 0.3: Verify local Supabase is running (optional)**

```bash
# Check if local Supabase is running
if ! supabase status &> /dev/null; then
  echo "Local Supabase is not running."
fi
```

Inform user: "Local Supabase not running. You can start it with `supabase start` to test migrations immediately."

### Phase 1: Gather Requirements

**Step 1.2: Identify ownership pattern**

Use AskUserQuestion tool to identify the pattern:

```javascript
{
  "question": "What's the data ownership model for this feature?",
  "header": "Ownership",
  "multiSelect": false,
  "options": [
    {
      "label": "Single-user SaaS",
      "description": "Users own their data. Each row belongs to one user. Classic SaaS pattern."
    },
    {
      "label": "Multi-tenant",
      "description": "Teams own data, members have roles. Workspaces, orgs, or project-based apps."
    },
    {
      "label": "Public + Auth hybrid",
      "description": "Some data public (anyone can read), some private (user-owned). Blog, marketplace patterns."
    },
    {
      "label": "Admin-only",
      "description": "Backoffice or CMS. Only admins can access. Regular users excluded."
    }
  ]
}
```

**Step 1.3: Load pattern template**

Based on answer, read the appropriate template:
- Single-user → Read `templates/single-user.md`
- Multi-tenant → Read `templates/multi-tenant.md`
- Public + Auth → Read `templates/public-auth.md`
- Admin-only → Read `templates/admin-only.md`

**Step 1.4: Ask pattern-specific questions**

Follow the template's question sequence. Each template has 3-5 questions that gather:
- Table names and columns
- Relationships (foreign keys)
- Access patterns (who reads/writes)
- Special requirements (soft deletes, timestamps, audit logs)

### Phase 2: Generate Migration

**Step 2.1: Create migration filename**

```bash
timestamp=$(date -u +"%Y%m%d%H%M%S")
feature_name="<feature-slug>"  # from user input
migration_file="supabase/migrations/${timestamp}_${feature_name}.sql"
```

**Step 2.2: Generate migration structure**

Write migration file with sections:
1. Tables (in dependency order)
2. Indexes (immediately after each table)
3. Commented RLS section
4. Helper functions (if needed)
5. Commented rollback section

**Step 2.3: Write migration file**

Use the Write tool to create the migration following this structure:

```sql
-- Migration: <feature_name>
-- Created: <timestamp>
-- Pattern: <ownership_pattern>

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE <table_name> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  <additional_columns>,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_<table>_user_id ON <table>(user_id);

-- ============================================
-- RLS POLICIES (disabled for development)
-- Uncomment before production deployment
-- ============================================

-- ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "users_read_own"
--   ON <table> FOR SELECT
--   USING (auth.uid() = user_id);

-- CREATE POLICY "users_write_own"
--   ON <table> FOR INSERT
--   WITH CHECK (auth.uid() = user_id);

-- CREATE POLICY "users_update_own"
--   ON <table> FOR UPDATE
--   USING (auth.uid() = user_id);

-- CREATE POLICY "users_delete_own"
--   ON <table> FOR DELETE
--   USING (auth.uid() = user_id);

-- ============================================
-- HELPER FUNCTIONS
-- ============================================

-- <Any helper functions for complex policy checks>

-- ============================================
-- ROLLBACK (run these commands to undo)
-- ============================================

-- DROP TABLE IF EXISTS <table> CASCADE;
```

**Step 2.4: Apply migration in dev**

```bash
supabase db reset  # Resets local DB and applies all migrations
```

### Phase 3: Validate Before Production

**Step 3.1: Create validation TodoWrite checklist**

Generate todos with specific test queries:

```javascript
[
  {
    "content": "Verify tables created with correct structure",
    "status": "pending",
    "activeForm": "Verifying table structure"
  },
  {
    "content": "Test queries work without RLS (development mode)",
    "status": "pending",
    "activeForm": "Testing development queries"
  },
  {
    "content": "Uncomment RLS sections before production",
    "status": "pending",
    "activeForm": "Enabling RLS policies"
  },
  {
    "content": "Test RLS policies with different user contexts",
    "status": "pending",
    "activeForm": "Testing RLS policies"
  },
  {
    "content": "Verify indexes exist and are used in queries",
    "status": "pending",
    "activeForm": "Verifying query performance"
  }
]
```

**Step 3.2: Provide test queries**

Output specific SQL test queries for the user:

```sql
-- Test 1: Verify table structure
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = '<table>';

-- Test 2: Insert test data
INSERT INTO <table> (user_id, <columns>)
VALUES ('<test-uuid>', <values>)
RETURNING *;

-- Test 3: Query as specific user (after enabling RLS)
SET request.jwt.claims.sub = '<user-uuid>';
SELECT * FROM <table>;
-- Expected: Only rows where user_id = '<user-uuid>'

-- Test 4: Verify index usage
EXPLAIN ANALYZE
SELECT * FROM <table> WHERE user_id = '<uuid>';
-- Expected: "Index Scan using idx_<table>_user_id"
```

**Step 3.3: Provide pre-production checklist**

Output markdown checklist:

```markdown
## Pre-Production Checklist

Before deploying to production:

1. ☐ Uncomment RLS sections in migration file
2. ☐ Run `supabase db reset` locally to test with RLS enabled
3. ☐ Execute test queries from Step 3.2 above
4. ☐ Verify all policies work correctly
5. ☐ Check for policy gaps (tables with RLS enabled but no policies)
6. ☐ Deploy to staging: `supabase db push --db-url <staging-url>`
7. ☐ Test in staging with real user sessions
8. ☐ Deploy to production: `supabase db push --db-url <production-url>`
```

## Ownership Patterns

### Single-User SaaS

Each user owns their data. Policies check `auth.uid() = user_id`.

**Template:** `templates/single-user.md`
**Policy:** `policies/library.md#user-owns-row`

### Multi-Tenant

Teams own data. Members have roles. Policies check team membership.

**Template:** `templates/multi-tenant.md`
**Policy:** `policies/library.md#user-in-team`

### Public + Auth Hybrid

Anonymous users can read public data. Auth users can write.

**Template:** `templates/public-auth.md`
**Policy:** `policies/library.md#public-read-auth-write`

### Admin-Only

Only admins can access. Regular users locked out.

**Template:** `templates/admin-only.md`
**Policy:** `policies/library.md#is-admin`

## Error Prevention

The skill prevents common mistakes:

**Missing Supabase project:** Check for `supabase/config.toml` before generating migration.

**Tables without policies:** Never generate a table without corresponding policy comments.

**Unclear ownership:** If user says "auth users can access" without clarifying owned vs all, ask explicitly.

**Missing dependencies:** If multi-tenant but no team membership table, alert and offer to generate.

**Soft deletes without policy updates:** When soft deletes requested, automatically update policies to filter `WHERE deleted_at IS NULL`.

## Common Mistakes to Avoid

**Forgetting to uncomment RLS:** The skill generates commented policies by design. User must uncomment before production.

**Testing without RLS locally:** Encourage testing with RLS enabled locally before deploying.

**Missing indexes:** Skill auto-generates indexes on foreign keys and ownership columns.

**Ambiguous access patterns:** Always clarify whether "users can read" means "their own data" or "all data".

## Examples

See `examples/` directory for complete examples:
- `examples/blog-posts.md` - Public read, auth write pattern
- `examples/todo-app.md` - Single-user SaaS pattern
- `examples/workspace-docs.md` - Multi-tenant pattern
- `examples/admin-panel.md` - Admin-only pattern
