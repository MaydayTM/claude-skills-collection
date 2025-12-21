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
