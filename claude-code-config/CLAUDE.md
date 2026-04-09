# CLAUDE.md

> This file is the primary behavioral context for Claude Code in this repository.
> It contains durable repository truth, engineering policy, and workflow conventions.
> Claude Code must read and apply every section before taking any action.

---

## Repository Identity

- **Repository**: [PROJECT-SPECIFIC — replace with repo name]
- **Purpose**: [PROJECT-SPECIFIC — one sentence describing what this repo does]
- **Owner**: [PROJECT-SPECIFIC — team or individual]
- **Primary language**: [PROJECT-SPECIFIC — e.g., Python 3.12]
- **Runtime target**: [PROJECT-SPECIFIC — e.g., AWS Lambda, Docker, CLI]
- **Dependency policy**: [PROJECT-SPECIFIC — e.g., pin all transitive deps]

---

## Architecture Constraints

[REFINE FOR THIS REPO — describe the key architectural decisions that must not be
violated. Examples below:]

- This is a monorepo. Services are in `services/`. Shared libraries are in `lib/`.
- Database access must go through the repository layer in `src/db/`.
- All external HTTP calls must use the client in `src/http/client.py`, never raw `requests`.
- Configuration must be loaded from environment variables; no hardcoded values.
- Do not introduce new top-level packages without discussion.

---

## Package, Build, and Run Commands

[PROJECT-SPECIFIC — fill in the exact commands for this repository]

```bash
# Install dependencies
[e.g., uv sync --all-extras]

# Run tests (impacted, fast)
[e.g., pytest tests/unit/ -x --tb=short]

# Run tests (full suite)
[e.g., pytest tests/ --tb=short]

# Lint
[e.g., ruff check .]

# Format
[e.g., ruff format .]

# Type check
[e.g., mypy src/]

# Pre-commit hooks
[e.g., pre-commit run --all-files]

# Build
[e.g., docker build -t myapp:dev .]
```

---

## Safe Implementation Policy

Claude Code must follow these rules on every implementation task, without exception.

### Before writing any code

1. Read the relevant existing code before proposing changes.
2. Understand what the code currently does — do not assume.
3. Clarify ambiguous requirements before starting.
4. Propose the smallest change that achieves the goal.
5. State explicitly what will change, and what will not change.

### During implementation

6. Change only what is necessary. Do not refactor surrounding code unless asked.
7. Do not add features, options, or abstractions beyond what was requested.
8. Do not add comments or docstrings to code you did not change.
9. Do not introduce new dependencies without asking first.
10. Do not add error handling for scenarios that cannot happen.
11. Do not add backwards-compatibility shims for code that has no callers.

### Validation sequence

12. After each logical unit of change, run impacted tests first.
13. Before declaring work complete, run the full validation suite.
14. Do not mark a task done while any test or lint check is red.
15. If a check cannot be run locally, say so explicitly before committing.

### Safety

16. Never overwrite uncommitted changes without explicit user confirmation.
17. Never delete files without explicit user confirmation.
18. Never force-push without explicit user confirmation.
19. Never skip pre-commit hooks (`--no-verify`) without explicit user confirmation.
20. If you discover unexpected repository state (unfamiliar files, branches, config),
    investigate before acting. Do not delete or overwrite unknown state.

---

## Testing Expectations

[REFINE FOR THIS REPO]

- All new features require tests. All bug fixes require a regression test.
- Tests must be deterministic, isolated, and fast.
- Unit tests live in `tests/unit/`. Integration tests live in `tests/integration/`.
- Test behavior, not implementation. Tests must not assert on private internals.
- Do not mock the database in integration tests — use a real test database.
  [PROJECT-SPECIFIC: adjust this to match your actual test strategy]
- Do not disable failing tests. Fix them or escalate.
- Coverage is a metric, not the goal. Meaningful tests matter more than coverage %.
- Minimum coverage threshold: [PROJECT-SPECIFIC — e.g., 85%]
- Run impacted tests during iteration. Run the full suite before committing.

### Test tooling

- Test runner: [PROJECT-SPECIFIC — e.g., pytest]
- Coverage tool: [PROJECT-SPECIFIC — e.g., pytest-cov]
- Fixture strategy: [PROJECT-SPECIFIC — e.g., factory_boy for model factories]
- Mocking: [PROJECT-SPECIFIC — e.g., unittest.mock; no third-party mock libs]

---

## Type Checking Policy

[LANGUAGE-SPECIFIC — this section applies to Python projects using mypy or pyright]

- All public APIs must have complete type annotations.
- All function signatures must be annotated (parameters + return type).
- All class attributes must be annotated at the class level.
- Use modern Python generics: `list[str]`, `dict[str, int]`, `X | Y` (Python 3.10+).
- Do not use `Any` without a code comment explaining why.
- Suppress type errors with `# type: ignore[error-code]` only, never bare `# type: ignore`.
- Type hints must never change runtime behavior.
- Run `mypy src/` before every commit.
- Type checker config: [PROJECT-SPECIFIC — e.g., see `pyproject.toml [tool.mypy]`]

---

## Linting and Formatting Policy

[LANGUAGE-SPECIFIC — adjust per repo]

- Linter: [PROJECT-SPECIFIC — e.g., ruff]
- Formatter: [PROJECT-SPECIFIC — e.g., ruff format]
- Pre-commit hooks enforce both.
- All lint errors must be fixed before committing.
- Do not use `# noqa` without a comment explaining the exception.
- Config: [PROJECT-SPECIFIC — e.g., see `pyproject.toml [tool.ruff]`]
