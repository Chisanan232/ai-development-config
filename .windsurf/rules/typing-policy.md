---
description: Type checking policy and type hint expectations for Python projects
tags: [python, typing, type-hints, mypy, quality]
language: python
---

# Typing Policy

## Purpose

This rule defines expectations for type hints and type checking in Python projects. Type hints improve code clarity, catch bugs early, and enable better IDE support.

## Core Principles

1. **Type hints are documentation**: They communicate intent and expected types to readers and tools.

2. **Gradual typing is acceptable**: Not all code needs type hints immediately. Prioritize new code and critical paths.

3. **Precision over suppression**: Prefer accurate type hints over `type: ignore` comments.

4. **Preserve runtime behavior**: Type hints must never change how code executes.

## Type Hint Expectations

### When to Add Type Hints

**ALWAYS add type hints for:**
* Public API functions and methods
* Function signatures (parameters and return types)
* Class attributes (especially in `__init__`)
* Module-level constants

**CONSIDER adding type hints for:**
* Complex internal functions
* Data structures with non-obvious types
* Generic containers (List, Dict, etc.)

**MAY SKIP type hints for:**
* Obvious local variables (when type is clear from assignment)
* Private helper functions with trivial logic
* Test code (unless it improves clarity)

### Type Hint Style

**[PROJECT-SPECIFIC]** Check AGENTS.md for:
* Python version (determines available syntax)
* Type checker tool (mypy, pyright, none)
* Strictness level
* Suppression policy

**Modern Python (3.9+)**: Use built-in generics
```python
# ✅ Good (Python 3.9+)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# ❌ Avoid (unless Python < 3.9)
from typing import List, Dict
def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}
```

**Python 3.10+**: Use union operator
```python
# ✅ Good (Python 3.10+)
def get_user(user_id: int) -> User | None:
    return users.get(user_id)

# ❌ Avoid (unless Python < 3.10)
from typing import Optional
def get_user(user_id: int) -> Optional[User]:
    return users.get(user_id)
```

**Python 3.12+**: Use PEP 695 type parameter syntax
```python
# ✅ Good (Python 3.12+)
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# ❌ Avoid (unless Python < 3.12)
from typing import TypeVar
T = TypeVar('T')
def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

## Type Checking Workflow

### Local Development

1. **Check AGENTS.md** for the type check command
2. **Run type checker before committing**:
   ```bash
   # Example (check AGENTS.md for actual command)
   mypy src/
   ```
3. **Fix type errors before moving on**

### During Implementation

* Add type hints as you write new code
* Don't let type checking block progress on prototypes
* Fix type errors before marking work as complete

### During Code Review

* Reviewers should check for missing type hints on public APIs
* Type errors should be fixed, not suppressed without justification

## Handling Type Errors

### Prefer Precise Fixes

**DO:**
```python
# ✅ Fix the actual type issue
def get_config(key: str) -> str | None:  # Was: -> str
    return config.get(key)  # Can return None
```

**DON'T:**
```python
# ❌ Suppress without fixing
def get_config(key: str) -> str:
    return config.get(key)  # type: ignore
```

### When Suppression is Acceptable

Use `type: ignore` ONLY when:

1. **Third-party library has incorrect stubs**
   ```python
   # Library incorrectly typed, reported upstream
   result = external_lib.process(data)  # type: ignore[arg-type]
   ```

2. **Dynamic behavior that type checker can't understand**
   ```python
   # Metaclass magic that mypy doesn't understand
   class Model(metaclass=ModelMeta):  # type: ignore[misc]
       pass
   ```

3. **Temporary during migration** (with TODO)
   ```python
   # TODO: Fix type after refactoring User model
   def legacy_function(user):  # type: ignore[no-untyped-def]
       pass
   ```

**ALWAYS:**
* Add a comment explaining WHY suppression is needed
* Use specific error codes (e.g., `# type: ignore[arg-type]`)
* Create a ticket to fix it properly if it's temporary

### Never Suppress Without Understanding

**DON'T:**
```python
# ❌ Bad: Suppressing without understanding
def process(data):  # type: ignore
    return data.transform()
```

**DO:**
```python
# ✅ Good: Understand and fix
def process(data: dict[str, Any]) -> ProcessedData:
    return ProcessedData.from_dict(data)
```

