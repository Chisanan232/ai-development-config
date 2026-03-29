---
name: python-ruff-fixing
description: Systematic approach to resolving Ruff linting and formatting issues in Python
metadata:
  when_to_use: When Ruff linting or formatting checks fail in Python projects
  tags: python, ruff, linting, formatting
  language: python
---

# Python Ruff Fixing Skill

## Purpose

This skill provides a systematic approach to resolving Ruff linting and formatting issues while maintaining code quality and consistency.

## When to Invoke This Skill

Use this skill when:
* Ruff linting fails locally or in CI
* Ruff formatting checks fail
* Adding Ruff to an existing Python project
* Resolving linting violations after code changes

## When NOT to Invoke This Skill

Do not use this skill for:
* Non-Python projects
* Projects not using Ruff (check AGENTS.md)
* Type checking errors (use `python-mypy-debugging` skill)

## Prerequisites

Before fixing Ruff issues:
1. **Consult AGENTS.md** for Ruff configuration and commands
2. **Have Ruff installed**: Verify with `ruff --version`
3. **Understand Ruff rules**: Check `pyproject.toml` or `ruff.toml` for enabled rules

## Ruff Fixing Process

### Phase 1: Run Ruff and Identify Issues

1. **Run Ruff check**
   * Consult AGENTS.md for Ruff command
   * Common: `ruff check .` or `ruff check src/`
   * For specific file: `ruff check path/to/file.py`

2. **Run Ruff format check** (if applicable)
   * Common: `ruff format --check .`
   * Or: `ruff format --diff .` to see changes

3. **Read the output**
   * Ruff provides file, line, column, rule code, and description
   * Example: `src/user.py:45:10: F401 [*] 'os' imported but unused`

4. **Understand rule codes**
   * F = Pyflakes errors
   * E/W = pycodestyle errors/warnings
   * I = isort import sorting
   * N = pep8-naming
   * UP = pyupgrade
   * And many more...

### Phase 2: Use Auto-Fix When Possible

Ruff can automatically fix many issues:

1. **Run auto-fix**
   * Consult AGENTS.md for auto-fix command
   * Common: `ruff check --fix .`
   * Preview changes: `ruff check --fix --diff .`

2. **Review auto-fix changes**
   * Always review what Ruff changed
   * Ensure changes are correct
   * Run tests after auto-fix

3. **Commit auto-fix separately** (if significant)
   * `fix: apply ruff auto-fix to codebase`

### Phase 3: Fix Issues Manually

For issues that cannot be auto-fixed:

#### Common Ruff Issues and Solutions

#### Issue 1: Unused Imports (F401)

**Error:**
```
src/user.py:1:1: F401 [*] 'os' imported but unused
```

**Solution:**
```python
# Before
import os
import sys

def main():
    print(sys.version)

# After
import sys

def main():
    print(sys.version)
```

#### Issue 2: Undefined Name (F821)

**Error:**
```
src/user.py:10:5: F821 Undefined name 'user'
```

**Solution:**
```python
# Before
def get_user_name():
    return user.name  # 'user' is not defined

# After
def get_user_name(user: User):
    return user.name
```

#### Issue 3: Line Too Long (E501)

**Error:**
```
src/user.py:15:80: E501 Line too long (95 > 88 characters)
```

**Solution:**
```python
# Before
def process_user_data(user_id, user_name, user_email, user_phone, user_address):
    ...

# After
def process_user_data(
    user_id,
    user_name,
    user_email,
    user_phone,
    user_address,
):
    ...
```

#### Issue 4: Incorrect Import Order (I001)

**Error:**
```
src/user.py:1:1: I001 Import block is un-sorted or un-formatted
```

**Solution:**
```python
# Before
from myapp.models import User
import sys
from typing import Optional
import os

# After (auto-fixable)
import os
import sys
from typing import Optional

from myapp.models import User
```

#### Issue 5: Bare Except (E722)

**Error:**
```
src/user.py:20:1: E722 Do not use bare 'except'
```

**Solution:**
```python
# Before
try:
    result = risky_operation()
except:  # Too broad
    handle_error()

# After - Option 1: Specific exception
try:
    result = risky_operation()
except ValueError:
    handle_error()

# After - Option 2: Catch all but explicit
try:
    result = risky_operation()
except Exception as e:
    handle_error(e)
```

#### Issue 6: Mutable Default Argument (B006)

**Error:**
```
src/user.py:5:20: B006 Do not use mutable data structures for argument defaults
```

**Solution:**
```python
# Before
def add_item(item, items=[]):  # Dangerous!
    items.append(item)
    return items

# After
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

#### Issue 7: Use of `type()` for Type Comparison (E721)

**Error:**
```
src/user.py:10:5: E721 Do not compare types, use 'isinstance()'
```

**Solution:**
```python
# Before
if type(value) == int:
    process_int(value)

# After
if isinstance(value, int):
    process_int(value)
```

#### Issue 8: Unused Variable (F841)

**Error:**
```
src/user.py:15:5: F841 Local variable 'result' is assigned to but never used
```

**Solution:**
```python
# Before
def process_data(data):
    result = expensive_computation(data)
    return data  # 'result' is unused

