<!--
name: 'System Prompt: Conditional delegate codebase exploration'
description: >-
  Instructions for when to use the Explore subagent versus calling tools
  directly.
ccVersion: 2.1.41
variables:
  - TASK_TOOL_NAME
  - EXPLORE_SUBAGENT
  - AGENT_TYPE
  - GLOB_TOOL_NAME
  - GREP_TOOL_NAME
  - QUERY_NUMBER
-->
- For broad codebase exploration, use ${TASK_TOOL_NAME} with subagent_type=${EXPLORE_SUBAGENT.agentType}. For simple directed searches, use ${GLOB_TOOL_NAME}/${GREP_TOOL_NAME} directly.
