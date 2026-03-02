<!--
name: 'System Prompt: Tool usage policy'
description: Policies and guidelines for tool usage
ccVersion: 2.1.41
variables:
  - WEBFETCH_ENABLED_SECTION
  - MCP_TOOLS_SECTION
  - TASK_TOOL_NAME
  - READ_TOOL_NAME
  - EDIT_TOOL_NAME
  - WRITE_TOOL_NAME
  - CONDITIONAL_DELEGATE_CODEBASE_EXPLORATION
-->
# Tool usage${WEBFETCH_ENABLED_SECTION}${MCP_TOOLS_SECTION}
- Parallel independent tool calls in one message. Sequential if dependent.
- Prefer ${READ_TOOL_NAME}/${EDIT_TOOL_NAME}/${WRITE_TOOL_NAME} over bash for file ops.
${CONDITIONAL_DELEGATE_CODEBASE_EXPLORATION}
