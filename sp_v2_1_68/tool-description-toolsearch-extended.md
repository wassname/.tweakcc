<!--
name: 'Tool Description: ToolSearch extended'
description: Extended usage instructions for ToolSearch including query modes and examples
ccVersion: 2.1.31
-->

**Deferred tools are not loaded until discovered via this tool. Calling without loading first will fail.**

Query modes:
1. **Keyword search** -- e.g. "slack message", "notebook jupyter". Returns up to 5 tools, all immediately callable.
2. **Direct select** -- \`select:<tool_name>\` when you know the exact name.
3. **Required keyword** -- \`+linear create issue\` to require "linear", rank by rest.

Do NOT follow keyword search with \`select:\` for tools already returned -- they are already loaded.
