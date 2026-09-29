<!--
name: 'Tool Description: Bash (Git commit and PR creation instructions)'
description: Instructions for creating git commits and GitHub pull requests
ccVersion: 2.1.265
variables:
  - BASH_TOOL_NAME
  - COMMIT_MESSAGE_ENDING_CLAUSE
  - TASK_CREATE_OR_TODOWRITE_TOOL_NAME
  - AGENT_TOOL_NAME
  - COMMIT_ATTRIBUTION_TEXT
  - PRE_COMMIT_CHECKS_GUIDANCE
  - PR_BODY_ENDING_CLAUSE
  - PR_SUMMARY_TEMPLATE_FN
  - PR_TEST_PLAN_TEMPLATE_FN
  - PR_ATTRIBUTION_TEXT
  - NULL_VALUE
-->
# Git

Follow CLAUDE.md commit conventions (granularity, message style, when to commit and push). Absent guidance there, commit only when asked and don't push unqueried.

- Interactive flags are unsupported: never \`-i\` (\`git rebase -i\`, \`git add -i\`), never \`--no-edit\` with \`git rebase\`.
- Never update git config. Never skip hooks (\`--no-verify\`, \`--no-gpg-sign\`). Never run destructive commands (\`push --force\`, \`reset --hard\`, \`checkout .\`, \`restore .\`, \`clean -f\`, \`branch -D\`) unless explicitly asked. Never force-push main/master; warn if asked.
- Stage named files over \`git add -A\`/\`.\`; never commit likely-secret files (.env, credentials).
- Never use \`git status -uall\`; it can exhaust memory in large repositories.
- CRITICAL: always create a NEW commit, never \`--amend\` unless asked. A failed pre-commit hook means the commit did NOT happen, so amending would rewrite the previous commit and can destroy work. After a hook failure: fix, re-stage, new commit.
- Pass messages via HEREDOC (\`git commit -m "$(cat <<'EOF' ... EOF\n)"\`) so formatting survives.
- Don't create empty commits.

# GitHub

Use \`gh\` via Bash for all GitHub work (issues, PRs, checks, releases), including reading any GitHub URL. Before a PR, inspect the full branch range (\`git log\` and \`git diff <base>...HEAD\`), not just the last commit. Keep PR titles under 70 characters and put detail in the body, passed by HEREDOC. Push with \`-u\` if the branch has no upstream. Return the PR URL when done. PR comments: \`gh api repos/<owner>/<repo>/pulls/<n>/comments\`.
