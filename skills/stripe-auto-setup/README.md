# Claude Code Commands Library

A collection of reusable Claude Code slash commands for common development tasks.

## What is This?

This repository contains ready-to-use slash commands for [Claude Code](https://claude.com/claude-code) that automate common setup and development tasks.

## Available Commands

### 🛒 E-commerce & Payments
- **`/setup-stripe-checkout`** - Complete Stripe checkout integration with Supabase Edge Functions

### 🗄️ Database & Backend (Coming Soon)
- **`/setup-supabase-auth`** - Authentication setup with Supabase
- **`/setup-blog-cms`** - Full-featured blog CMS with Supabase
- **`/debug-supabase`** - Troubleshoot common Supabase issues

### 🌍 Frontend & Deployment (Coming Soon)
- **`/setup-multilingual`** - i18n setup for multi-language sites
- **`/setup-vercel-deploy`** - Vercel deployment configuration

## How to Use

### Method 1: Install in Your Project (Recommended)

```bash
# In your project root
mkdir -p .claude/commands
curl -o .claude/commands/setup-stripe-checkout.md \
  https://raw.githubusercontent.com/YOUR_USERNAME/claude-code-commands/main/commands/setup-stripe-checkout.md
```

Then in Claude Code:
```
/setup-stripe-checkout
```

### Method 2: Clone Entire Library

```bash
# Clone this repo
git clone https://github.com/YOUR_USERNAME/claude-code-commands.git

# Copy commands to your project
cp claude-code-commands/commands/* your-project/.claude/commands/
```

### Method 3: Use as Git Submodule (Advanced)

```bash
# In your project root
git submodule add https://github.com/YOUR_USERNAME/claude-code-commands.git .claude/command-library
ln -s .claude/command-library/commands .claude/commands
```

## Command Documentation

Each command includes:
- ✅ Step-by-step instructions
- ✅ Required prerequisites
- ✅ Code templates
- ✅ Common troubleshooting
- ✅ Testing procedures

## Contributing

Have a useful command? Submit a PR!

1. Create command in `commands/your-command.md`
2. Follow the template structure
3. Test thoroughly
4. Submit PR with description

## Command Template

```markdown
# Command Name

Brief description of what this command does.

## Context
What problem does this solve?

## Required Information from User
What does the AI need to ask before starting?

## Step-by-Step Implementation
Detailed steps with code examples...

## Common Issues & Solutions
Troubleshooting guide...

## Success Criteria
How to verify it worked...
```

## License

MIT License - Use freely in your projects!

## Credits

Created by [Your Name] for the Claude Code community.
