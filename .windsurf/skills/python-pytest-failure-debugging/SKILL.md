---
name: python-pytest-failure-debugging
description: Debugs pytest test failures in Python by analyzing error messages, fixing assertions, updating fixtures, and resolving test dependencies. Use when pytest tests fail, test assertions break, fixtures error, or when debugging Python unit tests, integration tests, or parametrized tests.
metadata:
  when_to_use: When pytest tests fail locally or in CI
  tags: python, pytest, testing, debugging
  language: python
---

# Python Pytest Failure Debugging Skill

## Purpose

This skill provides a systematic approach to debugging pytest test failures quickly and safely, preserving test integrity while fixing the root cause.

## When to Invoke This Skill

Use this skill when:
* Pytest tests fail locally during development
* Tests fail in CI but pass locally
* Tests fail intermittently (flaky tests)
* Test fixtures or setup/teardown fail
* Assertion errors occur
* Tests timeout or hang

## When NOT to Invoke This Skill

Do not use this skill for:
* Designing new tests (use `test-design` skill)
* Coverage issues (use `coverage-regression-repair` skill)
* Type checking failures (use `python-mypy-debugging` skill)
* Linting failures (use `python-ruff-fixing` skill)

## Prerequisites

Before debugging pytest failures:
1. **Consult AGENTS.md**: Check test runner configuration and test conventions
2. **Understand the test**: Know what behavior the test is verifying
3. **Reproduce locally**: Ensure you can run the failing test locally

## Do Not Assume

* **Do NOT assume** all Python projects use pytest (check AGENTS.md first)
* **Do NOT assume** test file naming conventions (check AGENTS.md)
* **Do NOT assume** fixture locations or patterns
* **Do NOT assume** the test is wrong (the code might be wrong)
* **Do NOT assume** you can weaken assertions to make tests pass
* **Do NOT assume** you can skip or disable failing tests without justification

## Pytest Failure Debugging Process

### Phase 1: Identify the Failure Type

Read the pytest output and categorize the failure:

#### Assertion Failures
```
AssertionError: assert actual == expected
```
* Value mismatch
* Type mismatch
* Collection comparison failure
* Boolean assertion failure

#### Exception Failures
```
test_function raised an unexpected exception
```
* Unexpected exception during test execution
* Missing exception that should have been raised
* Wrong exception type raised

#### Fixture Failures
```
fixture 'my_fixture' not found
ERROR at setup of test_function
```
* Missing fixture
* Fixture scope issues
* Fixture dependency problems
* Setup/teardown failures

#### Timeout Failures
```
test_function timed out after 30 seconds
```
* Infinite loops
* Blocking I/O
* Deadlocks

#### Import Failures
```
ImportError: cannot import name 'X' from 'Y'
ModuleNotFoundError: No module named 'X'
```
* Missing dependencies
* Circular imports
* Path issues

### Phase 2: Gather Context

Before making changes, gather information:

1. **Read the full test output**
   ```bash
   # Run with verbose output
   pytest -vv path/to/test_file.py::test_function
   
   # Show local variables on failure
   pytest -l path/to/test_file.py::test_function
   
   # Show print statements
   pytest -s path/to/test_file.py::test_function
   ```

2. **Check test isolation**
   ```bash
   # Run the test alone
   pytest path/to/test_file.py::test_function
   
   # Run with other tests
   pytest path/to/test_file.py
   ```

3. **Inspect the test code**
   * What behavior is being tested?
   * What are the assertions checking?
   * What fixtures are used?
   * What is the test setup?

4. **Inspect the implementation code**
   * What changed recently?
   * Does the code match the test expectations?
   * Are there edge cases not handled?

### Phase 3: Classify the Root Cause

Determine the actual problem:

#### Test is Correct, Code is Wrong
* Implementation doesn't match specification
* Edge case not handled
* Regression introduced

**Action**: Fix the implementation code, not the test.

#### Test is Wrong, Code is Correct
* Test expectations are incorrect
* Test is outdated after intentional behavior change
* Test has wrong assertions

