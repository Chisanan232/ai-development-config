---
trigger: manual
description: Testing requirements and best practices
globs: 
---

# Testing Policy

## Testing Requirements

1. **All new features must include tests**: Features without tests will not be merged.

2. **All bug fixes must include regression tests**: Prove the bug is fixed and prevent it from recurring.

3. **Maintain or improve coverage**: Do not decrease test coverage. Consult AGENTS.md for coverage thresholds.

4. **Run impacted tests first**: Before running the full test suite, run only the tests directly affected by your changes.

## Test Organization

* **Follow project conventions**: Consult AGENTS.md for test directory structure and naming conventions.
* **Colocate tests with code**: Keep tests close to the code they test (or follow project-specific conventions).
* **One test file per source file**: Maintain a clear mapping between source and test files.

## Test Quality

* **Tests should be deterministic**: Tests must produce the same result every time. No flaky tests.
* **Tests should be independent**: Each test should run in isolation. No shared state between tests.
* **Tests should be fast**: Unit tests should run in milliseconds. Slow tests discourage running them.
* **Tests should be readable**: Tests are documentation. Make them easy to understand.

## Test Types

### Unit Tests

* **Test individual units**: Functions, methods, classes in isolation.
* **Mock external dependencies**: Database, network, file system, external services.
* **Fast execution**: Unit tests should complete in seconds for the entire suite.

### Integration Tests

* **Test component interactions**: Verify that components work together correctly.
* **Use test doubles sparingly**: Test real interactions where practical.
* **Acceptable slower execution**: Integration tests may take longer but should still be reasonably fast.

### End-to-End Tests

* **Test critical user flows**: Focus on the most important user journeys.
* **Keep E2E tests minimal**: They are slow and brittle. Use them sparingly.
* **Run in CI**: E2E tests should run automatically in the CI pipeline.

## Test-Driven Development (TDD)

* **Consider TDD for complex logic**: Write tests first for complex algorithms or business logic.
* **Red-Green-Refactor**: Write failing test → make it pass → refactor.
* **Not mandatory**: TDD is encouraged but not required for all changes.

## Testing Anti-Patterns to Avoid

* **Testing implementation details**: Test behavior, not internal structure.
* **Overly complex tests**: If a test is hard to understand, simplify it or the code under test.
* **Testing the framework**: Do not test library or framework behavior.
* **Brittle tests**: Tests should not break when unrelated code changes.

## When Tests Fail

* **Do not disable failing tests**: Fix the test or fix the code.
* **Do not weaken assertions**: If a test is too strict, understand why before relaxing it.
* **Investigate flaky tests**: Flaky tests indicate real problems. Fix them, do not ignore them.

## Coverage Guidelines

* **Coverage is a metric, not a goal**: 100% coverage does not mean bug-free code.
* **Focus on critical paths**: Ensure critical business logic is well-tested.
* **Consult AGENTS.md**: Check project-specific coverage requirements and tools.