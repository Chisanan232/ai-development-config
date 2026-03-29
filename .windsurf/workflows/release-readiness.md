---
description: Release readiness checklist
---

# Release Readiness Workflow

This workflow ensures your release is complete, tested, and ready for deployment.

## When to Use

Run this workflow before creating a release or deploying to production.

## Prerequisites

* All planned features are merged
* All critical bugs are fixed
* Release branch or tag is prepared

## Workflow Steps

### 1. Verify All PRs Are Merged

**Check that all intended work is included:**
- [ ] All feature PRs merged
- [ ] All bug fix PRs merged
- [ ] All dependency updates merged
- [ ] No pending critical work

**Review merged PRs:**

```bash
# List merged PRs since last release
git log --oneline v1.0.0..HEAD

# Or use GitHub/GitLab UI to review merged PRs
```

### 2. Run Full Test Suite

Consult AGENTS.md for test commands.

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv run pytest
# JavaScript: npm test
# Rust: cargo test
```

**Verify:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass (if applicable)
- [ ] No flaky tests
- [ ] Tests run in clean environment

### 3. Run All Quality Checks

#### Linting

```bash
# Consult AGENTS.md for lint command
```

- [ ] No linting errors
- [ ] No linting warnings (or documented)

#### Type Checking

```bash
# Consult AGENTS.md for type check command
```

- [ ] No type errors

#### Security Scanning

```bash
# Example commands
# Python: pip-audit or safety check
# JavaScript: npm audit
# Rust: cargo audit
```

- [ ] No critical vulnerabilities
- [ ] High-severity issues addressed or documented
- [ ] Dependency versions reviewed

### 4. Verify Test Coverage

```bash
# Consult AGENTS.md for coverage command
```

- [ ] Coverage meets or exceeds threshold
- [ ] Critical paths are well-covered
- [ ] No significant coverage regressions

### 5. Build and Verify Artifacts

Consult AGENTS.md for build commands.

```bash
# Example commands (replace with actual commands from AGENTS.md)
# Python: uv build
# JavaScript: npm run build
# Rust: cargo build --release
```

**Verify:**
- [ ] Build succeeds without errors
- [ ] Build artifacts are correct
- [ ] Artifact size is reasonable
- [ ] No unexpected files in artifacts

### 6. Update Version Number

Consult project versioning strategy (semantic versioning, calendar versioning, etc.).

**Update version in:**
- [ ] Package manifest (package.json, Cargo.toml, pyproject.toml, etc.)
- [ ] Version file (if separate)
- [ ] Documentation
- [ ] Changelog

**Commit version bump:**

```bash
git commit -am "chore: bump version to 1.1.0"
```

### 7. Update Changelog

Review all changes since last release:

```bash
# Generate commit log
git log --oneline v1.0.0..HEAD

# Or use a changelog generator
```

**Update CHANGELOG.md with:**
- [ ] New features
- [ ] Bug fixes
- [ ] Breaking changes
- [ ] Deprecations
- [ ] Security fixes
- [ ] Performance improvements
- [ ] Dependencies updated

**Changelog format example:**

```markdown
## [1.1.0] - 2024-01-15

