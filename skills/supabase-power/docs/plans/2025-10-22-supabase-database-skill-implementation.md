# SupabasePower Skill Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Claude Code skill that generates Supabase migrations with RLS policies from feature requirements.

**Architecture:** Template-driven skill using Markdown templates for four ownership patterns, SQL migration generation, and structured validation checklists. Includes Supabase CLI setup assistance. Follows pre-flight-check → gather → generate → validate workflow.

**Tech Stack:** Claude Code skill format (Markdown), SQL for migrations, Bash for Supabase CLI integration.

---

## Task 1: Create Skill File Structure

**Files:**
- Create: `SKILL.md`
- Create: `README.md`
- Create: `CLAUDE.md`
- Create: `CHANGELOG.md`
- Create: `templates/single-user.md`
- Create: `templates/multi-tenant.md`
- Create: `templates/public-auth.md`
- Create: `templates/admin-only.md`
- Create: `policies/library.md`
- Create: `examples/blog-posts.md`
- Create: `scripts/setup-supabase.sh`
- Create: `scripts/test-migration.sh`

**Step 1: Create skill directory structure**

Run:
```bash
cd /Users/mehdimichiels/Documents/supabase-database-skill/.worktrees/implement-skill
mkdir -p templates policies examples scripts
touch templates/.gitkeep policies/.gitkeep examples/.gitkeep scripts/.gitkeep
```

**Step 2: Verify directory structure**

Run: `ls -la`
Expected: See templates/, policies/, examples/ directories

**Step 3: Commit directory structure**

```bash
git add templates/.gitkeep policies/.gitkeep examples/.gitkeep
git commit -m "feat: add skill directory structure"
```

---

## Task 2: Write Main SKILL.md

**Files:**
- Create: `SKILL.md`

**Step 1: Write SKILL.md header and metadata**

Create `SKILL.md`:
```markdown
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
```

**Step 2: Write the four-phase workflow**

Add to `SKILL.md`:
```markdown
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
```

**Step 3: Commit SKILL.md**

```bash
git add SKILL.md
git commit -m "feat: add main skill workflow documentation"
```

---

## Task 3: Create Single-User Pattern Template

**Files:**
- Create: `templates/single-user.md`

**Step 1: Write single-user template**

Create `templates/single-user.md`:
```markdown
# Single-User SaaS Pattern

## Pattern Description

Each user owns their data. Typical SaaS applications where users sign up and manage their own content.

**Policy rule:** `auth.uid() = user_id`

## Questions to Ask

Use AskUserQuestion for each of these:

### Question 1: Table Structure

```javascript
{
  "question": "What tables do you need for this feature?",
  "header": "Tables",
  "multiSelect": false,
  "options": [
    {
      "label": "Single table",
      "description": "One table stores all the data (e.g., 'posts', 'tasks', 'notes')"
    },
    {
      "label": "Parent-child tables",
      "description": "One parent with related children (e.g., 'projects' has many 'tasks')"
    },
    {
      "label": "Multiple independent tables",
      "description": "Several tables without foreign key relationships"
    }
  ]
}
```

After user answers, ask for specific table names and columns as open-ended question.

### Question 2: Privacy Level

```javascript
{
  "question": "Can users see other users' data?",
  "header": "Privacy",
  "multiSelect": false,
  "options": [
    {
      "label": "Fully private",
      "description": "Users can only see their own data. Most common for SaaS apps."
    },
    {
      "label": "Read others, write own",
      "description": "Users can read everyone's data but only modify their own."
    },
    {
      "label": "Selective sharing",
      "description": "Users can share specific records with others via share links or permissions."
    }
  ]
}
```

### Question 3: Special Requirements

```javascript
{
  "question": "Do you need any of these features?",
  "header": "Features",
  "multiSelect": true,
  "options": [
    {
      "label": "Soft deletes",
      "description": "Add deleted_at column, hide deleted records instead of removing them."
    },
    {
      "label": "Audit logs",
      "description": "Track who created/modified records with created_by, updated_by columns."
    },
    {
      "label": "Full-text search",
      "description": "Add GIN indexes for text search on specific columns."
    },
    {
      "label": "File uploads",
      "description": "Store file paths/URLs, integrate with Supabase Storage."
    }
  ]
}
```

## Migration Template

Based on answers, generate migration with this structure:

```sql
-- Single-User SaaS Pattern
-- Privacy: <fully_private|read_others|selective_sharing>

CREATE TABLE <table_name> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  <user_specified_columns>,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
  <optional: deleted_at TIMESTAMPTZ>
);

CREATE INDEX idx_<table>_user_id ON <table>(user_id);
<optional: CREATE INDEX idx_<table>_deleted_at ON <table>(deleted_at) WHERE deleted_at IS NOT NULL;>

-- RLS Policies (commented for development)
-- ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;

-- Fully private pattern
-- CREATE POLICY "users_read_own" ON <table> FOR SELECT
--   USING (auth.uid() = user_id <optional: AND deleted_at IS NULL>);

-- CREATE POLICY "users_write_own" ON <table> FOR INSERT
--   WITH CHECK (auth.uid() = user_id);

-- CREATE POLICY "users_update_own" ON <table> FOR UPDATE
--   USING (auth.uid() = user_id <optional: AND deleted_at IS NULL>);

-- CREATE POLICY "users_delete_own" ON <table> FOR DELETE
--   USING (auth.uid() = user_id);

-- <If soft deletes: Instead of DELETE, use UPDATE to set deleted_at>
```

## Validation Tests

```sql
-- Test 1: Insert as user A
SET request.jwt.claims.sub = 'user-a-uuid';
INSERT INTO <table> (user_id, <columns>) VALUES ('user-a-uuid', <values>);

