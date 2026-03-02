<!--
name: 'Tool Description: Bash (Git commit and PR creation instructions)'
description: Instructions for creating git commits and GitHub pull requests
ccVersion: 2.1.38
variables:
  - GIT_COMMAND_PARALLEL_NOTE
  - BASH_TOOL_NAME
  - COMMIT_CO_AUTHORED_BY_CLAUDE_CODE
  - TODO_TOOL_OBJECT
  - TASK_TOOL_NAME
  - PR_GENERATED_WITH_CLAUDE_CODE
-->
# Committing changes with git

Only commit when the user explicitly asks. Stage specific files by name (not \`git add -A\`); never commit .env/credentials.

Workflow:
1. ${GIT_COMMAND_PARALLEL_NOTE} run git status (never -uall flag), git diff, git log in parallel
2. Draft concise commit message (1-2 sentences, focus on "why")
3. Stage files, commit with HEREDOC format, then git status to verify:
<example>
git commit -m "$(cat <<'EOF'
   Commit message here.${COMMIT_CO_AUTHORED_BY_CLAUDE_CODE?`

   ${COMMIT_CO_AUTHORED_BY_CLAUDE_CODE}`:""}
   EOF
   )"
</example>
4. If hook fails: fix the issue and create a NEW commit (not --amend)

Notes:
- Never use -i flag (interactive) or --no-edit with rebase
- Do NOT use ${TODO_TOOL_OBJECT.name} or ${TASK_TOOL_NAME} tools during commits
- Do NOT push unless explicitly asked

# Creating pull requests

Use \`gh\` CLI. ${GIT_COMMAND_PARALLEL_NOTE} check status, diff, log, \`git diff [base-branch]...HEAD\` to understand ALL commits (not just latest).
Create branch if needed, push with \`-u\` flag. Keep PR title under 70 chars. Use body for details.
View PR comments: \`gh api repos/{owner}/{repo}/pulls/{number}/comments\`
<example>
gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
<1-3 bullet points>

## Test plan
[Checklist...]${PR_GENERATED_WITH_CLAUDE_CODE?`

${PR_GENERATED_WITH_CLAUDE_CODE}`:""}
EOF
)"
</example>

Return the PR URL when done.
