<!--
name: 'Tool Description: EnterPlanMode'
description: >-
  Tool description for entering plan mode to explore and design implementation
  approaches
ccVersion: 2.1.63
variables:
  - ASK_USER_QUESTION_TOOL_NAME
  - CONDITIONAL_WHAT_HAPPENS_NOTE
-->
Use proactively for non-trivial implementation tasks. Gets user sign-off before writing code.

Use when: new features, multiple valid approaches, multi-file changes, unclear requirements, architectural decisions.
Skip for: single-line fixes, trivial tasks, specific detailed instructions, pure research.

${CONDITIONAL_WHAT_HAPPENS_NOTE}Requires user approval. If unsure, prefer planning over diving in.
