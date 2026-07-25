<!--
name: 'Tool Description: Agent (usage notes)'
description: >-
  Usage notes and instructions for the Task/Agent tool, including guidance on
  launching subagents, background execution, resumption, and worktree isolation
ccVersion: 2.1.105
variables:
  - TOOL_BASE_DESCRIPTION
  - WHEN_NOT_TO_USE_NOTE
  - CAN_RUN_BACKGROUND_AGENTS
  - IS_FORK_SUBAGENT_FEATURE_ENABLED
  - CAN_FORK_CONTEXT
  - SEND_MESSAGE_TOOL_NAME
  - AGENT_TOOL_NAME
  - IS_DEFAULT_SUBAGENT_STEERING_MODE
  - IS_REMOTE_ISOLATION_AVAILABLE_FN
  - IS_IN_PROCESS_TEAMMATE_CONTEXT_FN
  - IS_TEAMMATE_CONTEXT_FN
  - FORK_USAGE_GUIDELINES
  - WRITING_SUBAGENT_PROMPTS_GUIDANCE
  - FORK_CAPABLE_SUBAGENT_DELEGATION_EXAMPLES
  - NON_FORK_SUBAGENT_DELEGATION_EXAMPLES
-->

- Include a short description summarizing what the agent will do
- Agent results are not visible to the user -- relay their quotes and links to the user, don't re-summarize into unsupported claims
- Trust but verify: check actual changes before reporting done
- Instruct research/review agents to produce block quotes with links as primary output, not bare claims
- Use SendMessage with the agent's ID/name to continue with context; a new Agent call starts fresh
- Agents run in the background by default (you're notified on completion); pass run_in_background: false when you need results before proceeding
- For parallel agents, send multiple Agent calls in a single message
- isolation: "worktree" for agents that mutate files in parallel
