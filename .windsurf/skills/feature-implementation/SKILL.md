---
name: Feature Implementation
description: Safe, structured approach to implementing new features
when_to_use: When implementing new functionality or significant enhancements
tags: [implementation, features, development]
---

# Feature Implementation Skill

## Purpose

This skill provides a structured approach to implementing new features safely and effectively while maintaining code quality and test coverage.

## When to Invoke This Skill

Use this skill when:
* Implementing a new feature or capability
* Adding significant new functionality
* Building a new component, service, or module
* Extending existing functionality in non-trivial ways

## When NOT to Invoke This Skill

Do not use this skill for:
* Simple bug fixes (those are straightforward corrections)
* Minor refactoring without behavior changes
* Documentation-only changes
* Configuration updates

## Prerequisites

Before starting implementation:
1. **Consult AGENTS.md** for project-specific conventions
2. **Understand the requirement** clearly
3. **Identify the scope** of changes needed
4. **Check existing patterns** in the codebase

## Implementation Process

### Phase 1: Clarification and Planning

1. **Clarify the requirement**
   * What is the expected behavior?
   * What are the acceptance criteria?
   * Are there edge cases to consider?
   * What are the performance requirements?

2. **Identify affected areas**
   * Which files/modules need changes?
   * What dependencies exist?
   * What tests need to be added or updated?

3. **Check existing patterns**
   * How is similar functionality implemented?
   * What conventions should be followed?
   * Are there reusable components or utilities?

4. **Plan the implementation approach**
   * What is the high-level design?
   * What are the implementation steps?
   * What is the testing strategy?

### Phase 2: Test Design

**Design tests BEFORE implementing the feature.**

1. **Identify test scenarios**
   * Happy path: normal, expected usage
   * Edge cases: boundary conditions, empty inputs, null values
   * Error cases: invalid inputs, failure conditions
   * Integration points: interactions with other components

2. **Determine test types**
   * Unit tests: for individual functions/methods
   * Integration tests: for component interactions
   * E2E tests: for critical user flows (if applicable)

3. **Write test stubs or full tests**
   * Option A: Write full tests first (TDD approach)
   * Option B: Write test stubs outlining what will be tested
   * Consult AGENTS.md for project testing conventions

### Phase 3: Implementation

1. **Start with the smallest working increment**
   * Implement the simplest version first
   * Make it work, then make it better
   * Avoid premature optimization

2. **Follow project conventions**
   * Consult AGENTS.md for:
     * Code style and formatting
     * Naming conventions
     * File organization
     * Language-specific patterns

3. **Preserve existing behavior**
   * Do not change unrelated functionality
   * Minimize scope of changes
   * Keep refactoring separate from feature work

4. **Add necessary error handling**
   * Validate inputs
   * Handle edge cases
   * Provide clear error messages

5. **Document non-obvious decisions**
   * Add comments for complex logic
   * Explain "why" not "what"
   * Update relevant documentation

### Phase 4: Testing and Validation

1. **Run impacted tests first**
   * Run tests directly affected by your changes
   * Verify they pass before running full suite
   * Consult AGENTS.md for test commands

2. **Run full test suite**
   * Ensure no regressions
   * Verify all tests pass
   * Check test coverage

3. **Manual testing**
   * Test the feature manually
   * Verify edge cases
   * Check error handling

4. **Code quality checks**
   * Run linter (consult AGENTS.md for command)
   * Run type checker (consult AGENTS.md for command)
   * Run formatter (consult AGENTS.md for command)

### Phase 5: Commit and Documentation

1. **Review your changes**
   * Read through all changes
   * Remove debug code, console.log, print statements
   * Ensure no unintended changes

2. **Commit in logical increments**
   * Commit feature implementation
   * Commit tests separately (or together, per project convention)
   * Follow commit message conventions (consult AGENTS.md)

3. **Update documentation**
   * Update README if needed
   * Update API documentation
   * Update architecture docs if applicable

## Do Not Assume

* **Do not assume** project structure without checking
* **Do not assume** testing framework or conventions
* **Do not assume** commit message format
* **Do not assume** code style preferences
* **Do not assume** build or test commands

**Always consult AGENTS.md first.**

## Fallback Logic

If you encounter issues:

1. **Cannot find similar patterns**
   * Ask the user for guidance
   * Propose an approach based on language best practices
   * Document the decision

2. **Tests are unclear**
   * Clarify requirements with the user
   * Start with obvious test cases
   * Iterate based on feedback

3. **Implementation is complex**
   * Break it into smaller steps
   * Implement incrementally
   * Validate each step

4. **Existing code is unclear**
   * Ask the user for context
   * Add comments to document understanding
   * Refactor carefully if needed (in separate commit)

## Validation Checklist

Before considering the feature complete:

- [ ] Feature works as expected
- [ ] All tests pass (unit, integration, E2E)
- [ ] Code follows project style guidelines
- [ ] No linting or type checking errors
- [ ] Test coverage maintained or improved
- [ ] Edge cases handled
- [ ] Error handling implemented
- [ ] Documentation updated
- [ ] Commits follow project conventions
- [ ] No unintended changes or debug code

## Integration with Other Skills

* **After implementation**: Use `code-review-prep` skill to prepare PR
* **If tests fail**: Use `ci-failure-triage` skill to diagnose
* **If coverage drops**: Use `coverage-regression-repair` skill

## Example Workflow

```
1. User requests: "Add user authentication endpoint"

2. Clarify:
   - What auth method? (JWT, OAuth, session-based?)
   - What endpoints? (login, logout, refresh?)
   - What user model exists?

3. Consult AGENTS.md:
   - Check backend conventions
   - Check test location and framework
   - Check commit message format

4. Design tests:
   - Test successful login
   - Test invalid credentials
   - Test missing fields
   - Test token generation

5. Implement:
   - Create auth service
   - Add login endpoint
   - Add JWT token generation
   - Add error handling

6. Validate:
   - Run impacted tests
   - Run full test suite
   - Run linter and type checker
   - Manual testing

7. Commit:
   - "feat: add user authentication endpoint"
   - "test: add authentication endpoint tests"

8. Prepare PR using code-review-prep skill
```

## Notes

* This is a generic skill. Always adapt to project-specific requirements.
* Consult AGENTS.md before making assumptions.
* Prefer safe, incremental changes over large rewrites.
* When in doubt, ask the user for clarification.
