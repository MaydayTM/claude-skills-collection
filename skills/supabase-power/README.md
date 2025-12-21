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
