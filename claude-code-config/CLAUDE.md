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
