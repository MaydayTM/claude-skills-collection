#!/bin/bash

# Instructions to push dopamine-landing-skill to GitHub
# 
# BEFORE RUNNING THIS:
# 1. Log in to GitHub at https://github.com/login
# 2. Create new repo at https://github.com/new
#    - Name: dopamine-landing-skill
#    - Description: A reusable AI skill for building high-converting landing pages using dopamine-driven psychology
#    - Public repository
#    - DO NOT initialize with README/gitignore/license
# 3. Replace YOUR-USERNAME below with your actual GitHub username
# 4. Run this script OR copy-paste the commands below

# Replace this with your GitHub username!
GITHUB_USERNAME="YOUR-USERNAME"

cd /Users/mehdimichiels/.gemini/antigravity/scratch/dopamine-landing-skill

# Add the remote origin
git remote add origin https://github.com/$GITHUB_USERNAME/dopamine-landing-skill.git

# Push to GitHub
git branch -M main
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo "🌐 View your repo at: https://github.com/$GITHUB_USERNAME/dopamine-landing-skill"
