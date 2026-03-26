# Getting Started with Windsurf Cascade Configuration

This guide helps you get started with the Windsurf Cascade configuration kit.

## What is This?

This is a **production-minded Windsurf Cascade configuration starter kit** designed to structure AI-assisted software development.

It provides:
* `AGENTS.md` for project truth and context
* Rules for behavioral constraints
* Skills for reusable procedures
* Workflows for manual runbooks
* Hooks for enforcement and auditing

## Quick Start (5 Minutes)

### 1. Install Windsurf

If you haven't already, install Windsurf Cascade on your machine.

### 2. Copy Configuration to Your Repository

Copy the relevant files to your repository:

```bash
# Copy root AGENTS.md
cp AGENTS.md /path/to/your/repo/

# Copy .windsurf directory
cp -r .windsurf /path/to/your/repo/

# Copy hooks directory
cp -r hooks /path/to/your/repo/

# Optional: Copy example directory-scoped AGENTS.md files
cp -r examples/backend /path/to/your/repo/backend/
cp -r examples/frontend /path/to/your/repo/frontend/
cp -r examples/infra /path/to/your/repo/infra/
```

### 3. Customize AGENTS.md

Open `AGENTS.md` and fill in the `[PROJECT-SPECIFIC]` markers:

**Essential fields:**
```markdown
## Repository Identity
* **Repository name**: my-awesome-project
* **Purpose**: What this project does
* **Primary maintainers**: Your team
* **Repository type**: Application

## Languages and Technology Stack
* **Primary language(s)**: Python 3.11+
* **Frameworks**: FastAPI
* **Runtime environment**: Python 3.11

## Package and Build Management
* **Tool**: uv
* **Lock file**: uv.lock
* **Install command**: `uv sync`

## Testing Conventions
* **Test framework**: pytest
* **Run all tests**: `uv run pytest`
* **Run with coverage**: `uv run pytest --cov`

## Code Quality Tools
* **Linter**: ruff
* **Lint command**: `uv run ruff check .`
* **Type checker**: mypy
* **Type check command**: `uv run mypy .`
```

### 4. Test Commands

Verify all commands work:

```bash
# Test the commands you specified in AGENTS.md
uv run pytest
uv run ruff check .
uv run mypy .
```

If commands don't work, update AGENTS.md with correct commands.

### 5. Commit Configuration

```bash
git add AGENTS.md .windsurf hooks
git commit -m "chore: add Windsurf Cascade configuration"
```

**Done!** Your repository is now configured for Windsurf Cascade.

---

## What's Included

### Root Files

* **`AGENTS.md`**: Project truth and context (customize this first)
* **`README.md`**: Installation and usage guide

### `.windsurf/` Directory

* **`rules/`**: Behavioral constraints
  * `coding-standards.md`
  * `testing-policy.md`
  * `commit-policy.md`
  * `pr-policy.md`
  * `ci-policy.md`

* **`skills/`**: Reusable procedures
  * `feature-implementation/`
  * `test-design/`
  * `code-review-prep/`
  * `ci-failure-triage/`
  * `coverage-regression-repair/`
  * `python-mypy-debugging/` (Python-specific)
  * `python-ruff-fixing/` (Python-specific)
  * `python-precommit-repair/` (Python-specific)

* **`workflows/`**: Manual runbooks
  * `pr-readiness.md`
  * `release-readiness.md`
  * `dependency-upgrade-review.md`

* **`hooks.json`**: Hook configuration

### `hooks/` Directory

* **`quality_gate.py`**: Lightweight quality checks
* **`block_dangerous_commands.py`**: Dangerous command blocking
* **`audit_log.py`**: Command audit logging
* **`README.md`**: Hook documentation

### `docs/` Directory

* **`architecture-rationale.md`**: Why this architecture
* **`customization-guide.md`**: How to customize
* **`language-overlays.md`**: Language-specific guidance

### `examples/` Directory

* **`backend/AGENTS.md`**: Backend-specific context
* **`frontend/AGENTS.md`**: Frontend-specific context
* **`infra/AGENTS.md`**: Infrastructure-specific context

---

## Understanding the Architecture

### Five Layers

1. **AGENTS.md**: Project truth (languages, tools, commands, conventions)
2. **Rules**: Short behavioral constraints (coding standards, testing policy)
3. **Skills**: Multi-step procedures (feature implementation, CI triage)
4. **Workflows**: Manual checklists (PR readiness, release readiness)
5. **Hooks**: Automated enforcement (quality gates, dangerous command blocking)

### Why This Structure?

* **Separation of concerns**: Each layer has a distinct purpose
* **Reusability**: Skills and Rules are reusable across projects
* **Maintainability**: Changes are localized to specific layers
* **Scalability**: Scales to multiple languages and complex projects

