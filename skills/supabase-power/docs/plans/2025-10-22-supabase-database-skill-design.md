# Supabase Database Structure Skill Design

**Author:** Mehdi Michiels
**Date:** 2025-10-22
**Status:** Draft

## Problem

Developers waste hours debugging Supabase database structures and RLS policies. Common failures include policies that block legitimate queries, mismatches between development and production environments, wrong table structures, and auth integration bugs. These failures occur because developers must remember dozens of patterns, security rules, and gotchas while designing schemas.

## Solution

A Claude Code skill generates battle-tested Supabase migrations from feature requirements. The skill asks structured questions, applies proven patterns, generates migration files with commented-out RLS policies for development, and provides validation checklists for pre-production testing.

## Workflow

The skill follows three phases: Gather, Generate, Validate.

### Phase 1: Gather Requirements

The skill asks questions using the AskUserQuestion tool. First, it identifies the ownership pattern by presenting four scenarios:

- **Single-user SaaS:** Users own their data
- **Multi-tenant:** Teams own data, members have roles
- **Public + Auth hybrid:** Some data public, some private
- **Admin-only:** Backoffice or CMS patterns

Each scenario loads a question template. The skill asks 3-5 follow-up questions:
- Table names and column requirements
- Relationships between tables
- Access patterns (who reads and writes what)
- Special requirements (soft deletes, audit logs, timestamps)

### Phase 2: Generate Migration

The skill creates a migration file: `supabase/migrations/YYYYMMDDHHMMSS_feature_name.sql`

The migration includes:

**Tables:** Standard structure with `id`, `created_at`, `updated_at`, plus ownership columns (`user_id` or `team_id`). Foreign keys respect dependency order.

**Indexes:** Applied immediately after table creation. User-owned data gets indexes on `user_id`. Team-owned data gets indexes on `team_id`. Additional indexes follow query patterns.

**RLS Policies (commented out):** All policies start commented for fast development iteration. Clear section markers separate development from production code:

```sql
-- ============================================
-- RLS POLICIES (disabled for development)
-- Uncomment before production deployment
-- ============================================
-- ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "users_read_own" ON posts FOR SELECT
--   USING (auth.uid() = user_id);
```

**Helper Functions:** Generated when policies need complex checks (team membership, role verification). These also start commented out.

### Phase 3: Validate Before Production

The skill creates a TodoWrite checklist with specific test queries. Each test includes:
- The SQL query to run
- Instructions for setting test context (`SET request.jwt.claims.sub`)
- Expected results (which rows should appear)
- What the test verifies (policy correctness, performance, auth integration)

Example test:
```sql
-- Test: Authenticated users see only their rows
SET request.jwt.claims.sub = 'user-uuid-here';
SELECT * FROM posts;
-- Expected: Returns only posts where user_id = 'user-uuid-here'
-- Verifies: user_owns_row policy works correctly
```

The checklist includes a pre-production workflow:
1. Uncomment RLS sections in migration
2. Run `supabase db reset` in local dev
3. Execute each test query
4. Fix failures before deploying
5. Run `supabase db push` to staging first

## Components

### Question Templates

Each ownership scenario has pre-configured questions. The single-user template asks about user-owned tables and privacy levels. The multi-tenant template asks about team structure, member roles, and permission hierarchies. The public + auth template asks which data is public versus protected. The admin-only template asks about admin identification and role structure.

### Migration Templates

Templates provide proven SQL patterns. User-owned patterns use `auth.uid() = user_id`. Team-owned patterns join through membership tables. Public-read patterns allow anonymous SELECT. Admin patterns check role columns. All templates include:
- Standard timestamp columns
- Foreign key constraints with proper CASCADE rules
- Indexes on foreign keys and ownership columns
- Comments explaining policy intent

### Policy Library

Reusable policy patterns include:

**user_owns_row:** `auth.uid() = user_id`
**user_in_team:** Checks team membership via join table
**is_admin:** Verifies `profiles.role = 'admin'`
**public_read_auth_write:** Anonymous can SELECT, authenticated can INSERT/UPDATE/DELETE
**team_member_read:** Team members can read team data
**team_admin_write:** Only team admins can modify

### Validation Generator

Generates test queries based on the migration. For each policy, creates tests for:
- Positive case (should succeed)
- Negative case (should fail)
- Edge case (boundary conditions)
- Performance (query plan uses indexes)

## Development vs Production

The skill supports "work first, secure later" by generating migrations with commented RLS policies. Developers iterate fast without auth barriers. When ready for production, they uncomment policy sections and test locally with RLS enabled. This prevents last-minute security scrambling while keeping production secure.

## Error Prevention

The skill prevents common mistakes:

**Pre-flight checks** verify `supabase/migrations/` exists and Supabase CLI is available.

**Generation defaults** always enable RLS, never create tables without policies, add explanatory comments, and include rollback sections.

**Explicit clarification** asks follow-up questions when requirements are ambiguous. If user says "auth users can access" without specifying owned versus all data, the skill asks explicitly.

**Dependency detection** notices missing tables. If multi-tenant but no team membership table mentioned, the skill alerts and offers to generate it. If admin role mentioned but no `profiles.role` column, it flags the dependency.

**Soft delete handling** automatically adds `deleted_at` when requested and updates policies to filter soft-deleted rows.

## Success Criteria

The skill succeeds when:
- Developers generate correct migrations without manual policy writing
- RLS policies work on first uncomment without debugging
- Local testing catches security gaps before production
- Development iteration stays fast without auth complexity
- Production deployments have zero RLS-related failures

## Out of Scope

This skill does not:
- Modify existing tables (migrations only)
- Generate application code (queries, API routes)
- Handle database backups or recovery
- Optimize existing slow queries (focuses on new structures)
- Support databases other than Supabase/PostgreSQL
