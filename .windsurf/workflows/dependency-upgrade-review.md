---
description: Dependency upgrade review and testing procedure
---

# Dependency Upgrade Review Workflow

This workflow ensures dependency upgrades are safe, tested, and do not introduce regressions.

## When to Use

Run this workflow when:
* Upgrading dependencies (major, minor, or patch)
* Responding to security advisories
* Performing regular dependency maintenance
* Reviewing automated dependency update PRs (Dependabot, Renovate, etc.)

## Prerequisites

* Understand which dependencies are being upgraded
* Have access to dependency changelogs and release notes

## Workflow Steps

### 1. Review the Dependency Update

**Identify what's changing:**

```bash
# View dependency changes
# Python: check pyproject.toml or requirements.txt
# JavaScript: check package.json
# Rust: check Cargo.toml

# View lock file changes
git diff main -- package-lock.json
git diff main -- Cargo.lock
git diff main -- uv.lock
```

**For each dependency:**
- [ ] Note current version
- [ ] Note new version
- [ ] Identify version change type (major, minor, patch)
- [ ] Check if it's a direct or transitive dependency

### 2. Read Release Notes and Changelogs

**For each upgraded dependency:**

```bash
# Find release notes
# Usually at: https://github.com/owner/repo/releases
# Or: https://github.com/owner/repo/blob/main/CHANGELOG.md
```

**Review for:**
- [ ] New features
- [ ] Bug fixes
- [ ] Breaking changes
- [ ] Deprecations
- [ ] Security fixes
- [ ] Performance improvements
- [ ] Migration guides

**Pay special attention to:**
* **Major version changes**: Likely breaking changes
* **Security updates**: Understand the vulnerability
* **Deprecations**: Plan for future updates

### 3. Assess Breaking Changes

**If there are breaking changes:**

1. **Read the migration guide**
   - [ ] Understand what changed
   - [ ] Identify affected code
   - [ ] Plan necessary updates

2. **Search codebase for usage**

```bash
# Search for dependency usage
# Example: grep -r "import old_function" src/
# Or use IDE's "Find in Files"
```

- [ ] Identify all usage locations
- [ ] Assess impact of changes
- [ ] Plan code updates

3. **Update code if needed**
   - [ ] Make necessary changes
   - [ ] Follow migration guide
   - [ ] Test thoroughly

### 4. Check for Security Vulnerabilities

**Review security advisories:**

```bash
# Python
pip-audit
# Or: safety check

# JavaScript
npm audit
# Or: yarn audit

# Rust
cargo audit
```

**For each vulnerability:**
- [ ] Understand the vulnerability (CVE, severity)
- [ ] Check if your code is affected
- [ ] Verify the upgrade fixes it
- [ ] Document the fix

### 5. Update Dependencies

Consult AGENTS.md for dependency update commands.

**Update lock file:**

```bash
# Python with uv
uv sync

# Python with poetry
poetry update

# JavaScript with npm
npm install

# JavaScript with pnpm
pnpm install

# Rust
cargo update
```

**Verify lock file changes:**
- [ ] Only expected dependencies changed
- [ ] No unexpected version jumps
- [ ] Transitive dependencies are reasonable

### 6. Run Full Test Suite

Consult AGENTS.md for test commands.

```bash
# Run all tests
# Python: uv run pytest
# JavaScript: npm test
# Rust: cargo test
```

**Verify:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass (if applicable)
- [ ] No new test failures
- [ ] No flaky tests introduced

**If tests fail:**
* Investigate the failure
* Determine if it's due to the dependency update
* Fix the issue or revert the update

### 7. Run Code Quality Checks

#### Linting

```bash
# Consult AGENTS.md for lint command
```

- [ ] No new linting errors
- [ ] No new warnings (or acceptable)

#### Type Checking

```bash
# Consult AGENTS.md for type check command
```

- [ ] No new type errors
- [ ] Type definitions are compatible

#### Formatting

```bash
# Consult AGENTS.md for format command
```

- [ ] Code is properly formatted
- [ ] No formatting conflicts

### 8. Check for API Changes

**If the dependency is a library you use extensively:**

1. **Review API documentation**
   - [ ] Check for deprecated APIs
   - [ ] Check for removed APIs
   - [ ] Check for new recommended patterns

2. **Test critical paths**
   - [ ] Test main use cases
   - [ ] Test edge cases
   - [ ] Verify behavior is unchanged

3. **Check performance**
   - [ ] Run benchmarks (if available)
   - [ ] Check for performance regressions
   - [ ] Monitor resource usage

### 9. Test in Development Environment

**Manual testing:**
- [ ] Application starts successfully
- [ ] Core features work
- [ ] No errors in logs
- [ ] No console warnings
- [ ] Performance is acceptable

**Test critical user flows:**
- [ ] Authentication
- [ ] Data creation/modification
- [ ] API calls
- [ ] File uploads/downloads
- [ ] Any dependency-specific features

### 10. Review Transitive Dependencies

**Check what else changed:**

```bash
# View all dependency changes
# Python: uv tree or pip list
# JavaScript: npm list or pnpm list
# Rust: cargo tree
```

**Verify:**
- [ ] Transitive updates are reasonable
- [ ] No unexpected major version jumps
- [ ] No known vulnerable versions introduced

