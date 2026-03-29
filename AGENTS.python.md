## Python-Specific Example Configuration

**[PYTHON-SPECIFIC]** Below is a complete example for a modern Python project using recommended tools. Use this as a reference when filling in the **[PROJECT-SPECIFIC]** sections above.

### Example: Python 3.11+ Project with Modern Tooling

```markdown
## Repository Identity

* **Repository name**: my-python-service
* **Purpose**: REST API service for user management
* **Primary maintainers**: Backend Team
* **Repository type**: Application

## Languages and Technology Stack

* **Primary language(s)**: Python 3.11+
* **Frameworks**: FastAPI, SQLAlchemy, Pydantic
* **Runtime environment**: Python 3.11

## Package and Build Management

### Package Manager

* **Tool**: uv
* **Lock file**: uv.lock
* **Install command**: `uv sync`
* **Add dependency**: `uv add <package>`
* **Add dev dependency**: `uv add --dev <package>`

### Build System

* **Build tool**: uv
* **Build command**: `uv build`
* **Build artifacts location**: dist/

## Testing Conventions

### Test Organization

* **Test directories**: tests/unit/, tests/integration/
* **Test file naming**: test_*.py
* **Test framework**: pytest

### Test Execution

* **Run all tests**: `uv run pytest`
* **Run unit tests only**: `uv run pytest tests/unit/`
* **Run integration tests**: `uv run pytest tests/integration/`
* **Run specific test file**: `uv run pytest tests/unit/test_users.py`
* **Run with coverage**: `uv run pytest --cov=src --cov-report=html`

### Test Coverage

* **Coverage tool**: pytest-cov
* **Minimum coverage threshold**: 85%
* **Coverage report location**: htmlcov/
* **Coverage config**: pyproject.toml

## Code Quality Tools

### Linter

* **Tool**: ruff
* **Config file**: pyproject.toml
* **Lint command**: `uv run ruff check .`
* **Auto-fix command**: `uv run ruff check --fix .`

### Formatter

* **Tool**: ruff format
* **Config file**: pyproject.toml
* **Format command**: `uv run ruff format .`
* **Format check**: `uv run ruff format --check .`

### Type Checker

* **Tool**: mypy
* **Config file**: pyproject.toml
* **Type check command**: `uv run mypy src/`
* **Type suppression policy**: Avoid `type: ignore` unless absolutely necessary. Always document suppressions with comments explaining why.

## Pre-commit and Git Hooks

* **Pre-commit framework**: pre-commit
* **Config file**: .pre-commit-config.yaml
* **Install hooks**: `pre-commit install`
* **Run manually**: `pre-commit run --all-files`

## Python-Specific Best Practices

### Type Hints

* Use built-in generics for Python 3.9+ (`list`, `dict`, `set` instead of `List`, `Dict`, `Set`)
* Use `|` for unions in Python 3.10+ (`str | None` instead of `Optional[str]`)
* Add type hints to all public functions and methods
* Use `Protocol` for structural typing when appropriate

### Import Organization

* Standard library imports first
* Third-party imports second
* Local application imports last
* Use absolute imports for clarity

### Error Handling

* Raise specific exceptions, not generic `Exception`
* Use custom exception classes for domain errors
* Always include error context in exception messages

### Testing Strategy

* Write tests before or alongside implementation (TDD encouraged)
* Use fixtures for test setup and teardown
* Mock external dependencies (databases, APIs, file systems)
* Test edge cases and error conditions
* Use parametrize for testing multiple inputs

### Documentation

* Use docstrings for all public modules, classes, and functions
* Follow Google or NumPy docstring style (choose one)
* Keep docstrings up to date with code changes
```

**For more Python toolchain options**, see `docs/python-toolchain-guide.md` which covers:
* Alternative package managers (poetry, pip-tools, hatch)
* Alternative type checkers (pyright, basedpyright)
* Alternative linters/formatters (black, flake8)
* Different Python versions (3.7-3.12+)
* Different test frameworks (unittest)
