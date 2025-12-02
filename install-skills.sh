#!/bin/bash

# Claude Skills Collection - Install Script
# Installs all skills to your current project

set -e

echo "🧠 Installing Claude Skills Collection..."

# Create workflows directory if it doesn't exist
mkdir -p .agent/workflows

# Base URL for raw GitHub content
BASE_URL="https://raw.githubusercontent.com/MaydayTM/claude-skills-collection/main/skills"

# Install each skill
echo "📥 Downloading skills..."

# Dopamine Landing
curl -sL "$BASE_URL/dopamine-landing/dopamine-landing.md" -o .agent/workflows/dopamine-landing.md && \
  echo "✅ Installed: dopamine-landing"

# Precision Medicine
curl -sL "$BASE_URL/precision-medicine/precision-medicine.md" -o .agent/workflows/precision-medicine.md && \
  echo "✅ Installed: precision-medicine" || echo "⚠️  precision-medicine not yet published"

# Supabase Power
curl -sL "$BASE_URL/supabase-power/supabase-power.md" -o .agent/workflows/supabase-power.md && \
  echo "✅ Installed: supabase-power" || echo "⚠️  supabase-power not yet published"

# Stripe Auto Setup
curl -sL "$BASE_URL/stripe-auto-setup/stripe-auto.md" -o .agent/workflows/stripe-auto.md && \
  echo "✅ Installed: stripe-auto-setup" || echo "⚠️  stripe-auto-setup not yet published"

echo ""
echo "✨ Skills installed to .agent/workflows/"
echo ""
echo "Usage:"
echo "  /dopamine-landing    - Create dopamine-driven landing pages"
echo "  /precision-medicine  - Medical development workflows"
echo "  /supabase-power      - Supabase setup automation"
echo "  /stripe-auto         - Stripe integration automation"
echo ""
echo "🚀 Happy coding!"
