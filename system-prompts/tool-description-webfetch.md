<!--
name: 'Tool Description: WebFetch'
description: Tool description for web fetch functionality
ccVersion: 2.1.268
variables:
  - WEBFETCH_CACHE_TTL_FN
-->

- Fetches content from a specified URL and processes it using an AI model
- Takes a URL and a prompt as input
- Fetches the URL content, converts HTML to markdown
- Processes the content with the prompt using a small, fast model
- Returns the model's response about the content
- Use this tool when you need to retrieve and analyze web content

Usage notes:
  - IMPORTANT: If an MCP-provided web fetch tool or a skill is available for the specific domain (e.g., gh for GitHub, arxiv-fetch for arXiv), prefer using that instead as it has fewer restrictions and better formatting.
  - The URL must be a fully-formed valid URL. Do NOT generate or guess URLs unless confident they are correct.
  - HTTP URLs will be automatically upgraded to HTTPS
  - localhost and hostnames without a dot are unsupported; use curl for local servers
  - Preserve the user's requested output form in the prompt. A request for a quotation, raw excerpt, or download is not a request for a summary.
  - This tool is read-only and does not modify any files
  - For quotations, request the whole relevant passage verbatim with at least one sentence before and after the key sentence, unchanged spelling and punctuation, the key fragment bolded, and the final URL.
  - To download or save a page or file, use curl, wget, or a domain tool and write it to the requested path; WebFetch itself is read-only.
  - Includes a self-cleaning cache (entries expire after ${WEBFETCH_CACHE_TTL_FN()})
  - When a URL redirects to a different host, the tool will inform you and provide the redirect URL in a special format. You should then make a new WebFetch request with the redirect URL to fetch the content.
  - For GitHub URLs, prefer using the gh CLI via Bash instead (e.g., gh pr view, gh issue view, gh api).
  - For evidence-grade research, save the source to disk, then extract and relay exact contextual passages rather than re-summarizing them.
