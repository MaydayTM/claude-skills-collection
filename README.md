# 🧠 Claude Skills Collection

A central repository for all reusable Claude Code skills. Clone once, use everywhere!

## 📦 Available Skills

### 1. **Dopamine Landing** (`dopamine-landing`)
Build high-converting landing pages using dopamine-driven psychology
- 5-section framework
- Neuroscience-backed engagement
- [Full Docs](./skills/dopamine-landing/README.md)

### 2. **Precision Medicine** (`precision-medicine`)
Medical and health-tech development skill
- [Full Docs](./skills/precision-medicine/README.md)

### 3. **Supabase Power** (`supabase-power`)
Supabase setup and configuration automation
- [Full Docs](./skills/supabase-power/README.md)

### 4. **Stripe Auto Setup** (`stripe-auto-setup`)
Automated Stripe payment integration
- [Full Docs](./skills/stripe-auto-setup/README.md)

---

## 🚀 Quick Start

### Install All Skills to a Project

```bash
# From your project root
curl -L https://raw.githubusercontent.com/MaydayTM/claude-skills-collection/main/install-skills.sh | bash
```

### Install a Specific Skill

```bash
# Example: Install dopamine-landing skill
mkdir -p .agent/workflows
curl https://raw.githubusercontent.com/MaydayTM/claude-skills-collection/main/skills/dopamine-landing/dopamine-landing.md -o .agent/workflows/dopamine-landing.md
```

### Use Skills Locally

```bash
# Clone this repo once
git clone https://github.com/MaydayTM/claude-skills-collection.git ~/.claude-skills

# In any project, copy the skills you need
cp ~/.claude-skills/skills/dopamine-landing/*.md .agent/workflows/
```

---

## 📚 How to Use Skills

Once a skill is in your project's `.agent/workflows/` directory:

1. **Open Claude Code** in your project
2. **Invoke the skill** by typing: `/skill-name`
3. **Follow the prompts** from Claude

Example:
```
/dopamine-landing - Create a landing page for [your product]
/precision-medicine - Generate medical documentation
/supabase-power - Set up Supabase authentication
```

---

## ➕ Adding New Skills

To add a new skill to this collection:

1. Create your skill repository
2. Add it as a submodule or copy it to `skills/[skill-name]/`
3. Update this README
4. Commit and push

```bash
# Add as Git submodule
git submodule add https://github.com/MaydayTM/your-new-skill.git skills/your-skill-name

# Or copy manually
cp -r /path/to/your-skill skills/your-skill-name
git add skills/your-skill-name
git commit -m "Add [skill-name] skill"
```

---

## 🔄 Keeping Skills Updated

To update all skills from their source repositories:

```bash
cd ~/.claude-skills
git pull
git submodule update --remote --merge
```

---

## 🌟 Superpowers Integration

This collection is compatible with [Claude Superpowers Marketplace](https://github.com/obra/superpowers-marketplace).

To use these skills with Superpowers:
```bash
# Link to Superpowers directory
ln -s ~/.claude-skills/skills ~/.claude/plugins/cache/superpowers/skills/custom

# Update Superpowers
claude plugins update
```

---

## 📝 Skill Structure

Each skill should follow this structure:

```
skills/[skill-name]/
├── README.md              # Skill documentation
├── [skill-name].md        # Main workflow file (with YAML frontmatter)
├── examples/              # Example usage
└── templates/             # Optional templates
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch
3. Add your skill following the structure above
4. Submit a pull request

---

## 📄 License

MIT License - Use freely in personal and commercial projects.

---

**Built for speed. Designed for reuse. Ready to deploy.** 🚀