-- Test 2: Query as user A (should see their row)
SELECT * FROM <table>;
-- Expected: 1 row

-- Test 3: Query as user B (should see nothing)
SET request.jwt.claims.sub = 'user-b-uuid';
SELECT * FROM <table>;
-- Expected: 0 rows

-- Test 4: User B can't update user A's data
UPDATE <table> SET <column> = <value> WHERE user_id = 'user-a-uuid';
-- Expected: 0 rows updated

-- Test 5: Verify index usage
EXPLAIN ANALYZE SELECT * FROM <table> WHERE user_id = 'user-a-uuid';
-- Expected: Index Scan using idx_<table>_user_id
```
```

**Step 2: Commit single-user template**

```bash
git add templates/single-user.md
git commit -m "feat: add single-user SaaS pattern template"
```

---

## Task 4: Create Multi-Tenant Pattern Template

**Files:**
- Create: `templates/multi-tenant.md`

**Step 1: Write multi-tenant template**

Create `templates/multi-tenant.md`:
```markdown
# Multi-Tenant Pattern

## Pattern Description

Teams/organizations own data. Users are members of teams with roles. Common for workspace apps, project management tools, collaborative platforms.

**Policy rule:** Check team membership via join table or team_id foreign key.

## Questions to Ask

### Question 1: Team Structure

```javascript
{
  "question": "How are teams/workspaces structured?",
  "header": "Team model",
  "multiSelect": false,
  "options": [
    {
      "label": "Simple team ownership",
      "description": "Data belongs to team, all members have equal access."
    },
    {
      "label": "Role-based access",
      "description": "Team members have roles (owner, admin, member) with different permissions."
    },
    {
      "label": "Hierarchical orgs",
      "description": "Nested teams/departments with inheritance (complex, rarely needed)."
    }
  ]
}
```

### Question 2: Membership Table

```javascript
{
  "question": "Do you already have a team membership table?",
  "header": "Membership",
  "multiSelect": false,
  "options": [
    {
      "label": "Yes, it exists",
      "description": "I have a table tracking team members (provide table name next)."
    },
    {
      "label": "No, generate it",
      "description": "Create team_members table for me with user_id, team_id, role."
    }
  ]
}
```

If "Yes", ask for table name as follow-up open-ended question.

### Question 3: Feature Tables

Ask open-ended: "What tables does this feature need? (e.g., 'documents', 'comments')"

### Question 4: Role Permissions

If role-based access selected:

```javascript
{
  "question": "What can each role do?",
  "header": "Permissions",
  "multiSelect": false,
  "options": [
    {
      "label": "Owner: full control, Admin: manage, Member: read/write",
      "description": "Three-tier standard roles."
    },
    {
      "label": "Admin: full control, Member: read/write",
      "description": "Two-tier simplified roles."
    },
    {
      "label": "Custom roles",
      "description": "I'll specify exact permissions for each role."
    }
  ]
}
```

## Migration Template

```sql
-- Multi-Tenant Pattern
-- Roles: <simple|role_based|hierarchical>

-- Team membership table (if generating)
CREATE TABLE team_members (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role TEXT NOT NULL CHECK (role IN ('owner', 'admin', 'member')),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(team_id, user_id)
);

CREATE INDEX idx_team_members_team ON team_members(team_id);
CREATE INDEX idx_team_members_user ON team_members(user_id);

-- Feature table
CREATE TABLE <table_name> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  created_by UUID REFERENCES auth.users(id),
  <user_specified_columns>,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_<table>_team ON <table>(team_id);

-- RLS Policies (commented for development)
-- ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;

-- Helper function: Check team membership
-- CREATE OR REPLACE FUNCTION is_team_member(check_team_id UUID)
-- RETURNS BOOLEAN AS $$
--   SELECT EXISTS (
--     SELECT 1 FROM team_members
--     WHERE team_id = check_team_id
--     AND user_id = auth.uid()
--   );
-- $$ LANGUAGE SQL SECURITY DEFINER;

-- Policy: Team members can read
-- CREATE POLICY "team_members_read" ON <table> FOR SELECT
--   USING (is_team_member(team_id));

-- Policy: Team members can write
-- CREATE POLICY "team_members_write" ON <table> FOR INSERT
--   WITH CHECK (is_team_member(team_id));

-- Policy: Team members can update
-- CREATE POLICY "team_members_update" ON <table> FOR UPDATE
--   USING (is_team_member(team_id));

-- Policy: Only admins/owners can delete (if role-based)
-- CREATE OR REPLACE FUNCTION is_team_admin(check_team_id UUID)
-- RETURNS BOOLEAN AS $$
--   SELECT EXISTS (
--     SELECT 1 FROM team_members
--     WHERE team_id = check_team_id
--     AND user_id = auth.uid()
--     AND role IN ('owner', 'admin')
--   );
-- $$ LANGUAGE SQL SECURITY DEFINER;

-- CREATE POLICY "team_admins_delete" ON <table> FOR DELETE
--   USING (is_team_admin(team_id));
```

## Validation Tests

```sql
-- Setup: Create test team and members
INSERT INTO teams (id, name) VALUES ('team-1-uuid', 'Test Team');
INSERT INTO team_members (team_id, user_id, role) VALUES
  ('team-1-uuid', 'user-a-uuid', 'owner'),
  ('team-1-uuid', 'user-b-uuid', 'member');

-- Test 1: Team member can insert
SET request.jwt.claims.sub = 'user-a-uuid';
INSERT INTO <table> (team_id, <columns>) VALUES ('team-1-uuid', <values>);

