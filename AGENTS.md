# Repository Configuration for Windsurf Cascade

## Repository Identity

**[PROJECT-SPECIFIC]** Replace this section with your repository's actual identity:

* **Repository name**: [Your repository name]
* **Purpose**: [Brief description of what this repository does]
* **Primary maintainers**: [Team or individual names]
* **Repository type**: [Library / Application / Service / Infrastructure / Monorepo]

---

## Languages and Technology Stack

**[PROJECT-SPECIFIC]** Specify the languages and frameworks used in this repository:

* **Primary language(s)**: [e.g., Python 3.11+, TypeScript 5.x, Java 17, Rust 1.70+]
* **Frameworks**: [e.g., FastAPI, React, Spring Boot, Axum]
* **Runtime environment**: [e.g., Node.js 20.x, JVM 17, Python 3.11]

---

## Package and Build Management

**[PROJECT-SPECIFIC]** Define how dependencies are managed and how the project is built:

### Package Manager

* **Tool**: [e.g., uv, poetry, pip-tools, npm, pnpm, yarn, gradle, cargo]
* **Lock file**: [e.g., uv.lock, poetry.lock, package-lock.json, Cargo.lock]
* **Install command**: [e.g., `uv sync`, `poetry install`, `npm ci`, `cargo build`]

### Build System

* **Build tool**: [e.g., uv, setuptools, webpack, vite, gradle, cargo]
* **Build command**: [e.g., `uv build`, `npm run build`, `gradle build`, `cargo build --release`]
* **Build artifacts location**: [e.g., dist/, build/, target/]

---

## Testing Conventions

**[PROJECT-SPECIFIC]** Specify how tests are organized and executed:

### Test Organization

* **Test directories**: [e.g., tests/unit/, tests/integration/, tests/e2e/]
* **Test file naming**: [e.g., test_*.py, *.test.ts, *_test.go]
* **Test framework**: [e.g., pytest, jest, vitest, JUnit, cargo test]

### Test Execution

* **Run all tests**: [e.g., `uv run pytest`, `npm test`, `cargo test`]
* **Run unit tests only**: [e.g., `uv run pytest tests/unit/`, `npm run test:unit`]
* **Run integration tests**: [e.g., `uv run pytest tests/integration/`, `npm run test:integration`]
* **Run specific test file**: [e.g., `uv run pytest tests/unit/test_module.py`]
* **Run with coverage**: [e.g., `uv run pytest --cov`, `npm run test:coverage`]

### Test Coverage

* **Coverage tool**: [e.g., coverage.py, pytest-cov, c8, istanbul]
* **Minimum coverage threshold**: [e.g., 80%, 90%]
* **Coverage report location**: [e.g., htmlcov/, coverage/]
* **Coverage config**: [e.g., .coveragerc, pyproject.toml, jest.config.js]

---

## Code Quality Tools

**[PROJECT-SPECIFIC]** Define linting, formatting, and type checking tools:

### Linter

* **Tool**: [e.g., ruff, eslint, clippy, checkstyle]
* **Config file**: [e.g., pyproject.toml, .eslintrc.js, clippy.toml]
* **Lint command**: [e.g., `uv run ruff check .`, `npm run lint`, `cargo clippy`]
* **Auto-fix command**: [e.g., `uv run ruff check --fix .`, `npm run lint:fix`]

### Formatter

* **Tool**: [e.g., ruff format, prettier, rustfmt, google-java-format]
* **Config file**: [e.g., pyproject.toml, .prettierrc, rustfmt.toml]
* **Format command**: [e.g., `uv run ruff format .`, `npm run format`, `cargo fmt`]
* **Format check**: [e.g., `uv run ruff format --check .`, `npm run format:check`]

### Type Checker

* **Tool**: [e.g., mypy, pyright, TypeScript compiler, Flow]
* **Config file**: [e.g., pyproject.toml, tsconfig.json, mypy.ini]
* **Type check command**: [e.g., `uv run mypy .`, `npm run typecheck`, `tsc --noEmit`]
* **Type suppression policy**: [REFINE FOR THIS REPO - e.g., "Avoid type: ignore unless absolutely necessary", "Document all type suppressions with inline comments"]

