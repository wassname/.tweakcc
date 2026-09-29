<!--
name: 'Tool Description: WebFetch (concise)'
description: >-
  Concise tool description for WebFetch covering URL fetching, private URL
  limitations, redirects, and caching
ccVersion: 2.1.277
variables:
  - FORMAT_CONCISE_ARTIFACT_LINK_NOTE_FN
  - ARTIFACT_LINK_HANDLING_MODE
  - WEBFETCH_CACHE_TTL_FN
-->
Fetches a URL, converts the page to markdown, and answers \`prompt\` with a small model. Preserve the user's requested form: quotation, excerpt, raw content, and download are not summaries. For quotations, request the whole relevant passage verbatim with at least one sentence before and after the key sentence, unchanged spelling, attribution, and final URL. For downloads or a full raw page, use curl, wget, or a domain tool because WebFetch is read-only.

- Authenticated/private URLs need an authenticated MCP tool or \`gh\`.${FORMAT_CONCISE_ARTIFACT_LINK_NOTE_FN(ARTIFACT_LINK_HANDLING_MODE)}
- Localhost and other hostnames without a dot need curl via Bash. HTTP is upgraded to HTTPS; follow a reported cross-host redirect with a new call.
- Responses are cached for ${WEBFETCH_CACHE_TTL_FN()} per URL.