-- Test 2: Team member can read
SET request.jwt.claims.sub = 'user-b-uuid';
SELECT * FROM <table> WHERE team_id = 'team-1-uuid';
-- Expected: See the row

-- Test 3: Non-member can't read
SET request.jwt.claims.sub = 'user-c-uuid';
SELECT * FROM <table> WHERE team_id = 'team-1-uuid';
-- Expected: 0 rows

-- Test 4: Only admin can delete (if role-based)
SET request.jwt.claims.sub = 'user-b-uuid'; -- member, not admin
DELETE FROM <table> WHERE team_id = 'team-1-uuid';
-- Expected: 0 rows deleted (permission denied)

SET request.jwt.claims.sub = 'user-a-uuid'; -- owner
DELETE FROM <table> WHERE team_id = 'team-1-uuid';
-- Expected: 1 row deleted

-- Test 5: Verify index usage
EXPLAIN ANALYZE SELECT * FROM <table> WHERE team_id = 'team-1-uuid';
-- Expected: Index Scan using idx_<table>_team
```
```

**Step 2: Commit multi-tenant template**

```bash
git add templates/multi-tenant.md
git commit -m "feat: add multi-tenant pattern template"
```

---

## Task 5: Create Public + Auth Hybrid Template

**Files:**
- Create: `templates/public-auth.md`

**Step 1: Write public-auth template**

Create `templates/public-auth.md`:
```markdown
# Public + Auth Hybrid Pattern

## Pattern Description

Anonymous users can read public data. Authenticated users can create and manage their own content. Common for blogs, marketplaces, social platforms.

**Policy rules:**
- SELECT: Allow anonymous if public
- INSERT/UPDATE/DELETE: Require auth and ownership check

## Questions to Ask

### Question 1: What's Public?

```javascript
{
  "question": "Which data should be publicly readable?",
  "header": "Public data",
  "multiSelect": false,
  "options": [
    {
      "label": "Everything is public",
      "description": "All records visible to everyone (blog posts, product listings)."
    },
    {
      "label": "Published content only",
      "description": "Records with published=true or status='published' are public."
    },
    {
      "label": "User chooses per record",
      "description": "Each record has is_public boolean, user controls visibility."
    }
  ]
}
```

### Question 2: Feature Tables

Ask open-ended: "What tables does this feature need?"

### Question 3: Moderation

```javascript
{
  "question": "Do you need content moderation?",
  "header": "Moderation",
  "multiSelect": false,
  "options": [
    {
      "label": "No moderation",
      "description": "Content goes live immediately when created."
    },
    {
      "label": "Approval workflow",
      "description": "New content starts as draft, admin approves to publish."
    },
    {
      "label": "Flag for review",
      "description": "Users can flag content, moderators review flagged items."
    }
  ]
}
```

## Migration Template

```sql
-- Public + Auth Hybrid Pattern
-- Public: <everything|published_only|user_choice>

CREATE TABLE <table_name> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  <user_specified_columns>,
  <optional: is_public BOOLEAN DEFAULT true>,
  <optional: status TEXT CHECK (status IN ('draft', 'published')) DEFAULT 'draft'>,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_<table>_user ON <table>(user_id);
<optional: CREATE INDEX idx_<table>_public ON <table>(is_public) WHERE is_public = true;>
<optional: CREATE INDEX idx_<table>_status ON <table>(status) WHERE status = 'published';>

-- RLS Policies (commented for development)
-- ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;

-- Policy: Anyone can read public content
-- CREATE POLICY "public_read" ON <table> FOR SELECT
--   USING (
--     <option1: true> -- everything public
--     <option2: status = 'published'> -- only published
--     <option3: is_public = true> -- user-controlled
--   );

-- Policy: Authenticated users can insert
-- CREATE POLICY "auth_insert" ON <table> FOR INSERT
--   TO authenticated
--   WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own content
-- CREATE POLICY "users_update_own" ON <table> FOR UPDATE
--   TO authenticated
--   USING (auth.uid() = user_id);

-- Policy: Users can delete their own content
-- CREATE POLICY "users_delete_own" ON <table> FOR DELETE
--   TO authenticated
--   USING (auth.uid() = user_id);
```

## Validation Tests

```sql
-- Test 1: Anonymous user can read public content
RESET request.jwt.claims.sub; -- Simulate anonymous
SELECT * FROM <table> WHERE <public_condition>;
-- Expected: See public rows

-- Test 2: Authenticated user can insert
SET request.jwt.claims.sub = 'user-a-uuid';
INSERT INTO <table> (user_id, <columns>) VALUES ('user-a-uuid', <values>);

-- Test 3: User can update their own content
UPDATE <table> SET <column> = <value> WHERE user_id = 'user-a-uuid';
-- Expected: 1 row updated

-- Test 4: User can't update others' content
UPDATE <table> SET <column> = <value> WHERE user_id = 'user-b-uuid';
-- Expected: 0 rows updated

-- Test 5: Anonymous can't insert
RESET request.jwt.claims.sub;
INSERT INTO <table> (user_id, <columns>) VALUES (NULL, <values>);
-- Expected: Permission denied

-- Test 6: Verify public index usage
EXPLAIN ANALYZE SELECT * FROM <table> WHERE is_public = true;
-- Expected: Index Scan using idx_<table>_public
```
```

**Step 2: Commit public-auth template**

```bash
git add templates/public-auth.md
git commit -m "feat: add public + auth hybrid pattern template"
```

---

## Task 6: Create Admin-Only Pattern Template

**Files:**
- Create: `templates/admin-only.md`

**Step 1: Write admin-only template**