## Common Type Patterns

### Optional Values

```python
# ✅ Explicit None handling
def find_user(user_id: int) -> User | None:
    return users.get(user_id)

# Usage
user = find_user(123)
if user is not None:
    print(user.name)
```

### Collections

```python
# ✅ Specific collection types
def get_user_ids(users: list[User]) -> set[int]:
    return {user.id for user in users}

# ✅ Generic collections when type varies
from typing import Any
def merge_configs(configs: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for config in configs:
        result.update(config)
    return result
```

### Protocols (Structural Typing)

```python
# ✅ Use Protocol for duck typing
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

def render(item: Drawable) -> None:
    item.draw()
```

### TypedDict for Structured Dicts

```python
# ✅ Use TypedDict for dict with known structure
from typing import TypedDict

class UserDict(TypedDict):
    id: int
    name: str
    email: str

def create_user(data: UserDict) -> User:
    return User(**data)
```

## Type Checking Tools

### MyPy (Example)

**[PROJECT-SPECIFIC]** Check AGENTS.md for actual configuration.

```ini
# mypy.ini or pyproject.toml
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = False  # Start lenient
check_untyped_defs = True
```

### Pyright/Basedpyright (Example)

```json
// pyrightconfig.json
{
  "pythonVersion": "3.11",
  "typeCheckingMode": "basic",
  "reportMissingTypeStubs": false
}
```

## Integration with CI/CD

**[PROJECT-SPECIFIC]** Check AGENTS.md for CI type checking policy.

Common patterns:
* Type checking runs in CI on all PRs
* Failures block merge
* Warnings are informational only
* Incremental adoption: only check changed files

## Gradual Adoption Strategy

If adding types to an existing untyped codebase:

1. **Start with public APIs**: Add types to public functions first
2. **Work inward**: Add types to internal functions as needed
3. **Use strict mode selectively**: Enable strict checking per-file
4. **Don't block progress**: Allow `type: ignore` during migration with TODOs

## Library-Specific Considerations

**[LIBRARY REPOS ONLY]** If distributing a library:

* Include `py.typed` marker file
* Ensure all public APIs are typed
* Consider providing stub files for complex types
* Test type hints with type checkers

**[APPLICATION REPOS]** Type hints are for development only:
* No need for `py.typed`
* Focus on critical paths and public interfaces
* Pragmatic over perfect

## Safety Guidelines

### DO

* ✅ Add type hints to new code
* ✅ Fix type errors by correcting types
* ✅ Use specific error codes when suppressing
* ✅ Document why suppression is needed
* ✅ Check AGENTS.md for project type checking policy
* ✅ Run type checker before committing

### DO NOT

* ❌ Suppress type errors without understanding them
* ❌ Use `Any` everywhere to avoid type errors
* ❌ Change runtime behavior to satisfy type checker
* ❌ Add incorrect type hints (worse than no hints)
* ❌ Block PRs on type hints for legacy code
* ❌ Assume all Python projects use the same type checker

## Conflict Resolution

If type hints conflict with runtime behavior:

1. **Runtime behavior wins**: Type hints must never change execution
2. **Fix the type hint**: Make it match actual runtime behavior
3. **Consider refactoring**: If types are too complex, code might need simplification

## Examples

### Good Type Hints

```python
from typing import Protocol

class Repository(Protocol):
    def get(self, id: int) -> User | None: ...
    def save(self, user: User) -> None: ...

class UserService:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo
    
    def get_user_name(self, user_id: int) -> str:
        user = self.repo.get(user_id)
        if user is None:
            raise ValueError(f"User {user_id} not found")
        return user.name
```

### Acceptable Suppression

```python
# Third-party library has incorrect type stubs
# Reported: https://github.com/lib/issues/123
result = external_lib.process(data)  # type: ignore[arg-type]
```

### Unacceptable Suppression

```python
# ❌ No explanation, no specific error code
def process(data):  # type: ignore
    return data.transform()
```

## Summary

Type hints improve code quality and catch bugs early. Add them to new code, fix type errors properly, and only suppress when absolutely necessary with clear documentation. Always check AGENTS.md for project-specific type checking policy.
