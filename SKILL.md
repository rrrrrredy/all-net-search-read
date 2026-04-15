---
name: all-net-search-read
description: "Social media content search and extraction tool. Supports WeChat Official Accounts, Xiaohongshu, Twitter/X, YouTube, Reddit, Bilibili, Weibo. Triggers: search WeChat, search Xiaohongshu, search Weibo, search Twitter, search Bilibili, search YouTube, search Reddit, read article, full-web search, podcast transcript, Bilibili video download. Not for: internal corporate document search; login-required premium content; large-scale systematic scraping."
version: 18.0.0
tags: [search, social-media, wechat, xiaohongshu, twitter, youtube, bilibili, weibo]
---

# 🕵️ All-Net Search & Read 18.0.0

**Give your AI Agent the ability to search and read across all major platforms — WeChat, Weibo, Xiaohongshu, Twitter/X, YouTube, Reddit, Bilibili, and more.**

---

## ⚠️ Gotchas

> Known pitfalls — check here first before debugging.

⚠️ **Xiaohongshu notes require login cookies** → Both search and detail pages require authentication. Without cookies, only indirect third-party content is available via web search engines. Login options: ① F12 copy cookies (30 sec, recommended) ② SMS verification relay ③ QR code scan ④ Console JS one-liner.

⚠️ **Platform-specific search** → Each platform uses its own search strategy (site: prefix + web search). Don't mix platform search methods.

⚠️ **Twitter/X profile + timeline don't require login** → Use `x_scraper.py` (guest token method) for public profiles and timelines. Search functionality is still limited without auth-token.

⚠️ **Web search backend** → Supports two tiers: **agent-reach** (xreach/xread) for best results across 14+ platforms, with **Jina Search API** (free, no key) as automatic fallback. Install agent-reach via `npx clawhub install agent-reach` for full capabilities.

---

## 🛑 Hard Stop

If the same tool call fails more than 3 times, stop immediately. List all failed approaches and reasons, mark as **"Manual intervention required"**, and wait for user confirmation.

---

## ✨ Core Features

| Feature | Description |
|:---|:---|
| 🔍 **Full-Web Search** | Semantic search across the internet with time/source filtering |
| 📱 **WeChat Articles** | Search and read WeChat Official Account articles |
| 🐦 **Twitter/X** | View tweets, user profiles, search topics |
| 📕 **Xiaohongshu** | Note content extraction, search |
| 🎬 **Bilibili** | Video info, subtitles, comments |
| ▶️ **YouTube** | Video info, subtitles, comments |
| 💬 **Reddit** | Post and comment extraction |
| 📝 **Web Distilling** | Convert any webpage to clean Markdown |
| 📝 **Content Summary** | Auto-summarize long articles |
| 🏷️ **Keyword Extraction** | Auto-extract key info, people, terms |
| 🔔 **Scheduled Monitoring** | Monitor specific keywords/accounts for updates |
| 📊 **Content Comparison** | Compare viewpoints from multiple sources on same topic |
| 📥 **Multi-link Fetching** | Batch fetch multiple public links (max 5 per request, user confirms each) |
| 🎙️ **Voice Reading** | Convert articles to audio |
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
| Xiaohongshu | Playwright + cookies (with login) / web search fallback (without login) | ⚠️ Recommend configuring cookies |
| Weibo | Web search + Playwright (visitor cookie) | ❌ No |
| Bilibili | Bilibili API + yt-dlp | ❌ No |
| YouTube | yt-dlp | ❌ No |
| Reddit | Reddit JSON API | ❌ No |
| Twitter/X | xreach (agent-reach) → `x_scraper.py` (guest token fallback) | ❌ No (profile/timeline); search via xreach needs auth-token |
| General Web | xread (agent-reach) → Jina Reader / curl fallback | ❌ No |

> ⚠️ **Important**: Xiaohongshu search and note detail pages both require login cookies. Without cookies, only third-party aggregated content is available. With cookies, Playwright can directly search and read full notes.

---

## 🔄 Execution Strategy (Fallback Rules)

### Xiaohongshu Search

> Xiaohongshu notes require login cookies — search engines cannot effectively index Xiaohongshu note content without authentication. **Simplest login method: copy two cookie values from browser DevTools, ~30 seconds.**

#### 🔑 Option A: Cookie Configuration (Recommended, one-time setup)

```
1. Open https://www.xiaohongshu.com in your browser and log in
2. Press F12 → Application → Cookies → https://www.xiaohongshu.com
3. Copy the values of these two fields:
   - web_session
   - a1
4. Run the setup script:
   python3 scripts/xiaohongshu-setup-cookies.py
5. Paste both values when prompted; auto-saved to cookies config
```

