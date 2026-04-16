# AI Development Config

Multi-tool AI coding assistant configuration kit supporting Claude Code, Codex CLI,
Windsurf Cascade, and GitHub Copilot.

## Quick install

```bash
# Clone the repo
git clone https://github.com/Chisanan232/ai-development-config.git
cd ai-development-config

# Install for your tool
python install.py --tool claude-code   # global: ~/.claude/
python install.py --tool codex         # global: ~/.codex/
python install.py --tool windsurf      # per-project: ./.windsurf/
python install.py --tool copilot       # per-project: ./.github/ + ./.copilot/

# Preview without writing
python install.py --all --dry-run
```

## What this is

Each tool gets a configuration kit designed for its own interaction model — not a
weaker or stronger copy of the others. See [Architecture](architecture.md) for the
full design rationale and [Getting Started](getting-started.md) for setup steps.
