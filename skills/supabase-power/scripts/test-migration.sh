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
