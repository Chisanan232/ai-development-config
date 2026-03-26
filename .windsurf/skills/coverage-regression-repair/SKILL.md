---
name: Coverage Regression Repair
description: Fix test coverage regressions while maintaining code quality
when_to_use: When test coverage drops below threshold or CI coverage checks fail
tags: [testing, coverage, quality]
---

# Coverage Regression Repair Skill

## Purpose

This skill provides a systematic approach to fixing test coverage regressions while maintaining code quality and test integrity.

## When to Invoke This Skill

Use this skill when:
* CI coverage check fails
* Coverage drops below project threshold
* New code is not adequately tested
* Coverage report shows uncovered critical paths

## When NOT to Invoke This Skill

Do not use this skill for:
* Writing tests for new features (use `test-design` skill)
* Debugging failing tests (use `ci-failure-triage` skill)
* Improving coverage for its own sake (focus on critical paths)

## Prerequisites

Before fixing coverage:
1. **Consult AGENTS.md** for coverage requirements and tools
2. **Run coverage report** to identify gaps
3. **Understand the uncovered code** and its purpose

## Coverage Repair Process

### Phase 1: Assess the Coverage Gap

1. **Get coverage data**

   **If coverage_reporting MCP capability is available:**
   * Use MCP to read current coverage percentage
   * Use MCP to read file-level coverage
   * Use MCP to read uncovered line numbers
   * Use MCP to read coverage diff (if available)
   
   **If MCP is not configured:**
   * Run coverage report locally (consult AGENTS.md for command)
   * Generate HTML or detailed report
   * Manually identify uncovered lines

2. **Analyze the gap**
   * Which files have low coverage?
   * Which functions/methods are uncovered?
   * Which branches are not taken?
   * How much coverage is missing?

3. **Prioritize coverage work**
   * **Critical paths first**: Core business logic, security-sensitive code
   * **High-risk areas**: Complex algorithms, error handling
   * **Public APIs**: Externally facing interfaces
   * **Low priority**: Trivial getters/setters, simple utilities

### Phase 2: Understand the Uncovered Code

1. **Read the uncovered code**
   * What does it do?
   * What are the inputs and outputs?
   * What are the edge cases?
   * What are the error conditions?

2. **Check if it's testable**
   * Can it be tested in isolation?
   * Does it have external dependencies?
   * Is it pure or does it have side effects?

3. **Check for existing tests**
   * Are there related tests?
   * Can existing tests be extended?
   * Or do new tests need to be written?

### Phase 3: Design Coverage Tests

**Use the `test-design` skill for comprehensive test design.**

For coverage-focused tests:

1. **Identify uncovered scenarios**
   * Which code paths are not executed?
   * Which branches are not taken?
   * Which error conditions are not tested?

2. **Design minimal tests to cover gaps**
   * Focus on executing uncovered lines
   * Ensure branches are taken
   * Test error conditions

3. **Avoid coverage theater**
   * Do not write meaningless tests just for coverage
   * Tests should validate behavior, not just execute code
   * Coverage is a metric, not a goal

### Phase 4: Write Coverage Tests

1. **Write tests for uncovered code**
   * Follow project test conventions (consult AGENTS.md)
   * Use existing test patterns
   * Keep tests simple and focused

2. **Focus on behavior, not coverage**
   * Tests should verify correct behavior
   * Coverage is a side effect of good tests
   * Do not test implementation details

3. **Cover critical paths thoroughly**
   * Happy path
   * Edge cases
   * Error conditions
   * Boundary values

### Phase 5: Verify Coverage Improvement

1. **Run tests**
   * Ensure all tests pass
   * Verify new tests are correct

2. **Run coverage report**
   * Check coverage has improved
   * Verify uncovered lines are now covered
   * Ensure threshold is met

3. **Review coverage report**
   * Are there still critical gaps?
   * Is coverage evenly distributed?
   * Are there false positives?

### Phase 6: Commit Coverage Improvements

1. **Commit tests separately** (if appropriate)
   * Separate commit for coverage tests
   * Clear commit message

**Examples:**
* `test: add coverage for user authentication edge cases`
* `test: cover error handling in payment service`
* `test: increase coverage for data validation logic`

2. **Push and verify CI**
   * Ensure CI coverage check passes
   * Verify no regressions

## Do Not Assume

* **Do not assume** coverage tool or configuration
* **Do not assume** coverage threshold
* **Do not assume** what code is critical
* **Do not assume** test location or conventions

**Always consult AGENTS.md first.**

## Coverage Strategies

### Strategy 1: Extend Existing Tests

If there are related tests, extend them:

```python
# Existing test
def test_user_login_success():
    result = auth.login("user@example.com", "password")
    assert result.success

# Extended test for coverage
def test_user_login_with_invalid_email():
    result = auth.login("invalid-email", "password")
    assert not result.success
    assert result.error == "Invalid email format"
```

### Strategy 2: Add Parameterized Tests

Cover multiple scenarios efficiently:

```python
@pytest.mark.parametrize("input,expected", [
    ("", False),           # Empty string
    ("a", False),          # Too short
    ("abc123", True),      # Valid
    ("a" * 100, False),    # Too long
])
def test_password_validation(input, expected):
    assert validate_password(input) == expected
```

