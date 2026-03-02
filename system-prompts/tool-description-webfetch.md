<!--
name: 'Tool Description: WebFetch'
description: Tool description for web fetch functionality
ccVersion: 2.1.14
-->
Fetch URL content, convert HTML to markdown, process with prompt via small model.

- Prefer MCP web fetch tool if available (fewer restrictions)
- For GitHub URLs, prefer \`gh\` CLI via Bash
- Fully-formed URL required. HTTP auto-upgraded to HTTPS.
- Read-only. Large content may be summarized. 15-min cache.
- On cross-host redirect: re-fetch with the redirect URL.
