<!--
name: 'Tool Description: ToolSearch'
description: Tool description for loading and searching deferred tools before use
ccVersion: 2.1.31
variables:
  - EXTENDED_TOOL_SEARCH_PROMPT
-->
Load deferred tools before calling them. Deferred tools are NOT available until discovered via this tool. Check <available-deferred-tools> messages for discoverable tools. Both search and select modes load the returned tools immediately.${EXTENDED_TOOL_SEARCH_PROMPT}
