---
description: Commit message conventions and commit hygiene
tags: [git, commits, version-control]
---

# Commit Policy

## Commit Message Format

Consult AGENTS.md for project-specific commit message style (e.g., Conventional Commits, git emoji, Angular style).

### General Guidelines

* **Subject line**: Clear, concise summary (< 72 characters)
* **Body**: Optional detailed explanation of what and why (not how)
* **Footer**: Optional references to issues, breaking changes, etc.

### Subject Line Best Practices

* **Use imperative mood**: "Add feature" not "Added feature" or "Adds feature"
* **Be specific**: "Fix null pointer in user service" not "Fix bug"
* **No period at the end**: Subject lines are titles, not sentences
* **Reference issues when relevant**: Include issue numbers if applicable

## Commit Hygiene

### Commit Frequency

* **Commit in logical increments**: Each commit should represent a single logical change
* **Event-based commits**: Commit after implementing a feature, fixing a bug, adding tests, etc.
* **Do not commit broken code**: Each commit should leave the codebase in a working state
* **Commit before switching contexts**: Save your work before moving to a different task

### Commit Atomicity

* **One concern per commit**: Do not mix refactoring, bug fixes, and new features in one commit
* **Self-contained changes**: Each commit should be understandable on its own
* **Bisectable history**: Each commit should pass tests so git bisect works

### What to Commit

**Include:**
* Source code changes
* Test changes
* Configuration updates
* Documentation updates
* Dependency updates (in separate commits)

**Exclude:**
* Build artifacts (dist/, build/, target/)
* IDE-specific files (.idea/, .vscode/ unless shared)
* Temporary files (.DS_Store, *.swp, *.tmp)
* Sensitive data (API keys, passwords, tokens)
* Large binary files (unless necessary and tracked with LFS)

### Commit Workflow

1. **Review your changes**: Use `git diff` to see what you're committing
2. **Stage selectively**: Use `git add -p` to stage specific changes
3. **Write a clear message**: Follow project conventions
4. **Verify before pushing**: Ensure tests pass and code is clean

## Amending and Rewriting History

### When to Amend

* **Fix typos in the last commit**: `git commit --amend`
* **Add forgotten files to the last commit**: Stage files, then `git commit --amend --no-edit`
* **Improve the last commit message**: `git commit --amend`

### When NOT to Amend

* **After pushing to shared branches**: Do not rewrite public history
* **When others have based work on your commits**: Coordinate with the team first

### Interactive Rebase

* **Clean up local history**: Use `git rebase -i` to squash, reorder, or edit commits before pushing
* **Only for unpushed commits**: Do not rebase commits that have been pushed to shared branches
* **Squash fixup commits**: Combine "fix typo" or "oops" commits into meaningful commits

## Branch Hygiene

* **Keep branches focused**: One branch per feature or bug fix
* **Use descriptive branch names**: `feature/user-authentication`, `fix/null-pointer-bug`
* **Delete merged branches**: Clean up branches after they are merged
* **Sync with main regularly**: Rebase or merge from main to avoid conflicts

## Merge vs Rebase

Consult AGENTS.md or team conventions for project-specific merge strategy:

* **Merge commits**: Preserve complete history, create merge commits
* **Rebase and merge**: Linear history, cleaner log
* **Squash and merge**: Condense PR into single commit

## Commit Signing

If required by the project:

* **Sign commits**: Use GPG or SSH signing
* **Configure signing**: Set up signing key in git config
* **Verify signatures**: Ensure commits are signed before merging