---

## Pre-commit and Git Hooks

**[PROJECT-SPECIFIC]** Specify pre-commit configuration if used:

* **Pre-commit framework**: [e.g., pre-commit, husky, lefthook]
* **Config file**: [e.g., .pre-commit-config.yaml, .husky/, lefthook.yml]
* **Install hooks**: [e.g., `pre-commit install`, `npm run prepare`]
* **Run manually**: [e.g., `pre-commit run --all-files`, `npm run pre-commit`]

---

## Safe Implementation Policy

When implementing changes, always follow these principles:

1. **Preserve runtime behavior**: Do not change observable behavior unless explicitly required by the task.
2. **Minimize scope**: Keep changes focused on the specific requirement. Do not broaden refactors during bug fixes.
3. **Run impacted tests first**: Before running the full test suite, run only the tests directly affected by your changes.
4. **Validate incrementally**: After each logical change, verify that tests still pass.
5. **Consult existing patterns**: Follow established patterns in the codebase for similar functionality.
6. **Document non-obvious decisions**: Add comments for complex logic or non-obvious design choices.

---

## Commit Policy

**[PROJECT-SPECIFIC]** Define commit message conventions:

### Commit Message Format

* **Style**: [e.g., Conventional Commits, git emoji + summary, Angular style]
* **Example**: [e.g., "✨ Add user authentication endpoint", "feat: add user authentication", "fix(api): handle null pointer in user service"]

### Commit Hygiene

* **Commit frequency**: Commit in traceable, event-based increments (e.g., after implementing a feature, after fixing a bug, after adding tests).
* **Commit atomicity**: Each commit should represent a single logical change.
* **Commit message length**: Keep subject line under 72 characters. Use body for additional context if needed.
* **Reference issues**: Include issue/ticket references where applicable [e.g., "Fixes #123", "Relates to PROJ-456"].

### What to Commit

* **Include**: Source code changes, test changes, configuration updates, documentation updates.
* **Exclude**: Build artifacts, IDE-specific files, temporary files, sensitive data.
* **Generated files**: [REFINE FOR THIS REPO - specify whether generated files should be committed]

---

## Pull Request Policy

**[PROJECT-SPECIFIC]** Define PR conventions and expectations:

### PR Preparation

* **PR template location**: [e.g., .github/pull_request_template.md, .gitlab/merge_request_templates/]
* **Title format**: [e.g., "[FEATURE] Add user authentication", "fix: resolve null pointer in user service"]
* **Description style**: Concise, bullet-based summary of changes and their purpose.

### PR Body Structure

When preparing a PR, include:

1. **What changed**: Brief bullet list of changes made.
2. **Why it changed**: Engineering purpose and context.
3. **How to verify**: Steps to test or verify the changes.
4. **Related issues**: Links to related issues or tickets.
5. **Breaking changes**: Highlight any breaking changes or migration steps.

### PR Size

* **Preferred size**: Keep PRs focused and reviewable (typically < 500 lines changed).
* **Large PRs**: If a PR must be large, break it into logical commits and provide a detailed description.

### PR Checklist

Before submitting a PR:

* [ ] All tests pass locally
* [ ] Code follows project style guidelines
* [ ] New tests added for new functionality
* [ ] Documentation updated if needed
* [ ] No linting or type checking errors
* [ ] Commit messages follow project conventions

---

## CI/CD Observation Policy

**[PROJECT-SPECIFIC]** Define CI/CD expectations and failure handling:

### CI Pipeline

* **CI platform**: [e.g., GitHub Actions, GitLab CI, Jenkins, CircleCI]
* **Pipeline config**: [e.g., .github/workflows/, .gitlab-ci.yml, Jenkinsfile]
* **Required checks**: [e.g., tests, linting, type checking, build, security scan]

