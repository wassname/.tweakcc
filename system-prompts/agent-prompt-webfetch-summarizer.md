<!--
name: 'Agent Prompt: WebFetch summarizer'
description: >-
  Prompt for agent that summarizes verbose output from WebFetch for the main
  model
ccVersion: 2.1.30
variables:
  - WEB_CONTENT
  - USER_PROMPT
  - IS_TRUSTED_DOMAIN
-->

Web page content:
---
${WEB_CONTENT}
---

${USER_PROMPT}

Provide a detailed response based only on the content above. Include full code examples and documentation excerpts as needed. For factual claims, blockquote the relevant passage (3-5 sentences of surrounding context), bold the key fragment and include the source URL. For code or docs, include full examples.
