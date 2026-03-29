---
name: python-precommit-repair
description: Systematic approach to resolving pre-commit hook failures in Python projects
metadata:
  when_to_use: When pre-commit hooks fail locally or in CI
  tags: python, pre-commit, git-hooks, quality
  language: python
---

# Python Pre-commit Repair Skill

## Purpose

This skill provides a systematic approach to resolving pre-commit hook failures while maintaining code quality and commit hygiene.

## When to Invoke This Skill

Use this skill when:
* Pre-commit hooks fail locally before commit
* Pre-commit CI check fails
* Setting up pre-commit in a Python project
* Resolving hook failures after dependency updates

## When NOT to Invoke This Skill

Do not use this skill for:
* Non-Python projects (unless they use pre-commit)
* Projects not using pre-commit (check AGENTS.md)
* General linting/type checking (use specific skills)

## Prerequisites

Before fixing pre-commit issues:
1. **Consult AGENTS.md** for pre-commit configuration and commands
2. **Have pre-commit installed**: Verify with `pre-commit --version`
3. **Hooks are installed**: Run `pre-commit install` if needed

## Pre-commit Repair Process

### Phase 1: Understand Pre-commit Failure

1. **Read the failure output**
   * Pre-commit shows which hook failed
   * Each hook has a specific purpose
   * Errors are usually clear and actionable

2. **Identify the failing hook**
   * Check `.pre-commit-config.yaml` for hook configuration
   * Common hooks:
     * `trailing-whitespace`: Remove trailing whitespace
     * `end-of-file-fixer`: Ensure files end with newline
     * `check-yaml`: Validate YAML syntax
     * `check-added-large-files`: Prevent committing large files
     * `ruff`: Linting and formatting
     * `mypy`: Type checking
     * `pytest`: Run tests

3. **Consult AGENTS.md**
   * Check for project-specific pre-commit configuration
   * Check for pre-commit commands
   * Check for hook-specific policies

### Phase 2: Run Pre-commit Manually

1. **Run all hooks**
   * Consult AGENTS.md for command
   * Common: `pre-commit run --all-files`

2. **Run specific hook**
   * `pre-commit run <hook-id>`
   * Example: `pre-commit run ruff`

3. **Run on specific files**
   * `pre-commit run --files path/to/file.py`

### Phase 3: Fix Common Pre-commit Issues

#### Hook 1: trailing-whitespace

**Error:**
```
Trim Trailing Whitespace.................................................Failed
- hook id: trailing-whitespace
- exit code: 1
- files were modified by this hook

Fixing src/user.py
```

**Solution:**
* Auto-fixed by the hook
* Review changes and re-stage: `git add src/user.py`
* Re-run pre-commit

#### Hook 2: end-of-file-fixer

**Error:**
```
Fix End of Files.........................................................Failed
- hook id: end-of-file-fixer
- exit code: 1
- files were modified by this hook

Fixing src/user.py
```

**Solution:**
* Auto-fixed by the hook
* Review changes and re-stage: `git add src/user.py`
* Re-run pre-commit

#### Hook 3: check-yaml

**Error:**
```
Check Yaml...............................................................Failed
- hook id: check-yaml
- exit code: 1

config.yaml: syntax error
```

**Solution:**
* Fix YAML syntax errors
* Common issues: incorrect indentation, missing colons, invalid characters
* Validate with a YAML linter

#### Hook 4: check-added-large-files

**Error:**
```
Check for added large files..............................................Failed
- hook id: check-added-large-files
- exit code: 1

data/large_file.csv (5.2 MB) exceeds 500 KB
```

**Solution:**
* Do not commit large files
* Add to `.gitignore`
* Use Git LFS if necessary
* Store large files elsewhere (S3, external storage)

#### Hook 5: ruff (linting)

**Error:**
```
ruff.....................................................................Failed
- hook id: ruff
- exit code: 1

src/user.py:10:1: F401 'os' imported but unused
```

**Solution:**
* Use `python-ruff-fixing` skill
* Or run: `ruff check --fix .`
* Re-stage files and re-run pre-commit

#### Hook 6: ruff-format

**Error:**
```
ruff-format..............................................................Failed
- hook id: ruff-format
- exit code: 1
- files were modified by this hook

1 file reformatted
```

**Solution:**
* Auto-fixed by the hook
* Review changes and re-stage: `git add src/user.py`
* Re-run pre-commit

#### Hook 7: mypy (type checking)

**Error:**
```
mypy.....................................................................Failed
- hook id: mypy
- exit code: 1

src/user.py:45: error: Argument 1 has incompatible type "str"; expected "int"
```

**Solution:**
* Use `python-mypy-debugging` skill
* Fix type errors
* Re-stage files and re-run pre-commit

#### Hook 8: pytest (tests)

**Error:**
```
pytest...................................................................Failed
- hook id: pytest
- exit code: 1

tests/test_user.py::test_user_creation FAILED
```