Create `templates/admin-only.md`:
```markdown
# Admin-Only Pattern

## Pattern Description

Only administrators can access data. Regular users are completely locked out. Common for backoffice tools, CMS admin panels, internal dashboards.

**Policy rule:** Check admin status via role column in profiles table.

## Questions to Ask

### Question 1: Admin Identification

```javascript
{
  "question": "How do you identify admin users?",
  "header": "Admin check",
  "multiSelect": false,
  "options": [
    {
      "label": "profiles.role column",
      "description": "Check if profiles.role = 'admin' (most common)."
    },
    {
      "label": "admin_users table",
      "description": "Separate table lists admin user IDs."
    },
    {
      "label": "Email domain",
      "description": "Check if user email ends with @company.com."
    }
  ]
}
```

### Question 2: Admin Levels

```javascript
{
  "question": "Are there different admin roles?",
  "header": "Admin roles",
  "multiSelect": false,
  "options": [
    {
      "label": "Single admin role",
      "description": "All admins have the same permissions."
    },
    {
      "label": "Super admin + admin",
      "description": "Super admins can manage admins, admins manage content."
    },
    {
      "label": "Custom admin roles",
      "description": "Multiple admin types with different permissions."
    }
  ]
}
```

### Question 3: Feature Tables

Ask open-ended: "What tables does this feature need?"

## Migration Template

```sql
-- Admin-Only Pattern
-- Admin check: <profiles_role|admin_table|email_domain>

-- Ensure profiles table has role column (if using profiles.role)
-- ALTER TABLE profiles ADD COLUMN IF NOT EXISTS role TEXT DEFAULT 'user';
-- CREATE INDEX IF NOT EXISTS idx_profiles_role ON profiles(role);

CREATE TABLE <table_name> (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_by UUID REFERENCES auth.users(id),
  <user_specified_columns>,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- RLS Policies (commented for development)
-- ALTER TABLE <table> ENABLE ROW LEVEL SECURITY;

-- Helper function: Check if user is admin
-- CREATE OR REPLACE FUNCTION is_admin()
-- RETURNS BOOLEAN AS $$
--   <option1: profiles.role check>
--   SELECT EXISTS (
--     SELECT 1 FROM profiles
--     WHERE id = auth.uid()
--     AND role = 'admin'
--   );
--
--   <option2: admin_users table>
--   SELECT EXISTS (
--     SELECT 1 FROM admin_users
--     WHERE user_id = auth.uid()
--   );
--
--   <option3: email domain>
--   SELECT EXISTS (
--     SELECT 1 FROM auth.users
--     WHERE id = auth.uid()
--     AND email LIKE '%@company.com'
--   );
-- $$ LANGUAGE SQL SECURITY DEFINER;

-- Policy: Only admins can read
-- CREATE POLICY "admin_read" ON <table> FOR SELECT
--   TO authenticated
--   USING (is_admin());

-- Policy: Only admins can insert
-- CREATE POLICY "admin_insert" ON <table> FOR INSERT
--   TO authenticated
--   WITH CHECK (is_admin());

-- Policy: Only admins can update
-- CREATE POLICY "admin_update" ON <table> FOR UPDATE
--   TO authenticated
--   USING (is_admin());

-- Policy: Only admins can delete
-- CREATE POLICY "admin_delete" ON <table> FOR DELETE
--   TO authenticated
--   USING (is_admin());
```

## Validation Tests

```sql
-- Setup: Create admin and regular user
INSERT INTO profiles (id, email, role) VALUES
  ('admin-uuid', 'admin@company.com', 'admin'),
  ('user-uuid', 'user@email.com', 'user');

-- Test 1: Admin can insert
SET request.jwt.claims.sub = 'admin-uuid';
INSERT INTO <table> (<columns>) VALUES (<values>);

-- Test 2: Admin can read
SELECT * FROM <table>;
-- Expected: See all rows

-- Test 3: Regular user can't read
SET request.jwt.claims.sub = 'user-uuid';
SELECT * FROM <table>;
-- Expected: 0 rows (permission denied)

-- Test 4: Regular user can't insert
INSERT INTO <table> (<columns>) VALUES (<values>);
-- Expected: Permission denied

-- Test 5: Anonymous user can't read
RESET request.jwt.claims.sub;
SELECT * FROM <table>;
-- Expected: 0 rows (permission denied)
```
```

**Step 2: Commit admin-only template**

```bash
git add templates/admin-only.md
git commit -m "feat: add admin-only pattern template"
```

---

## Task 7: Create Policy Library

**Files:**
- Create: `policies/library.md`

**Step 1: Write policy library**

Create `policies/library.md`:
```markdown
# RLS Policy Library

Reusable policy patterns with explanations and examples.

## user-owns-row

**Pattern:** User can only access rows where user_id matches their auth.uid().

**Use case:** Single-user SaaS, personal data, user-specific content.

**SQL:**
```sql
CREATE POLICY "users_read_own"
  ON table_name FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "users_write_own"
  ON table_name FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_update_own"
  ON table_name FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "users_delete_own"
  ON table_name FOR DELETE
  USING (auth.uid() = user_id);
```

**Gotcha:** Make sure user_id is NOT NULL and has foreign key to auth.users.

---

## user-in-team

**Pattern:** User can access rows if they're a member of the team that owns the row.

**Use case:** Multi-tenant, workspace apps, team collaboration.

**SQL:**
```sql
-- Helper function
CREATE OR REPLACE FUNCTION is_team_member(check_team_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members
    WHERE team_id = check_team_id
    AND user_id = auth.uid()
  );
$$ LANGUAGE SQL SECURITY DEFINER;

-- Policies
CREATE POLICY "team_members_read"
  ON table_name FOR SELECT
  USING (is_team_member(team_id));

CREATE POLICY "team_members_write"
  ON table_name FOR INSERT
  WITH CHECK (is_team_member(team_id));
```

**Gotcha:** Requires team_members join table with proper indexes.

---

## is-admin

**Pattern:** Only users with admin role can access.

**Use case:** Admin panels, backoffice tools, moderation interfaces.

**SQL:**
```sql
-- Helper function
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid()
    AND role = 'admin'
  );
