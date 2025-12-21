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
