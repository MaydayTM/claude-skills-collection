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
