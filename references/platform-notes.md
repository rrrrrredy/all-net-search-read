# 各平台注意事项

## 小红书
- full note pages often require login; this skill does not collect or use cookies, tokens, SMS codes, QR login, or browser profiles
- 降级：public web search → readable public page or user-provided text

## 微信公众号
- 必须走上游代理：YOUR_PROXY_HOST:PORT
- 直连沙箱 IP 被微信封锁

## 推特/X
- 需要 opencli 或 agent-reach，直接 fetch 被封

## 微博（Weibo）

**沙箱可用路径**（优先级排序）：

| 方法 | 可用性 | 说明 |
|------|--------|------|
| catclaw-search + agent-browser | ✅ 稳定 | **主路径，见下方 SOP** |
| opencli weibo | ❌ 不可用 | 需要 Chrome extension relay，沙箱不通 |
| 微博 ajax API（未登录） | ❌ 不可用 | 返回 -100，需登录 |
| Camoufox headless | ❌ 不稳定 | 初始化时访问 github.com/releases 超时 |

**SOP（catclaw-search + agent-browser）**：

1. **定位用户 UID 和帖子 URL**
   - catclaw-search 搜索：`"@用户名 site:weibo.com"` 或 `"weibo.com/u/用户名"`
   - 从搜索结果 URL 提取 UID（`weibo.com/u/<UID>` 格式）

2. **使用访客态公开渲染**（agent-browser 打开微博公开页面）
   - `browser open: https://weibo.com/u/<UID>`
   - 只读取公开可见内容；不要检查、导出、复制或保存 cookie/session 值

3. **抓取单条微博正文**
   - 正文 CSS selector：`.detail_wbtext_4CRf9`
   - selector 失效备选：提取页面中时间戳附近的文本块（时间戳前约50字符）

4. **获取最近N条帖子（两种方案）**
   - 方案A（推荐）：catclaw-search 搜索 `site:weibo.com/u/<UID>` 枚举近期 URL，逐一访问
   - 方案B：agent-browser 打开用户主页，抓取帖子列表（未登录显示有限）

**限制**：
- 未登录只能看公开帖子，无法看"仅粉丝可见"内容
- 获取带图片/视频的帖子时只能得到文本，不能直接下载媒体文件
- 精确时间线依赖搜索结果排序，不保证绝对准确顺序
- 需要完整历史/登录内容 → 本 skill 不支持；请用户提供其有权分享的公开 URL 或文本

## B站
- 字幕内容需要 Chrome 插件 attach tab（用户手动点 Attach Tab）
- 热榜数据可直接 web_fetch 无需登录

### B站公开视频转写 SOP

**边界**：仅用于无需登录即可访问的公开视频，并且只为转写/摘要临时处理媒体文件。不处理付费、大会员、私密、地区受限或需要 cookie 的内容。

**原理**：B站公开 API 无需 cookie 即可获取部分公开视频流 CDN URL，但 bilivideo.com 沙箱直连可能超时，必要时走用户配置的上游代理。

**可用路径表**：

| 方法 | 可用性 | 说明 |
|------|--------|------|
| 公开 API + 上游代理临时获取 | 可用性需运行时验证 | **主路径** |
| yt-dlp 直连 | ❌ 不可用 | B站 412 反爬，无 cookie |
| yt-dlp + 代理 | ❌ 不可用 | bilivideo.com 代理 403 CONNECT tunnel |
| 直连 bilivideo.com | ❌ 不可用 | 沙箱出口 IP 超时 |

**SOP（5步）**：

**步骤1：获取视频元信息（BV → cid/aid）**
```bash
curl -s "https://api.bilibili.com/x/web-interface/view?bvid=<BV>" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print('title:', d['title']); print('cid:', d['cid']); print('aid:', d['aid'])"
```

**步骤2：获取最新视频列表（UID → BV号列表）**
```bash
~/.local/bin/yt-dlp "https://space.bilibili.com/<UID>/video" \
  --flat-playlist --playlist-end 5 --print "%(id)s"
```
> 注：`/x/space/arc/search` API 需登录（返回 -799），用 yt-dlp 代替。

