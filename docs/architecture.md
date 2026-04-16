# Architecture

## Overview

This repo provides configuration kits for four AI coding assistant tools, each designed
from its own interaction paradigm — not as weaker or stronger copies of each other.

## Tool tiers

| Tier | Tool | Interaction model | Who drives |
|---|---|---|---|
| 1A — Autonomous agent | Claude Code | CLI; full autonomous dev cycles, multi-agent orchestration, hooks | AI drives, human sets direction |
| 1B — Autonomous agent | Codex CLI | CLI; autonomous execution, MCP, skills | AI drives, human delegates tasks |
| 2 — IDE collaborative | Windsurf Cascade | IDE dock; developer always present | Human drives, AI assists each step |
| 3 — Reactive inline | GitHub Copilot | IDE inline; autocomplete + chat | Human drives everything, AI reacts |

## What `shared/` contains

Only content that **humans consume** regardless of which tool produced it:

- `coding-standards.md` — what good code looks like
- `commit-policy.md` — commit message format (humans read git log)
- `pr-policy.md` — PR format (humans review PRs)
- `branch-naming.md` — branch naming convention
- `testing-philosophy.md` — test design principles

Everything about *how the AI works* is tier-specific and lives inside each tool's own
directory. The AI tools never know `shared/` exists — `install.py` copies shared
content into each tool's directory at install time.

## Directory structure

```
ai-development-config/
├── shared/                    ← universal policies (distribution source)
├── tools/
│   ├── claude-code/.claude/   ← Tier 1A: agents, skills, hooks, MCP
│   ├── codex/.codex/          ← Tier 1B: instructions, skills, hooks, MCP
│   ├── windsurf/.windsurf/    ← Tier 2: rules, skills, workflows, MCP
│   └── copilot/               ← Tier 3: instructions, policy files
├── install.py                 ← distribution script (Python stdlib only)
├── Makefile                   ← CI sync and lint targets
├── pyproject.toml             ← dev tooling (ruff, mypy, isort, mkdocs)
└── mkdocs.yml                 ← documentation site config
```

## Install scope

Claude Code and Codex install **globally** (like shell config, applied to all projects).
Windsurf and Copilot install **per-project** (the tool reads from the project root).

| Tool | Install target |
|---|---|
| Claude Code | `~/.claude/` |
| Codex CLI | `~/.codex/` |
| Windsurf | `<project>/.windsurf/` |
| Copilot | `<project>/` |

## Why Codex is Tier 1B, not Tier 2

Codex CLI is an autonomous agentic tool with MCP support, file system access, and
command execution capability — a peer of Claude Code. Its config warrants the same
architectural depth: behavioral instructions, MCP configuration, skills, and hooks.
Windsurf Cascade, by contrast, always has a developer watching each suggestion in real
time; it needs guidance, not autonomous enforcement.
