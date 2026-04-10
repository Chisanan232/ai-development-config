# SKILL.md — code-review-prep

## Purpose
Verify that the current branch is ready for code review. Produce a PR description
that meets the project's PR policy.

## Type
Auto-used. Claude Code invokes this skill before any PR is opened.

## Do Not Assume
- Do not assume CI is passing — check the current branch status.
- Do not assume the diff is small — review it explicitly.
- Do not assume all tests are covered — run the full suite.

## Steps

### Phase 1 — Self-review
1. Run `git diff main...HEAD` (or equivalent base branch) and review every changed line.
2. Ask: does any change exceed the scope of the stated goal?
3. Ask: is there any debug code, temporary scaffolding, or TODO without an issue reference?
4. Ask: are all changed public APIs annotated?
5. Ask: is there a test for every changed behavior?

### Phase 2 — Validation gate
6. Run the full test suite.
7. Run the linter.
8. Run the type checker.
9. Run pre-commit hooks.
10. All must pass. If any fail, stop and fix before proceeding.

### Phase 3 — PR description
11. Write the PR title: `<emoji> <scope>: <imperative summary under 70 chars>`
12. Write the PR body with these sections:
    - **Summary**: what changed (one paragraph)
    - **Motivation**: why it changed, issue reference
    - **Changes**: bullet list of key changes
    - **How to Verify**: test commands or manual steps
    - **Checklist**: tests pass, lint pass, type check pass, docs updated, no secrets
13. Link related issues: `Closes #<issue>` or `Refs #<issue>`.

### Phase 4 — Final check
14. Confirm the branch name follows the project convention.
15. Confirm no merge conflicts with the base branch.
16. Confirm the commit history is clean and atomic.
    If commits need squashing or reordering, do it now (before the PR is open).

## Safe-Fix Guidance
- If a pre-commit hook fails: run the language-appropriate pre-commit repair skill
  (see CLAUDE.md Skill Invocation Guide — e.g., `python-precommit-repair`,
  `node-precommit-repair`).
- If a type checker fails: run the language-appropriate type-checking repair skill
  (e.g., `python-mypy-debugging`, `typescript-tsc-debugging`, `go-vet-debugging`).
- If a linter fails: run the language-appropriate linter-fixing skill
  (e.g., `python-ruff-fixing`, `typescript-eslint-fixing`, `go-golangci-fixing`).
- If tests fail: run the language-appropriate test failure debugging skill
  (e.g., `python-pytest-failure-debugging`).
- Never open a PR while any check is red.

## Validation Guidance
- Full validation is required. No impacted-only shortcut here.