### Added
- User authentication with JWT tokens (#123)
- Password reset functionality (#145)

### Fixed
- Null pointer error in user service (#156)
- Memory leak in data processing (#167)

### Changed
- Updated API response format (BREAKING CHANGE) (#178)
- Improved error messages (#189)

### Security
- Updated dependency with security vulnerability (#190)
```

### 8. Review Documentation

**Verify documentation is up to date:**
- [ ] README reflects current state
- [ ] API documentation is current
- [ ] Architecture docs are current
- [ ] Deployment guide is current
- [ ] Migration guide (if breaking changes)
- [ ] Troubleshooting guide

**Update if needed:**
- [ ] Installation instructions
- [ ] Configuration examples
- [ ] Usage examples
- [ ] Breaking change migration steps

### 9. Test in Staging Environment

If applicable, deploy to staging:

```bash
# Consult AGENTS.md or deployment docs for staging deployment
```

**Verify in staging:**
- [ ] Application starts successfully
- [ ] All services are healthy
- [ ] Critical user flows work
- [ ] Performance is acceptable
- [ ] No errors in logs
- [ ] Database migrations succeed (if applicable)

**Run smoke tests:**
- [ ] Health check endpoint responds
- [ ] Authentication works
- [ ] Core features functional
- [ ] API endpoints respond correctly

### 10. Create Release Branch or Tag

Consult project branching strategy.

**Option 1: Release branch**

```bash
git checkout -b release/1.1.0
git push origin release/1.1.0
```

**Option 2: Release tag**

```bash
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

### 11. Prepare Release Notes

Write clear, user-focused release notes:

**Include:**
- [ ] Overview of release
- [ ] Highlights (most important changes)
- [ ] New features with examples
- [ ] Bug fixes
- [ ] Breaking changes with migration guide
- [ ] Deprecation notices
- [ ] Known issues
- [ ] Upgrade instructions
- [ ] Contributors (if applicable)

**Release notes template:**

```markdown
# Release 1.1.0

## Highlights

This release adds user authentication and improves performance.

## New Features

### User Authentication
We've added JWT-based authentication. See the [authentication guide](link) for details.

### Password Reset
Users can now reset their passwords via email.

## Bug Fixes

- Fixed null pointer error in user service (#156)
- Fixed memory leak in data processing (#167)

## Breaking Changes

### API Response Format
The API response format has changed. See [migration guide](link) for details.

Before:
```json
{ "data": {...} }
```

After:
```json
{ "result": {...}, "meta": {...} }
```

## Upgrade Instructions

1. Update to version 1.1.0
2. Run database migrations: `./migrate.sh`
3. Update API client code (if using old response format)
4. Restart services

## Known Issues

- Issue #200: Performance degradation with large datasets (workaround available)

## Contributors

Thank you to all contributors!
```

### 12. Verify CI/CD Pipeline

**Check CI/CD for release:**
- [ ] CI passes on release branch/tag
- [ ] All required checks pass
- [ ] Build artifacts are created
- [ ] Deployment pipeline is ready

### 13. Notify Stakeholders

**Before release:**
- [ ] Notify team of upcoming release
- [ ] Notify users of breaking changes (if applicable)
- [ ] Schedule maintenance window (if needed)
- [ ] Prepare rollback plan

### 14. Deploy to Production

Consult AGENTS.md or deployment docs for production deployment.

**Deployment checklist:**
- [ ] Backup current production state
- [ ] Run database migrations (if applicable)
- [ ] Deploy new version
- [ ] Verify deployment succeeded
- [ ] Run smoke tests in production
- [ ] Monitor logs for errors
- [ ] Verify metrics are healthy

**Deployment verification:**

```bash
# Check health endpoint
curl https://api.example.com/health

# Check version endpoint
curl https://api.example.com/version

# Monitor logs
# (consult deployment docs for log access)
```

### 15. Post-Release Verification

**Immediately after release:**
- [ ] Application is running
- [ ] No critical errors in logs
- [ ] Metrics are normal
- [ ] Users can access the application
- [ ] Core features work

**Monitor for:**
- [ ] Error rates
- [ ] Response times
- [ ] Resource usage (CPU, memory, disk)
- [ ] User feedback
- [ ] Support tickets

### 16. Publish Release

**Publish release notes:**
- [ ] Create GitHub/GitLab release
- [ ] Publish to package registry (npm, PyPI, crates.io, etc.)
- [ ] Update documentation site
- [ ] Announce on blog/social media (if applicable)
- [ ] Notify users via email/newsletter (if applicable)

### 17. Post-Release Tasks

**After successful release:**
- [ ] Close release milestone
- [ ] Update project board
- [ ] Archive release branch (if used)
- [ ] Document lessons learned
- [ ] Plan next release

**If issues occur:**
- [ ] Triage issues immediately
- [ ] Prepare hotfix if needed
- [ ] Communicate with users
- [ ] Execute rollback if necessary

## Rollback Plan

If the release has critical issues:

### 1. Assess the Situation

- [ ] Identify the issue
- [ ] Determine severity
- [ ] Decide: fix forward or rollback?

### 2. Execute Rollback

```bash
# Consult deployment docs for rollback procedure
# Example: redeploy previous version
```

- [ ] Rollback application
- [ ] Rollback database (if needed and possible)
- [ ] Verify rollback succeeded
- [ ] Notify stakeholders

### 3. Post-Rollback

- [ ] Investigate root cause
- [ ] Fix the issue
- [ ] Test thoroughly
- [ ] Plan re-release

## Quick Checklist

Use this for a final verification:

### Pre-Release
- [ ] All PRs merged
- [ ] All tests pass
- [ ] All quality checks pass
- [ ] Security scan clean
- [ ] Version bumped
- [ ] Changelog updated
- [ ] Documentation updated
- [ ] Staging tested

### Release
- [ ] Release branch/tag created
- [ ] Release notes written
- [ ] CI/CD passes
- [ ] Stakeholders notified
- [ ] Backup created
- [ ] Deployed to production
- [ ] Smoke tests pass

### Post-Release
- [ ] Application healthy
- [ ] Metrics normal
- [ ] Release published
- [ ] Users notified
- [ ] Monitoring active

## Notes

* This is a generic workflow. Adapt to your project's specific requirements.
* Always consult AGENTS.md for project-specific commands and procedures.
* Have a rollback plan ready before releasing.
* Monitor closely after release.