### Strategy 3: Test Error Paths

Ensure error handling is covered:

```python
def test_api_call_with_network_error():
    with mock.patch('requests.get', side_effect=NetworkError):
        with pytest.raises(ServiceUnavailable):
            api_client.fetch_data()
```

### Strategy 4: Test Branch Coverage

Ensure all branches are taken:

```python
def test_discount_calculation_with_coupon():
    # Test the "if coupon" branch
    price = calculate_price(100, coupon="SAVE10")
    assert price == 90

def test_discount_calculation_without_coupon():
    # Test the "else" branch
    price = calculate_price(100, coupon=None)
    assert price == 100
```

## Coverage Anti-Patterns to Avoid

### Anti-Pattern 1: Coverage Theater

**Bad:**
```python
def test_user_creation():
    user = User("test@example.com")
    # Just creating the object for coverage, not testing behavior
```

**Good:**
```python
def test_user_creation():
    user = User("test@example.com")
    assert user.email == "test@example.com"
    assert user.is_active == True
    assert user.created_at is not None
```

### Anti-Pattern 2: Testing Implementation Details

**Bad:**
```python
def test_internal_cache():
    service._cache = {}  # Testing internal implementation
    service.get_data()
    assert len(service._cache) == 1
```

**Good:**
```python
def test_data_retrieval_is_cached():
    # First call hits the API
    data1 = service.get_data()
    # Second call should be cached (faster)
    data2 = service.get_data()
    assert data1 == data2
    # Verify API was only called once
    assert mock_api.call_count == 1
```

### Anti-Pattern 3: Meaningless Assertions

**Bad:**
```python
def test_process_data():
    result = process_data([1, 2, 3])
    assert result is not None  # Meaningless assertion
```

**Good:**
```python
def test_process_data():
    result = process_data([1, 2, 3])
    assert result == [2, 4, 6]  # Verify actual behavior
```

## Handling Difficult-to-Test Code

### Scenario 1: Code with External Dependencies

**Solution:** Use dependency injection and mocking

```python
# Hard to test
def fetch_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Easier to test
def fetch_user_data(user_id, http_client=requests):
    response = http_client.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test
def test_fetch_user_data():
    mock_client = Mock()
    mock_client.get.return_value.json.return_value = {"id": 1, "name": "Test"}
    result = fetch_user_data(1, http_client=mock_client)
    assert result["name"] == "Test"
```

### Scenario 2: Code with Side Effects

**Solution:** Extract testable logic

```python
# Hard to test
def process_and_save(data):
    processed = complex_processing(data)
    database.save(processed)
    send_email(processed)

# Easier to test
def process_data(data):
    return complex_processing(data)

def save_and_notify(processed_data):
    database.save(processed_data)
    send_email(processed_data)

# Test the logic separately
def test_process_data():
    result = process_data({"value": 10})
    assert result["value"] == 20
```

### Scenario 3: Legacy Code

**Solution:** Add characterization tests

```python
# Don't know what this does, but need coverage
def mysterious_function(x, y):
    # Complex legacy logic
    ...

# Characterization test: document current behavior
def test_mysterious_function_behavior():
    # Document what it currently does
    assert mysterious_function(1, 2) == 3
    assert mysterious_function(0, 0) == 0
    assert mysterious_function(-1, 1) == 0
```

## Validation Checklist

Before considering coverage repair complete:

- [ ] Coverage threshold met
- [ ] Critical paths covered
- [ ] Tests verify behavior, not just execute code
- [ ] All new tests pass
- [ ] No meaningless or trivial tests
- [ ] Tests follow project conventions
- [ ] Coverage report reviewed
- [ ] CI coverage check passes

## Integration with Other Skills

* **For test design**: Use `test-design` skill
* **For feature testing**: Use `feature-implementation` skill
* **For CI failures**: Use `ci-failure-triage` skill

## [PROJECT-SPECIFIC MCP MAPPING]

For projects with MCP configured, capabilities map to:

* **coverage_reporting**: Use to read Codecov/Coveralls/SonarQube coverage data
* **code_repository**: Use to read PR coverage diff (optional)

Consult AGENTS.md for your project's specific MCP configuration and source-of-truth mappings.

## Example Workflow

```
1. CI fails: "Coverage 78%, threshold 80%"

2. Run coverage report:
   - Consult AGENTS.md: `pytest --cov --cov-report=html`
   - Open htmlcov/index.html

3. Identify gaps:
   - src/auth/service.py: 65% coverage
   - Lines 45-52 not covered (error handling)
   - Lines 78-82 not covered (edge case)

4. Understand uncovered code:
   - Lines 45-52: Handle invalid token format
   - Lines 78-82: Handle expired token

5. Write tests:
   - test_auth_with_invalid_token_format()
   - test_auth_with_expired_token()

6. Verify:
   - Run tests: All pass
   - Run coverage: 82% (above threshold)

7. Commit:
   - "test: add coverage for auth error handling"

8. Push and verify:
   - CI passes ✓
```

## Notes

* This is a generic skill. Always adapt to project-specific requirements.
* Consult AGENTS.md before making assumptions.
* Coverage is a means to an end (quality), not an end itself.
* Focus on meaningful tests that prevent bugs.
* When in doubt, ask the user for clarification.
