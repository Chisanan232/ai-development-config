---
description: Pull request requirements and best practices
tags: [pull-requests, code-review, collaboration]
---

# Pull Request Policy

## PR Requirements

Before submitting a PR:

* [ ] All tests pass locally
* [ ] Code follows project style guidelines (linting, formatting, type checking)
* [ ] New tests added for new functionality
* [ ] Documentation updated if needed
* [ ] No linting or type checking errors
* [ ] Commit messages follow project conventions
* [ ] PR description is complete and clear

## PR Preparation

### Read the PR Template

Consult AGENTS.md for the PR template location (e.g., `.github/pull_request_template.md`).

Follow the template structure when writing your PR description.

### PR Title

* **Be specific**: "Add user authentication endpoint" not "Update code"
* **Follow project conventions**: Consult AGENTS.md for title format
* **Include issue reference**: Link to related issues when applicable

### PR Description

Write a concise, bullet-based description that includes:

1. **What changed**: Brief list of changes made
2. **Why it changed**: Engineering purpose and context
3. **How to verify**: Steps to test or verify the changes
4. **Related issues**: Links to related issues or tickets
5. **Breaking changes**: Highlight any breaking changes or migration steps

**Example:**

```markdown
## What changed
- Added JWT authentication middleware
- Created login and logout endpoints
- Added user session management

## Why
- Implement user authentication as required by #123
- Secure API endpoints from unauthorized access

## How to verify
1. Run `npm test` to verify all tests pass
2. Start the server with `npm start`
3. Test login at POST /api/auth/login
4. Verify protected endpoints require authentication

## Related issues
Closes #123

## Breaking changes
None
```

## PR Size

* **Keep PRs small**: Aim for < 500 lines changed when possible
* **One concern per PR**: Do not mix refactoring, bug fixes, and new features
* **Split large changes**: Break large features into multiple PRs with clear dependencies

If a PR must be large:
* Break it into logical commits
* Provide detailed description
* Consider splitting into multiple PRs

## PR Review Process

### Requesting Review

* **Review your own code first**: Read through your changes as if you were the reviewer
* **Assign reviewers**: Tag appropriate team members
* **Provide context**: Add comments to explain non-obvious decisions

### Responding to Feedback

* **Respond promptly**: Address review comments in a timely manner
* **Be open to feedback**: Code review is collaborative, not adversarial
* **Ask for clarification**: If feedback is unclear, ask questions
* **Mark conversations resolved**: After addressing feedback, mark the conversation as resolved

### Making Changes

* **Push new commits**: Add new commits to address feedback (do not force-push during review)
* **Reference feedback**: Mention which review comment you're addressing
* **Re-request review**: After making changes, re-request review from reviewers

## PR Approval

* **Required approvals**: Consult AGENTS.md or team policy for approval requirements
* **Address all feedback**: Resolve or discuss all review comments before merging
* **CI must pass**: All CI checks must be green before merging

## Merging

### Before Merging

* [ ] All required approvals obtained
* [ ] All CI checks passing
* [ ] All review comments addressed
* [ ] Branch is up to date with target branch
* [ ] No merge conflicts

### Merge Strategy

Consult AGENTS.md for project-specific merge strategy:

* **Merge commit**: Preserves all commits and creates a merge commit
* **Squash and merge**: Combines all commits into a single commit
* **Rebase and merge**: Replays commits on top of the target branch

### After Merging

* **Delete the branch**: Clean up merged branches
* **Close related issues**: Ensure linked issues are closed
* **Monitor CI/CD**: Watch deployment and verify changes in production

## PR Anti-Patterns to Avoid

* **"Work in progress" PRs without draft status**: Use draft PRs for work in progress
* **Massive PRs**: Break large changes into smaller, reviewable PRs
* **Mixing concerns**: Keep refactoring, features, and bug fixes separate
* **Ignoring CI failures**: Fix CI before requesting review
* **Force-pushing during review**: Breaks review context and comments
* **Merging your own PRs without review**: Always get review unless explicitly allowed

## Draft PRs

Use draft PRs for:
* Early feedback on approach
* Work in progress that's not ready for review
* Demonstrating a concept

Mark as "Ready for review" when:
* All tests pass
* Code is complete
* Ready for thorough review

## PR Labels and Tags

Use labels to categorize PRs (if project uses labels):
* `bug`, `feature`, `refactor`, `docs`, `chore`
* `breaking-change`, `needs-review`, `work-in-progress`
* Priority labels: `p0-critical`, `p1-high`, `p2-medium`, `p3-low`

Consult project conventions for label usage.
