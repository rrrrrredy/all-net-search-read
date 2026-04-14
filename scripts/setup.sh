#!/usr/bin/env bash
# setup.sh - 首次使用依赖检测与安装
# Usage: bash scripts/setup.sh

set -e

echo "🔍 检测 all-net-search-read 依赖..."

MISSING=0

# 检测依赖 Skill: agent-reach
echo ""
echo "--- Skill 依赖 ---"
if [ -f ~/.openclaw/skills/agent-reach/SKILL.md ]; then
  echo "✅ agent-reach Skill 已安装"
else
  echo "⚠️  agent-reach Skill 未安装"
  MISSING=1
  echo "📦 安装 agent-reach..."
  echo "   注意：agent-reach 不在 Friday 广场，mtskills i agent-reach 会报 400，这是正常现象"
  if command -v mtskills &>/dev/null; then
    mtskills i agent-reach --target-dir ~/.openclaw/skills || {
      echo "❌ agent-reach 安装失败，请手动执行: mtskills i agent-reach --target-dir ~/.openclaw/skills"
    }
  else
    echo "⚠️  mtskills 未安装，先安装 mtskills..."
    npm install -g @mtfe/mtskills --registry=http://r.npm.sankuai.com
    mtskills i agent-reach --target-dir ~/.openclaw/skills || {
      echo "❌ agent-reach 安装失败，请手动执行: mtskills i agent-reach --target-dir ~/.openclaw/skills"
    }
  fi
fi

# 检测 npm 依赖: xreach-cli（Twitter/X 功能）
echo ""
echo "--- npm 依赖 ---"
if command -v xreach &>/dev/null; then
  echo "✅ xreach-cli"
else
  echo "⚠️  xreach-cli 未安装（Twitter/X 搜索功能需要）"
  MISSING=1
  echo "📦 安装 xreach-cli..."
  npm install -g xreach-cli || echo "⚠️  xreach-cli 安装失败，Twitter/X 搜索功能将不可用"
fi

# 检测 Python 依赖
echo ""
echo "--- Python 依赖 ---"
PIP_MISSING=0
for pkg in requests beautifulsoup4; do
  mod="$pkg"
  [ "$pkg" = "beautifulsoup4" ] && mod="bs4"
  if python3 -c "import $mod" &>/dev/null; then
    echo "✅ $pkg"
  else
    echo "⚠️  $pkg 未安装"
    PIP_MISSING=1
  fi
done

if [ "$PIP_MISSING" -eq 1 ]; then
  MISSING=1
  echo "📦 安装缺失的 Python 依赖..."
  pip install requests beautifulsoup4
fi

if [ "$MISSING" -eq 0 ]; then
  echo ""
  echo "✅ 所有依赖已就绪"
else
  echo ""
  echo "✅ 依赖安装完成"
fi

# 最终验证
echo ""
echo "🔍 最终验证..."
[ -f ~/.openclaw/skills/agent-reach/SKILL.md ] && echo "✅ agent-reach" || echo "❌ agent-reach 缺失"
command -v xreach &>/dev/null && echo "✅ xreach-cli" || echo "⚠️  xreach-cli 缺失（仅影响 Twitter/X 搜索）"
python3 -c "import requests, bs4; print('✅ Python 依赖')"

echo "🎉 setup 完成，可以正常使用 all-net-search-read"
