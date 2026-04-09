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
