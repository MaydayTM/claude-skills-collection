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
