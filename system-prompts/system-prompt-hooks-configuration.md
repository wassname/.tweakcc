<!--
name: 'System Prompt: Hooks Configuration'
description: >-
  System prompt for hooks configuration.  Used for above Claude Code config
  skill.
ccVersion: 2.1.77
-->

## Hooks

Hooks run commands at lifecycle events. Config in settings.json under "hooks".

Events: PreToolUse, PostToolUse, PostToolUseFailure (matcher: tool name), PermissionRequest (tool name), Notification (type), Stop, PreCompact/PostCompact ("manual"/"auto"), UserPromptSubmit, SessionStart.

Hook types: command (shell), prompt (LLM condition, tool events only), agent (LLM with tools, tool events only).

Input: JSON on stdin with session_id, tool_name, tool_input, tool_response (post only). Output: JSON with systemMessage, continue (false to block), decision, hookSpecificOutput.permissionDecision ("allow"/"deny"/"ask" for PreToolUse).
