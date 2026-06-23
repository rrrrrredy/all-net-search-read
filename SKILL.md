---
name: all-net-search-read
description: 'Public social media content search and extraction tool. Supports WeChat Official Accounts, Xiaohongshu public web results, Twitter/X public profiles, YouTube, Reddit, Bilibili public metadata/transcripts, and Weibo visible posts. Triggers: search WeChat, search Xiaohongshu, search Weibo, search Twitter, search Bilibili, search YouTube, search Reddit, read article, full-web search, podcast transcript. Not for: internal documents; login-required or premium content; cookies/tokens/SMS/QR login; large-scale systematic scraping.'
---

# 🕵️ All-Net Search & Read 18.0.0

**Give your AI Agent the ability to search and read across all major platforms — WeChat, Weibo, Xiaohongshu, Twitter/X, YouTube, Reddit, Bilibili, and more.**

---

## ⚠️ Gotchas

> Known pitfalls — check here first before debugging.

⚠️ **Xiaohongshu full note pages often require login** → Do not request or store cookies, SMS codes, QR login, or session tokens. Use public web search results only; if the user needs exact note text, ask them to paste the content or provide a public page that is readable without login.

⚠️ **Platform-specific search** → Each platform uses its own search strategy (site: prefix + web search). Don't mix platform search methods.

⚠️ **Twitter/X profile + timeline don't require login** → Use agent-reach (`xreach`) for public profiles and timelines. Search functionality is limited without authentication; do not request auth tokens or cookies.

⚠️ **Web search backend** → Supports two tiers: **agent-reach** (xreach/xread) for best results across 14+ platforms, with **Jina Search API** (free, no key) as automatic fallback. Install agent-reach via `npx clawhub install agent-reach` for full capabilities.

⚠️ **小红书沙箱 IP 被封或页面要求登录** → 只能用 web search `site:xiaohongshu.com` 降级获取公开摘要或第三方索引结果。

⚠️ **微信公众号需要代理** → 沙箱直连微信服务器超时，必须配置 HTTP 代理（`HTTP_PROXY`）。

⚠️ **B站字幕/弹幕可能需要登录** → 不请求 cookie；仅处理无需登录即可访问的公开视频元数据、音频或转写结果。

⚠️ **多链接批量获取需确认** → 一次请求含多个 URL 时，必须列出并获得用户确认（最多 5 个/批）。

---

## 🛑 Hard Stop

If the same tool call fails more than 3 times, stop immediately. List all failed approaches and reasons, mark as **"Manual intervention required"**, and wait for user confirmation.

---

## Input / Output Contract

Required input is one of: a public URL, a platform + keyword query, a public account/profile identifier, or pasted content. For multi-link requests, list the URLs and obtain confirmation before processing more than one link.

Return a fixed result shape:

1. Task interpreted: platform, query/URL, and access mode.
2. Retrieval path: primary tool and any fallback used.
3. Results: extracted public content, summaries, metadata, or transcript snippets.
4. Source evidence: links, timestamps, account/profile identifiers, and caveats.
5. Missing or blocked content: login walls, deleted content, rate limits, or unsupported private access.

Do not output private content, cookies, tokens, login instructions, or claims that a login-only page was fully read.

---

## ✨ Core Features

| Feature | Description |
|:---|:---|
| 🔍 **Full-Web Search** | Semantic search across the internet with time/source filtering |
| 📱 **WeChat Articles** | Search and read WeChat Official Account articles |
| 🐦 **Twitter/X** | View tweets, user profiles, search topics |
| 📕 **Xiaohongshu** | Public web-search snippets and source-page discovery |
| 🎬 **Bilibili** | Public video info and transcript-oriented workflows |
| ▶️ **YouTube** | Video info, subtitles, comments |
| 💬 **Reddit** | Post and comment extraction |
| 📝 **Web Distilling** | Convert any webpage to clean Markdown |
| 📝 **Content Summary** | Auto-summarize long articles |
| 🏷️ **Keyword Extraction** | Auto-extract key info, people, terms |
| 🔔 **Scheduled Monitoring** | Monitor specific keywords/accounts for updates |
| 📥 **Multi-link Fetching** | Batch fetch multiple public links (max 5 per request, user confirms each) |
| 📚 **Bookmarks** | Save interesting content |
| 🕐 **History** | Remember previous searches |

---

## 🎯 Trigger Words

### Search
- `搜 {keyword}` — Full-web search (e.g., `搜 OpenAI latest news`)
- `{keyword} recent news` — Filter by time
- `{platform} {keyword}` — Platform-specific search

### Platform-Specific
- `看 {account name} 最新文章` — WeChat article reading
- `搜小红书 {keyword}` — Xiaohongshu search
- `搜 Twitter {keyword}` / `搜推特 {keyword}` — Twitter search
- `搜 B站 {keyword}` — Bilibili search
- `搜 YouTube {keyword}` — YouTube search
- `搜 Reddit {keyword}` — Reddit search

### Content Processing
- `{URL}` — Web distilling/reading
- `总结 {content/link}` — Content summary
- `提取关键词 {content/link}` — Keyword extraction

### Management
- `我的收藏` — View bookmarks
- `收藏这个` — Bookmark current content
- `搜索历史` / `我的记录` — History
- `监控 {keyword}` — Set up scheduled monitoring

---

## 📖 Usage Examples

