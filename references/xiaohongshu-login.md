# Xiaohongshu Login Methods

Xiaohongshu notes require login cookies — search engines cannot effectively index note content without authentication.

## Option A: Cookie Configuration (Recommended, ~30 seconds)

```
1. Open https://www.xiaohongshu.com in your browser and log in
2. Press F12 → Application → Cookies → https://www.xiaohongshu.com
3. Copy the values of these two fields:
   - web_session
   - a1
4. Send both values to the agent
5. Agent saves them to cookies config
```

Cookies typically last several days to weeks; repeat steps when expired.

## Option B: SMS Verification Code Relay (Backup)

> Use when cookies have expired and browser DevTools is inconvenient.

```
1. Agent opens Xiaohongshu login page via Playwright (with HTTP_PROXY if needed)
2. Use JS injection to check user agreement, then click "Get verification code"
3. User receives SMS and sends code back within 15 seconds
4. Agent fills in the code and completes login
5. Extract cookies and save to config
```

## Option C: QR Code Scan Login

User scans QR code with phone. May need HTTP proxy to complete login.

## Option D: Console JS Copy (Fastest)

```
1. Open https://www.xiaohongshu.com in browser (already logged in)
2. Press F12 → Console, paste:
   copy(document.cookie.split(';').reduce((o,s)=>{const[k,v]=s.trim().split('=');o[k]=v;return o},{}))
3. Send the clipboard JSON to the agent
4. Agent extracts web_session and a1, saves to config
```

## Execution Strategy

```
Step 1: Check if cookie config exists and is valid
  ✅ Has cookies → Use Playwright to search notes
  ❌ No cookies → Step 2

Step 2: Ask user for login method (A/B/C/D/E)
  E = Skip login, use web search for indirect content

Step 3: Web search fallback
  → Search via Bing/Google for third-party content
  → Inform user: this is indirect content
```

## Reading a Single Note (Known URL)

- With cookies: Use Playwright to load and extract
- Without cookies: Cannot read directly → Ask user to provide cookies or manually copy note content