See `docs/architecture-rationale.md` for detailed explanation.

---

## Customization Roadmap

### Phase 1: Essential Customization (Day 1)

1. Fill in `AGENTS.md` with project specifics
2. Verify all commands work
3. Set test coverage threshold
4. Define commit message format
5. Locate PR template

**Time: 30 minutes**

### Phase 2: Review and Adjust (Week 1)

1. Review all Rules
2. Review all Skills
3. Add project-specific notes to Skills (if needed)
4. Test configuration with AI tool

**Time: 2 hours**

### Phase 3: Enhance (Month 1)

1. Add project-specific Rules (if needed)
2. Add project-specific Skills (if needed)
3. Customize Workflows
4. Tune Hooks

**Time: 4 hours**

### Phase 4: Iterate (Ongoing)

1. Gather team feedback
2. Adjust based on usage
3. Add missing pieces
4. Remove unused components

**Time: 1 hour/month**

---

## Common Use Cases

### Use Case 1: Implementing a Feature

1. Windsurf Cascade uses `feature-implementation` skill
2. Consults `AGENTS.md` for project conventions
3. Follows `coding-standards` and `testing-policy` rules
4. Runs quality gate hook after writing code
5. Uses `code-review-prep` skill before submitting PR

### Use Case 2: Fixing CI Failure

1. Windsurf Cascade uses `ci-failure-triage` skill
2. Identifies failure type (test, lint, type check)
3. Uses language-specific skill if needed (e.g., `python-mypy-debugging`)
4. Fixes issue following safe implementation principles
5. Commits fix with appropriate message

### Use Case 3: Preparing a Release

1. Developer runs `/pr-readiness` workflow
2. Follows checklist to ensure PR is complete
3. After merge, runs `/release-readiness` workflow
4. Follows steps to prepare and deploy release

---

## Tips for Success

### Start Simple

* Don't customize everything at once
* Start with minimal AGENTS.md
* Add complexity as needed

### Consult AGENTS.md

* Always check AGENTS.md first
* Keep it up to date
* Make it the single source of truth

### Iterate Based on Usage

* Monitor which Skills are used
* Gather team feedback
* Adjust based on pain points

### Keep It Maintainable

* Don't let files grow too large
* Split when necessary
* Remove unused components

### Test Regularly

* Verify commands still work
* Test with AI tool
* Update when tools change

---

## Troubleshooting

### AI Tool Not Following Configuration

**Check:**
1. Is AGENTS.md in the repository root?
2. Are all `[PROJECT-SPECIFIC]` markers filled in?
3. Are commands correct and working?
4. Is the AI tool reading AGENTS.md?

### Commands Not Working

**Fix:**
1. Test each command manually
2. Update AGENTS.md with correct commands
3. Verify environment is set up correctly

### Hooks Failing

**Check:**
1. Are hook scripts executable?
2. Is Python 3 installed?
3. Are environment variables set correctly?
4. Check hook logs for errors

### Configuration Too Complex

**Simplify:**
1. Remove unused Skills
2. Consolidate Rules
3. Simplify Workflows
4. Disable unnecessary Hooks

---

## Next Steps

### Learn More

* Read `docs/architecture-rationale.md` to understand the design
* Read `docs/customization-guide.md` for detailed customization
* Read `docs/language-overlays.md` for language-specific guidance

### Set Up Global Configuration

Set up global configuration on your machine:

```bash
# Create global directories
mkdir -p ~/.codeium/windsurf/memories
mkdir -p ~/.codeium/windsurf/skills

# Add global rules
# Edit: ~/.codeium/windsurf/memories/global_rules.md

# Copy generic skills to global
cp -r .windsurf/skills/feature-implementation ~/.codeium/windsurf/skills/
cp -r .windsurf/skills/test-design ~/.codeium/windsurf/skills/
```

### Share with Team

* Commit configuration to repository
* Document in team wiki
* Add to onboarding guide
* Gather feedback and iterate

---

## Getting Help

If you need help:

1. Review documentation in `docs/`
2. Check examples in `examples/`
3. Review existing configuration
4. Ask your team
5. Iterate based on feedback

---

## Summary

**Quick start:**
1. Copy configuration to your repository
2. Customize AGENTS.md (30 minutes)
3. Test commands
4. Commit and use

**Key files:**
* `AGENTS.md`: Start here
* `.windsurf/`: Configuration directory
* `hooks/`: Enforcement scripts
* `docs/`: Detailed documentation

**Remember:** Start simple, iterate based on usage, keep AGENTS.md up to date.

Happy coding with Windsurf Cascade! 🚀
