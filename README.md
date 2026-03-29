# Installing and Using This Windsurf Cascade Configuration Kit

## Purpose

This repository provides a **generic, production-minded Windsurf Cascade configuration starter kit**.

It is designed to help you structure AI-assisted software development using:

* `AGENTS.md` for project truth and directory-scoped context
* Rules for short, durable behavioral constraints
* Skills for reusable multi-step procedures
* Workflows for manual runbooks
* Hooks for enforcement, auditing, and lightweight validation

This kit is intentionally **generic-first**. You are expected to refine it for your own repository.

---

## What Windsurf supports

Windsurf supports the following relevant configuration layers:

* **Root `AGENTS.md`**: always-on context for the whole repository
* **Directory-scoped `AGENTS.md`**: automatically applies to matching directories
* **Workspace Rules**: `.windsurf/rules/*.md`
* **Global Rules**: `~/.codeium/memories/global_rules.md`
* **Workspace Skills**: `.windsurf/skills/`
* **Global Skills**: `~/.codeium/skills/`
* **Workspace Hooks**: `.windsurf/hooks.json`
* **Workspace Workflows**: `.windsurf/workflows/`
* **Global Workflows**: `~/.codeium/global_workflows/`

---

## Recommended installation strategy

Use this kit in two layers:

### Layer 1 — Global configuration on your machine

Put your **personal cross-project preferences** here.

Good candidates:

* personal coding preferences
* general review habits
* general safe-fix philosophy
* language-specific global skills you want available everywhere
* global engineering heuristics

### Layer 2 — Project configuration inside each repository

Put **repository-specific truth and process** here.

Good candidates:

* package manager
* build/test/lint/typecheck commands
* directory conventions
* CI expectations
* PR expectations
* repo-specific workflows
* repo-specific hooks
* repo-specific skills

---

## Local machine setup

### 1. Create your global Windsurf directories

On macOS or Linux:

```bash
mkdir -p ~/.codeium/memories
mkdir -p ~/.codeium/skills
```

On Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codeium\memories"
New-Item -ItemType Directory -Force "$HOME\.codeium\skills"
```

### 2. Add your global rules

**Step 1**: Create the rules directory and copy workspace rules (optional):

```bash
# macOS / Linux
mkdir -p ~/.codeium/memories/rules
cp -r .windsurf/rules/* ~/.codeium/memories/rules/

# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.codeium\memories\rules"
Copy-Item -Path ".windsurf\rules\*" -Destination "$HOME\.codeium\memories\rules\" -Recurse
```

**Step 2**: Create the global rules file:

* macOS / Linux: `~/.codeium/memories/global_rules.md`
* Windows: `%USERPROFILE%\.codeium\memories\global_rules.md`

This file should reference the detailed policies in `~/.codeium/memories/rules/` and include your personal preferences.

**See**: 
- `examples/global_rules.md` for a template that references detailed policies
- `docs/rules-guide.md` for detailed rules documentation including activation modes

### 3. Add your global skills

Create skill folders under:

* macOS / Linux: `~/.codeium/skills/`
* Windows: `%USERPROFILE%\.codeium\skills\`

Example:

```text
~/.codeium/skills/
├── ci-failure-triage/
│   └── SKILL.md
├── python-mypy-debugging/
│   └── SKILL.md
└── code-review-prep/
    └── SKILL.md
```

Use global skills for:

* reusable cross-repository procedures
* language-specific debugging skills
* generic review and triage skills

Do **not** put repository-specific commands into global skills unless clearly marked as examples.

### 4. Add your global workflows (optional)

Create workflow files under:

* macOS / Linux: `~/.codeium/global_workflows/`
* Windows: `%USERPROFILE%\.codeium\global_workflows\`

Example:

```text
~/.codeium/global_workflows/
├── dependency-upgrade-review.md
├── pr-readiness.md
└── release-readiness.md
```

Use global workflows for:

* cross-project manual runbooks
* common checklists you use across repositories
* personal workflow templates

You can copy workspace workflows to global location:

```bash
# macOS / Linux
mkdir -p ~/.codeium/global_workflows
cp .windsurf/workflows/*.md ~/.codeium/global_workflows/

# Windows PowerShell
New-Item -ItemType Directory -Force "$HOME\.codeium\global_workflows"
Copy-Item -Path ".windsurf\workflows\*.md" -Destination "$HOME\.codeium\global_workflows\" -Recurse
```

---

## Repository setup

Inside each repository, create a `.windsurf/` directory and add a root `AGENTS.md`.

Recommended layout:

```text
your-repo/
├── AGENTS.md
├── backend/
│   └── AGENTS.md
├── frontend/
│   └── AGENTS.md
├── infra/
│   └── AGENTS.md
└── .windsurf/
    ├── rules/
    │   ├── coding-standards.md
    │   ├── testing-policy.md
    │   ├── commit-policy.md
    │   ├── pr-policy.md
    │   └── ci-policy.md
    ├── skills/
    │   ├── feature-implementation/
    │   │   └── SKILL.md
    │   ├── test-design/
    │   │   └── SKILL.md
    │   ├── code-review-prep/
    │   │   └── SKILL.md
    │   ├── ci-failure-triage/
    │   │   └── SKILL.md
    │   ├── coverage-regression-repair/
    │   │   └── SKILL.md
    │   ├── python-mypy-debugging/
    │   │   └── SKILL.md
    │   ├── python-ruff-fixing/
    │   │   └── SKILL.md
    │   └── python-precommit-repair/
    │       └── SKILL.md
    ├── workflows/
    │   ├── pr-readiness.md
    │   ├── release-readiness.md
    │   └── dependency-upgrade-review.md
    └── hooks.json
```

---

## Where each kind of information should go

### Put this in `AGENTS.md`

Use `AGENTS.md` for repository truth:

* language(s)
* package manager
* test runner
* type checker
* lint / format tools
* test locations
* coding conventions
* commit style
* PR style
* CI expectations
* directory-specific instructions

Examples:

* “This repository uses uv.”
* “Run tests with `uv run pytest`.”
* “The PR template lives at `.github/pull_request_template.md`.”
* “Use git emoji + concise commit messages.”

### Put this in Rules

Use Rules for short durable constraints:

* prefer small safe changes
* run impacted tests before full suite
* preserve runtime behavior
* do not broaden refactors during bug fixes
* keep PR bodies concise and bullet-based

### Put this in Skills

Use Skills for reusable procedures:

* implementing features
* designing tests
* preparing PRs
* triaging CI failures
* fixing coverage regressions
* debugging MyPy
* fixing Ruff issues
* repairing pre-commit failures

### Put this in Workflows

Use Workflows for manual checklists:

* PR readiness
* release readiness
* dependency upgrade review
* onboarding a repo

### Put this in Hooks

Use Hooks for enforcement and auditing:

* blocking dangerous commands
* lightweight quality checks
* audit logging
* project-specific safety policies

Keep hook config simple.
Put real conditional logic into scripts.

---

## Python-specific recommendation

For a Python repository, refine the kit by filling in:

* package manager: `uv`, `poetry`, `pip-tools`, or another tool
* test command
* type check command
* lint command
* format command
* pre-commit command
* test directories
* type suppression policy
* CI gate expectations

Suggested Python-specific skills:

* `python-mypy-debugging`
* `python-ruff-fixing`
* `python-precommit-repair`
* `python-pytest-failure-debugging`

Important:

* keep Python assumptions out of the generic baseline unless clearly marked
* make repository-specific Python commands explicit in `AGENTS.md`

---

## Hook setup guidance

Create `.windsurf/hooks.json` in the repository root.

Keep it minimal.

Use hook scripts for:

* diff-aware checks
* scope-aware checks
* fast vs strict mode
* environment variable overrides
* cooldown logic
* project command mapping

Good pattern:

```json
{
  "hooks": {
    "post_write_code": [
      {
        "command": "python3 hooks/quality_gate.py",
        "show_output": true
      }
    ],
    "pre_run_command": [
      {
        "command": "python3 hooks/block_dangerous_commands.py",
        "show_output": true
      }
    ]
  }
}
```

Do **not** blindly run full test suites or heavy type checks on every single edit by default.

---

## How to roll this out safely

### Step 1

Install a very small global setup first:

* one global rules file
* two or three global skills

### Step 2

Add only the root `AGENTS.md` to one repository.

### Step 3

Add a few repository Rules.

### Step 4

Add only the most valuable Skills first:

* feature implementation
* test design
* CI failure triage
* PR prep

### Step 5

Add lightweight hooks only after the team understands the workflow.

Do not start with too many hooks or too many project-specific skills.

---

## Recommended refinement order for a real repository

1. Fill in root `AGENTS.md`
2. Add repository Rules
3. Add the core Skills
4. Add language-specific Skills
5. Add manual Workflows
6. Add lightweight Hooks
7. Tune hook scripts for performance and developer experience

---

## How to avoid confusion across many languages

If you work across Python, Java, Rust, TypeScript, and other stacks:

* keep generic cross-project skills global
* keep language-specific skills clearly named
* keep repo truths in project `AGENTS.md`
* do not hardcode one language’s tools into another language’s skill
* include “Do not assume” sections in skills
* always consult `AGENTS.md` before using repository commands

Examples of good names:

* `python-mypy-debugging`
* `java-build-debugging`
* `rust-clippy-and-tests`
* `ts-eslint-and-tests`

Examples of bad names:

* `type-fixing`
* `build-repair`
* `quality-tooling`

---

## Final advice

This kit works best when you treat it as a layered system:

* facts in `AGENTS.md`
* constraints in Rules
* procedures in Skills
* runbooks in Workflows
* enforcement in Hooks

Do not try to solve everything in one file.

Start generic.
Refine carefully.
Keep repository truth explicit.
Keep procedural knowledge reusable.