**Action**: Update the test to match correct behavior. Document why.

#### Test is Flaky
* Race conditions
* Timing dependencies
* External dependencies (network, filesystem)
* Shared state between tests

**Action**: Fix test isolation or add proper synchronization.

#### Environment Issue
* Missing dependencies
* Wrong Python version
* Missing environment variables
* File permissions

**Action**: Fix environment setup, update documentation.

### Phase 4: Apply the Fix

Based on root cause, apply the appropriate fix:

#### Fixing Implementation Code

1. **Identify the minimal fix**
   * Change only what's necessary
   * Preserve existing behavior for other cases
   * Don't refactor while fixing bugs

2. **Verify the fix**
   ```bash
   # Run the failing test
   pytest path/to/test_file.py::test_function
   
   # Run related tests
   pytest path/to/test_file.py
   
   # Run impacted tests (if known)
   pytest -k "pattern"
   ```

3. **Check for regressions**
   ```bash
   # Run full test suite for the module
   pytest path/to/module/
   ```

#### Fixing Test Code

1. **Understand why the test is wrong**
   * Was there an intentional behavior change?
   * Was the test always wrong?
   * Is this a new edge case?

2. **Update test carefully**
   * Preserve test intent
   * Update assertions to match correct behavior
   * Add comments explaining the change

3. **Verify other tests still pass**
   ```bash
   pytest path/to/test_file.py
   ```

#### Fixing Flaky Tests

1. **Identify the source of flakiness**
   * Run test multiple times: `pytest --count=10 path/to/test_file.py::test_function`
   * Check for shared state
   * Check for timing assumptions

2. **Apply proper fixes**
   * Use proper fixtures for isolation
   * Use mocking for external dependencies
   * Add proper waits/polling instead of sleep
   * Use pytest-timeout for hanging tests

3. **Verify stability**
   ```bash
   pytest --count=20 path/to/test_file.py::test_function
   ```

#### Fixing Fixture Issues

1. **Check fixture scope**
   * `function` - new instance per test
   * `class` - shared within test class
   * `module` - shared within module
   * `session` - shared across all tests

2. **Check fixture dependencies**
   * Ensure all required fixtures exist
   * Check fixture order
   * Verify fixture cleanup

3. **Fix fixture definition**
   ```python
   import pytest
   
   @pytest.fixture(scope="function")
   def my_fixture():
       # Setup
       resource = create_resource()
       yield resource
       # Teardown
       resource.cleanup()
   ```

### Phase 5: Validate the Fix

After applying the fix:

1. **Run the specific test**
   ```bash
   pytest path/to/test_file.py::test_function
   ```

2. **Run related tests**
   ```bash
   # Same file
   pytest path/to/test_file.py
   
   # Same module
   pytest path/to/module/
   ```

3. **Check coverage if relevant**
   ```bash
   pytest --cov=module_under_test path/to/test_file.py
   ```

4. **Run full suite before committing** (if time permits)
   ```bash
   pytest
   ```

### Phase 6: Document and Commit

1. **Document the fix**
   * If test was wrong, explain why in commit message
   * If code was wrong, ensure fix is clear
   * If flakiness was fixed, document the root cause

2. **Commit with clear message**
   ```
   🐛 Fix failing test_user_authentication
   
   - Root cause: Missing null check in User.authenticate()
   - Added null check before password comparison
   - Test now passes consistently
   ```

   Or for test fixes:
   ```
   ✅ Update test_calculate_discount expectations
   
   - Behavior changed in #123 to round discounts
   - Updated assertions to expect rounded values
   - All tests now pass
   ```

## Common Pytest Patterns

### Running Specific Tests

```bash
# Single test
pytest path/to/test_file.py::test_function

# Single test class
pytest path/to/test_file.py::TestClass

# Single method in class
pytest path/to/test_file.py::TestClass::test_method

# Pattern matching
pytest -k "test_user"

# By marker
pytest -m "slow"
```

