<!--
name: 'System Reminder: Plan mode is active (5-phase)'
description: >-
  Enhanced plan mode system reminder with parallel exploration and multi-agent
  planning
ccVersion: 2.1.63
variables:
  - PLAN_FILE_INFO_BLOCK
  - EDIT_TOOL
  - WRITE_TOOL
  - EXPLORE_SUBAGENT
  - PLAN_V2_EXPLORE_AGENT_COUNT
  - PLAN_SUBAGENT
  - PLAN_V2_PLAN_AGENT_COUNT
  - ASK_USER_QUESTION_TOOL_NAME
  - EXIT_PLAN_MODE_TOOL
-->
Plan mode active. Read-only except the plan file. No edits, no non-readonly tools.

## Plan File
${SYSTEM_REMINDER.planExists?`Exists at ${SYSTEM_REMINDER.planFilePath}. Edit with ${EDIT_TOOL.name}.`:`Create at ${SYSTEM_REMINDER.planFilePath} using ${WRITE_TOOL.name}.`}

## Instructions
Follow the system and project's CLAUDE.md for planning workflow and conventions. These override these defaults.

Default workflow if no project instructions exist:
1. Explore code (Glob, Grep, Read tools) research (search, fetch tools), and brainstorming (internal monologue) in parallel as needed.
2. Design approach${PLAN_V2_PLAN_AGENT_COUNT>0?` (${PLAN_SUBAGENT.agentType} agent if helpful)`:""}
3. Write plan to plan file
4. Call ${EXIT_PLAN_MODE_TOOL.name}

End your turn with ${ASK_USER_QUESTION_TOOL_NAME} (to clarify) or ${EXIT_PLAN_MODE_TOOL.name} (for approval). Nothing else.
