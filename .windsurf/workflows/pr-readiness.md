---
description: Pull request readiness checklist
---

# PR Readiness Workflow

This workflow ensures your pull request is complete and ready for review.

## When to Use

Run this workflow before submitting a pull request.

## Prerequisites

* All development work is complete
* You are ready to request code review

## Workflow Steps

### 1. Self-Review

Review your own code first:

```bash
# View all changes
git diff main...HEAD

# Or use a visual diff tool
git difftool main...HEAD
```

**Check for:**
- [ ] Debug code removed (console.log, print, debugger)
- [ ] Commented-out code removed
- [ ] TODO comments have tracking issues
- [ ] No hardcoded values that should be configurable
- [ ] No sensitive data (API keys, passwords)
- [ ] Code is clear and readable
- [ ] Complex logic has explanatory comments

### 2. Run All Tests

Consult AGENTS.md for test commands.

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run pytest
# JavaScript: npm test
# Rust: cargo test
```

**Verify:**
- [ ] All tests pass
- [ ] No flaky tests
- [ ] New features have tests
- [ ] Bug fixes have regression tests

### 3. Run Code Quality Checks

Consult AGENTS.md for quality check commands.

#### Linting

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run ruff check .
# JavaScript: npm run lint
# Rust: cargo clippy
```

- [ ] No linting errors
- [ ] Warnings addressed or documented

#### Type Checking

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run mypy .
# TypeScript: npm run typecheck
```

- [ ] No type errors
- [ ] Type suppressions minimized and documented

#### Formatting

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run ruff format .
# JavaScript: npm run format
# Rust: cargo fmt
```

- [ ] Code is properly formatted

### 4. Check Test Coverage

Consult AGENTS.md for coverage commands.

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run pytest --cov
# JavaScript: npm run test:coverage
```

**Verify:**
- [ ] Coverage meets project threshold
- [ ] New code is adequately covered
- [ ] Critical paths are tested

### 5. Run Pre-commit Hooks

If the project uses pre-commit:

```bash
# Consult AGENTS.md for pre-commit command
pre-commit run --all-files
```

- [ ] All pre-commit hooks pass

### 6. Review Commits

**Check commit messages:**
- [ ] Follow project conventions (consult AGENTS.md)
- [ ] Clear and descriptive
- [ ] Reference issues where applicable

**Check commit structure:**
- [ ] Logical, atomic commits
- [ ] Each commit represents one change
- [ ] No "fix typo" or "oops" commits (squash them if needed)

**Clean up if needed:**

```bash
# Interactive rebase to clean up commits
git rebase -i main

# Squash fixup commits
git commit --fixup <commit-hash>
git rebase -i --autosquash main
```

### 7. Update Branch

Ensure your branch is up to date:

```bash
# Fetch latest changes
git fetch origin

# Option 1: Merge (creates merge commit)
git merge origin/main

# Option 2: Rebase (linear history)
git rebase origin/main

# Consult AGENTS.md for project merge strategy
```

**After merge/rebase:**
- [ ] No merge conflicts
- [ ] All tests still pass
- [ ] No new linting/type errors

### 8. Write PR Description

Consult AGENTS.md for PR template location.

**PR Title:**
- [ ] Clear and specific
- [ ] Follows project conventions
- [ ] Includes issue reference if applicable

**PR Body:**

Include these sections:

#### What changed
- Brief bullet list of changes made
- Focus on what, not how

#### Why it changed
- Engineering purpose and context
- Link to requirements or issues

#### How to verify
- Steps to test the changes
- Commands to run
- Expected outcomes

#### Related issues
- Link to related issues or tickets
- Use "Closes #123" or "Fixes #456"

#### Breaking changes
- Highlight any breaking changes
- Provide migration steps if needed

### 9. Final Verification

**Before submitting:**
- [ ] All tests pass
- [ ] All quality checks pass
- [ ] Branch is up to date
- [ ] PR description is complete
- [ ] Self-review completed
- [ ] No unintended changes

### 10. Submit PR

```bash
# Push your branch
git push origin your-branch-name

# Or force push if you rebased (be careful!)
git push --force-with-lease origin your-branch-name
```

**After creating PR:**
- [ ] Assign reviewers
- [ ] Add labels (if applicable)
- [ ] Link to related issues
- [ ] Post in team chat (if required)

### 11. Monitor CI

Watch the CI pipeline:

- [ ] All CI checks pass
- [ ] No unexpected failures
- [ ] Build succeeds
- [ ] Tests pass in CI

**If CI fails:**
* Use the `ci-failure-triage` skill to diagnose and fix

### 12. Respond to Review Feedback

When reviewers provide feedback:

- [ ] Respond promptly
- [ ] Address all comments
- [ ] Ask for clarification if needed
- [ ] Push new commits to address feedback
- [ ] Re-request review after changes
- [ ] Mark conversations as resolved

## Quick Checklist

Use this quick checklist for a final verification:

### Code Quality
- [ ] All tests pass
- [ ] No linting errors
- [ ] No type errors
- [ ] Code formatted
- [ ] No debug code
- [ ] No commented-out code

### Testing
- [ ] New features tested
- [ ] Bug fixes have regression tests
- [ ] Coverage meets threshold
- [ ] Edge cases covered

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated (if needed)
- [ ] Architecture docs updated (if needed)

### Commits
- [ ] Messages follow conventions
- [ ] Logical, atomic commits
- [ ] No fixup commits

### PR
- [ ] Clear title
- [ ] Complete description
- [ ] What/Why/How sections filled
- [ ] Related issues linked
- [ ] Breaking changes noted

### Branch
- [ ] Up to date with main
- [ ] No merge conflicts
- [ ] Tests pass after merge/rebase

## Notes

* This is a generic workflow. Adapt to your project's specific requirements.
* Always consult AGENTS.md for project-specific commands and conventions.
* A well-prepared PR gets reviewed faster and merged sooner.
