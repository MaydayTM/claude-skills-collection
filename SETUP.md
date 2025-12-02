# Quick Setup Guide

## ✅ What's Done

Your Claude Skills Collection is created with:
- ✅ dopamine-landing
- ✅ precision-medicine  
- ✅ supabase-power
- ✅ stripe-auto-setup

## 🚀 Next Steps

### 1. Push to GitHub

```bash
cd /Users/mehdimichiels/.gemini/antigravity/scratch/claude-skills-collection

# Create repo on GitHub first, then:
git remote add origin https://github.com/MaydayTM/claude-skills-collection.git
git push -u origin main
```

### 2. Use Skills in Any Project

**Option A: Install all skills**
```bash
cd your-project
curl -L https://raw.githubusercontent.com/MaydayTM/claude-skills-collection/main/install-skills.sh | bash
```

**Option B: Clone locally once**
```bash
git clone https://github.com/MaydayTM/claude-skills-collection.git ~/.claude-skills

# Then in any project:
cp ~/.claude-skills/skills/dopamine-landing/*.md .agent/workflows/
```

**Option C: Install specific skill**
```bash
mkdir -p .agent/workflows
cp /Users/mehdimichiels/.gemini/antigravity/scratch/claude-skills-collection/skills/dopamine-landing/dopamine-landing.md .agent/workflows/
```

### 3. Invoke Skills in Claude

Once skills are in `.agent/workflows/`:
```
/dopamine-landing - Create landing page
/precision-medicine - Medical workflows
/supabase-power - Supabase setup
/stripe-auto - Stripe integration
```

## 🌟 About Superpowers

The Superpowers you mentioned from `~/.claude/plugins/cache/superpowers/skills/` is a separate Claude plugin system.

**These are two different systems:**

1. **This Skills Collection** → For Claude Code (this editor)
2. **Superpowers** → For Claude.ai chat interface

You can use both! They complement each other.

## 📝 Adding More Skills

When you create a new skill:

1. Create it as a GitHub repo
2. Clone it into `skills/[skill-name]/`
3. Update README.md
4. Commit and push

```bash
cd claude-skills-collection
git clone https://github.com/MaydayTM/new-skill.git skills/new-skill
git add .
git commit -m "Add new-skill"
git push
```
