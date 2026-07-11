<!--
name: 'Tool Description: Agent (usage notes)'
description: >-
  Usage notes and instructions for the Task/Agent tool, including guidance on
  launching subagents, background execution, resumption, and worktree isolation
ccVersion: 2.1.105
variables:
  - TOOL_BASE_DESCRIPTION
  - TOOL_PARAMETERS_DESCRIPTION
  - ENVIRONMENT_CONFIG
  - IS_SUBAGENT_CONTEXT_FN
  - HAS_SUBAGENT_TYPES
  - SEND_MESSAGE_TOOL_NAME
  - AGENT_TOOL_NAME
  - CAN_FORK_CONTEXT
  - IS_REMOTE_ISOLATION_AVAILABLE_FN
  - IS_TEAMMATE_CONTEXT_FN
  - ADDITIONAL_USAGE_NOTES
  - EXTRA_USAGE_NOTES
  - SUBAGENT_TYPE_DEFINITIONS
  - DEFAULT_AGENT_DESCRIPTION
-->

- Include a short description summarizing what the agent will do
- Agent results are not visible to the user -- relay their quotes and links to the user, don't re-summarize into unsupported claims
- Trust but verify: check actual changes before reporting done
- Instruct research/review agents to produce block quotes with links as primary output, not bare claims
- Use SendMessage with the agent's ID/name to continue with context; a new Agent call starts fresh
- Agents run in the background by default (you're notified on completion); pass run_in_background: false when you need results before proceeding
- For parallel agents, send multiple Agent calls in a single message
- isolation: "worktree" for agents that mutate files in parallel
