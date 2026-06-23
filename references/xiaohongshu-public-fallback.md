# Xiaohongshu Public Fallback Policy

Xiaohongshu note search and detail pages often require a logged-in session. This skill does not request, store, relay, or extract cookies, SMS codes, QR logins, browser profiles, session tokens, or private account state.

## Allowed Path

1. Search public web indexes with queries such as `site:xiaohongshu.com <keyword>`.
2. Open only results that are readable without login.
3. Summarize public snippets or readable public pages with a source caveat.
4. If the exact note is login-gated, ask the user to paste the content they are authorized to share.

## Not Allowed

- DevTools cookie copying.
- Console JavaScript to extract `document.cookie`.
- SMS verification relay.
- QR-code login relay.
- Saving cookies or session values to config.
- Using the user's logged-in browser state to access restricted notes.

## Output Caveat

When using search snippets or third-party indexed results, state that the result is indirect and may be incomplete, stale, or reordered by the search engine.
