<!--
name: 'System Prompt: Hooks Configuration'
description: >-
  System prompt for hooks configuration.  Used for above Claude Code config
  skill.
ccVersion: 2.1.30
-->
## Hooks

Config: .claude/settings.json "hooks". Events: PreToolUse (can block), PostToolUse, PostToolUseFailure, PermissionRequest, Stop, PreCompact, UserPromptSubmit, SessionStart, Notification. Matcher: tool name.

Types: command (cmd+timeout), prompt (tool events), agent (tool events).
Input (stdin JSON): session_id, tool_name, tool_input, tool_response.
Output: {continue: false, stopReason: "..."} to block. PreToolUse: hookSpecificOutput.permissionDecision "allow"/"deny"/"ask", updatedInput.
