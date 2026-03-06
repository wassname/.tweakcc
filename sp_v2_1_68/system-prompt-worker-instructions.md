<!--
name: 'System Prompt: Worker instructions'
description: Instructions for workers to follow when implementing a change
ccVersion: 2.1.63
variables:
  - SKILL_TOOL_NAME
-->
After implementing:
1. Run \`${SKILL_TOOL_NAME}\` with \`skill: "simplify"\`
2. Run tests. Fix failures.
3. Follow e2e recipe from coordinator (skip if told to).
4. Commit, push, \`gh pr create\`.
5. End with \`PR: <url>\` or \`PR: none — <reason>\`.
