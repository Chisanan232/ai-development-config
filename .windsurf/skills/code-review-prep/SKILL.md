---
name: code-review-prep
description: Prepare high-quality pull requests ready for review
metadata:
  when_to_use: When preparing to submit a pull request
  tags: pull-request, code-review, collaboration
---

# Code Review Preparation Skill

## Purpose

This skill provides a systematic approach to preparing pull requests that are clear, complete, and ready for effective code review.

## When to Invoke This Skill

Use this skill when:
* Preparing to submit a pull request
* Finalizing work before requesting review
* Ensuring PR meets quality standards

## When NOT to Invoke This Skill

Do not use this skill for:
* Work in progress (use draft PRs instead)
* Incomplete features
* Code with failing tests or CI checks

## Prerequisites

Before preparing a PR:
1. **All work is complete** and tested
2. **All tests pass** locally
3. **Code quality checks pass** (linting, type checking, formatting)
4. **Commits follow conventions** (consult AGENTS.md)

## PR Preparation Process

### Phase 1: Self-Review

**Review your own code first, as if you were the reviewer.**

1. **Read through all changes**
   * Open each changed file
   * Read every line of code
   * Look for issues you would catch in review

2. **Check for common issues**
   * Debug code left in (console.log, print statements, debugger)
   * Commented-out code that should be removed
   * TODO comments without tracking issues
   * Hardcoded values that should be configurable
   * Overly complex logic that could be simplified
   * Missing error handling
   * Inconsistent naming or style

3. **Verify test coverage**
   * All new code is tested
   * Edge cases are covered
   * Error cases are tested
   * Run coverage report (consult AGENTS.md)

4. **Check documentation**
   * Public APIs are documented
   * Complex logic has explanatory comments
   * README updated if needed
   * Architecture docs updated if needed

### Phase 2: Verify Quality Checks

1. **Run all tests**
   * Consult AGENTS.md for test command
   * Ensure all tests pass
   * Check for flaky tests

2. **Run linter**
   * Consult AGENTS.md for lint command
   * Fix all linting errors
   * Address warnings if possible

3. **Run type checker**
   * Consult AGENTS.md for type check command
   * Fix all type errors
   * Avoid type suppressions unless necessary

4. **Run formatter**
   * Consult AGENTS.md for format command
   * Ensure code is properly formatted

5. **Run pre-commit hooks** (if applicable)
   * Consult AGENTS.md for pre-commit command
   * Fix any pre-commit failures

### Phase 3: Review Commits

1. **Check commit messages**
   * Follow project conventions (consult AGENTS.md)
   * Clear, descriptive messages
   * Reference issues where applicable

2. **Check commit structure**
   * Logical, atomic commits
   * Each commit represents one change
   * No "fix typo" or "oops" commits (squash them)

3. **Consider squashing** (if project uses squash-and-merge)
   * Clean up commit history
   * Combine related commits
   * Use interactive rebase if needed

### Phase 4: Write PR Description

1. **Read the PR template**
   * Consult AGENTS.md for PR template location
   * Follow the template structure
   * Fill in all required sections

2. **Write a clear title**
   * Follow project conventions (consult AGENTS.md)
   * Be specific: "Add user authentication endpoint" not "Update code"
   * Include issue reference if applicable

3. **Write the PR body**

Use this structure (or follow project template):

#### What changed
* Brief bullet list of changes made
* Focus on what, not how
* Be concise but complete

#### Why it changed
* Engineering purpose and context
* Link to requirements or issues
* Explain the problem being solved

#### How to verify
* Steps to test the changes
* Commands to run
* Expected outcomes

#### Related issues
* Link to related issues or tickets
* Use "Closes #123" or "Fixes #456" for automatic closing

#### Breaking changes
* Highlight any breaking changes
* Provide migration steps if needed
* Mark as breaking in title if applicable

**Example:**

```markdown
## What changed
- Added JWT authentication middleware
- Created login and logout endpoints
- Added user session management
- Updated API documentation

## Why
- Implement user authentication as required by #123
- Secure API endpoints from unauthorized access
- Enable user-specific features

## How to verify
1. Run tests: `npm test`
2. Start server: `npm start`
3. Test login: `POST /api/auth/login` with `{"email": "test@example.com", "password": "password"}`
4. Verify protected endpoints require authentication

## Related issues
Closes #123

## Breaking changes
None
```

### Phase 5: Final Checks

1. **Verify branch is up to date**
   * Merge or rebase from target branch (main, develop, etc.)
   * Resolve any conflicts
   * Re-run tests after merge/rebase

2. **Check PR size**
   * Prefer < 500 lines changed
   * If larger, ensure it's well-organized
   * Consider splitting if too large

