<!--
name: 'Tool Description: WebSearch'
description: Tool description for web search functionality
ccVersion: 2.1.42
variables:
  - CURRENT_MONTH_YEAR
-->
Search the web for up-to-date information. Returns results as markdown hyperlinks.

MUST include "Sources:" section with [Title](URL) links after answering.

Current month: ${CURRENT_MONTH_YEAR()}. Use this year in queries for recent info.
Domain filtering supported. US only.
