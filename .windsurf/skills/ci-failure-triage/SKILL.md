---
name: CI Failure Triage
description: Systematic approach to diagnosing and fixing CI failures
when_to_use: When CI checks fail on a pull request or branch
tags: [ci-cd, debugging, troubleshooting]
---

# CI Failure Triage Skill

## Purpose

This skill provides a systematic approach to diagnosing and fixing CI failures quickly and safely.

## When to Invoke This Skill

Use this skill when:
* CI checks fail on your PR
* Tests fail in CI but pass locally
* Linting, type checking, or other quality checks fail in CI
* Build fails in CI
* CI pipeline encounters errors

## When NOT to Invoke This Skill

Do not use this skill for:
* Local test failures (debug them directly)
* Expected CI failures during development (use draft PRs)
* CI configuration changes (that's a different task)

## Prerequisites

Before triaging CI failures:
1. **Access CI logs**: Ensure you can view the full CI output
2. **Consult AGENTS.md**: Check CI platform and expected checks
3. **Understand the change**: Know what you modified

## CI Failure Triage Process

### Phase 1: Identify the Failure Type

Review CI output and categorize the failure:

#### Test Failures
* Unit tests failing
* Integration tests failing
* E2E tests failing
* Test timeouts

#### Code Quality Failures
* Linting errors
* Type checking errors
* Formatting issues
* Code style violations

#### Build Failures
* Compilation errors
* Dependency resolution failures
* Build script errors
* Missing files or resources

#### Coverage Failures
* Coverage below threshold
* Uncovered new code
* Coverage regression

#### Security Failures
* Dependency vulnerabilities
* Security scan failures
* Secret detection

#### Infrastructure Failures
* CI runner issues
* Network timeouts
* Resource exhaustion
* Service unavailability

### Phase 1.5: Gather Context from External Systems (If MCP Configured)

**If MCP servers are configured, gather additional context:**

#### Read PR and CI State (code_repository capability)
* Check which CI checks failed
* Read failure messages and logs
* Identify affected files and tests
* Review recent commits

#### Read Static Analysis Results (static_analysis capability, if available)
* Check for new quality issues
* Check for security vulnerabilities
* Identify code smells
* Review quality gate status

#### Read Coverage Data (coverage_reporting capability, if available)
* Check coverage percentage
* Identify uncovered lines
* Compare with previous coverage
* Identify coverage regression

**If MCP is not configured:**
* Manually access CI logs
* Manually check static analysis reports
* Manually review coverage reports
* Proceed with manual triage

**Consult AGENTS.md** for MCP source-of-truth system mappings.

### Phase 2: Reproduce Locally

**Critical step: Always try to reproduce the failure locally.**

1. **Check environment differences**
   * Node/Python/Java version
   * Operating system (CI vs local)
   * Environment variables
   * Installed dependencies

2. **Run the exact CI command locally**
   * Consult AGENTS.md for test/lint/build commands
   * Use the same command CI uses
   * Check if it fails locally

3. **If reproducible locally**
   * Debug as you normally would
   * Fix the issue
   * Verify the fix works
   * Commit and push

4. **If NOT reproducible locally**
   * Proceed to Phase 3 for CI-specific debugging

### Phase 3: Analyze CI Logs

1. **Read the full error output**
   * Do not rely on summaries
   * Read the complete stack trace
   * Look for the root cause, not just symptoms

2. **Identify the root cause**
   * What is the actual error?
   * What line of code or test is failing?
   * What is the error message?
   * Are there multiple failures or just one?

3. **Check for common CI-specific issues**
   * **Timing issues**: Tests that depend on specific timing
   * **Race conditions**: Concurrent access issues
   * **Resource limits**: Memory, CPU, disk space
   * **Network issues**: External service calls, DNS resolution
   * **File system differences**: Case sensitivity, line endings
   * **Flaky tests**: Tests that sometimes pass, sometimes fail

### Phase 4: Fix the Issue

#### For Test Failures

1. **Understand why the test is failing**
   * Read the test code
   * Read the error message
   * Identify what assertion failed

2. **Determine if it's a real bug or a test issue**
   * Real bug: The code is wrong
   * Test issue: The test is wrong or flaky

3. **Fix safely**
   * If code bug: Fix the code, preserve behavior
   * If test bug: Fix the test, ensure it still validates behavior
   * If flaky test: Make it deterministic or quarantine it

4. **Verify the fix**
   * Run the test locally multiple times
   * Ensure it passes consistently

#### For Linting/Type Checking Failures

1. **Run the linter/type checker locally**
   * Consult AGENTS.md for commands
   * Use the exact command CI uses

2. **Fix the issues**
   * Address each error or warning
   * Follow project style guidelines
   * Avoid type suppressions unless necessary

3. **Run auto-fix if available**
   * Consult AGENTS.md for auto-fix commands
   * Review auto-fix changes before committing

#### For Build Failures

1. **Check dependency versions**
   * Lock file is up to date
   * No version conflicts
   * All dependencies installed

2. **Check for missing files**
   * All required files are committed
   * No gitignored files that should be included

3. **Check build configuration**
   * Build scripts are correct
   * Environment variables are set
   * Paths are correct

#### For Coverage Failures

1. **Check coverage report**
   * Which files have low coverage?
   * Which lines are not covered?

2. **Add tests for uncovered code**
   * Focus on critical paths
   * Use `coverage-regression-repair` skill if needed

3. **Verify coverage threshold**
   * Consult AGENTS.md for threshold
   * Ensure new code meets threshold

### Phase 5: Commit and Push Fix

1. **Commit by issue category**
   * Group fixes by failure type
   * Use clear commit messages

**Examples:**
* `fix: resolve mypy type errors in user module`
* `fix: correct linting violations in api handlers`
* `test: fix flaky integration test for auth service`
* `build: update dependency to fix build failure`

2. **Push and monitor CI**
   * Push the fix
   * Watch CI run
   * Verify the fix works

3. **Iterate if needed**
   * If CI still fails, repeat the process
   * Do not give up after one attempt

### Phase 6: Prevent Future Failures

1. **Add regression tests** (if applicable)
   * Ensure the failure cannot happen again
   * Test the fix

2. **Update documentation** (if needed)
   * Document non-obvious fixes
   * Update troubleshooting guides

3. **Improve CI** (if applicable)
   * Make error messages clearer
   * Add better logging
   * Improve test reliability

## Do Not Assume

* **Do not assume** CI platform or configuration
* **Do not assume** test commands or scripts
* **Do not assume** environment variables or secrets
* **Do not assume** CI-specific quirks

**Always consult AGENTS.md first.**

## Common CI Failure Patterns

### Pattern 1: Flaky Tests

**Symptoms:**
* Test passes sometimes, fails sometimes
* No code changes between runs
* Different results on different runs

**Solutions:**
* Make tests deterministic
* Remove timing dependencies
* Fix race conditions
* Use proper synchronization
* Mock time-dependent code

### Pattern 2: Environment Differences

**Symptoms:**
* Works locally, fails in CI
* Different OS or runtime version
* Missing environment variables

**Solutions:**
* Match local environment to CI
* Check runtime versions
* Set required environment variables
* Use consistent dependencies

### Pattern 3: Resource Exhaustion

**Symptoms:**
* Tests timeout
* Out of memory errors
* Disk space errors

**Solutions:**
* Optimize resource usage
* Clean up test data
* Increase timeouts (if justified)
* Split large test suites

### Pattern 4: External Dependencies

**Symptoms:**
* Network errors
* API call failures
* Service unavailability

**Solutions:**
* Mock external services
* Use test doubles
* Add retry logic
* Check service status

## Fallback Logic

If you cannot resolve the failure:

1. **Document what you tried**
   * List all debugging steps
   * Share findings with the team

2. **Ask for help**
   * Tag team members with expertise
   * Provide full context and logs

3. **Create an issue**
   * Document the failure
   * Track the investigation

4. **Consider workarounds**
   * Skip flaky test temporarily (with tracking issue)
   * Increase timeouts (if justified)
   * Adjust thresholds (if justified)

## Validation Checklist

Before considering the fix complete:

- [ ] Root cause identified
- [ ] Fix implemented
- [ ] Fix verified locally
- [ ] Commit message follows conventions
- [ ] CI passes
- [ ] No new failures introduced
- [ ] Regression test added (if applicable)

## Integration with Other Skills

* **For coverage failures**: Use `coverage-regression-repair` skill
* **For Python type errors**: Use `python-mypy-debugging` skill
* **For Python lint errors**: Use `python-ruff-fixing` skill
* **For pre-commit failures**: Use `python-precommit-repair` skill

## [PROJECT-SPECIFIC MCP MAPPING]

For projects with MCP configured, capabilities map to:

* **code_repository**: Use to read GitHub/GitLab PR checks and CI logs
* **static_analysis**: Use to read SonarQube/CodeClimate quality gate
* **coverage_reporting**: Use to read Codecov/Coveralls reports
* **communication**: Use to notify team of CI failures (optional)
* **issue_tracking**: Use to update related issues (optional)

Consult AGENTS.md for your project's specific MCP configuration and source-of-truth mappings.

## Example Workflow

```
1. CI fails with test failure

2. Identify failure type:
   - Test: test_user_authentication failed
   - Error: AssertionError: expected 200, got 401

3. Reproduce locally:
   - Run: pytest tests/test_auth.py::test_user_authentication
   - Result: Passes locally

4. Analyze CI logs:
   - CI uses different database
   - Test user not created in CI environment

5. Fix:
   - Update test to create test user in setup
   - Ensure test is self-contained

6. Commit:
   - "test: fix user authentication test to be self-contained"

7. Push and verify:
   - CI passes ✓
```

## Notes

* This is a generic skill. Always adapt to project-specific requirements.
* Consult AGENTS.md before making assumptions.
* CI failures are normal. Fix them systematically, not frantically.
* When in doubt, ask the user for clarification.
