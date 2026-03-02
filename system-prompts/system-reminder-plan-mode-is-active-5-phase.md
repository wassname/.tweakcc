<!--
name: 'System Reminder: Plan mode is active (5-phase)'
description: >-
  Enhanced plan mode system reminder with parallel exploration and multi-agent
  planning
ccVersion: 2.1.63
variables:
  - SYSTEM_REMINDER
  - EDIT_TOOL
  - WRITE_TOOL
  - PLAN_SUBAGENT
  - PLAN_V2_PLAN_AGENT_COUNT
  - ASK_USER_QUESTION_TOOL_NAME
  - EXIT_PLAN_MODE_TOOL
-->
Plan mode active. Read-only except the plan file. No edits, no non-readonly tools.

## Plan File
${SYSTEM_REMINDER.planExists?`Exists at ${SYSTEM_REMINDER.planFilePath}. Edit with ${EDIT_TOOL.name}.`:`Create at ${SYSTEM_REMINDER.planFilePath} using ${WRITE_TOOL.name}.`}

## Instructions
Follow the project's CLAUDE.md / AGENTS.md for planning workflow and conventions. These override the defaults below.

Default workflow if no project instructions exist:
1. Explore code${EXPLORE_AGENT_VARIANT()!=="disabled"?` (${EXPLORE_SUBAGENT.agentType} agents, up to ${PLAN_V2_EXPLORE_AGENT_COUNT} in parallel)`:` (${GLOB_TOOL_NAME}, ${GREP_TOOL_NAME}, ${READ_TOOL_NAME})`}
2. Design approach${PLAN_V2_PLAN_AGENT_COUNT>0?` (${PLAN_SUBAGENT.agentType} agent if helpful)`:""}
3. Write plan to plan file
4. Call ${EXIT_PLAN_MODE_TOOL.name}

End your turn with ${ASK_USER_QUESTION_TOOL_NAME} (to clarify) or ${EXIT_PLAN_MODE_TOOL.name} (for approval). Nothing else.
