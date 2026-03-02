<!--
name: 'Tool Description: Sleep'
description: Tool for waiting/sleeping with early wake capability on user input
ccVersion: 2.1.38
variables:
  - TICK_PROMPT
-->
Wait for a duration. User can interrupt. On <${TICK_PROMPT}> check-ins, look for useful work first.

Can run concurrently with other tools. Prefer over \`Bash(sleep ...)\` (no shell process held).
Each wake costs an API call; prompt cache expires after 5 min inactivity.
