<!--
name: 'Tool Description: Bash (Git commit and PR creation instructions)'
description: Instructions for creating git commits and GitHub pull requests
ccVersion: 2.1.205
variables:
  - BASH_TOOL_NAME
  - COMMIT_CO_AUTHORED_BY_CLAUDE_CODE
  - GET_TODO_TOOL_FN
  - TASK_TOOL_NAME
  - PR_INSTRUCTIONS_PREFIX
  - PR_WRITING_GUIDANCE_BLOCK
  - PR_GENERATED_WITH_CLAUDE_CODE
  - PR_SUMMARY_TEMPLATE_FN
  - PR_TEST_PLAN_TEMPLATE_FN
  - PR_COMMON_OPERATIONS_NOTE
-->
# Git

Follow CLAUDE.md commit conventions (granularity, message style, when to commit and push). Absent guidance there, commit only when asked and don't push unqueried.

- Interactive flags are unsupported: never \`-i\` (\`git rebase -i\`, \`git add -i\`), never \`--no-edit\` with \`git rebase\`.
- Never update git config. Never skip hooks (\`--no-verify\`, \`--no-gpg-sign\`). Never run destructive commands (\`push --force\`, \`reset --hard\`, \`checkout .\`, \`restore .\`, \`clean -f\`, \`branch -D\`) unless explicitly asked; warn on force-push to main/master.
- Stage named files over \`git add -A\`/\`.\`; never commit likely-secret files (.env, credentials).
- CRITICAL: always create a NEW commit, never \`--amend\` unless asked. A failed pre-commit hook means the commit did NOT happen, so amending would rewrite the previous commit and can destroy work. After a hook failure: fix, re-stage, new commit.
- Pass messages via HEREDOC (\`git commit -m "$(cat <<'EOF' ... EOF\n)"\`) so formatting survives.
- Don't create empty commits.

# GitHub

Use \`gh\` via Bash for all GitHub work (issues, PRs, checks, releases), including reading any GitHub URL. Before a PR, inspect the full branch range (\`git log\` and \`git diff <base>...HEAD\`), not just the last commit. Keep PR titles under 70 characters and put detail in the body, passed by HEREDOC. Push with \`-u\` if the branch has no upstream. Return the PR URL when done. PR comments: \`gh api repos/<owner>/<repo>/pulls/<n>/comments\`.