$$ LANGUAGE SQL SECURITY DEFINER;

-- Policies
CREATE POLICY "admin_only_read"
  ON table_name FOR SELECT
  TO authenticated
  USING (is_admin());

CREATE POLICY "admin_only_write"
  ON table_name FOR INSERT
  TO authenticated
  WITH CHECK (is_admin());
```

**Gotcha:** Ensure profiles.role column exists and is indexed.

---

## public-read-auth-write

**Pattern:** Anyone can read, authenticated users can write (their own).

**Use case:** Blogs, public profiles, marketplaces.

**SQL:**
```sql
CREATE POLICY "public_read"
  ON table_name FOR SELECT
  USING (true); -- or add: WHERE is_public = true

CREATE POLICY "auth_write"
  ON table_name FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_update_own"
  ON table_name FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id);
```

**Gotcha:** Consider adding is_public or status column for granular control.

---

## team-member-read

**Pattern:** All team members can read team data.

**Use case:** Collaborative documents, shared resources.

**SQL:**
```sql
CREATE POLICY "team_members_read"
  ON table_name FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM team_members
      WHERE team_members.team_id = table_name.team_id
      AND team_members.user_id = auth.uid()
    )
  );
```

**Gotcha:** Performance can suffer without proper indexes on team_members.

---

## team-admin-write

**Pattern:** Only team admins/owners can modify data.

**Use case:** Critical team settings, member management, billing.

**SQL:**
```sql
CREATE OR REPLACE FUNCTION is_team_admin(check_team_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM team_members
    WHERE team_id = check_team_id
    AND user_id = auth.uid()
    AND role IN ('owner', 'admin')
  );
$$ LANGUAGE SQL SECURITY DEFINER;

CREATE POLICY "team_admins_write"
  ON table_name FOR UPDATE
  USING (is_team_admin(team_id));

CREATE POLICY "team_admins_delete"
  ON table_name FOR DELETE
  USING (is_team_admin(team_id));
```

**Gotcha:** Make sure to have separate policies for reads (team members) and writes (admins).

---

## Combining Policies

Multiple policies for the same operation are combined with OR. This means:

```sql
-- Policy 1: Users can read their own
CREATE POLICY "read_own" ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Policy 2: Admins can read all
CREATE POLICY "admin_read_all" ON posts FOR SELECT
  TO authenticated
  USING (is_admin());
```

Result: Regular users see their own posts, admins see all posts.

## Testing Policies

Always test policies with:

```sql
-- Set user context
SET request.jwt.claims.sub = 'user-uuid-here';

-- Run your query
SELECT * FROM table_name;

-- Reset context
RESET request.jwt.claims.sub;
```

## Performance Tips

1. **Index foreign keys:** CREATE INDEX on user_id, team_id, etc.
2. **Index policy columns:** CREATE INDEX on is_public, status, deleted_at
3. **Use SECURITY DEFINER sparingly:** Can bypass RLS, use only when needed
4. **Avoid N+1 queries:** Join team_members in app queries, don't rely on policy alone

## Common Mistakes

**Forgetting ENABLE ROW LEVEL SECURITY:** Policies don't work until RLS is enabled.

**Using WITH CHECK on SELECT:** SELECT policies only use USING clause.

**Chaining auth.uid() calls:** Cache it once in helper function for performance.

**Missing TO authenticated:** Without this, policies apply to anonymous users too.
```

**Step 2: Commit policy library**

```bash
git add policies/library.md
git commit -m "feat: add RLS policy library with reusable patterns"
```

---

## Task 8: Create Example - Blog Posts

**Files:**
- Create: `examples/blog-posts.md`

**Step 1: Write blog posts example**

Create `examples/blog-posts.md`:
```markdown
# Example: Blog Posts Feature

**Pattern:** Public + Auth Hybrid
**Use case:** Users can write blog posts. Published posts are public. Users manage their own drafts.

## Requirements Gathered

- **Ownership:** Public + Auth hybrid
- **Tables:** posts, post_comments
- **Public data:** Published posts only (status = 'published')
- **Privacy:** Users can only edit their own posts

## Generated Migration

File: `supabase/migrations/20251022192100_blog_posts.sql`

```sql
-- Migration: blog_posts
-- Created: 2025-10-22 19:21:00
-- Pattern: Public + Auth Hybrid

-- ============================================
-- TABLES
-- ============================================

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('draft', 'published')) DEFAULT 'draft',
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_posts_user ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status) WHERE status = 'published';
CREATE INDEX idx_posts_slug ON posts(slug);

CREATE TABLE post_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_comments_post ON post_comments(post_id);
CREATE INDEX idx_comments_user ON post_comments(user_id);

-- ============================================
-- RLS POLICIES (disabled for development)
-- Uncomment before production deployment
-- ============================================

-- ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE post_comments ENABLE ROW LEVEL SECURITY;

-- Posts: Anyone can read published
-- CREATE POLICY "public_read_published" ON posts FOR SELECT
--   USING (status = 'published');

-- Posts: Authors can read their own drafts
-- CREATE POLICY "authors_read_own" ON posts FOR SELECT
--   TO authenticated
--   USING (auth.uid() = user_id);

