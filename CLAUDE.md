# CLAUDE.md — AI Assistant Guide for ai-development-config

## Repository Identity

- **Repository**: ai-development-config
- **Purpose**: Production-minded, generic-first Windsurf Cascade configuration starter kit for structuring AI-assisted software development
- **Owner**: Chisanan232
- **Type**: Configuration framework / Template kit
- **Primary AI Target**: Windsurf Cascade (also applicable to Claude Code and other AI assistants)

---

## What This Repository Is

This is a **configuration framework**, not an application. It provides templates, rules, scripts, and conventions for teams to adopt AI-assisted development workflows. When working in this repo, you are editing **the framework itself**, not using it as an end user.

The kit uses a **six-layer architecture**:

| Layer | Directory | Purpose |
|---|---|---|
| Project Truth | `AGENTS.md` | Declarative facts about a target project (template) |
| Rules | `.windsurf/rules/`, `.windsurf/memory/rules/` | Behavioral constraints (always-on) |
| Skills | `.windsurf/skills/` | Reusable multi-step procedures |
| MCP Servers | `.windsurf/mcp_config.json`, `docker-compose.yml` | External capability providers |
| Workflows | `.windsurf/workflows/` | Manual runbooks and checklists |
| Hooks | `.windsurf/hooks/`, `.windsurf/hooks.json` | Automated enforcement and auditing |

---

## Directory Structure

```
.
├── AGENTS.md                        # Template: project truth for a target repo
├── AGENTS.python.md                 # Example: Python project AGENTS.md
├── CONFIGURATION-OVERVIEW.md        # Full architecture documentation
├── DOCKER-MCP-README.md             # Docker MCP server setup guide
├── GETTING-STARTED.md               # 5-minute quick start guide
├── README.md                        # Installation and usage overview
├── docker-compose.yml               # MCP server Docker definitions
├── docker-compose.override.yml      # Local development overrides
├── .env.example                     # Environment variable template
├── .github/
│   └── CODEOWNERS                   # All files owned by @Chisanan232
├── .windsurf/
│   ├── hooks.json                   # Hook trigger configuration
│   ├── mcp_config.json              # MCP server definitions
│   ├── hooks/                       # Python enforcement scripts
│   │   ├── policy_engine.py         # Scope-aware policy enforcement
│   │   ├── quality_gate.py          # Lightweight quality checks
│   │   ├── block_dangerous_commands.py  # Dangerous command blocking
│   │   ├── audit_log.py             # Command audit logging
│   │   └── README.md
│   ├── memory/
│   │   ├── global_rules.md          # Cross-project global rules
│   │   └── rules/
│   │       ├── coding-standards.md
│   │       ├── testing-policy.md
│   │       ├── commit-policy.md
│   │       ├── pr-policy.md
│   │       └── ci-policy.md
│   ├── rules/
│   │   └── typing-policy.md         # Type hint standards
│   ├── skills/
│   │   ├── feature-implementation/SKILL.md
│   │   ├── test-design/SKILL.md
│   │   ├── code-review-prep/SKILL.md
│   │   ├── ci-failure-triage/SKILL.md
│   │   ├── coverage-regression-repair/SKILL.md
│   │   ├── python-mypy-debugging/SKILL.md
│   │   ├── python-ruff-fixing/SKILL.md
│   │   ├── python-precommit-repair/SKILL.md
│   │   └── python-pytest-failure-debugging/SKILL.md
│   └── workflows/
│       ├── pr-readiness.md
│       ├── release-readiness.md
│       └── dependency-upgrade-review.md
└── examples/
    ├── backend/AGENTS.md
    ├── frontend/AGENTS.md
    └── infra/AGENTS.md
```

---

## Key Files to Know

### AGENTS.md (root)
The primary template that end users copy into their own repositories. All `[PROJECT-SPECIFIC]` markers are intentional placeholders — do **not** fill them in with real values unless directed. This file is the template, not an instance.

### AGENTS.python.md
A filled-in example for a Python project using `uv`, `pytest`, `ruff`, and `mypy`. Use this as a reference when updating the main template.

