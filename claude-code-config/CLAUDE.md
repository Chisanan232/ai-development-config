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

---

## Commit Policy

Every commit must be:

- **Atomic**: one logical concern per commit. If you need two sentences to describe it, split it.
- **Small**: prefer many small commits over one large commit.
- **Bisectable**: the repository must be in a working state after every commit.
- **Descriptive**: subject line under 72 characters in imperative mood.

### Commit message format

```
<emoji> <scope>: <imperative summary under 72 chars>

[Optional body: what changed and why. Not how.]

[Optional footer: closes #123, refs #456]
```

### GitEmoji conventions for this repo

[ORG POLICY — adjust to your organization's emoji set]

| Emoji | Scope |
|---|---|
| `✨` | New feature |
| `🐛` | Bug fix |
| `♻️` | Refactor |
| `✅` | Tests |
| `📝` | Documentation |
| `🔧` | Configuration |
| `🔌` | MCP / integrations |
| `🪝` | Hooks |
| `👨‍💻` | Skills |
| `🧭` | Workflow skills |
| `⬆️` | Dependency upgrade |
| `🗑️` | Delete / remove |
| `🚨` | Fix linting / type errors |

### What not to commit

- `.env` files or secrets of any kind
- Build artifacts, compiled outputs
- IDE-specific files not in `.gitignore`
- Large binary files
- Commented-out dead code

---

## Pull Request Policy

### Before opening a PR

- All tests pass locally.
- All lint and type checks pass locally.
- Pre-commit hooks pass.
- CI is not blocked by an unrelated red branch.
- You have reviewed your own diff before requesting review.

### PR size and scope

- Keep PRs under 500 lines when possible.
- One concern per PR. Do not bundle unrelated changes.
- If a change is large, break it into a sequence of stacked PRs.

### PR description must include

1. What changed (one paragraph)
2. Why it changed (motivation, context, issue reference)
3. How to verify (manual steps or automated test reference)
4. Related issues / tickets: `Closes #[PROJECT-SPECIFIC]`

### Review process

- Address all reviewer comments before merging.
- Do not force-push during active review.
- CI must be green before merging.
- Merge strategy: [PROJECT-SPECIFIC — e.g., squash merge / rebase merge]

---

## CI/CD Triage Expectations

When CI fails, Claude Code must follow this sequence:

1. **Identify** the failure type: test failure, lint error, type error, build error,
   coverage drop, security alert, infrastructure issue.
2. **Reproduce locally** before proposing a fix. Do not guess from CI logs alone.
3. **Analyze** the root cause. Do not apply surface-level fixes.
4. **Fix** the underlying problem. Do not bypass or suppress CI checks.
5. **Verify** the fix resolves the failure locally.
6. **Commit** the fix as a focused, isolated commit.
7. **Push** and confirm CI passes.

### What not to do

- Do not merge on red CI.
- Do not add `# noqa`, `# type: ignore`, or test `skip` markers to silence failures.
- Do not delete failing tests.
- Do not bypass pre-commit with `--no-verify`.
- If a failure cannot be reproduced locally, say so before proposing a fix.

### Flaky tests

Flaky tests indicate real problems. Do not mark them as skip. Investigate
the root cause: race conditions, shared state, external dependencies, timing assumptions.

---

## Source-of-Truth Systems

[PROJECT-SPECIFIC — describe where canonical information lives for this project]

| System | Purpose | Reference |
|---|---|---|
| GitHub Issues | Bug tracking and feature requests | [PROJECT-SPECIFIC] |
| [JIRA / Linear / etc.] | Sprint planning and task tracking | [PROJECT-SPECIFIC] |
| [Confluence / Notion / etc.] | Architecture decisions and runbooks | [PROJECT-SPECIFIC] |
| [Slack channel] | Team discussion and incident alerts | [PROJECT-SPECIFIC] |

---

## MCP-Backed Systems

Claude Code can use MCP-connected tools when available. Check `.mcp.json` for
what is configured in this project. The following capability categories may be available:

| Capability | What it provides | When to use |
|---|---|---|
| `code_repository` | Git operations, PR creation, branch management | Branching, PRs, diffs |
| `issue_tracking` | Read/write issues and tickets | Linking commits to issues |
| `communication` | Post to Slack, notify teams | Status updates on deploys |
| `static_analysis` | SonarQube quality gates, code smells | Pre-PR quality checks |
| `coverage_reporting` | Codecov coverage trends | Coverage regression detection |
| `observability` | Datadog, Sentry alerts, logs | Incident triage |
| `knowledge_search` | Confluence, Notion, internal docs | Architecture lookups |

When an MCP-backed capability is available for a task, prefer it over manual
approximation. When it is not available, proceed without it and note the gap.

---

## Time-Layer Design — Skill-First Polling and Scheduling

Claude Code may run recurring tasks using `/loop` or a scheduler. The rule is:
**prefer waking narrow skills, not full agents, for polling and status checks.**

### Default rule

- Wake a **skill** for narrow, scoped checks (PR health, bot PR maintenance, pipeline state).
- Wake **`dev-lead-agent`** only when strategic re-planning or multi-step coordination
  is needed as a result of what the polling found.

### Primary recurring automation targets

| Target | Skill to wake | Wake agent if |
|---|---|---|
| PR health checks | `pr-health-check` | A PR requires merge decision or escalation |
| Bot PR maintenance | `bot-pr-maintainer` (via `pr-health-check`) | CI failure caused by the update itself |
| Release pipeline observation | `release-watch` | Pipeline fails and engineer action is needed |

### Polling intervals (project-configurable)

- PR health check: every [PROJECT-SPECIFIC] minutes (e.g., every 30 min during working hours)
- Release watch: every [PROJECT-SPECIFIC] minutes during an open release window (e.g., every 5 min)

### How to configure

Use `/loop <interval> /pr-health-check` to start a recurring PR health check.
Use `/loop <interval> /release-preparation` then `/loop <interval> /release-watch`
during a release window.

Do not start a loop on a full agent (`dev-lead-agent`) for routine polling.
Agents are stateful and expensive to wake repeatedly — use them only when
the skill's output indicates a decision or coordination is needed.

### Loop safety rules

- A skill woken by a loop must not trigger another loop.
- A skill must not enter a self-repair cycle — it must report failure and exit.
- If a repair action is needed, the skill reports it; the engineer or agent decides.

---

## Skill Invocation Guide

The following skills are available for this repository. Invoke them by their
slash command or by asking Claude Code to run the named procedure.

| Skill | Type | When to use |
|---|---|---|
| `feature-implementation` | Auto | When implementing any new feature |
| `test-design` | Auto | When designing tests for new or changed code |
| `code-review-prep` | Auto | Before opening a PR |
| `ci-failure-triage` | Auto | When CI is red |
| `python-mypy-debugging` | Auto | When mypy reports type errors |
| `python-ruff-fixing` | Auto | When ruff reports lint violations |
| `python-precommit-repair` | Auto | When pre-commit hooks fail |
| `task-decomposition` | Auto | When a ticket arrives and needs decomposition |
| `acceptance-validation` | Auto | Before declaring implementation complete (qa-agent) |
| `bot-pr-maintainer` | Auto | When a bot PR is classified as clean or conflicted |
| `/pr-readiness` | Command | Before opening a PR (full checklist run) |
| `/pr-health-check` | Command | At each polling interval to assess all open PRs |
| `/release-readiness` | Command | Before tagging a release |
| `/release-preparation` | Command | When a release window opens |
| `/dependency-upgrade-review` | Command | Before merging a dependency bump PR |

---

## Auto-Merge Policy

A pull request may be merged automatically only when **all** of the following conditions are met:

1. **Code owner approval is present** — at least one required reviewer has approved.
2. **All required CI checks pass** — no red status checks on the PR.
3. **No merge conflicts** — the branch merges cleanly into the base.
4. **No unresolved blocking comments** — all `Request Changes` reviews are resolved or dismissed.
5. **Branch is up to date** — the PR branch includes the latest commits from the base branch.

If any condition is not met, do not merge. Wait, fix, or escalate.

### Who may trigger auto-merge

- `dev-lead-agent` is the only agent that may approve merge decisions.
- `dev-agent` and `qa-agent` must not independently trigger merges.
- Engineer may override and merge manually at any time.

### Merge strategy

Use the merge strategy configured for this repository.
[PROJECT-SPECIFIC — e.g., squash merge for feature PRs, rebase merge for dependency bumps]

---

## Bot PR Policy

Dependency bots (Dependabot, Renovate) and pre-commit maintenance bots produce
automated PRs that follow a distinct handling path.

### Standard bot PR handling

If a bot PR meets all of the following:
- CI is green
- No merge conflicts
- No scope expansion beyond the automated update

Then: **approve and merge automatically**.

### Bot PR with lock-file conflicts

If a bot PR has lock-file conflicts (e.g., `poetry.lock`, `uv.lock`, `package-lock.json`):

1. Request a rebase using the bot's supported rebase mechanism
   (e.g., comment `@dependabot rebase` or `@renovatebot rebase`).
2. Wait for the bot to rebase and CI to rerun.
3. Re-evaluate the PR against the standard bot PR handling criteria.
4. Approve and merge only when it is clean and CI is green.

Do not manually resolve lock-file conflicts in bot PRs — let the bot handle it.

### Bot PR with CI failure

If a bot PR has CI failure after rebase:
- Investigate the failure root cause.
- If the failure is unrelated to the update, note it and proceed.
- If the failure is caused by the update itself, escalate to the engineer — do not merge.

### Bot PR oversight

The `bot-pr-maintainer` skill and `pr-health-check` skill manage this loop.
`dev-lead-agent` coordinates bot PR state at each polling interval.

---

## Push Gate Policy

Claude Code must not push to any remote branch unless all of the following are true:

1. **Full test suite passes** — run the complete test suite locally, not just impacted tests.
2. **Pre-commit hooks pass** — run `pre-commit run --all-files`. Zero failures.
3. **Linter is clean** — zero violations.
4. **Type checker is clean** — zero errors.
5. **No uncommitted changes remain** — working tree is clean before pushing.
6. **Branch is not behind remote** — pull or rebase before pushing to avoid clobbering.

### Force-push rules

- Force-push is **forbidden** on `main` / `master` / release branches under any circumstance.
- Force-push on feature branches requires **explicit engineer confirmation** and is
  only permitted when rebasing on the base branch (not to rewrite merged history).
- Never force-push during an active code review.

### What gates the push

The `full-test-gate.sh` and `precommit-gate.sh` hooks enforce this automatically.
If either hook fails, the push is blocked. Fix the failure — do not use `--no-verify`.

---

## Development Preconditions

Before beginning any implementation task, Claude Code must verify:

1. **Branch is current** — local branch is up to date with the expected remote base.
   Run `git fetch origin` and confirm no divergence before writing code.
2. **CI is not red on the base branch** — do not start work on top of a broken base.
   Check the most recent CI run on `main` (or the target branch) before branching.
3. **No uncommitted state** — working tree must be clean before switching branches
   or beginning a new task.
4. **Dependencies are installed** — run the install command if `uv.lock` / `package-lock.json`
   (or equivalent) has changed since the last install.
5. **Pre-commit hooks are active** — confirm `.git/hooks/pre-commit` is installed.
   Run `pre-commit install` if missing.

If any precondition fails, stop and resolve it before writing any code.
Do not proceed on a stale or broken foundation.

---

## Release Operations Policy

The external release workflow (automated tag creation, version bumping, changelog
generation) handles the mechanics of releasing. Claude Code's role is **observational
and preparatory**, not operational.

### What Claude Code does during a release window

1. **Identify changes** — inspect the commits in the release window (since the last tag).
2. **Prepare release notes** — draft human-readable changelog content.
3. **Update release intent config** — update version references or release config files
   if the project uses them (e.g., `pyproject.toml`, `package.json`, `CHANGELOG.md`).
4. **Observe release workflow state** — monitor the automated release CI pipeline.
5. **Summarize outcome** — report success or failure with links to the release artifact.

### What Claude Code must not do during release

- Do not manually create git tags unless the automated workflow has definitively failed
  and the engineer has explicitly requested manual intervention.
- Do not push directly to `main` / `master` during a release window.
- Do not modify CI/CD pipeline definitions during active release.
- Do not publish packages to registries — this is the automated workflow's job.

### Release coordination

`release-agent` handles release observation. It is thin by design — it does not
replace the automated workflow, it monitors and summarizes it.

---

## Agent Delegation Model

Claude Code may invoke specialized sub-agents for complex multi-step tasks.
Each agent has a defined scope. Do not conflate responsibilities across agents.

### Agent roster

| Agent | File | Primary scope |
|---|---|---|
| `dev-lead-agent` | `.claude/agents/dev-lead-agent.md` | Planning, decomposition, PR decisions, coordination |
| `dev-agent` | `.claude/agents/dev-agent.md` | Code implementation, test writing, local validation |
| `qa-agent` | `.claude/agents/qa-agent.md` | Acceptance validation, regression checks, edge cases |
| `release-agent` | `.claude/agents/release-agent.md` | Release observation, notes, outcome summary |

### Delegation rules

1. `dev-lead-agent` is the orchestrator. It decomposes tasks, assigns work to other
   agents, reviews PRs, and makes merge decisions.
2. `dev-agent` implements. It must not make merge decisions or orchestration choices.
3. `qa-agent` validates from an external tester perspective. It must not implement.
4. `release-agent` observes and summarizes. It must not trigger releases directly.
5. When no agent delegation is needed (simple focused tasks), Claude Code acts directly.
6. Never collapse all responsibilities into a single agent invocation.

### When to wake each agent

- **`dev-lead-agent`**: when a ticket arrives, when a PR needs review, when strategic
  re-planning is required, when coordinating bot PR maintenance.
- **`dev-agent`**: when implementation, test writing, or focused CI repair is needed.
- **`qa-agent`**: when acceptance criteria must be verified, before a PR is merged.
- **`release-agent`**: when a release window opens or the release pipeline needs monitoring.

---

## What Claude Code Must Never Do Without Explicit Confirmation

- Delete any file
- Force-push to any branch
- Run `git reset --hard`
- Run `git clean -fd`
- Drop or truncate database tables
- Pipe remote content directly to a shell (`curl | bash`)
- Publish packages to registries
- Modify CI/CD pipeline definitions without review
- Commit `.env` or any file containing credentials