Cookies typically last several days to weeks; repeat steps when expired.

#### 📱 Option B: SMS Verification Code Relay (Backup)

> Use when cookies have expired and browser DevTools is inconvenient.

**Steps:**
```
1. Agent opens Xiaohongshu login page via Playwright (with HTTP_PROXY if needed)
2. Use JS injection to check user agreement, then click "Get verification code"
3. User receives SMS and sends code back within 15 seconds
4. Agent fills in the code and completes login
5. Extract cookies and save to config
```

#### 📷 Option C: QR Code Scan Login

> User scans QR code with phone. May need HTTP proxy to complete login.

#### 🌐 Option D: Console JS Copy (Fastest)

```
1. Open https://www.xiaohongshu.com in browser (already logged in)
2. Press F12 → Console, paste:
   copy(document.cookie.split(';').reduce((o,s)=>{const[k,v]=s.trim().split('=');o[k]=v;return o},{}))
3. Send the clipboard JSON to the agent
4. Agent extracts web_session and a1, saves to config
```

#### Execution Strategy

```
Step 1: Check if cookie config exists and is valid
  ✅ Has cookies → Use Playwright to search notes
  ❌ No cookies → Step 2

Step 2: Ask user for login method
  A → Cookie Configuration
  B → SMS Verification Relay
  C → QR Code Scan
  D → Console JS Copy
  E → Skip login, use web search for indirect content

Step 3: Web search fallback
  → Search via Bing/Google for third-party content about Xiaohongshu topics
  → Inform user: this is indirect content; for original notes, choose a login option
```

#### Reading a Single Note (Known URL)

```
With cookies: Use Playwright to load and extract
Without cookies: Cannot read directly → Ask user to provide cookies or manually copy note content
```

### Twitter/X Search / Profile / Timeline

```
Step 1: Get profile or timeline (no login required)
  python3 scripts/x_scraper.py profile <handle>
  python3 scripts/x_scraper.py timeline <handle> --count 20
  ✅ Success → Return followers, bio, tweet list
  ❌ Proxy unavailable / API change → Step 2

Step 2: Fallback web search
  Web search for "site:twitter.com {keyword}"
  ✅ Success → Return tweets
  ❌ Failure → Inform user to configure search API or try again later
```

> ⚠️ `x_scraper.py` requires `HTTP_PROXY` to be set for environments where direct X access is blocked.

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
- [x-twitter-scraper](https://github.com/rrrrrredy/x-twitter-scraper) — Twitter/X guest token scraper (for profile/timeline without login)

---


> 各平台详细技术笔记（代理配置、API 特性、已知限制）见 `references/platform-notes.md`。

## 🔒 Security Constraints (Mandatory)

1. **Public internet content only**: Do not access internal/corporate domains
2. **Multi-link fetching requires user confirmation**: When multiple URLs are in one request, agent must list them and get explicit user approval before fetching (max 5 per batch)
3. **No large-scale scraping**: Do not use for systematic batch collection, automated loop downloads, or high-frequency requests to a single site
4. **Respect robots.txt and anti-scraping protections**
5. **Scheduled monitoring requires user notification**: Before setting up monitoring tasks, explain monitoring target, frequency, and data destination to the user

## ⚠️ Notes

1. **Twitter/X profile/timeline don't require login**: Use `x_scraper.py` (guest token) for profiles and timelines; search uses web search fallback
2. **Platform-specific search**: Each platform uses `site:` prefix with web search — don't mix search methods
3. **Xiaohongshu notes require login cookies**: Without cookies, only web search fallback provides indirect content. Two login options: ① Cookie copy (recommended, 30 sec) ② SMS verification relay
4. Some platforms (WeChat, Xiaohongshu) may be subject to anti-scraping restrictions
5. Scheduled monitoring requires cron job configuration

---

## Gotchas

⚠️ **小红书沙箱 IP 被封** → 所有登录路径失败，只能用 web search `site:xiaohongshu.com` 降级获取摘要。
⚠️ **微信公众号需要代理** → 沙箱直连微信服务器超时，必须配置 HTTP 代理。
⚠️ **Twitter/X guest token 有效期短** → 通常几小时过期，脚本会自动重新获取，但连续失败 3 次应停止。
⚠️ **B站字幕需要登录** → 无 cookie 只能获取视频流，字幕/弹幕需要登录态。
⚠️ **多链接批量获取需确认** → 一次请求含多个 URL 时，必须列出并获得用户确认（最多 5 个/批）。

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 18.0.0 | 2026-04-15 | Quality fix: standardize versioning, add Gotchas/Hard Stop sections |