### CI Failure Handling

When CI fails:

1. **Triage the failure**: Identify the root cause (test failure, lint error, type error, build failure).
2. **Reproduce locally**: Attempt to reproduce the failure in your local environment.
3. **Fix safely**: Address the root cause with minimal changes. Do not broaden the scope.
4. **Commit by issue category**: Group fixes by failure type (e.g., "fix: resolve mypy errors in user module").
5. **Verify before pushing**: Run the failing check locally before pushing the fix.
6. **Iterate until green**: Repeat until all CI checks pass.

### CI Performance

* **Expected CI duration**: [REFINE FOR THIS REPO - e.g., "Full CI should complete in < 10 minutes"]
* **Flaky tests**: [REFINE FOR THIS REPO - policy for handling flaky tests]

---

## Directory Structure and Conventions

**[PROJECT-SPECIFIC]** Document key directories and their purposes:

```
[EXAMPLE - REPLACE WITH YOUR ACTUAL STRUCTURE]
.
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── core/              # Core business logic
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── tests/                 # Test code
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── docs/                  # Documentation
├── scripts/               # Build and utility scripts
├── .windsurf/             # Windsurf Cascade configuration
│   ├── rules/             # Behavioral constraints
│   ├── skills/            # Procedural strategies
│   ├── workflows/         # Manual runbooks
│   └── hooks.json         # Enforcement hooks
└── AGENTS.md              # This file
```

---

## Directory-Specific Instructions

**[PROJECT-SPECIFIC]** Add directory-scoped AGENTS.md files for specialized areas:

* **backend/AGENTS.md**: Backend-specific conventions, API design patterns, database interaction rules.
* **frontend/AGENTS.md**: Frontend-specific conventions, component structure, state management patterns.
* **infra/AGENTS.md**: Infrastructure-specific conventions, deployment procedures, configuration management.

---

## Dependencies and Upgrades

**[PROJECT-SPECIFIC]** Define dependency management policy:

### Dependency Updates

* **Update frequency**: [e.g., Monthly, quarterly, as-needed]
* **Update process**: [e.g., "Use dependabot", "Manual review required", "Follow workflow in .windsurf/workflows/dependency-upgrade-review.md"]
* **Breaking changes**: Always review release notes before upgrading major versions.

### Security Updates

* **Security scanning**: [e.g., "Dependabot security alerts", "Snyk", "npm audit"]
* **Response time**: [e.g., "Critical vulnerabilities must be addressed within 48 hours"]

---

## Communication and Collaboration

**[ORG POLICY]** Define how the team communicates:

* **Issue tracker**: [e.g., GitHub Issues, Jira, Linear]
* **Chat platform**: [e.g., Slack, Discord, Microsoft Teams]
* **Documentation**: [e.g., Confluence, Notion, GitHub Wiki]
* **Code review tool**: [e.g., GitHub PR reviews, GitLab MR reviews]

---

## Additional Resources

**[PROJECT-SPECIFIC]** Link to additional documentation:

* **Architecture documentation**: [e.g., docs/architecture.md]
* **API documentation**: [e.g., docs/api.md, OpenAPI spec]
* **Deployment guide**: [e.g., docs/deployment.md]
* **Troubleshooting guide**: [e.g., docs/troubleshooting.md]

---

## Refinement Checklist

When adapting this template for your repository, ensure you:

- [ ] Replace all **[PROJECT-SPECIFIC]** markers with actual values
- [ ] Replace all **[REFINE FOR THIS REPO]** markers with project-specific policies
- [ ] Replace all **[ORG POLICY]** markers with organization-specific policies
- [ ] Remove example commands and replace with actual commands
- [ ] Document actual directory structure
- [ ] Add directory-scoped AGENTS.md files where needed
- [ ] Verify all commands work in your environment
- [ ] Update CI/CD expectations to match your pipeline
- [ ] Define actual coverage thresholds
- [ ] Specify actual dependency management process
