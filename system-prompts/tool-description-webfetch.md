<!--
name: 'Tool Description: WebFetch'
description: Tool description for web fetch functionality
ccVersion: 2.1.14
-->
Fetch URL content, convert HTML to markdown, process with prompt via small model. Full content is always often summarized by a subagent -- original text is not preserved.

- prefer specific mcp or skills if available for this domain for better formatting and fewer restrictions
- For evidence-grade research (need full text, blockquotes, save to disk), use bash: \`$CMD {url} > docs/evidence/{slug}.md\` instead
- Fully-formed URL required. HTTP auto-upgraded to HTTPS.
- Read-only. Large content may be summarized. 15-min cache.
- On cross-host redirect: re-fetch with the redirect URL.
