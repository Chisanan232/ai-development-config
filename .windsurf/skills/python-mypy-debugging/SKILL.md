---
name: python-mypy-debugging
description: Systematic approach to resolving MyPy type checking errors in Python
when_to_use: When MyPy type checking fails in Python projects
tags: [python, mypy, type-checking, debugging]
language: python
---

# Python MyPy Debugging Skill

## Purpose

This skill provides a systematic approach to resolving MyPy type checking errors while maintaining type safety and code quality.

## When to Invoke This Skill

Use this skill when:
* MyPy type checking fails locally or in CI
* Adding type hints to existing code
* Resolving type errors after dependency updates
* Improving type coverage in Python code

## When NOT to Invoke This Skill

Do not use this skill for:
* Non-Python projects
* Runtime errors (those are different from type errors)
* Projects not using MyPy (check AGENTS.md)

## Prerequisites

Before debugging MyPy errors:
1. **Consult AGENTS.md** for MyPy configuration and commands
2. **Understand MyPy basics**: Types, generics, protocols, type narrowing
3. **Have MyPy installed**: Verify with `mypy --version`

## MyPy Debugging Process

### Phase 1: Run MyPy and Identify Errors

1. **Run MyPy**
   * Consult AGENTS.md for MyPy command
   * Common: `mypy .` or `mypy src/`
   * Check for specific config: `mypy --config-file pyproject.toml`

2. **Read the error output**
   * MyPy provides file, line number, and error description
   * Example: `src/user.py:45: error: Argument 1 has incompatible type "str"; expected "int"`

3. **Categorize the errors**
   * Missing type annotations
   * Type incompatibility
   * Missing imports or stubs
   * Incorrect type narrowing
   * Generic type issues
   * Optional/None handling

### Phase 2: Understand Common MyPy Error Patterns

#### Pattern 1: Missing Type Annotations

**Error:**
```
error: Function is missing a type annotation
```

**Solution:**
```python
# Before
def calculate_total(items):
    return sum(item.price for item in items)

# After
from typing import List
def calculate_total(items: List[Item]) -> float:
    return sum(item.price for item in items)
```

#### Pattern 2: Incompatible Types

**Error:**
```
error: Argument 1 has incompatible type "str"; expected "int"
```

**Solution:**
```python
# Before
user_id: int = "123"  # Wrong!

# After
user_id: int = 123  # Correct
# Or if you need to convert:
user_id: int = int("123")
```

#### Pattern 3: Optional/None Handling

**Error:**
```
error: Item "None" of "Optional[User]" has no attribute "name"
```

**Solution:**
```python
# Before
def get_user_name(user: Optional[User]) -> str:
    return user.name  # Error: user might be None

# After - Option 1: Guard clause
def get_user_name(user: Optional[User]) -> str:
    if user is None:
        return "Unknown"
    return user.name

# After - Option 2: Assert
def get_user_name(user: Optional[User]) -> str:
    assert user is not None
    return user.name

# After - Option 3: Return Optional
def get_user_name(user: Optional[User]) -> Optional[str]:
    return user.name if user is not None else None
```

#### Pattern 4: List/Dict Type Annotations

**Error:**
```
error: Need type annotation for "items" (hint: "items: List[<type>] = ...")
```

**Solution:**
```python
# Before
items = []  # MyPy doesn't know the type

# After
from typing import List
items: List[str] = []
# Or with Python 3.9+
items: list[str] = []
```

#### Pattern 5: Return Type Mismatch

**Error:**
```
error: Incompatible return value type (got "None", expected "User")
```

**Solution:**
```python
# Before
def find_user(user_id: int) -> User:
    user = database.get(user_id)
    if user is None:
        return None  # Error: should return User, not None

# After - Option 1: Raise exception
def find_user(user_id: int) -> User:
    user = database.get(user_id)
    if user is None:
        raise ValueError(f"User {user_id} not found")
    return user

# After - Option 2: Return Optional
def find_user(user_id: int) -> Optional[User]:
    return database.get(user_id)
```

#### Pattern 6: Any Type Issues

**Error:**
```
error: Returning Any from function declared to return "User"
```

**Solution:**
```python
# Before
def get_user(data: dict) -> User:
    return data.get("user")  # Returns Any

# After
def get_user(data: dict) -> User:
    user = data.get("user")
    if not isinstance(user, User):
        raise TypeError("Invalid user data")
    return user
```

### Phase 3: Fix MyPy Errors Safely

1. **Fix errors one at a time**
   * Start with the first error
   * Fix it completely
   * Re-run MyPy
   * Move to the next error

2. **Preserve runtime behavior**
   * Type annotations should not change behavior
   * Do not add logic just to satisfy MyPy
   * If behavior must change, do it intentionally

3. **Use appropriate type hints**
   * `Optional[T]` for values that can be None
   * `Union[T1, T2]` for values that can be multiple types
   * `List[T]`, `Dict[K, V]`, `Set[T]` for collections
   * `Callable[[Args], Return]` for functions
   * `Protocol` for structural typing