3. **Verify CI will pass**
   * All local checks pass
   * No known CI-specific issues
   * Environment variables set correctly

4. **Add labels** (if project uses labels)
   * Type: bug, feature, refactor, docs, chore
   * Priority: p0-critical, p1-high, p2-medium, p3-low
   * Status: needs-review, work-in-progress, blocked

### Phase 6: Submit PR

1. **Create the pull request**
   * Push branch to remote
   * Open PR in GitHub/GitLab/etc.
   * Fill in title and description

2. **Assign reviewers**
   * Tag appropriate team members
   * Consider code owners
   * Request review from domain experts

3. **Add comments** (if needed)
   * Explain non-obvious decisions
   * Highlight areas needing special attention
   * Ask specific questions

4. **Link to related work**
   * Link to design docs
   * Link to related PRs
   * Link to deployment plans

## Do Not Assume

* **Do not assume** PR template location or format
* **Do not assume** commit message conventions
* **Do not assume** merge strategy (merge, squash, rebase)
* **Do not assume** required approvals
* **Do not assume** labeling conventions

**Always consult AGENTS.md first.**

## PR Quality Checklist

Use this checklist before submitting:

### Code Quality
- [ ] All tests pass locally
- [ ] No linting errors
- [ ] No type checking errors
- [ ] Code is properly formatted
- [ ] No debug code or console.log/print statements
- [ ] No commented-out code
- [ ] No hardcoded values that should be configurable

### Testing
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] Edge cases are tested
- [ ] Test coverage maintained or improved

### Documentation
- [ ] Public APIs are documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] Architecture docs updated if needed

### Commits
- [ ] Commit messages follow conventions
- [ ] Commits are logical and atomic
- [ ] No "fix typo" or "oops" commits

### PR Description
- [ ] Clear, descriptive title
- [ ] Complete PR body following template
- [ ] What changed section filled in
- [ ] Why it changed section filled in
- [ ] How to verify section filled in
- [ ] Related issues linked
- [ ] Breaking changes highlighted (if any)

### Branch
- [ ] Branch is up to date with target
- [ ] No merge conflicts
- [ ] CI will pass (all local checks pass)

### Review
- [ ] Reviewers assigned
- [ ] Labels added (if applicable)
- [ ] Self-review completed

## Common PR Issues to Avoid

* **Massive PRs**: Keep PRs focused and reviewable (< 500 lines)
* **Mixing concerns**: Do not mix refactoring, features, and bug fixes
* **Poor descriptions**: Vague or missing PR descriptions
* **Failing CI**: Submitting PR with known CI failures
* **Missing tests**: New code without tests
* **Ignoring template**: Not following PR template
* **No context**: Not explaining why changes were made

## Integration with Other Skills

* **Before PR prep**: Use `feature-implementation` to build the feature
* **After PR submission**: Monitor CI and address feedback
* **If CI fails**: Use `ci-failure-triage` to diagnose and fix

## Example Workflow

```
1. Feature implementation complete

2. Self-review:
   - Read through all changes
   - Remove debug code
   - Check for TODOs
   - Verify test coverage

3. Quality checks:
   - Run tests: ✓ All pass
   - Run linter: ✓ No errors
   - Run type checker: ✓ No errors
   - Run formatter: ✓ Code formatted

4. Review commits:
   - Check commit messages: ✓ Follow conventions
   - Squash "fix typo" commits

5. Write PR description:
   - Read template at .github/pull_request_template.md
   - Write clear title: "feat: add user authentication endpoint"
   - Fill in What/Why/How sections
   - Link to issue: "Closes #123"

6. Final checks:
   - Merge from main: ✓ Up to date
   - Re-run tests: ✓ All pass
   - Check PR size: ✓ 347 lines (good)

7. Submit:
   - Create PR
   - Assign reviewers
   - Add labels: feature, needs-review
   - Post in Slack: "PR ready for review"
```

## [PROJECT-SPECIFIC MCP MAPPING]

For projects with MCP configured, capabilities map to:

* **code_repository**: Use to verify GitHub/GitLab PR status and CI checks
* **static_analysis**: Use to check SonarQube/CodeClimate quality gate
* **coverage_reporting**: Use to verify Codecov/Coveralls coverage
* **communication**: Use to notify team when PR is ready (optional)

Consult AGENTS.md for your project's specific MCP configuration and source-of-truth mappings.

## Notes

* This is a generic skill. Always adapt to project-specific requirements.
* Consult AGENTS.md before making assumptions.
* A well-prepared PR gets reviewed faster and merged sooner.
* When in doubt, ask the user for clarification.