### 11. Check Build Size Impact

**For frontend dependencies:**

```bash
# Check bundle size
# JavaScript: npm run build && ls -lh dist/
# Or use bundle analyzer
```

- [ ] Bundle size increase is acceptable
- [ ] No unexpected large dependencies added
- [ ] Tree shaking still works

### 12. Test in Staging Environment

If applicable, deploy to staging:

```bash
# Consult deployment docs for staging deployment
```

**Verify in staging:**
- [ ] Application deploys successfully
- [ ] All services are healthy
- [ ] Critical flows work
- [ ] No errors in logs
- [ ] Performance is acceptable

### 13. Document the Update

**Update documentation if needed:**
- [ ] Update README (if dependency requirements changed)
- [ ] Update installation instructions
- [ ] Update configuration examples
- [ ] Document breaking changes
- [ ] Update troubleshooting guide

**Create or update CHANGELOG:**

```markdown
## [Unreleased]

### Changed
- Updated dependency-name from 1.0.0 to 2.0.0
  - Includes security fix for CVE-2024-1234
  - Breaking change: API method renamed (see migration guide)
```

### 14. Commit the Update

**Commit message format:**

```bash
# For single dependency
git commit -m "chore: upgrade dependency-name from 1.0.0 to 2.0.0"

# For security fix
git commit -m "security: upgrade dependency-name to fix CVE-2024-1234"

# For multiple dependencies
git commit -m "chore: upgrade dependencies"
```

**Include in commit message:**
- [ ] What was upgraded
- [ ] Why (security, features, bug fixes)
- [ ] Any breaking changes
- [ ] Reference to issue or security advisory

### 15. Create Pull Request

**PR title:**
* `chore: upgrade dependency-name to 2.0.0`
* `security: upgrade dependency-name to fix CVE-2024-1234`

**PR description:**

```markdown
## What changed
- Upgraded dependency-name from 1.0.0 to 2.0.0

## Why
- Security fix for CVE-2024-1234 (severity: high)
- Includes bug fixes and performance improvements

## Breaking changes
- API method `oldMethod()` renamed to `newMethod()`
- Updated all usage in codebase

## Testing
- [x] All tests pass
- [x] Manual testing completed
- [x] Tested in staging
- [x] No regressions found

## Release notes
[Link to dependency release notes]

## Related issues
Fixes #123
```

### 16. Monitor After Merge

**After the update is merged and deployed:**
- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Watch for user reports
- [ ] Check logs for warnings
- [ ] Verify no regressions in production

## Special Cases

### Major Version Upgrades

For major version changes:

1. **Read migration guide thoroughly**
2. **Test extensively**
3. **Consider gradual rollout**
4. **Have rollback plan ready**
5. **Monitor closely after deployment**

### Security Updates

For security fixes:

1. **Prioritize urgently**
2. **Understand the vulnerability**
3. **Test quickly but thoroughly**
4. **Deploy as soon as safe**
5. **Document the fix**

### Multiple Dependencies

When updating many dependencies:

1. **Group by risk level**
   - Low risk: patch updates, no breaking changes
   - Medium risk: minor updates, some changes
   - High risk: major updates, breaking changes

2. **Update in batches**
   - Update low-risk dependencies together
   - Update high-risk dependencies separately

3. **Test between batches**

### Automated Dependency Updates

For Dependabot/Renovate PRs:

1. **Review the PR description**
2. **Check release notes (linked in PR)**
3. **Verify CI passes**
4. **Review code changes (if any)**
5. **Merge if safe, or request changes**

## Risk Assessment

**Low Risk (safe to merge quickly):**
* Patch version updates (1.0.0 → 1.0.1)
* No breaking changes
* All tests pass
* No security implications

**Medium Risk (review carefully):**
* Minor version updates (1.0.0 → 1.1.0)
* New features added
* Deprecations introduced
* Some API changes

**High Risk (extensive testing required):**
* Major version updates (1.0.0 → 2.0.0)
* Breaking changes
* Significant refactoring needed
* Core dependency

## Rollback Plan

If issues are discovered after deployment:

1. **Revert the dependency update**

```bash
git revert <commit-hash>
```

2. **Reinstall old dependencies**

```bash
# Consult AGENTS.md for install command
```

3. **Deploy the rollback**
4. **Investigate the issue**
5. **Plan a proper fix**

## Quick Checklist

### Pre-Update
- [ ] Read release notes
- [ ] Identify breaking changes
- [ ] Check security advisories
- [ ] Plan code updates

### Update
- [ ] Update dependencies
- [ ] Update lock file
- [ ] Update code (if needed)
- [ ] Run all tests
- [ ] Run quality checks

### Verification
- [ ] Manual testing
- [ ] Staging testing
- [ ] Performance check
- [ ] Bundle size check

### Documentation
- [ ] Update docs
- [ ] Update changelog
- [ ] Clear commit message
- [ ] Complete PR description

### Post-Update
- [ ] Monitor production
- [ ] Watch for issues
- [ ] Verify no regressions

## Notes

* This is a generic workflow. Adapt to your project's specific requirements.
* Always consult AGENTS.md for project-specific commands.
* Be more cautious with major version updates.
* Security updates should be prioritized but still tested.
