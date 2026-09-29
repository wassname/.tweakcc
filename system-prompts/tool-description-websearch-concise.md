<!--
name: 'Tool Description: WebSearch (concise)'
description: >-
  Describes the concise WebSearch tool variant with US-only results,
  current-month guidance, domain filters, and required sources
ccVersion: 2.1.173
variables:
  - CURRENT_MONTH_YEAR
-->
Search the web. Results include titles and URLs. Snippets are discovery, not primary evidence: open or fetch a result before quoting or asserting page content, then relay the contextual passage.

- Use ${CURRENT_MONTH_YEAR} for recent information.
- \`allowed_domains\` and \`blocked_domains\` filter results.
- End answers based on results with a Sources list of the URLs used.
