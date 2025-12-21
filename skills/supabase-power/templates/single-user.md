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
  updated_at TIMESTAMPTZ DEFAULT now(),
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