# After - Option 1: Use the variable
def process_data(data):
    result = expensive_computation(data)
    return result

# After - Option 2: Prefix with underscore if intentionally unused
def process_data(data):
    _result = expensive_computation(data)  # Intentionally unused
    return data
```

#### Issue 9: Use of `assert` for Runtime Checks (S101)

**Error:**
```
src/user.py:10:5: S101 Use of 'assert' detected
```

**Solution:**
```python
# Before
def process_user(user):
    assert user is not None  # Assertions can be disabled with -O

# After
def process_user(user):
    if user is None:
        raise ValueError("User cannot be None")
```

#### Issue 10: f-string Without Placeholders (F541)

**Error:**
```
src/user.py:5:12: F541 f-string without any placeholders
```

**Solution:**
```python
# Before
message = f"Hello, world!"  # No placeholders

# After
message = "Hello, world!"
```

### Phase 4: Handle Formatting Issues

1. **Run Ruff format**
   * Consult AGENTS.md for format command
   * Common: `ruff format .`

2. **Review formatting changes**
   * Ruff format is opinionated
   * Changes should be automatic and consistent

3. **Commit formatting separately**
   * `style: apply ruff formatting`

### Phase 5: Disable Rules When Necessary

**Only disable rules when absolutely necessary.**

#### Per-line Disable

```python
# Disable specific rule
result = eval(user_input)  # noqa: S307

# Disable all rules (avoid)
result = eval(user_input)  # noqa
```

#### Per-file Disable

```python
# At top of file
# ruff: noqa: E501
```

#### Project-wide Disable

In `pyproject.toml`:
```toml
[tool.ruff]
ignore = ["E501"]  # Ignore line length
```

**Consult AGENTS.md for project-specific rule configuration.**

### Phase 6: Verify the Fix

1. **Run Ruff again**
   * Ensure all issues are resolved
   * Check for new issues introduced

2. **Run tests**
   * Ensure runtime behavior is preserved
   * Linting fixes should not break tests

3. **Run other quality checks**
   * MyPy (if used)
   * Tests
   * Pre-commit hooks

### Phase 7: Commit Ruff Fixes

1. **Commit fixes by category**
   * Group related fixes together
   * Clear commit messages

**Examples:**
* `fix: remove unused imports`
* `fix: correct import order with ruff`
* `style: apply ruff formatting`
* `fix: resolve ruff linting violations in user module`

2. **Separate auto-fix from manual fixes**
   * Auto-fix in one commit
   * Manual fixes in separate commits

## Do Not Assume

* **Do not assume** Ruff configuration without checking AGENTS.md
* **Do not assume** which rules are enabled
* **Do not assume** line length limit
* **Do not assume** project's rule suppression policy

**Always consult AGENTS.md first.**

## Ruff Configuration

Common Ruff config (in `pyproject.toml`):

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "B", "S"]
ignore = ["E501"]  # Ignore line length

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S101"]  # Allow assert in tests
```

Consult AGENTS.md for project-specific configuration.

## Rule Suppression Policy

**When to use `# noqa`:**
* False positive (rare with Ruff)
* Intentional violation with good reason
* Legacy code that cannot be changed

**How to use it:**
```python
# Specific rule (preferred)
result = eval(user_input)  # noqa: S307

# With explanation (always)
result = eval(user_input)  # noqa: S307  # Safe: input is validated
```

**Consult AGENTS.md for project-specific suppression policy.**

## Validation Checklist

Before considering Ruff issues fixed:

- [ ] All Ruff check errors resolved
- [ ] Ruff format applied (if required)
- [ ] All tests still pass
- [ ] Runtime behavior preserved
- [ ] Rule suppressions minimized and documented
- [ ] Commit message follows conventions

## Integration with Other Skills

* **For CI failures**: Use `ci-failure-triage` skill
* **For type errors**: Use `python-mypy-debugging` skill
* **For pre-commit failures**: Use `python-precommit-repair` skill

## Example Workflow

```
1. CI fails: "Ruff linting failed"

2. Run Ruff locally:
   - Consult AGENTS.md: `ruff check src/`
   - Output: 12 errors in src/auth/service.py

3. Run auto-fix:
   - `ruff check --fix src/`
   - 8 errors auto-fixed

4. Review remaining errors:
   - Line 45: F821 Undefined name 'user_id'
   - Line 67: E722 Bare except
   - Line 89: B006 Mutable default argument
   - Line 102: E501 Line too long

5. Fix manually:
   - Line 45: Add user_id parameter
   - Line 67: Change to `except Exception:`
   - Line 89: Use `items=None` with None check
   - Line 102: Break line into multiple lines

6. Verify:
   - Run Ruff: All errors resolved ✓
   - Run tests: All pass ✓

7. Commit:
   - "fix: apply ruff auto-fix"
   - "fix: resolve remaining ruff violations in auth service"

8. Push and verify:
   - CI passes ✓
```

## Notes

* This is a Python-specific skill for Ruff.
* Always consult AGENTS.md for project-specific Ruff configuration.
* Ruff is fast and comprehensive - use it to maintain code quality.
* When in doubt, ask the user for clarification.
