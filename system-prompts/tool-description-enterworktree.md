<!--
name: 'Tool Description: EnterWorktree'
description: Tool description for the EnterWorktree tool.
ccVersion: 2.1.51
-->
ONLY when user explicitly says "worktree". Creates isolated git worktree in \`.claude/worktrees/\` with new branch from HEAD. NOT for branch switching or normal feature work.

Requires: git repo (or WorktreeCreate/WorktreeRemove hooks). Must not already be in a worktree.
On exit: user prompted to keep/remove. Optional \`name\` parameter.
