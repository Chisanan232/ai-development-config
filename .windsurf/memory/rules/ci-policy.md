---
trigger: manual
description: CI/CD expectations and failure handling procedures
globs: 
---

# CI/CD Policy

## CI Pipeline Expectations

Consult AGENTS.md for project-specific CI configuration:
* CI platform (GitHub Actions, GitLab CI, Jenkins, CircleCI)
* Pipeline configuration location
* Required checks
* Expected CI duration

## CI Requirements

### All PRs Must Pass CI

* **No merging on red**: PRs with failing CI checks cannot be merged
* **Fix failures promptly**: Address CI failures as soon as they occur
* **Do not disable checks**: Do not bypass or disable CI checks to merge

### CI Checks

Typical CI checks include:
* **Tests**: Unit, integration, and E2E tests or other test types
* **Linting**: Code style and quality checks
* **Type checking**: Static type analysis
* **Build**: Verify the project builds successfully
* **Security scanning**: Dependency vulnerabilities, code security
* **Coverage**: Ensure test coverage meets thresholds

## CI Failure Handling

When CI fails, follow this procedure:

### 1. Triage the Failure

Identify the root cause:
* **Test failure**: Which test(s) failed and why?
* **Lint error**: Which linting rules were violated?
* **Type error**: Which type checks failed?
* **Build failure**: What caused the build to fail?
* **Security issue**: Which vulnerabilities were detected?

### 2. Reproduce Locally

* **Run the failing check locally**: Use the same command that CI uses
* **Verify you can reproduce**: Ensure the failure is consistent
* **Check for environment differences**: CI environment vs local environment

### 3. Fix Safely

* **Address the root cause**: Fix the underlying problem, not just the symptom
* **Make minimal changes**: Do not broaden the scope of fixes
* **Preserve runtime behavior**: Do not change observable behavior unless required
* **Follow safe-fix principles**: Consult `.windsurf/rules/coding-standards.md`

### 4. Commit by Issue Category

Group fixes by failure type:
* `fix: resolve mypy type errors in user module`
* `fix: correct linting violations in api handlers`
* `test: fix flaky integration test for auth service`
* `build: update dependency to fix build failure`

### 5. Verify Before Pushing

* **Run the failing check locally**: Ensure it passes before pushing
* **Run related checks**: Verify you didn't break something else
* **Push and monitor**: Watch CI to confirm the fix works

### 6. Iterate Until Green

* **Repeat the process**: If CI still fails, repeat steps 1-5
* **Ask for help if stuck**: If you cannot resolve the failure, ask the team

## Flaky Tests

Flaky tests are tests that sometimes pass and sometimes fail without code changes.

### Handling Flaky Tests

* **Do not ignore**: Flaky tests indicate real problems
* **Investigate immediately**: Identify the root cause
* **Fix or quarantine**: Either fix the flakiness or temporarily skip the test with a tracking issue
* **Track with issues**: Create an issue to track flaky test fixes

### Common Causes of Flakiness

* **Race conditions**: Asynchronous code without proper synchronization
* **Timing dependencies**: Tests that depend on specific timing
* **Shared state**: Tests that interfere with each other
* **External dependencies**: Tests that depend on external services
* **Non-deterministic behavior**: Random data, timestamps, etc.

## CI Performance

### Expected CI Duration

Consult AGENTS.md for project-specific expectations.

General guidelines:
* **Fast feedback**: CI should complete in < 10 minutes for most projects
* **Optimize slow tests**: Identify and optimize slow-running tests
* **Parallelize**: Run tests in parallel when possible
* **Cache dependencies**: Cache dependencies to speed up builds

### Monitoring CI Performance

* **Track CI duration**: Monitor how long CI takes over time
* **Identify bottlenecks**: Find which checks are slowest
* **Optimize incrementally**: Improve CI performance over time

## CI/CD Pipeline Stages

Typical pipeline stages:

### 1. Build Stage

* Install dependencies
* Compile code
* Build artifacts

### 2. Test Stage

* Run unit tests
* Run integration tests
* Run E2E tests (if applicable)
* Generate coverage reports

### 3. Quality Stage

* Run linting
* Run type checking
* Run security scans
* Check code coverage

### 4. Deploy Stage (for main/production branches)

* Build container images
* Push to registry
* Deploy to environment
* Run smoke tests

## Branch-Specific CI Behavior

### Feature Branches / PRs

* Run all quality checks
* Run all tests
* Do not deploy

### Main Branch

* Run all quality checks
* Run all tests
* Deploy to staging/dev environment
* Run smoke tests

### Release Branches / Tags

* Run all quality checks
* Run all tests
* Deploy to production
* Run smoke tests
* Create release artifacts

## CI Notifications

* **Slack/Email notifications**: Configure for CI failures on main branch
* **PR comments**: CI should comment on PRs with results
* **Status checks**: CI status should be visible in PR interface

## CI Security

* **Secrets management**: Use CI platform's secret management (GitHub Secrets, GitLab CI/CD variables)
* **Never log secrets**: Ensure secrets are not printed in CI logs
* **Limit permissions**: Use least-privilege access for CI jobs
* **Audit CI changes**: Review changes to CI configuration carefully

## Debugging CI Failures

### Access CI Logs

* **View full logs**: Check complete CI output, not just the summary
* **Download artifacts**: Download test reports, coverage reports, build artifacts
* **SSH into CI environment**: If available, SSH into the CI runner to debug

### Common CI Issues

* **Environment differences**: CI environment differs from local (Node version, Python version, etc.)
* **Missing dependencies**: Dependency not installed or cached incorrectly
* **Timing issues**: Tests that pass locally but fail in CI due to timing
* **Resource constraints**: CI runner has limited CPU/memory

## CI Best Practices

* **Keep CI configuration in version control**: `.github/workflows/`, `.gitlab-ci.yml`, etc.
* **Make CI reproducible**: CI should produce the same result every time
* **Fail fast**: Run quick checks first, slow checks later
* **Provide clear error messages**: CI failures should be easy to diagnose
* **Keep CI green**: Fix failures immediately, do not let them accumulate