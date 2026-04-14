# Platform-Specific Notes

## Xiaohongshu (Little Red Book)
- Requires login cookies for search and note detail pages
- Without cookies: fallback to web search engines for indirect content
- Cookie setup: F12 → Application → Cookies → copy `web_session` + `a1`

## WeChat Official Accounts
- WeChat articles require HTTP proxy in some network environments
- Direct access from cloud IPs may be blocked by WeChat
- Set `HTTP_PROXY` environment variable if direct access fails

## Twitter/X
- Use `x_scraper.py` (guest token) for profiles and timelines — no account needed
- Search uses web search fallback (site:twitter.com queries)
- Set `HTTP_PROXY` if direct access to X is blocked

## Weibo

**Recommended approach**: Web search engine + Playwright (visitor cookie)

| Method | Status | Notes |
|------|--------|------|
| Web search + Playwright | ✅ Stable | **Primary path, see SOP below** |
| Weibo AJAX API (no login) | ❌ Unavailable | Returns -100, requires login |

**SOP (Web Search + Playwright)**:

1. **Locate user UID and post URLs**
   - Search: `"@username site:weibo.com"` or `"weibo.com/u/username"`
   - Extract UID from search result URLs (`weibo.com/u/<UID>` format)

2. **Get visitor cookie** (Playwright opens any Weibo page → auto-sets visitor cookie)
   - Navigate to `https://weibo.com/u/<UID>`
   - Page will auto-set visitor cookie, no login required for public content

3. **Extract single post content**
   - Text CSS selector: `.detail_wbtext_4CRf9`
   - Fallback: extract text blocks near timestamp elements

4. **Get recent N posts (two approaches)**
   - Approach A (recommended): Search `site:weibo.com/u/<UID>` to enumerate recent URLs, visit each
   - Approach B: Open user homepage in Playwright, scrape post list (limited without login)

**Limitations**:
- Only public posts visible without login (cannot see "followers-only" content)
- Media (images/video) viewable but not directly downloadable
- Timeline accuracy depends on search result ordering
- For full history/login content → user needs browser extension or manual login

## Bilibili
- Hot/trending data accessible without login via web APIs
- Subtitles may need browser extension for extraction

### Bilibili Video Download SOP

**Principle**: Bilibili public API provides video stream CDN URLs without cookies, but the CDN domain may require HTTP proxy in some environments.

**SOP (5 steps)**:

**Step 1: Get video metadata (BV → cid/aid)**
```bash
curl -s "https://api.bilibili.com/x/web-interface/view?bvid=<BV>" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print('title:', d['title']); print('cid:', d['cid']); print('aid:', d['aid'])"
```

**Step 2: Get latest video list (UID → BV IDs)**
```bash
yt-dlp "https://space.bilibili.com/<UID>/video" \
  --flat-playlist --playlist-end 5 --print "%(id)s"
```

**Step 3: Get video stream CDN URL**
```bash
curl -s "https://api.bilibili.com/x/player/playurl?avid=<aid>&cid=<cid>&qn=16&fnval=0&fnver=0&fourk=0" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/video/<BV>" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['durl'][0]['url'])"
```

**Step 4: Download (use HTTP_PROXY if needed)**
```bash
curl ${HTTP_PROXY:+-x $HTTP_PROXY} -L "<CDN_URL>" -o /tmp/bili_video.mp4 \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/video/<BV>" \
  --progress-bar
```

**Step 5 (Optional): Transcribe with faster-whisper**
```python
from faster_whisper import WhisperModel
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, _ = model.transcribe('/tmp/bili_video.mp4', language='zh')
text = ' '.join([s.text for s in segments])
```

**Notes**:
- CDN URLs expire in ~1 hour; download promptly
- Referer header is required; CDN returns 403 without it
- Paid/VIP content cannot be accessed this way
- /tmp files are ephemeral; persist if needed

## Xiaoyuzhou Podcast (xiaoyuzhoufm.com)

**Characteristics**: Next.js SPA — direct web fetch methods fail; use RSS feed approach.

**Recommended approach**: iTunes API → RSS → audio download → transcription

| Method | Status | Notes |
|------|--------|------|
| iTunes API → RSS → audio | ✅ Stable | **Primary path** |
| web_fetch direct access | ❌ Unavailable | SPA, returns JS skeleton only |
| Jina Reader | ❌ Unavailable | Cannot render SPA |
| yt-dlp | ❌ Unavailable | Returns HTTP 404 |

**SOP (iTunes API → RSS → faster-whisper)**:

1. **Find RSS URL (iTunes Search, no proxy needed)**
   ```bash
   curl "https://itunes.apple.com/search?term=<podcast_name>&media=podcast&country=CN&limit=5" \
     | python3 -c "import json,sys; data=json.load(sys.stdin); [print(r['collectionName'],'->',r.get('feedUrl','N/A')) for r in data['results']]"
   ```

2. **Download RSS XML (use HTTP_PROXY if needed)**
   ```bash
   curl ${HTTP_PROXY:+-x $HTTP_PROXY} -L "<feedUrl>" -o /tmp/podcast_feed.xml
   ```

3. **Parse latest episode**
   ```python
   import xml.etree.ElementTree as ET
   tree = ET.parse("/tmp/podcast_feed.xml")
   channel = tree.getroot().find('channel')
   latest = channel.findall('item')[0]
   audio_url = latest.find('enclosure').get('url')
   title = latest.find('title').text
   print(f"{title} -> {audio_url}")
   ```

4. **Download audio (use HTTP_PROXY if needed)**
   ```bash
   curl ${HTTP_PROXY:+-x $HTTP_PROXY} -L "<audio_url>" -o /tmp/podcast.m4a --progress-bar
   ```

5. **Transcribe (faster-whisper, CPU mode)**
   ```python
   from faster_whisper import WhisperModel
   model = WhisperModel("small", device="cpu", compute_type="int8")
   segments, info = model.transcribe("/tmp/podcast.m4a", language="zh", beam_size=5)
   with open("/tmp/transcript.txt", "w") as f:
       for seg in segments: f.write(f"[{seg.start:.1f}s] {seg.text}\n")
   ```
   ⚠️ An 80-minute audio file takes ~15-30 minutes on CPU. Notify the user before starting.

**Limitations**:
- Only works with podcasts that provide RSS feeds (most Xiaoyuzhou podcasts do)
- Transcription is local CPU, speed ~3-5x realtime (small model, CPU int8)
- For AI features (summarization/QA) → feed transcript to LLM after completion