**Solution:**
* Fix failing tests
* Use `ci-failure-triage` skill if needed
* Ensure all tests pass before committing

#### Hook 9: check-merge-conflict

**Error:**
```
Check for merge conflicts................................................Failed
- hook id: check-merge-conflict
- exit code: 1

src/user.py:45: Merge conflict marker detected
```

**Solution:**
* Resolve merge conflicts
* Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
* Complete the merge properly

#### Hook 10: check-case-conflict

**Error:**
```
Check for case conflicts.................................................Failed
- hook id: check-case-conflict
- exit code: 1

Both 'User.py' and 'user.py' exist
```

**Solution:**
* Rename one of the files
* Avoid case-only differences in filenames
* Use consistent naming conventions

### Phase 4: Handle Auto-fixing Hooks

Many hooks auto-fix issues:

1. **Review auto-fix changes**
   * Use `git diff` to see what changed
   * Ensure changes are correct

2. **Re-stage modified files**
   * `git add <file>`
   * Or `git add -u` to stage all modified tracked files

3. **Re-run pre-commit**
   * `pre-commit run --all-files`
   * Or attempt commit again

### Phase 5: Skip Hooks When Necessary

**Only skip hooks when absolutely necessary.**

#### Skip all hooks for one commit

```bash
git commit --no-verify -m "Emergency fix"
```

#### Skip specific hook

Not directly supported, but you can:
1. Temporarily comment out the hook in `.pre-commit-config.yaml`
2. Commit
3. Restore the hook configuration

**Consult AGENTS.md for project policy on skipping hooks.**

### Phase 6: Update Pre-commit Hooks

If hooks are outdated:

1. **Update to latest versions**
   * `pre-commit autoupdate`

2. **Review changes**
   * Check what changed in `.pre-commit-config.yaml`
   * Test hooks still work

3. **Commit hook updates separately**
   * `chore: update pre-commit hooks`

### Phase 7: Verify and Commit

1. **Ensure all hooks pass**
   * `pre-commit run --all-files`
   * All hooks should show "Passed"

2. **Commit changes**
   * `git commit -m "your message"`
   * Pre-commit will run automatically

3. **If hooks fail again**
   * Review the failure
   * Fix the issue
   * Repeat until all hooks pass

## Do Not Assume

* **Do not assume** pre-commit configuration without checking AGENTS.md
* **Do not assume** which hooks are enabled
* **Do not assume** hook-specific settings
* **Do not assume** policy on skipping hooks

**Always consult AGENTS.md first.**

## Pre-commit Configuration

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

Consult AGENTS.md for project-specific configuration.

## Troubleshooting Pre-commit

### Issue: Hooks not running

**Solution:**
* Ensure hooks are installed: `pre-commit install`
* Check `.git/hooks/pre-commit` exists

### Issue: Hooks running on wrong files

**Solution:**
* Check `files` pattern in `.pre-commit-config.yaml`
* Use `--files` flag to test specific files

### Issue: Hooks taking too long

**Solution:**
* Use `stages: [manual]` for slow hooks
* Run manually: `pre-commit run <hook-id> --all-files`
* Optimize hook configuration

### Issue: Hook fails in CI but not locally

**Solution:**
* Check environment differences (Python version, dependencies)
* Run `pre-commit run --all-files` locally
* Check CI logs for specific errors

## Validation Checklist

Before considering pre-commit issues fixed:

- [ ] All pre-commit hooks pass
- [ ] Auto-fixed files reviewed and re-staged
- [ ] All tests still pass
- [ ] Runtime behavior preserved
- [ ] Commit message follows conventions
- [ ] No hooks skipped without justification

## Integration with Other Skills

* **For Ruff issues**: Use `python-ruff-fixing` skill
* **For MyPy issues**: Use `python-mypy-debugging` skill
* **For test failures**: Use `ci-failure-triage` skill
* **For CI failures**: Use `ci-failure-triage` skill

## Example Workflow

```
1. Attempt to commit: `git commit -m "feat: add user authentication"`

2. Pre-commit runs and fails:
   - trailing-whitespace: Fixed
   - ruff: Failed (unused imports)
   - mypy: Failed (type errors)

3. Review auto-fixes:
   - `git diff` shows trailing whitespace removed
   - Re-stage: `git add -u`

4. Fix Ruff issues:
   - Run: `ruff check --fix .`
   - Remove unused imports
   - Re-stage: `git add src/auth/service.py`

5. Fix MyPy issues:
   - Add type annotations
   - Fix type errors
   - Re-stage: `git add src/auth/service.py`

6. Re-run pre-commit:
   - `pre-commit run --all-files`
   - All hooks pass ✓

7. Commit:
   - `git commit -m "feat: add user authentication"`
   - Pre-commit runs and passes ✓
```

## Notes

* This is a Python-focused skill but pre-commit works with any language.
* Always consult AGENTS.md for project-specific pre-commit configuration.
* Pre-commit hooks enforce quality before code is committed.
* When in doubt, ask the user for clarification.