**步骤3：获取视频流 CDN URL**
```bash
curl -s "https://api.bilibili.com/x/player/playurl?avid=<aid>&cid=<cid>&qn=16&fnval=0&fnver=0&fourk=0" \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/video/<BV>" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['durl'][0]['url'])"
```

**步骤4：用上游代理临时获取媒体（仅公开视频）**
```bash
curl -x http://YOUR_PROXY_HOST:PORT -L "<CDN_URL>" -o /tmp/bili_video.mp4 \
  -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.bilibili.com/video/<BV>" \
  --progress-bar
```

**步骤5（可选）：faster-whisper 转写**
```python
from faster_whisper import WhisperModel
model = WhisperModel('base', device='cpu', compute_type='int8')
segments, _ = model.transcribe('/tmp/bili_video.mp4', language='zh')
text = ' '.join([s.text for s in segments])
```

**踩坑**：
- bilivideo.com CDN URL 约 1 小时有效，尽快处理并删除临时文件
- 本地代理 127.0.0.1:8118 对 bilivideo.com 返回 403 CONNECT tunnel，必须用 YOUR_PROXY_HOST:PORT
- Referer 头不能省，否则 CDN 返回 403
- 付费/会员视频无法用此方法
- /tmp 重启丢失，及时持久化

## 小宇宙播客（xiaoyuzhoufm.com）

**特性**：Next.js SPA，直接静态读取通常只能得到 JS 骨架，优先走 RSS Feed。

**沙箱可用路径**（推荐顺序）：

| 方法 | 可用性 | 说明 |
|------|--------|------|
| iTunes API → RSS → 临时音频获取 | 可用性需运行时验证 | **主路径，见下方 SOP** |
| web_fetch 直接访问 | ❌ 不可用 | SPA，只返回 JS 骨架 |
| Jina Reader | ❌ 不可用 | SPA 无法渲染 |
| yt-dlp | ❌ 不可用 | 返回 HTTP 404 |
| 小宇宙 APP API | ❌ 不可用 | 需登录 token（401） |

**SOP（iTunes API → RSS → faster-whisper）**：

1. **查 RSS URL（iTunes Search，无需代理）**
   ```bash
   curl "https://itunes.apple.com/search?term=<播客名>&media=podcast&country=CN&limit=5" \
     | python3 -c "import json,sys; data=json.load(sys.stdin); [print(r['collectionName'],'->',r.get('feedUrl','N/A')) for r in data['results']]"
   ```

2. **下载 RSS XML（必须走上游代理）**
   ```bash
   curl -x http://YOUR_PROXY_HOST:PORT -L "<feedUrl>" -o /tmp/podcast_feed.xml
   ```

3. **解析最新一期**
   ```python
   import xml.etree.ElementTree as ET
   tree = ET.parse("/tmp/podcast_feed.xml")
   channel = tree.getroot().find('channel')
   latest = channel.findall('item')[0]
   audio_url = latest.find('enclosure').get('url')
   title = latest.find('title').text
   print(f"{title} -> {audio_url}")
   ```

4. **临时获取音频（必须走上游代理）**
   ```bash
   curl -x http://YOUR_PROXY_HOST:PORT -L "<audio_url>" -o /tmp/podcast.m4a --progress-bar
   ```

5. **转写（faster-whisper，CPU 模式）**
   ```python
   # pip install faster-whisper -q
   from faster_whisper import WhisperModel
   model = WhisperModel("small", device="cpu", compute_type="int8")
   segments, info = model.transcribe("/tmp/podcast.m4a", language="zh", beam_size=5)
   with open("/tmp/transcript.txt", "w") as f:
       for seg in segments: f.write(f"[{seg.start:.1f}s] {seg.text}\n")
   ```
   ⚠️ 80 分钟音频约需 15-30 分钟 CPU 时间，执行前告知用户。

**限制**：
- 只能获取有 RSS Feed 的播客（大部分小宇宙播客均提供 RSS）
- 转写为本地 CPU，速度约 3-5x 实时（small 模型，CPU int8）
- 需要完整 AI 功能（总结/QA）→ 转写完成后喂给 LLM 处理
