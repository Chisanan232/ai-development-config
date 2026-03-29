---
name: test-design
description: Systematic approach to designing comprehensive tests
metadata:
  when_to_use: When designing tests for new features or existing code
  tags: testing, test-design, quality
---

# Test Design Skill

## Purpose

This skill provides a systematic approach to designing comprehensive, maintainable tests that verify behavior and prevent regressions.

## When to Invoke This Skill

Use this skill when:
* Designing tests for a new feature
* Adding tests to untested code
* Improving test coverage
* Refactoring tests for better clarity

## When NOT to Invoke This Skill

Do not use this skill for:
* Running existing tests (just run them)
* Debugging failing tests (use ci-failure-triage)
* Simple test updates (make the change directly)

## Prerequisites

Before designing tests:
1. **Consult AGENTS.md** for testing conventions
2. **Understand the behavior** being tested
3. **Identify test types** needed (unit, integration, E2E)
4. **Check existing test patterns** in the codebase

## Test Design Process

### Phase 1: Understand What to Test

1. **Identify the behavior**
   * What should this code do?
   * What are the inputs and outputs?
   * What are the side effects?
   * What are the dependencies?

2. **Identify test boundaries**
   * What is in scope for this test?
   * What should be mocked or stubbed?
   * What is the appropriate test level (unit, integration, E2E)?

3. **Consult AGENTS.md**
   * Where should tests be located?
   * What test framework is used?
   * What naming conventions apply?
   * What coverage threshold is required?

### Phase 2: Identify Test Scenarios

Use this framework to identify scenarios:

#### 1. Happy Path (Normal Cases)

* **Valid inputs**: Normal, expected usage
* **Typical workflows**: Common user journeys
* **Expected outputs**: Correct results for valid inputs

#### 2. Edge Cases (Boundary Conditions)

* **Empty inputs**: Empty strings, empty arrays, zero values
* **Null/undefined**: Missing or null values
* **Boundary values**: Min/max values, first/last elements
* **Large inputs**: Large datasets, long strings
* **Special characters**: Unicode, special symbols, escape sequences

#### 3. Error Cases (Failure Conditions)

* **Invalid inputs**: Wrong types, out-of-range values
* **Missing required data**: Null when non-null expected
* **Constraint violations**: Duplicate keys, invalid formats
* **External failures**: Network errors, database errors, file system errors

#### 4. Integration Points

* **Component interactions**: How components work together
* **External dependencies**: APIs, databases, file systems
* **State changes**: How state is modified and persisted
* **Concurrent access**: Race conditions, locking (if applicable)

### Phase 3: Choose Test Types

#### Unit Tests

**When to use:**
* Testing individual functions, methods, or classes
* Testing business logic in isolation
* Testing pure functions and calculations

**Characteristics:**
* Fast (milliseconds)
* Isolated (mock external dependencies)
* Focused (one unit of behavior)

**Example scenarios:**
* Function returns correct value for given input
* Method throws error for invalid input
* Class maintains correct internal state

#### Integration Tests

**When to use:**
* Testing component interactions
* Testing database queries
* Testing API endpoints
* Testing service integrations

**Characteristics:**
* Slower than unit tests (seconds)
* Use real dependencies where practical
* Test multiple components together

**Example scenarios:**
* API endpoint returns correct data from database
* Service correctly calls external API
* Components communicate correctly

#### End-to-End Tests

**When to use:**
* Testing critical user flows
* Testing full system behavior
* Testing UI interactions

**Characteristics:**
* Slowest (seconds to minutes)
* Test the entire system
* Use real environment

**Example scenarios:**
* User can complete signup flow
* User can checkout and purchase
* Admin can manage users

### Phase 4: Write Test Structure

#### Test Naming

Follow project conventions (consult AGENTS.md), but generally:

* **Descriptive names**: `test_user_login_with_valid_credentials`
* **Behavior-focused**: `should_return_error_when_email_is_invalid`
* **Scenario-based**: `given_empty_cart_when_checkout_then_error`

#### Test Organization

Use the AAA pattern (Arrange-Act-Assert):

```
// Arrange: Set up test data and conditions
const user = createTestUser();
const credentials = { email: user.email, password: 'password123' };

// Act: Execute the behavior being tested
const result = await authService.login(credentials);

// Assert: Verify the outcome
expect(result.token).toBeDefined();
expect(result.user.id).toBe(user.id);
```

Or Given-When-Then for BDD:

```
// Given: Initial context
Given a registered user with email "test@example.com"

// When: Action or event
When the user logs in with correct credentials

// Then: Expected outcome
Then a valid JWT token is returned
And the user session is created
```

