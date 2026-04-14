#!/usr/bin/env bash
# setup.sh - Dependency detection and installation
# Usage: bash scripts/setup.sh

set -e

echo "🔍 Checking all-net-search-read dependencies..."

MISSING=0

# Check npm dependency: xreach-cli (Twitter/X features)
echo ""
echo "--- npm dependencies ---"
if command -v xreach &>/dev/null; then
  echo "✅ xreach-cli"
else
  echo "⚠️  xreach-cli not installed (needed for Twitter/X search)"
  MISSING=1
  echo "📦 Installing xreach-cli..."
  npm install -g xreach-cli || echo "⚠️  xreach-cli installation failed; Twitter/X search will be unavailable"
fi

# Check Python dependencies
echo ""
echo "--- Python dependencies ---"
PIP_MISSING=0
for pkg in requests beautifulsoup4; do
  mod="$pkg"
  [ "$pkg" = "beautifulsoup4" ] && mod="bs4"
  if python3 -c "import $mod" &>/dev/null; then
    echo "✅ $pkg"
  else
    echo "⚠️  $pkg not installed"
    PIP_MISSING=1
  fi
done

if [ "$PIP_MISSING" -eq 1 ]; then
  MISSING=1
  echo "📦 Installing missing Python dependencies..."
  pip install requests beautifulsoup4
fi

if [ "$MISSING" -eq 0 ]; then
  echo ""
  echo "✅ All dependencies ready"
else
  echo ""
  echo "✅ Dependency installation complete"
fi

# Final verification
echo ""
echo "🔍 Final verification..."
command -v xreach &>/dev/null && echo "✅ xreach-cli" || echo "⚠️  xreach-cli missing (only affects Twitter/X search)"
python3 -c "import requests, bs4; print('✅ Python dependencies')"

echo "🎉 Setup complete — all-net-search-read is ready to use"
