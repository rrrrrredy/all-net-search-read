# 🕵️ All-Net Search & Read

**Give your AI Agent the ability to search and read across all major social media platforms.**

Supports: WeChat Official Accounts, Xiaohongshu (Little Red Book), Twitter/X, YouTube, Reddit, Bilibili, Weibo, and more.

## Features

| Feature | Description |
|---|---|
| 🔍 Full-Web Search | Semantic search across the internet |
| 📱 WeChat Articles | Search and read WeChat Official Account articles |
| 🐦 Twitter/X | View tweets, profiles, search topics |
| 📕 Xiaohongshu | Note content extraction and search |
| 🎬 Bilibili | Video info, subtitles, comments |
| ▶️ YouTube | Video info, subtitles, comments |
| 💬 Reddit | Post and comment extraction |
| 📝 Web Distilling | Convert any webpage to clean Markdown |
| 🔔 Monitoring | Scheduled keyword/account monitoring |

## Quick Start

```bash
# Install dependencies
bash scripts/setup.sh

# Run
python3 scripts/all_net_search_read.py "搜 AI Agent latest news"
```

## Dependencies

- Python 3.8+
- `requests`, `beautifulsoup4`
- Optional: `xreach-cli` (for Twitter/X search)

## Structure

```
all-net-search-read/
├── SKILL.md                    # Full skill documentation
├── README.md                   # This file
├── config/
│   └── default_config.json     # Default configuration
├── references/
│   └── platform-notes.md       # Platform-specific notes & SOPs
└── scripts/
    ├── setup.sh                # Dependency installer
    └── all_net_search_read.py  # Main entry point
```

## Platform Support

| Platform | Login Required | Notes |
|---|---|---|
| Twitter/X | ❌ (profile/timeline) | Guest token method, no account needed |
| Weibo | ❌ | Visitor cookie auto-set |
| Bilibili | ❌ | Public API |
| YouTube | ❌ | yt-dlp |
| Reddit | ❌ | JSON API |
| Xiaohongshu | ⚠️ Recommended | Cookie setup enables full search |
| WeChat | ❌ | May need HTTP proxy |

## License

MIT
