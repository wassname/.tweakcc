<!--
name: 'Tool Description: Task'
description: Tool description for launching specialized sub-agents to handle complex tasks
ccVersion: 2.1.53
variables:
  - TASK_TOOL_PREAMBLE
  - TASK_TOOL
  - READ_TOOL
  - GLOB_TOOL
  - GET_SUBSCRIPTION_TYPE_FN
  - IS_TRUTHY_FN
  - PROCESS_OBJECT
  - IS_IN_TEAMMATE_CONTEXT_FN
  - TASK_TOOL_OBJECT
  - WRITE_TOOL
-->
${TASK_TOOL_PREAMBLE}

When NOT to use: for specific file reads (use ${READ_TOOL}/${GLOB_TOOL}), searching 2-3 files, or tasks unrelated to agent descriptions.

Usage:
- Short description (3-5 words) per agent${GET_SUBSCRIPTION_TYPE_FN()!=="pro"?`
- Launch multiple agents concurrently in a single message`:""}${!IS_TRUTHY_FN(PROCESS_OBJECT.env.CLAUDE_CODE_DISABLE_BACKGROUND_TASKS)&&!FALSE()?`
- run_in_background: you will be notified on completion — do NOT sleep, poll, or proactively check`:""}
- Agent results are not visible to user; summarize them in text
- resume: pass agent ID to continue previous context
- isolation: "worktree" for isolated repo copy (auto-cleaned if no changes)
- Tell agents whether to write code or just research
- If agent should be used proactively per its description, do so
- Parallel: multiple ${TASK_TOOL_OBJECT.name} calls in one message${FALSE()?`
- run_in_background, name, team_name, mode not available here`:""}
