# Admin-Only Pattern

## Pattern Description

Only administrators can access data. Regular users are completely locked out. Common for backoffice tools, CMS admin panels, internal dashboards.

**Policy rule:** Check admin status via role column in profiles table.

## Questions to Ask

Use AskUserQuestion for each of these:

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
