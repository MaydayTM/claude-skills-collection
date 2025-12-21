#!/bin/bash
# SupabasePower - Supabase Setup Helper
# Guides users through Supabase CLI installation and project initialization

set -e

echo "=== SupabasePower Setup Helper ==="
echo

# Check if Supabase CLI is installed
if command -v supabase &> /dev/null; then
  echo "✓ Supabase CLI is already installed ($(supabase --version))"
else
  echo "✗ Supabase CLI is not installed"
  echo
  echo "Would you like to install it now? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
      echo "Installing via Homebrew..."
      brew install supabase/tap/supabase
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
      echo "Installing via install script..."
      curl -fsSL https://cli.supabase.com/install.sh | sh
    else
      echo "Please install manually: https://supabase.com/docs/guides/cli"
      exit 1
    fi
  else
    echo "Skipping installation. Visit https://supabase.com/docs/guides/cli"
    exit 0
  fi
fi

echo
echo "=== Project Initialization ==="
echo

# Check if already in a Supabase project
if [ -f "supabase/config.toml" ]; then
  echo "✓ Supabase project already initialized"
else
  echo "✗ No Supabase project found in current directory"
  echo
  echo "Initialize Supabase project here? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    supabase init
    echo "✓ Supabase project initialized"
  else
    echo "Skipping initialization"
    exit 0
  fi
fi

echo
echo "=== Local Development Setup ==="
echo

# Check if local Supabase is running
if supabase status &> /dev/null; then
  echo "✓ Local Supabase is running"
else
  echo "✗ Local Supabase is not running"
  echo
  echo "Start local Supabase now? (y/n)"
  read -r answer

  if [ "$answer" = "y" ]; then
    echo "Starting local Supabase (this may take a few minutes)..."
    supabase start
    echo
    echo "✓ Local Supabase is running"
    echo
    supabase status
  else
    echo "You can start it later with: supabase start"
  fi
fi

echo
echo "=== Setup Complete ==="
echo "You're ready to use SupabasePower!"
echo "Try: Ask Claude to 'use supabasepower skill' to generate migrations"