### Phase 5: Implement Tests

1. **Write the test**
   * Follow the test structure (AAA or Given-When-Then)
   * Use clear, descriptive assertions
   * Keep tests simple and focused

2. **Use appropriate assertions**
   * Be specific: `expect(value).toBe(42)` not `expect(value).toBeTruthy()`
   * Test behavior: `expect(fn).toThrow(Error)` not implementation details
   * Use meaningful messages: `expect(result, 'User should be authenticated').toBeDefined()`

3. **Mock external dependencies**
   * Mock network calls
   * Mock database queries (for unit tests)
   * Mock file system operations
   * Use test doubles (mocks, stubs, spies) appropriately

4. **Set up and tear down**
   * Use setup/teardown hooks (beforeEach, afterEach)
   * Clean up resources (close connections, delete test data)
   * Ensure tests are independent

### Phase 6: Validate Tests

1. **Run the tests**
   * Verify tests pass
   * Verify tests fail when they should (test the test)
   * Check test output is clear

2. **Check test quality**
   * Are tests deterministic (same result every time)?
   * Are tests independent (no shared state)?
   * Are tests fast enough?
   * Are tests readable and maintainable?

3. **Verify coverage**
   * Run coverage tool (consult AGENTS.md)
   * Check that critical paths are covered
   * Identify gaps in coverage

## Do Not Assume

* **Do not assume** test framework without checking AGENTS.md
* **Do not assume** test location or naming conventions
* **Do not assume** mocking library or patterns
* **Do not assume** coverage requirements
* **Do not assume** test commands

**Always consult AGENTS.md first.**

## Test Design Patterns

### Pattern 1: Test Data Builders

Create reusable test data builders:

```python
def create_test_user(**overrides):
    defaults = {
        'email': 'test@example.com',
        'name': 'Test User',
        'role': 'user'
    }
    return User(**{**defaults, **overrides})
```

### Pattern 2: Parameterized Tests

Test multiple scenarios with one test:

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("", ""),
])
def test_uppercase(input, expected):
    assert uppercase(input) == expected
```

### Pattern 3: Test Fixtures

Reuse setup logic:

```python
@pytest.fixture
def authenticated_client():
    client = TestClient()
    client.login(username='test', password='test')
    return client
```

## Common Test Anti-Patterns to Avoid

* **Testing implementation details**: Test behavior, not internal structure
* **Overly complex tests**: If a test is hard to understand, simplify it
* **Brittle tests**: Tests should not break when unrelated code changes
* **Slow tests**: Optimize slow tests or move them to integration/E2E
* **Flaky tests**: Tests must be deterministic
* **Testing the framework**: Do not test library or framework behavior
* **Shared state between tests**: Each test should be independent

## Validation Checklist

Before considering tests complete:

- [ ] All scenarios identified (happy path, edge cases, errors)
- [ ] Appropriate test types chosen (unit, integration, E2E)
- [ ] Tests follow project conventions (consult AGENTS.md)
- [ ] Tests are deterministic and independent
- [ ] Tests are readable and maintainable
- [ ] External dependencies are mocked appropriately
- [ ] Coverage meets project requirements
- [ ] All tests pass

## Integration with Other Skills

* **Before test design**: Use `feature-implementation` to understand the feature
* **After test design**: Run tests and verify they pass
* **If tests fail**: Use `ci-failure-triage` to diagnose
* **If coverage is low**: Use `coverage-regression-repair`

## Example Workflow

```
1. User requests: "Add tests for user authentication"

2. Consult AGENTS.md:
   - Test location: tests/unit/auth/
   - Test framework: pytest
   - Naming: test_*.py

3. Identify scenarios:
   Happy path:
   - Valid credentials → successful login
   - Valid token → authenticated request
   
   Edge cases:
   - Empty email → validation error
   - Empty password → validation error
   
   Error cases:
   - Invalid credentials → authentication error
   - Expired token → token expired error
   - Missing token → unauthorized error

4. Choose test types:
   - Unit tests for auth service logic
   - Integration tests for auth endpoints

5. Write tests:
   - test_login_with_valid_credentials()
   - test_login_with_invalid_credentials()
   - test_login_with_empty_email()
   - test_authenticated_request_with_valid_token()
   - test_authenticated_request_with_expired_token()

6. Run and validate:
   - All tests pass
   - Coverage meets threshold
```

## Notes

* This is a generic skill. Always adapt to project-specific requirements.
* Consult AGENTS.md before making assumptions.
* Good tests are an investment in code quality and maintainability.
* When in doubt, ask the user for clarification.
