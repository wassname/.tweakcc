# Git Commit and PR Creation (cc-commit)

## Committing

Only commit when explicitly asked. Stage by name (not `git add -A`); never commit .env/credentials.

1. Run git status (no -uall), git diff, git log in parallel
2. Draft concise commit message (1-2 sentences, focus on "why")
3. Stage files, commit with HEREDOC, verify with git status:

```sh
git commit -m "$(cat <<'EOF'
Commit message here.
EOF
)"
```

4. If hook fails: fix root cause, create a NEW commit (not --amend). Do NOT push unless explicitly asked.

## Creating pull requests

Use `gh` CLI. Check status, diff, log, and `git diff [base-branch]...HEAD` in parallel first.
Create branch if needed, push with `-u`. PR title under 70 chars.
View PR comments: `gh api repos/{owner}/{repo}/pulls/{number}/comments`

```sh
gh pr create --title "the pr title" --body "$(cat <<'EOF'
## Summary
- bullet points

## Test plan
- [ ] ...
EOF
)"
```

Return the PR URL when done.
