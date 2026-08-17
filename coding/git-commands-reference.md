---
created: 2026-08-15T12:00:00+08:00
tags: [git, testing]
---

# Git Commands Reference

## Basic Workflow
1. Initialize repo: `git init`
2. Check status: `git status`
3. Add files: `git add <file>`
4. Commit: `git commit -m "message"`
5. Push to remote: `git push origin main`

## Advanced Commands
- `git rebase --interactive` — rewrite commit history
- `git cherry-pick` — apply commits from another branch
- `git stash` — temporarily save work
- `git diff <commit>...HEAD` — view changes

## Troubleshooting
- Fix conflicts before merge/rebase
- Use `git reflog` to recover lost commits
- Clear staged files: `git reset HEAD <file>`

See also: [[deep-learning-fundamentals]] for research context, [[unknown-user-input]] for user-provided examples.