-- Posts: Authenticated users can create
-- CREATE POLICY "auth_create" ON posts FOR INSERT
--   TO authenticated
--   WITH CHECK (auth.uid() = user_id);

-- Posts: Authors can update their own
-- CREATE POLICY "authors_update_own" ON posts FOR UPDATE
--   TO authenticated
--   USING (auth.uid() = user_id);

-- Posts: Authors can delete their own
-- CREATE POLICY "authors_delete_own" ON posts FOR DELETE
--   TO authenticated
--   USING (auth.uid() = user_id);

-- Comments: Anyone can read comments on published posts
-- CREATE POLICY "public_read_comments" ON post_comments FOR SELECT
--   USING (
--     EXISTS (
--       SELECT 1 FROM posts
--       WHERE posts.id = post_comments.post_id
--       AND posts.status = 'published'
--     )
--   );

-- Comments: Authenticated users can create
-- CREATE POLICY "auth_create_comment" ON post_comments FOR INSERT
--   TO authenticated
--   WITH CHECK (auth.uid() = user_id);

-- Comments: Users can update their own
-- CREATE POLICY "users_update_own_comment" ON post_comments FOR UPDATE
--   TO authenticated
--   USING (auth.uid() = user_id);

-- Comments: Users can delete their own
-- CREATE POLICY "users_delete_own_comment" ON post_comments FOR DELETE
--   TO authenticated
--   USING (auth.uid() = user_id);

-- ============================================
-- ROLLBACK (run these commands to undo)
-- ============================================

-- DROP TABLE IF EXISTS post_comments CASCADE;
-- DROP TABLE IF EXISTS posts CASCADE;
```

## Validation Tests

```sql
-- Test 1: Anonymous can read published posts
RESET request.jwt.claims.sub;
SELECT * FROM posts WHERE status = 'published';
-- Expected: See published posts only

-- Test 2: Anonymous can't read drafts
SELECT * FROM posts WHERE status = 'draft';
-- Expected: 0 rows

-- Test 3: Author can create post
SET request.jwt.claims.sub = 'author-uuid';
INSERT INTO posts (user_id, title, content, slug, status)
VALUES ('author-uuid', 'My First Post', 'Content here', 'my-first-post', 'draft');

-- Test 4: Author can see their own draft
SELECT * FROM posts WHERE user_id = 'author-uuid' AND status = 'draft';
-- Expected: 1 row

-- Test 5: Other users can't see author's draft
SET request.jwt.claims.sub = 'other-user-uuid';
SELECT * FROM posts WHERE user_id = 'author-uuid' AND status = 'draft';
-- Expected: 0 rows

-- Test 6: Author publishes post
SET request.jwt.claims.sub = 'author-uuid';
UPDATE posts SET status = 'published', published_at = now()
WHERE user_id = 'author-uuid' AND slug = 'my-first-post';

-- Test 7: Now anonymous can see published post
RESET request.jwt.claims.sub;
SELECT * FROM posts WHERE slug = 'my-first-post';
-- Expected: 1 row

-- Test 8: User can comment on published post
SET request.jwt.claims.sub = 'commenter-uuid';
INSERT INTO post_comments (post_id, user_id, content)
SELECT id, 'commenter-uuid', 'Great post!'
FROM posts WHERE slug = 'my-first-post';

-- Test 9: Anonymous can read comment
RESET request.jwt.claims.sub;
SELECT * FROM post_comments;
-- Expected: See the comment

-- Test 10: Verify index usage
EXPLAIN ANALYZE SELECT * FROM posts WHERE status = 'published';
-- Expected: Index Scan using idx_posts_status
```

## Development Workflow

1. Generate migration with RLS commented out
2. Run `supabase db reset` to apply
3. Test queries work without auth (fast iteration)
4. Build the blog UI and features
5. When ready for production:
   - Uncomment RLS sections
   - Run `supabase db reset` locally
   - Execute validation tests above
   - Fix any policy issues
   - Deploy to staging first
   - Test with real user sessions
   - Deploy to production
```

**Step 2: Commit blog posts example**

```bash
git add examples/blog-posts.md
git commit -m "docs: add blog posts example with migration and tests"
```

---

## Task 9: Write README

**Files:**
- Create: `README.md`

**Step 1: Write README**

