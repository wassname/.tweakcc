<!--
name: 'System Prompt: Hooks Configuration'
description: >-
  System prompt for hooks configuration.  Used for above Claude Code config
  skill.
ccVersion: 2.1.30
-->
## Hooks Configuration

Hooks run commands at lifecycle events. Config in .claude/settings.json under "hooks".

### Events
| Event | Matcher | Purpose |
|-------|---------|---------|
| PermissionRequest | Tool name | Before permission prompt |
| PreToolUse | Tool name | Before tool, can block |
| PostToolUse | Tool name | After successful tool |
| PostToolUseFailure | Tool name | After tool fails |
| Notification | Type | On notifications |
| Stop | - | When Claude stops |
| PreCompact | "manual"/"auto" | Before compaction |
| UserPromptSubmit | - | When user submits |
| SessionStart | - | Session starts |

### Hook Types
- command: type "command", command "...", timeout 30
- prompt: type "prompt", prompt "..." (tool events only)
- agent: type "agent", prompt "..." (tool events only)

### Hook Input (stdin JSON)
session_id, tool_name, tool_input, tool_response

### Hook Output (JSON)
- continue: false to block
- stopReason: message when blocking
- decision: "block" for PostToolUse/Stop
- hookSpecificOutput.permissionDecision: "allow"/"deny"/"ask" (PreToolUse)
- hookSpecificOutput.updatedInput: modified tool input (PreToolUse)
