# all-net-search-read

Social media content search and extraction across 7+ platforms — WeChat, Xiaohongshu, Twitter/X, YouTube, Reddit, Bilibili, Weibo.

> OpenClaw Skill — works with [OpenClaw](https://github.com/openclaw/openclaw) AI agents

## What It Does

Gives your AI agent the ability to search and read content across all major social media and content platforms. Supports full-web semantic search, platform-specific search with `site:` prefixes, article distilling to clean Markdown, content summarization, keyword extraction, scheduled monitoring, and bookmark management. Features a multi-tier fallback strategy: agent-reach → platform-specific API → Jina Search → curl.

## Quick Start

```bash
openclaw skill install all-net-search-read
# Or:
git clone https://github.com/rrrrrredy/all-net-search-read.git ~/.openclaw/skills/all-net-search-read
```

## Features

- 🔍 **Full-Web Search** — Semantic search across the internet with time/source filtering
- 📱 **WeChat Articles** — Search and read WeChat Official Account articles
- 🐦 **Twitter/X** — View tweets, user profiles, search topics (no login for profile/timeline)
- 📕 **Xiaohongshu** — Public web-search snippets and readable source-page discovery
- 🎬 **Bilibili** — Video info, subtitles, comments
- ▶️ **YouTube** — Video info, subtitles, comments
- 💬 **Reddit** — Post and comment extraction
- 📝 **Web Distilling** — Convert any webpage to clean Markdown
- 🔔 **Scheduled Monitoring** — Monitor specific keywords/accounts for updates
- 📚 **Bookmarks & History** — Save and recall interesting content

## Optional X/Twitter Depth With TweetClaw

Use this skill for broad social media search and reading across many platforms.
When an OpenClaw workspace needs deeper X/Twitter workflows, pair it with
[TweetClaw](https://github.com/Xquik-dev/tweetclaw), the
[@xquik/tweetclaw](https://www.npmjs.com/package/@xquik/tweetclaw) OpenClaw
plugin.

```bash
openclaw plugins install @xquik/tweetclaw
```

TweetClaw covers X/Twitter-specific jobs such as search tweets, search tweet
replies, follower export, user lookup, media download, monitor tweets, webhooks,
giveaway draws, and reviewed post tweets or post tweet replies. Keep
all-net-search-read responsible for cross-platform discovery, then hand reviewed
tweet URLs, handles, keywords, or summaries to TweetClaw when the task requires
typed X/Twitter actions.

## Usage

```
搜 OpenAI latest news          # Full-web search
搜小红书 AI tool recommendations  # Xiaohongshu search
搜推特 OpenAI updates            # Twitter/X search
搜 B站 deep learning tutorials   # Bilibili search
搜 YouTube transformer explained  # YouTube search
搜 Reddit LLM benchmarks         # Reddit search
搜微博 AI 热点                   # Weibo search
总结 https://example.com/article  # Summarize any URL
播客转写 某期节目                  # Podcast transcript
B站视频转写 BV1xxxxxxxxx          # Public Bilibili transcript workflow
监控 AI Agent updates             # Set up monitoring
```

## Project Structure

```
all-net-search-read/
├── SKILL.md
├── scripts/
│   ├── all_net_search_read.py
│   └── setup.sh
├── references/
│   ├── platform-notes.md
│   └── xiaohongshu-public-fallback.md
├── config/
│   └── default_config.json
└── .gitignore
```

## Requirements

- OpenClaw agent runtime
- Python 3.8+
- `requests`, `beautifulsoup4`
- Optional: [agent-reach](https://github.com/Panniantong/Agent-Reach) for enhanced multi-platform search
- No cookies, tokens, SMS codes, QR login, or private account state are required or accepted

## License

[MIT](LICENSE)