### 1. Full-Web Search
```
搜 OpenAI latest funding news
```
→ Returns relevant content from across the web

### 2. WeChat Article Reading
```
搜 机器之心 最近文章
```
→ Returns latest article list from the WeChat account

### 3. Platform-Specific Search
```
小红书 AI tool recommendations
推特 OpenAI latest updates
B站 deep learning tutorials
```

### 4. Web Distilling
```
https://example.com/article
```
→ Auto-converts to clean Markdown, removes ads

### 5. Content Summary
```
总结 https://mp.weixin.qq.com/s/xxx
```
→ Returns core takeaways

### 6. Keyword Extraction
```
提取关键词 https://news.ycombinator.com/xxx
```
→ Returns key people, terms, organizations

### 7. Scheduled Monitoring
```
监控 AI Agent updates
```
→ Push daily/weekly updates on the topic

### 8. Bookmark Management
```
我的收藏
收藏这个
```

---

## 🛠️ Technical Backend

Each platform uses appropriate tools:

| Platform | Backend Tool | Account Required |
|---|---|---|
| Xiaohongshu | Public web search fallback only | ❌ No; login-only notes are out of scope |
| Weibo | Web search + Playwright visitor-mode public rendering | ❌ No |
| Bilibili | Public Bilibili API + yt-dlp where permitted | ❌ No |
| YouTube | yt-dlp | ❌ No |
| Reddit | Reddit JSON API | ❌ No |
| Twitter/X | xreach (agent-reach) → web search fallback | ❌ No; authenticated search is out of scope |
| General Web | xread (agent-reach) → Jina Reader / curl fallback | ❌ No |

> ⚠️ **Important**: Xiaohongshu search and note detail pages often require login. This skill does not request or store cookies; use public search snippets, public source pages, or user-provided text only.

---

## 🔄 Execution Strategy (Fallback Rules)

### Xiaohongshu Search

> Xiaohongshu full note pages often require login. This skill does not collect login cookies or run login flows.
> For the public-only fallback policy, see `references/xiaohongshu-public-fallback.md`.

**Quick path**: public web search (`site:xiaohongshu.com`) → readable public result → summarize with source caveat; login wall → ask user to paste content or provide a readable public source.

### Twitter/X Search / Profile / Timeline

```
Step 1: Use agent-reach (xreach) for profile or timeline (no login required)
  xreach twitter profile <handle>
  xreach twitter timeline <handle> --count 20
  ✅ Success → Return followers, bio, tweet list
  ❌ agent-reach unavailable / API change → Step 2

Step 2: Fallback web search
  Web search for "site:twitter.com {keyword}"
  ✅ Success → Return tweets
  ❌ Failure → Inform user to configure search API or try again later
```

> ⚠️ In environments where direct X access is blocked, ensure `HTTP_PROXY` is set for agent-reach to connect.

### General Fallback Principle
Prefer agent-reach (xreach/xread) → platform-specific API → Jina web search → curl

---

## First Use

Run the dependency check script before first use:
```bash
bash scripts/setup.sh
```
> The agent will auto-run this on first trigger; usually no manual action needed.

---

## 📦 Dependencies & Installation

### Python packages
- Python 3.8+
- `requests`
- `beautifulsoup4`

### Optional: Search API
For better search results, configure a search API key in `config/default_config.json`. Supported: Brave Search, SerpAPI, or any compatible web search API.

### Recommended: Agent Reach (enhanced multi-platform search & read)

**agent-reach** provides powerful multi-platform search and content extraction across 14+ platforms. The skill auto-detects and uses it when available; without it, falls back to Jina Search API.

**Install agent-reach (choose one):**
```bash
# Option 1: pip (recommended — installs Python package + CLI)
pip install agent-reach
agent-reach install --env=auto --safe

# Option 2: ClawHub (installs skill entry point)
npx clawhub install agent-reach
```

After installation, run `agent-reach doctor` to check which platforms are available. The skill automatically detects `xreach` (search) and `xread` (content extraction) CLIs at runtime.

**Optional add-ons for agent-reach** (unlock more platforms):
```bash
# Exa semantic search (recommended)
npm install -g mcporter
mcporter config add exa https://mcp.exa.ai/mcp

# Reddit
pip install 'rdt-cli>=0.4.2'
```

> Without agent-reach, the skill falls back to **Jina Search API** (free, no key required) — still works for most use cases.

### Optional: Dependency Skills
- [agent-reach](https://clawhub.com) — Multi-platform search & read (xreach/xread/mcporter CLIs)

---


> 各平台详细技术笔记（代理配置、API 特性、已知限制）见 `references/platform-notes.md`。

## 🔒 Security Constraints (Mandatory)

1. **Public internet content only**: Do not access internal/corporate domains
2. **Multi-link fetching requires user confirmation**: When multiple URLs are in one request, agent must list them and get explicit user approval before fetching (max 5 per batch)
3. **No large-scale scraping**: Do not use for systematic batch collection, automated loop downloads, or high-frequency requests to a single site
4. **Respect robots.txt and anti-scraping protections**
5. **Scheduled monitoring requires user notification**: Before setting up monitoring tasks, explain monitoring target, frequency, and data destination to the user
6. **No credential collection**: Do not ask for cookies, tokens, SMS codes, QR-code login, browser profiles, or private account state.

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 18.0.0 | 2026-04-15 | Quality fix: standardize versioning, add Gotchas/Hard Stop sections |
