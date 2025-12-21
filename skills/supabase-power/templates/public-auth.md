# Public + Auth Hybrid Pattern

## Pattern Description

Anonymous users can read public data. Authenticated users can create and manage their own content. Common for blogs, marketplaces, social platforms.

**Policy rules:**
- SELECT: Allow anonymous if public
- INSERT/UPDATE/DELETE: Require auth and ownership check

## Questions to Ask

Use AskUserQuestion for each of these:

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

CREATE INDEX idx_<table>_user_id ON <table>(user_id);
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