Create `README.md`:
```markdown
# SupabasePower

A Claude Code skill that generates Supabase migrations with RLS policies from feature requirements.

**Author:** Mehdi Michiels

## Features

- **Supabase CLI setup help:** Checks for CLI installation and offers guided setup
- **Template-driven generation:** Choose from four proven ownership patterns
- **Dev-first workflow:** RLS policies are commented out for fast iteration
- **Battle-tested patterns:** Reusable policy library with common scenarios
- **Validation checklists:** Specific test queries to verify policies work
- **Helper scripts:** Setup and testing automation included

## Ownership Patterns

1. **Single-user SaaS:** Users own their data (`auth.uid() = user_id`)
2. **Multi-tenant:** Teams own data, members have roles
3. **Public + Auth hybrid:** Anonymous read, authenticated write
4. **Admin-only:** Backoffice and CMS patterns

## Installation

### Option 1: Clone to Claude Skills Directory

```bash
cd ~/.claude/skills
git clone https://github.com/mehdimichiels/supabasepower.git
```

### Option 2: Use in Project

```bash
cd your-project
git clone https://github.com/mehdimichiels/supabasepower.git .claude/skills/supabasepower
```

### Option 3: Add as Git Submodule

```bash
cd your-project
git submodule add https://github.com/mehdimichiels/supabasepower.git .claude/skills/supabasepower
```

## Quick Start

Run the setup helper:

```bash
./scripts/setup-supabase.sh
```

This will:
- Check and install Supabase CLI if needed
- Initialize your Supabase project
- Start local development environment

## Usage

In Claude Code, say:

```
Use the supabasepower skill to generate a migration for my blog posts feature.
```

The skill will:
1. Ask about your ownership pattern
2. Ask pattern-specific questions
3. Generate migration file in `supabase/migrations/`
4. Provide validation checklist with test queries

## Development Workflow

**Fast Iteration (RLS disabled):**
```bash
# Migration has RLS sections commented out
supabase db reset
# Build your features, test without auth friction
```

**Pre-Production (Enable RLS):**
```bash
# Uncomment RLS sections in migration file
supabase db reset
# Run validation tests from skill output
# Fix any policy issues
```

**Deploy to Production:**
```bash
supabase db push --db-url $STAGING_URL  # Test in staging first
supabase db push --db-url $PRODUCTION_URL
```

## Examples

See `examples/` directory:
- `blog-posts.md` - Public read, auth write
- `todo-app.md` - Single-user SaaS
- `workspace-docs.md` - Multi-tenant
- `admin-panel.md` - Admin-only

## Policy Library

See `policies/library.md` for reusable patterns:
- user-owns-row
- user-in-team
- is-admin
- public-read-auth-write
- team-member-read
- team-admin-write

## Requirements

- Supabase project initialized (`supabase init`)
- Supabase CLI installed (`brew install supabase/tap/supabase`)
- PostgreSQL knowledge (basic)

## Contributing

Found a bug or have a pattern to add? Open an issue or PR!

## License

MIT - Use freely, attribute Mehdi Michiels

## Credits

Built by Mehdi Michiels
Powered by Claude Code superpowers
```

**Step 2: Commit README**

```bash
git add README.md
git commit -m "docs: add README with installation and usage instructions"
```

---

## Task 10: Create Helper Scripts

**Files:**
- Create: `scripts/setup-supabase.sh`
- Create: `scripts/test-migration.sh`

**Step 1: Create setup-supabase.sh**

Create `scripts/setup-supabase.sh`:
```bash
#!/bin/bash
# SupabasePower - Supabase Setup Helper
# Guides users through Supabase CLI installation and project initialization

set -e

echo "=== SupabasePower Setup Helper ==="
echo

# Check if Supabase CLI is installed
if command -v supabase &> /dev/null; then
  echo "✓ Supabase CLI is already installed ($(supabase --version))"
else
  echo "✗ Supabase CLI is not installed"
  echo
  echo "Would you like to install it now? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "Installing via Homebrew..."
      brew install supabase/tap/supabase
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      echo "Installing via install script..."
      curl -fsSL https://cli.supabase.com/install.sh | sh
    else
      echo "Please install manually: https://supabase.com/docs/guides/cli"
      exit 1
    fi
  else
    echo "Skipping installation. Visit https://supabase.com/docs/guides/cli"
    exit 0
  fi
fi

echo
echo "=== Project Initialization ==="
echo

# Check if already in a Supabase project
if [ -f "supabase/config.toml" ]; then
  echo "✓ Supabase project already initialized"
else
  echo "✗ No Supabase project found in current directory"
  echo
  echo "Initialize Supabase project here? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    supabase init
    echo "✓ Supabase project initialized"
  else
    echo "Skipping initialization"
    exit 0
  fi
fi

echo
echo "=== Local Development Setup ==="
echo

# Check if local Supabase is running
if supabase status &> /dev/null; then
  echo "✓ Local Supabase is running"
else
  echo "✗ Local Supabase is not running"
  echo
  echo "Start local Supabase now? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    echo "Starting local Supabase (this may take a few minutes)..."
    supabase start
    echo
    echo "✓ Local Supabase is running"
    echo
    supabase status
  else
    echo "You can start it later with: supabase start"
  fi
fi

echo
echo "=== Setup Complete ==="
echo "You're ready to use SupabasePower!"
echo "Try: Ask Claude to 'use supabasepower skill' to generate migrations"
```

**Step 2: Create test-migration.sh**

Create `scripts/test-migration.sh`:
```bash
#!/bin/bash
# SupabasePower - Migration Test Helper
# Tests a migration file before deploying to production

set -e

if [ -z "$1" ]; then
  echo "Usage: ./test-migration.sh <migration-file>"
  echo "Example: ./test-migration.sh supabase/migrations/20251022_blog_posts.sql"
  exit 1
fi

MIGRATION_FILE="$1"

if [ ! -f "$MIGRATION_FILE" ]; then
  echo "Error: Migration file not found: $MIGRATION_FILE"
  exit 1
fi

echo "=== Testing Migration: $(basename "$MIGRATION_FILE") ==="
echo

# Check if local Supabase is running
if ! supabase status &> /dev/null; then
  echo "✗ Local Supabase is not running"
  echo "Start it with: supabase start"
  exit 1
fi

echo "✓ Local Supabase is running"
echo

# Reset database and apply all migrations
echo "Resetting database and applying migrations..."
supabase db reset

echo
echo "✓ Migration applied successfully"
echo

# Check for common issues
echo "=== Running Checks ==="
echo

# Check if RLS is enabled
echo "Checking RLS status..."
psql postgresql://postgres:postgres@localhost:54322/postgres -t -c "
  SELECT tablename, rowsecurity
  FROM pg_tables
  WHERE schemaname = 'public'
" | while read -r table rls; do
  if [ -n "$table" ]; then
    if [ "$rls" = " f" ]; then
      echo "⚠  Table '$table' has RLS disabled (expected for development)"
    else
      echo "✓ Table '$table' has RLS enabled"
    fi
  fi
done

echo
echo "=== Test Complete ==="
echo "Review the output above for any issues"
echo "To test with RLS enabled:"
echo "  1. Uncomment RLS sections in migration"
echo "  2. Run: supabase db reset"
echo "  3. Test queries with different user contexts"
```

