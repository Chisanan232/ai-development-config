---
description: Core coding standards and quality expectations
tags: [code-quality, standards, best-practices]
---

# Coding Standards

## Core Principles

1. **Write clear, readable code**: Code is read far more often than it is written. Prioritize clarity over cleverness.

2. **Follow language idioms**: Use idiomatic patterns for the language you're working in. Consult AGENTS.md for language-specific conventions.

3. **Keep functions small and focused**: Each function should do one thing well. If a function is doing multiple things, split it.

4. **Use meaningful names**: Variable, function, and class names should clearly communicate their purpose.

5. **Avoid premature optimization**: Write correct, clear code first. Optimize only when profiling shows a real performance issue.

## Code Organization

* **Imports**: Keep imports organized and minimal. Remove unused imports.
* **File length**: Keep files focused. If a file exceeds 500 lines, consider splitting it.
* **Function length**: Keep functions under 50 lines when possible. Long functions are hard to understand and test.
* **Nesting depth**: Avoid deep nesting (> 3 levels). Use early returns or extract helper functions.

## Error Handling

* **Handle errors explicitly**: Do not silently ignore errors or use bare except/catch blocks.
* **Fail fast**: Validate inputs early and fail with clear error messages.
* **Provide context**: Error messages should help diagnose the problem.

## Comments and Documentation

* **Write self-documenting code**: Good names reduce the need for comments.
* **Comment the "why", not the "what"**: Explain non-obvious decisions, not obvious code.
* **Keep comments up to date**: Outdated comments are worse than no comments.
* **Document public APIs**: All public functions, classes, and modules should have clear documentation.

## Testing

* **Write tests for new code**: All new features and bug fixes should include tests.
* **Test behavior, not implementation**: Tests should verify what the code does, not how it does it.
* **Keep tests simple**: Tests should be easy to understand and maintain.

## Dependencies

* **Minimize dependencies**: Only add dependencies when they provide clear value.
* **Pin versions**: Use lock files to ensure reproducible builds.
* **Review security**: Check dependencies for known vulnerabilities.

## Code Review

* **Review your own code first**: Before requesting review, read through your changes as if you were the reviewer.
* **Keep changes focused**: Each PR should address one concern. Do not mix refactoring with feature work.
* **Respond to feedback**: Address review comments promptly and thoughtfully.