### Debugging Options

```bash
# Verbose output
pytest -v

# Very verbose (show test names and results)
pytest -vv

# Show local variables on failure
pytest -l

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Drop into debugger on failure
pytest --pdb

# Show slowest tests
pytest --durations=10
```

### Fixture Debugging

```bash
# Show fixture setup
pytest --setup-show

# Show available fixtures
pytest --fixtures
```

## Safety Guidelines

### DO

* ✅ Read the full error message and traceback
* ✅ Reproduce the failure locally before fixing
* ✅ Understand what the test is verifying
* ✅ Fix the root cause, not the symptom
* ✅ Run related tests after fixing
* ✅ Preserve test intent when updating tests
* ✅ Document why tests were changed

### DO NOT

* ❌ Weaken assertions to make tests pass
* ❌ Skip or disable tests without justification
* ❌ Change test behavior without understanding why it failed
* ❌ Refactor code while debugging test failures
* ❌ Commit fixes without running related tests
* ❌ Assume the test is wrong (code might be wrong)
* ❌ Fix flaky tests with `time.sleep()` (use proper synchronization)

## Common Failure Patterns and Solutions

### Pattern: "AssertionError: assert None is not None"

**Cause**: Function returning None instead of expected value

**Solution**: Check function implementation, ensure return statement exists

### Pattern: "fixture 'X' not found"

**Cause**: Fixture not imported or not in conftest.py

**Solution**: Move fixture to conftest.py or import it properly

### Pattern: "Test passes locally but fails in CI"

**Cause**: Environment differences, timing issues, or missing dependencies

**Solution**: Check CI environment, add missing dependencies, fix timing assumptions

### Pattern: "Tests fail when run together but pass individually"

**Cause**: Shared state between tests, improper cleanup

**Solution**: Use proper fixtures, ensure test isolation, check for global state

### Pattern: "ImportError in tests"

**Cause**: Missing test dependencies, wrong Python path

**Solution**: Install test dependencies, check PYTHONPATH, verify package installation

## Integration with Other Skills

* **After fixing tests**: Use `coverage-regression-repair` if coverage dropped
* **If type errors appear**: Use `python-mypy-debugging`
* **If lint errors appear**: Use `python-ruff-fixing`
* **Before committing**: Use `code-review-prep` to prepare PR

## Project-Specific Considerations

Check AGENTS.md for:
* Test runner command (might not be `pytest`)
* Test file naming conventions
* Fixture locations
* Test markers and their meanings
* CI test execution strategy
* Coverage requirements

## Validation Checklist

Before considering the debugging complete:

- [ ] Failing test now passes
- [ ] Related tests still pass
- [ ] No new test failures introduced
- [ ] Root cause identified and documented
- [ ] Fix is minimal and focused
- [ ] Test intent preserved (if test was updated)
- [ ] Coverage maintained or improved
- [ ] Commit message clearly explains the fix

## Example Debugging Session

```bash
# 1. Identify the failure
$ pytest tests/test_user.py::test_create_user
FAILED tests/test_user.py::test_create_user - AssertionError: assert None == User(...)

# 2. Run with more details
$ pytest -vv -l tests/test_user.py::test_create_user
# Read full output, check local variables

# 3. Check the test
$ cat tests/test_user.py
# Understand what's being tested

# 4. Check the implementation
$ cat src/user.py
# Found: create_user() missing return statement

# 5. Fix the implementation
# Add: return user

# 6. Verify the fix
$ pytest tests/test_user.py::test_create_user
PASSED

# 7. Run related tests
$ pytest tests/test_user.py
PASSED (5 tests)

# 8. Commit
$ git add src/user.py
$ git commit -m "🐛 Fix create_user missing return statement"
```

## Summary

This skill helps you debug pytest failures systematically by:
1. Identifying the failure type
2. Gathering context
3. Classifying the root cause
4. Applying the appropriate fix
5. Validating the fix
6. Documenting and committing

Always fix the root cause, preserve test intent, and verify related tests still pass.
