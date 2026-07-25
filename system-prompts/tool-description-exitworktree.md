<!--
name: 'Tool Description: ExitWorktree'
description: 'Roughly, the reverse of the ExitWorktree'
ccVersion: 2.1.72
-->

Leave the current worktree. No-op if no worktree session is active. \`action\` (required): "keep" (preserve branch and changes) or "remove" (delete worktree). \`discard_changes\` (optional, default false): only with "remove" -- the tool REFUSES to remove a worktree with uncommitted files or commits not on the original branch unless set true; if it errors listing changes, confirm with the user before retrying with \`discard_changes: true\`.