**Step 3: Make scripts executable**

```bash
chmod +x scripts/setup-supabase.sh scripts/test-migration.sh
```

**Step 4: Commit helper scripts**

```bash
git add scripts/
git commit -m "feat: add setup and testing helper scripts"
```

---

## Task 11: Create CLAUDE.md and CHANGELOG.md

**Files:**
- Create: `CLAUDE.md`
- Create: `CHANGELOG.md`

**Step 1: Create CLAUDE.md**

Create `CLAUDE.md`:
```markdown
# SupabasePower - Instructions for Claude

This skill generates Supabase migrations with RLS policies from feature requirements.

## When to Use

Use this skill after feature design when the user needs database structure. Look for phrases like:
- "I need a database for..."
- "Help me create tables for..."
- "Generate a migration for..."
- "I need RLS policies for..."

## Workflow

1. **Pre-flight Check:** Always check for Supabase CLI and project setup first
2. **Gather:** Ask about ownership pattern, then pattern-specific questions
3. **Generate:** Create migration file with commented RLS policies
4. **Validate:** Provide TodoWrite checklist with specific test queries

## Key Principles

- **RLS policies start commented:** Dev-first workflow. Uncomment before production.
- **Battle-tested patterns:** Use templates, don't improvise
- **Specific test queries:** Always provide exact SQL tests with expected results
- **Help with CLI setup:** Don't assume Supabase CLI is installed

## Common Patterns

- **Single-user SaaS:** `auth.uid() = user_id`
- **Multi-tenant:** Check team membership via join
- **Public + Auth:** Public read, authenticated write
- **Admin-only:** Check role/admin table

## Example Usage

User: "I need a database for a blog with posts and comments"

You:
1. Check Supabase CLI (offer help if missing)
2. Identify pattern: Public + Auth (published posts are public)
3. Generate migration with tables, indexes, commented RLS
4. Provide validation TodoWrite with specific test SQL

## Files to Reference

- `templates/` - Pattern-specific question flows
- `policies/library.md` - Reusable RLS patterns
- `examples/` - Complete working examples
```

**Step 2: Create CHANGELOG.md**

Create `CHANGELOG.md`:
```markdown
# Changelog

All notable changes to SupabasePower will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial skill implementation
- Four ownership patterns (single-user, multi-tenant, public-auth, admin-only)
- Template-driven migration generation
- Commented RLS policies for dev-first workflow
- Policy library with reusable patterns
- Pre-flight checks for Supabase CLI and project setup
- Helper scripts for setup and testing
- Complete examples for each pattern
- Validation checklists with specific test queries

## [1.0.0] - 2025-10-22

### Added
- SupabasePower skill created by Mehdi Michiels
- Core workflow: Pre-flight → Gather → Generate → Validate
- Integration with Claude Code superpowers framework
```

**Step 3: Commit documentation files**

```bash
git add CLAUDE.md CHANGELOG.md
git commit -m "docs: add CLAUDE.md and CHANGELOG.md"
```

---

## Task 12: Update README with SupabasePower Name

**Files:**
- Review: All created files
- Test: SKILL.md workflow

**Step 1: Review all files for consistency**

Run:
```bash
cd /Users/mehdimichiels/Documents/supabase-database-skill/.worktrees/implement-skill
find . -name "*.md" -type f
```

Check that all files exist and follow consistent formatting.

**Step 2: Create a checklist for skill validation**

Create `docs/VALIDATION_CHECKLIST.md`:
```markdown
# Skill Validation Checklist

Before publishing, verify:

## Structure
- [ ] SKILL.md exists with proper YAML frontmatter
- [ ] README.md has installation instructions
- [ ] All four pattern templates exist in templates/
- [ ] Policy library exists in policies/
- [ ] At least one example exists in examples/

## Content
- [ ] SKILL.md clearly explains when to use the skill
- [ ] Each template has AskUserQuestion examples
- [ ] Policy library has SQL code blocks
- [ ] Examples show complete migrations

## Functionality
- [ ] Test single-user pattern workflow manually
- [ ] Verify migration SQL syntax is valid
- [ ] Check that RLS policies are properly commented
- [ ] Confirm validation tests are specific and runnable

## Documentation
- [ ] README has clear installation steps
- [ ] Examples show realistic use cases
- [ ] Policy library explains gotchas
- [ ] Templates explain when to use each pattern
```

**Step 3: Run validation checks**

```bash
# Check all markdown files are valid
for file in $(find . -name "*.md" -type f); do
  echo "Checking $file"
  # Could use markdownlint or similar
done
```

**Step 4: Commit validation checklist**

```bash
git add docs/VALIDATION_CHECKLIST.md
git commit -m "docs: add validation checklist for skill quality"
```

**Step 5: Create final commit**

```bash
git add .
git commit -m "feat: complete Supabase database skill implementation

- Four ownership patterns (single-user, multi-tenant, public-auth, admin-only)
- Template-driven generation with AskUserQuestion integration
- Commented RLS policies for dev-first workflow
- Policy library with reusable patterns
- Complete examples and validation tests
- Comprehensive documentation

Ready for testing and marketplace submission."
```

---

## Post-Implementation

After completing all tasks:

1. Test the skill in a real Supabase project
2. Gather feedback from initial users
3. Iterate on templates based on real usage
4. Consider submitting to Claude Code marketplace
5. Share with community and document learnings
