#!/usr/bin/env bash
# setup.sh - Dependency detection and installation
# Usage: bash scripts/setup.sh

set -e

echo "🔍 Checking all-net-search-read dependencies..."

MISSING=0

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
command -v curl &>/dev/null && echo "✅ curl" || echo "⚠️  curl missing (needed for web search)"
python3 -c "import requests, bs4; print('✅ Python dependencies')"

echo "🎉 Setup complete — all-net-search-read is ready to use"