### .windsurf/hooks/policy_engine.py
The most complex hook. It performs scope-aware, diff-based policy validation across 9+ languages (Python, TypeScript, JavaScript, React, Vue, Java, Kotlin, Scala, Rust, Go). Reads from `AGENTS.md` in the target project.

### .windsurf/mcp_config.json
Two-tier MCP configuration:
- **Native (always-on)**: `fetch`, `git`, `github-mcp-server`, `memory`, `slack`, `sonarqube`, `terraform`
- **Docker-based (disabled by default)**: `jira`, `clickup`, `codecov`, `datadog`, `sentry`, `confluence`

Docker-based servers require `docker compose up -d <service>` before enabling in config.

---

## Commit Conventions

This repo uses **emoji-prefixed commit messages**:

| Emoji | Meaning |
|---|---|
| `✏️` | Update / modify existing content |
| `➕` | Add new content |
| `🔧` | Fix / repair |
| `🗑️` | Remove / delete |

Commits should be **atomic and focused**. Reference related files in the message when the change scope isn't obvious.

---

## How to Contribute / Make Changes

### Adding a new Skill
1. Create `.windsurf/skills/<skill-name>/SKILL.md`
2. Follow the structure of existing skills (trigger conditions, steps, outputs)
3. Reference the skill in `CONFIGURATION-OVERVIEW.md` if appropriate

### Adding a new Rule
1. Create a `.md` file in `.windsurf/memory/rules/` or `.windsurf/rules/`
2. Keep rules short, durable, and unambiguous
3. Rules in `memory/rules/` apply globally; rules in `rules/` are project-scoped

### Updating the AGENTS.md template
- Keep all `[PROJECT-SPECIFIC]` markers intact — they are instructions, not gaps
- Update `AGENTS.python.md` to reflect any new sections added to the template
- Ensure the examples in `examples/` remain consistent with the template structure

### Modifying Hooks
- Hooks in `.windsurf/hooks/` are copied to `~/.codeium/hooks/` on the user's machine during setup
- `.windsurf/hooks.json` configures when hooks fire (`post_write_code`, `pre_run_command`, `post_run_command`)
- Hook timeout is 30 seconds; `fail_on_error` is `false` (hooks warn, do not block)

### Updating MCP Configuration
- Native MCP servers go in `.windsurf/mcp_config.json`
- Docker-based optional servers go in `docker-compose.yml` + added as disabled entries in `mcp_config.json`
- Document any new server in `DOCKER-MCP-README.md`

---

## MCP Server Setup (for local development)

```bash
# Copy env template and fill in credentials
cp .env.example .env

# Start default MCP servers
docker compose up -d

# Start optional servers (e.g., JIRA)
docker compose --profile optional up -d mcp-jira
```

Native servers (`fetch`, `git`, `github-mcp-server`, `memory`, `slack`, `sonarqube`, `terraform`) use Docker and require credentials in `.env`.

---

## What NOT to Do

- Do not fill in `[PROJECT-SPECIFIC]` placeholders in `AGENTS.md` — it is a template
- Do not add project-specific logic to the hooks — they must remain generic
- Do not commit `.env` files (it is in `.gitignore`)
- Do not add language-specific rules to `global_rules.md` — put them in `rules/` subdirectories
- Do not hardcode credentials in `mcp_config.json` — use environment variable references

---

## No Build or Test Commands

This repository has no build system, test framework, or CI pipeline of its own. It is a configuration kit consumed by other projects. There are no commands to run to validate it beyond manual review.

---

## Documentation Map

| Document | Purpose |
|---|---|
| `README.md` | Installation steps and overall approach |
| `GETTING-STARTED.md` | 5-minute quick start, customization roadmap |
| `CONFIGURATION-OVERVIEW.md` | Full six-layer architecture reference |
| `DOCKER-MCP-README.md` | Docker MCP server setup and credential guide |
| `AGENTS.md` | Template for project-specific AI configuration |
| `AGENTS.python.md` | Worked example for Python projects |
| `.windsurf/hooks/README.md` | Hook scripts documentation |