4. **Avoid type: ignore unless necessary**
   * Try to fix the type error properly first
   * Use `# type: ignore` only as a last resort
   * Always add a comment explaining why

### Phase 4: Handle Difficult Cases

#### Case 1: Third-Party Libraries Without Stubs

**Problem:** Library has no type stubs

**Solutions:**

1. **Install type stubs if available:**
```bash
pip install types-requests  # For requests library
pip install types-redis     # For redis library
```

2. **Create local stub file:**
```python
# stubs/external_lib.pyi
def some_function(x: int) -> str: ...
```

3. **Use type: ignore with comment:**
```python
from external_lib import some_function  # type: ignore[import]
```

#### Case 2: Dynamic Code

**Problem:** Code uses dynamic attributes or `getattr`

**Solutions:**

1. **Use Protocol for structural typing:**
```python
from typing import Protocol

class HasName(Protocol):
    name: str

def get_name(obj: HasName) -> str:
    return obj.name
```

2. **Use TypedDict for dictionaries:**
```python
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str
    email: str

def process_user(user: UserDict) -> None:
    print(user["name"])
```

3. **Use cast for unavoidable cases:**
```python
from typing import cast

result = some_dynamic_function()
typed_result = cast(User, result)
```

#### Case 3: Complex Generics

**Problem:** Generic types are complex

**Solutions:**

1. **Use TypeVar:**
```python
from typing import TypeVar, List

T = TypeVar('T')

def first(items: List[T]) -> T:
    return items[0]
```

2. **Use Generic classes:**
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Container(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    
    def get(self) -> T:
        return self.value
```

### Phase 5: Verify the Fix

1. **Run MyPy again**
   * Ensure the error is fixed
   * Check for new errors introduced

2. **Run tests**
   * Ensure runtime behavior is preserved
   * No tests should break due to type annotations

3. **Check for regressions**
   * Ensure no new MyPy errors elsewhere
   * Verify related code still type-checks

### Phase 6: Commit Type Fixes

1. **Commit type fixes separately**
   * Separate from feature work
   * Clear commit message

**Examples:**
* `fix: resolve mypy type errors in user module`
* `fix: add type annotations to auth service`
* `fix: correct return type for data processing functions`

2. **Group related fixes**
   * Fix all errors in one module together
   * Or fix all errors of one type together

## Do Not Assume

* **Do not assume** MyPy configuration without checking AGENTS.md
* **Do not assume** MyPy version or strictness level
* **Do not assume** which type stubs are installed
* **Do not assume** project's type suppression policy

**Always consult AGENTS.md first.**

## MyPy Configuration Tips

Common MyPy config options (in `pyproject.toml` or `mypy.ini`):

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

Consult AGENTS.md for project-specific configuration.

## Type Suppression Policy

**When to use `# type: ignore`:**
* Third-party library without stubs (and no stubs available)
* Known MyPy bug or limitation
* Intentionally dynamic code that cannot be typed

**How to use it:**
```python
# Specific error code (preferred)
result = some_function()  # type: ignore[return-value]

# General ignore (avoid if possible)
result = some_function()  # type: ignore

# With explanation (always)
result = some_function()  # type: ignore[return-value]  # Library has no stubs
```

**Consult AGENTS.md for project-specific type suppression policy.**

## Validation Checklist

Before considering MyPy errors fixed:

- [ ] All MyPy errors resolved
- [ ] No new MyPy errors introduced
- [ ] All tests still pass
- [ ] Runtime behavior preserved
- [ ] Type suppressions minimized and documented
- [ ] Commit message follows conventions

## Integration with Other Skills

* **For CI failures**: Use `ci-failure-triage` skill
* **For general Python issues**: Use `python-ruff-fixing` skill
* **For pre-commit failures**: Use `python-precommit-repair` skill

## Example Workflow

```
1. CI fails: "MyPy type checking failed"

2. Run MyPy locally:
   - Consult AGENTS.md: `mypy src/`
   - Output: 5 errors in src/auth/service.py

3. Read errors:
   - Line 45: Argument 1 has incompatible type "str"; expected "int"
   - Line 67: Item "None" of "Optional[User]" has no attribute "email"
   - Line 89: Function is missing a return type annotation

4. Fix errors:
   - Line 45: Convert string to int: `user_id = int(user_id_str)`
   - Line 67: Add None check: `if user is not None: return user.email`
   - Line 89: Add return type: `def get_user(...) -> Optional[User]:`

5. Verify:
   - Run MyPy: All errors resolved ✓
   - Run tests: All pass ✓

6. Commit:
   - "fix: resolve mypy type errors in auth service"

7. Push and verify:
   - CI passes ✓
```

## Notes

* This is a Python-specific skill for MyPy.
* Always consult AGENTS.md for project-specific MyPy configuration.
* Type hints improve code quality and catch bugs early.
* When in doubt, ask the user for clarification.
