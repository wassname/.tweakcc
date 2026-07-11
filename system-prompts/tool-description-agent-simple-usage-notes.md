<!--
name: 'Tool Description: Agent (simple usage notes)'
description: >-
  Simplified usage notes for the Agent tool, including when to delegate, fork
  behavior, resumption, worktree isolation, background execution, parallel
  launches, and context restrictions
ccVersion: 2.1.140
variables:
  - TOOL_BASE_DESCRIPTION
  - HAS_PRO_RESTRICTION_NOTE
  - CAN_FORK_CONTEXT
  - SEND_MESSAGE_TOOL_NAME
  - AGENT_TOOL_NAME
  - RUN_IN_BACKGROUND_NOTE
  - PARALLEL_AGENTS_NOTE
  - CONTEXT_RESTRICTION_NOTE
-->

Delegate when the task matches an agent type, when you have independent parallel work, or when answering requires reading many files. For single-fact lookups where you know the file, search directly. Don't duplicate work you've delegated.

- Agent results are not shown to the user -- relay their quotes and links to the user, don't re-summarize into unsupported claims
- Trust but verify: check actual changes before reporting done
- Instruct research/review agents to produce block quotes with links as primary output, not bare claims
- Use SendMessage to resume an agent with context; new Agent call starts fresh
- isolation: "worktree" for parallel file mutations
