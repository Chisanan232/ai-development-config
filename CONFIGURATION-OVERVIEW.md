# AI Development Configuration Kit — Complete Overview

This document provides a complete overview of both configuration kits in this repository.

## What is This Kit?

A **production-minded, generic-first configuration starter kit** for structuring AI-assisted software development. Two parallel kits are provided — one for Windsurf Cascade and one for Claude Code — both expressing the same engineering philosophy using each tool's native layers.

---

## Claude Code Configuration Kit

### Overview

The Claude Code kit lives under `claude-code-config/` and is designed from scratch for Claude Code's native configuration system. It uses shell-based hooks, `CLAUDE.md` as the project truth document, and Claude Code's Skills system.

### Directory Structure

```
claude-code-config/
├── CLAUDE.md                            # 13-section project truth template
├── settings.json                        # Hook wiring (PreToolUse / PostToolUse)
├── .mcp.json                            # MCP capability map
└── .claude/
    ├── hooks/
    │   ├── block_dangerous_commands.sh  # PreToolUse[Bash]: blocks rm -rf, force push, curl|bash, etc.
    │   ├── quality_gate.sh              # PostToolUse[Write|Edit]: debug detection, TODO hygiene, file size
    │   └── audit_log.sh                 # PostToolUse[Bash]: append-only JSONL audit log with rotation
    └── skills/
        ├── feature-implementation/SKILL.md   # Auto-used: test-first feature implementation (6 phases)
        ├── test-design/SKILL.md              # Auto-used: behavior-first test design
        ├── code-review-prep/SKILL.md         # Auto-used: pre-PR quality gate + description generation
        ├── ci-failure-triage/SKILL.md        # Auto-used: 6-phase CI failure triage
        ├── python-mypy-debugging/SKILL.md    # Auto-used: mypy error diagnosis and safe repair
        ├── python-ruff-fixing/SKILL.md       # Auto-used: ruff violation fixing with auto-fix review
        ├── python-precommit-repair/SKILL.md  # Auto-used: pre-commit repair without --no-verify
        ├── pr-readiness/SKILL.md             # Command-like (/pr-readiness): full PR readiness checklist
        ├── release-readiness/SKILL.md        # Command-like (/release-readiness): release gate checklist
        └── dependency-upgrade-review/SKILL.md # Command-like: dependency upgrade risk classification
```

### Key Differences from Windsurf Cascade Kit

| Aspect | Windsurf Cascade | Claude Code |
|--------|-----------------|-------------|
| Project truth | `AGENTS.md` | `CLAUDE.md` |
| Config directory | `.windsurf/` | `.claude/` |
| Hook language | Python (`.py`) | Shell (`.sh`) |
| Hook trigger config | `.windsurf/hooks.json` | `settings.json` (PreToolUse/PostToolUse) |
| Hook triggers | `post_write_code`, `pre_run_command` | `PreToolUse[Bash]`, `PostToolUse[Write\|Edit\|Bash]` |
| Workflows | `.windsurf/workflows/*.md` | Command-like skills (`/pr-readiness`, etc.) |
| Rules | `.windsurf/rules/*.md` | Inline sections in `CLAUDE.md` |
| MCP config | `.windsurf/mcp_config.json` | `.mcp.json` |

### CLAUDE.md Sections

The `CLAUDE.md` template covers 13 sections:

1. Repository Identity
2. Architecture Constraints
3. Package and Build Commands
4. Safe Implementation Policy
5. Testing Expectations
6. Type Checking Policy
7. Linting and Formatting Policy
8. Commit Policy
9. Pull Request Policy
10. CI/CD Triage Expectations
11. Source-of-Truth Systems
12. MCP-Backed Systems
13. Skill Invocation Guide and Hard Limits

### Hook Wiring (settings.json)

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": ".claude/hooks/block_dangerous_commands.sh" }] }
    ],
    "PostToolUse": [
      { "matcher": "Write|Edit", "hooks": [{ "type": "command", "command": ".claude/hooks/quality_gate.sh" }] },
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": ".claude/hooks/audit_log.sh" }] }
    ]
  }
}
```

### MCP Capability Map (.mcp.json)

| Server | Capabilities | Default State |
|--------|-------------|---------------|
| `github-mcp-server` | `code_repository`, `issue_tracking` | Active |
| `fetch` | Web and URL fetching | Active |
| `sonarqube` | `static_analysis` | Disabled |
| `codecov` | `coverage_reporting` | Disabled |
| `slack` | `communication` | Disabled |
| `datadog` | `observability` | Disabled |

---

## Windsurf Cascade Configuration Kit

A **production-minded, generic-first Windsurf Cascade configuration starter kit** for structuring AI-assisted software development.

## Architecture

### Six-Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│                        AGENTS.md                            │
│              Project Truth & Declarative Context            │
│  (languages, tools, commands, conventions, structure)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                          Rules                              │
│            Short, Durable Behavioral Constraints            │
│     (coding standards, testing policy, commit policy)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                          Skills                             │
│           Procedural Strategy & Reusable Methods            │
│   (feature implementation, test design, CI triage)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                       MCP Servers                           │
│         External Capability Providers & Data Access         │
│  (GitHub, Slack, SonarQube, Codecov, JIRA, observability)  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        Workflows                            │
│              Manually Triggered Runbooks                    │
│    (PR readiness, release readiness, dep upgrades)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                          Hooks                              │
│          Enforcement, Interception & Auditing               │
│   (quality gate, dangerous commands, audit logging)         │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer           | Purpose                    | Examples                          | When to Use                 |
|-----------------|----------------------------|-----------------------------------|-----------------------------|
| **AGENTS.md**   | Project truth              | Languages, tools, commands        | Facts about the project     |
| **Rules**       | Behavioral constraints     | Coding standards, testing policy  | Always-on constraints       |
| **Skills**      | Procedural strategies      | Feature implementation, CI triage | Multi-step procedures       |
| **MCP Servers** | External capability access | GitHub, Slack, SonarQube, Codecov | Access to external systems  |
| **Workflows**   | Manual runbooks            | PR readiness, release checklist   | Manual milestone checklists |
| **Hooks**       | Automated enforcement      | Quality gate, command blocking    | Automated validation        |

## Complete File Structure

```
your-repository/
├── AGENTS.md                                    # Root project context
├── GETTING-STARTED.md                           # Quick start guide
├── CONFIGURATION-OVERVIEW.md                    # This file
├── README.md                                    # Installation guide
│
├── .windsurf/                                   # Windsurf configuration
│   ├── rules/                                   # Behavioral constraints
│   │   ├── coding-standards.md
│   │   ├── testing-policy.md
│   │   ├── commit-policy.md
│   │   ├── pr-policy.md
│   │   └── ci-policy.md
│   │
│   ├── skills/                                  # Reusable procedures
│   │   ├── feature-implementation/
│   │   │   └── SKILL.md
│   │   ├── test-design/
│   │   │   └── SKILL.md
│   │   ├── code-review-prep/
│   │   │   └── SKILL.md
│   │   ├── ci-failure-triage/
│   │   │   └── SKILL.md
│   │   ├── coverage-regression-repair/
│   │   │   └── SKILL.md
│   │   ├── python-mypy-debugging/
│   │   │   └── SKILL.md
│   │   ├── python-ruff-fixing/
│   │   │   └── SKILL.md
│   │   └── python-precommit-repair/
│   │       └── SKILL.md
│   │
│   ├── workflows/                               # Manual runbooks
│   │   ├── pr-readiness.md
│   │   ├── release-readiness.md
│   │   └── dependency-upgrade-review.md
│   │
│   └── hooks.json                               # Hook configuration
│
├── hooks/                                       # Hook scripts
│   ├── quality_gate.py
│   ├── block_dangerous_commands.py
│   ├── audit_log.py
│   └── README.md
│
├── docs/                                        # Documentation
│   ├── architecture-rationale.md
│   ├── customization-guide.md
│   ├── language-overlays.md
│   ├── mcp-integration.md
│   └── mcp-setup-guide.md
│
└── examples/                                    # Example configurations
    ├── mcp_config.json                          # Example MCP configuration
    ├── backend/
    │   └── AGENTS.md
    ├── frontend/
    │   └── AGENTS.md
    └── infra/
        └── AGENTS.md
```

## Component Inventory

### Core Components (Required)

| Component        | Location                              | Purpose                   | Customize?          |
|------------------|---------------------------------------|---------------------------|---------------------|
| Root AGENTS.md   | `/AGENTS.md`                          | Project truth             | **YES** (essential) |
| Coding Standards | `.windsurf/rules/coding-standards.md` | Code quality expectations | Review              |
| Testing Policy   | `.windsurf/rules/testing-policy.md`   | Testing requirements      | Review              |
| Commit Policy    | `.windsurf/rules/commit-policy.md`    | Commit conventions        | Review              |
| PR Policy        | `.windsurf/rules/pr-policy.md`        | PR requirements           | Review              |
| CI Policy        | `.windsurf/rules/ci-policy.md`        | CI/CD expectations        | Review              |

### Generic Skills (Reusable)

| Skill                      | Purpose                       | Language-Agnostic? |
|----------------------------|-------------------------------|--------------------|
| feature-implementation     | Implement new features safely | ✓ Yes              |
| test-design                | Design comprehensive tests    | ✓ Yes              |
| code-review-prep           | Prepare PRs for review        | ✓ Yes              |
| ci-failure-triage          | Diagnose and fix CI failures  | ✓ Yes              |
| coverage-regression-repair | Fix coverage regressions      | ✓ Yes              |

### Language-Specific Skills (Python)

| Skill                   | Purpose                 | Language |
|-------------------------|-------------------------|----------|
| python-mypy-debugging   | Fix MyPy type errors    | Python   |
| python-ruff-fixing      | Fix Ruff linting issues | Python   |
| python-precommit-repair | Fix pre-commit failures | Python   |

### Workflows (Manual Checklists)

| Workflow                  | Purpose                   | When to Use          |
|---------------------------|---------------------------|----------------------|
| pr-readiness              | Ensure PR is complete     | Before submitting PR |
| release-readiness         | Ensure release is ready   | Before releasing     |
| dependency-upgrade-review | Review dependency updates | When upgrading deps  |

### Hooks (Automated)

| Hook                        | Purpose                    | Blocking? |
|-----------------------------|----------------------------|-----------|
| quality_gate.py             | Lightweight quality checks | No        |
| block_dangerous_commands.py | Block dangerous commands   | Yes       |
| audit_log.py                | Log command execution      | No        |

### Documentation

| Document                  | Purpose                    | Audience                |
|---------------------------|----------------------------|-------------------------|
| GETTING-STARTED.md        | Quick start guide          | New users               |
| CONFIGURATION-OVERVIEW.md | Complete overview          | All users               |
| architecture-rationale.md | Design decisions           | Advanced users          |
| customization-guide.md    | How to customize           | Maintainers             |
| language-overlays.md      | Language-specific guidance | Multi-language projects |
| mcp-integration.md        | MCP architecture & design  | All users               |
| mcp-setup-guide.md        | MCP setup walkthrough      | New users               |

## Customization Priority

### Priority 1: Essential (Do First)

1. **Fill in AGENTS.md** with project specifics
2. **Verify commands** work in your environment
3. **Set coverage threshold** for your project
4. **Define commit style** for your team
5. **Locate PR template** in your repository
6. **Configure MCP servers** for essential systems (GitHub, Slack) - see `docs/mcp-setup-guide.md`

**Time: 1-2 hours (including MCP setup)**

### Priority 2: Review (Do Soon)

1. **Review all Rules** and adjust if needed
2. **Review all Skills** and add project notes
3. **Test configuration** with Windsurf Cascade
4. **Gather team feedback** on initial setup

**Time: 2 hours**

### Priority 3: Enhance (Do Later)

1. **Add project-specific Rules** if needed
2. **Add project-specific Skills** if needed
3. **Customize Workflows** for your process
4. **Tune Hooks** for your environment

**Time: 4 hours**

### Priority 4: Iterate (Ongoing)

1. **Monitor usage** and gather feedback
2. **Adjust based on pain points**
3. **Add missing pieces** as discovered
4. **Remove unused components**

**Time: 1 hour/month**

## Usage Patterns

### Pattern 1: Feature Development

```
1. Developer starts feature work
2. Windsurf Cascade invokes feature-implementation skill
3. Skill consults AGENTS.md for project conventions
4. Skill follows coding-standards and testing-policy rules
5. Developer writes code with AI assistance
6. quality_gate hook runs after code is written
7. Developer uses code-review-prep skill before PR
8. Developer runs pr-readiness workflow
9. Developer submits PR
```

### Pattern 2: CI Failure Repair

```
1. CI fails on PR
2. Developer asks Windsurf Cascade to fix
3. Cascade invokes ci-failure-triage skill
4. Skill identifies failure type (test, lint, type)
5. Skill invokes language-specific skill if needed
6. Skill fixes issue following safe implementation policy
7. Developer commits fix with appropriate message
8. CI passes
```

### Pattern 3: Release Preparation

```
1. Developer ready to release
2. Developer runs /release-readiness workflow
3. Workflow guides through checklist
4. Developer verifies all steps complete
5. Developer creates release
6. Developer deploys to production
7. Developer monitors post-release
```

## Configuration Modes

### Mode 1: Minimal (Starter)

**Includes:**
- Root AGENTS.md (customized)
- Core Rules (as-is)
- Generic Skills (as-is)
- No Hooks

**Best for:**
- Small teams
- Simple projects
- Getting started

### Mode 2: Standard (Recommended)

**Includes:**
- Root AGENTS.md (customized)
- Core Rules (reviewed)
- Generic Skills (reviewed)
- Core Workflows (reviewed)
- Lightweight Hooks (quality_gate only)

**Best for:**
- Most projects
- Medium teams
- Production use

### Mode 3: Advanced (Full)

**Includes:**
- Root AGENTS.md (customized)
- Directory-scoped AGENTS.md (customized)
- Core Rules (customized)
- Generic + Project-specific Skills
- Core + Project-specific Workflows
- All Hooks (tuned)

**Best for:**
- Large projects
- Large teams
- Complex requirements

## Language Support

### Fully Supported

- **Python**: Complete skill set (mypy, ruff, pre-commit)
- **TypeScript/JavaScript**: Generic skills apply
- **Rust**: Generic skills apply
- **Java**: Generic skills apply
- **Go**: Generic skills apply

### Adding Language Support

See `docs/language-overlays.md` for:
- Python overlay
- TypeScript/JavaScript overlay
- Rust overlay
- Java overlay
- Go overlay

## Global vs Project Configuration

### Global Configuration (~/.codeium/windsurf/)

**Put here:**
- Personal coding preferences
- Cross-project skills
- General engineering heuristics
- Language-agnostic guidelines

**Example:**
```
~/.codeium/windsurf/
├── memories/
│   └── global_rules.md
└── skills/
    ├── feature-implementation/
    ├── test-design/
    └── code-review-prep/
```

### Project Configuration (repository/.windsurf/)

**Put here:**
- Project-specific facts (AGENTS.md)
- Project-specific rules
- Project-specific skills
- Project-specific workflows
- Project-specific hooks

**Example:**
```
your-repo/.windsurf/
├── rules/
├── skills/
├── workflows/
└── hooks.json
```

## Maintenance Schedule

### Daily
- Update AGENTS.md if tools change
- Add project-specific notes to skills as discovered

### Weekly
- Review audit logs
- Tune hook performance if needed

### Monthly
- Review which skills are used most
- Gather team feedback
- Adjust based on pain points

### Quarterly
- Review all rules
- Update skills for process changes
- Refresh workflows
- Clean up unused components

## Success Metrics

### Configuration Quality

- [ ] AGENTS.md is complete and accurate
- [ ] All commands in AGENTS.md work
- [ ] Team understands the configuration
- [ ] AI tool follows configuration consistently

### Usage Metrics

- [ ] Skills are invoked regularly
- [ ] Workflows are followed
- [ ] Hooks provide useful feedback
- [ ] Team finds configuration helpful

### Outcome Metrics

- [ ] Faster feature development
- [ ] Fewer CI failures
- [ ] More consistent code quality
- [ ] Easier onboarding

## Common Questions

### Q: Do I need to use everything?

**A:** No. Start with AGENTS.md and core Rules. Add more as needed.

### Q: Can I modify the generic skills?

**A:** Yes, but prefer adding project-specific notes over modifying the generic content.

### Q: What if my language isn't supported?

**A:** Generic skills work for all languages. Add language-specific skills as needed. See `docs/language-overlays.md`.

### Q: Are hooks required?

**A:** No. Hooks are optional. Start without them and add later if needed.

### Q: How do I disable a component?

**A:** 
- Rules: Remove or comment out
- Skills: Delete the directory
- Workflows: Delete the file
- Hooks: Comment out in hooks.json

### Q: Can I use this with multiple languages?

**A:** Yes. Use directory-scoped AGENTS.md and clearly named language-specific skills.

### Q: How do I share configuration across repositories?

**A:** Use global configuration for cross-project skills and rules. Keep project-specific configuration in each repository.

## Troubleshooting

### Issue: AI tool not following configuration

**Solution:**
1. Verify AGENTS.md is in repository root
2. Check all [PROJECT-SPECIFIC] markers are filled
3. Verify commands work
4. Test with simple request

### Issue: Hooks failing or slow

**Solution:**
1. Check hook logs
2. Increase timeout in hooks.json
3. Disable expensive hooks
4. Adjust cooldown period

### Issue: Configuration too complex

**Solution:**
1. Remove unused components
2. Simplify workflows
3. Consolidate rules
4. Start with minimal mode

### Issue: Team not using configuration

**Solution:**
1. Gather feedback
2. Simplify if too complex
3. Add training/documentation
4. Iterate based on needs

## Next Steps

1. **Read GETTING-STARTED.md** for quick start
2. **Customize AGENTS.md** for your project
3. **Review docs/** for detailed guidance
4. **Test with Windsurf Cascade**
5. **Gather feedback and iterate**

## Resources

- **GETTING-STARTED.md**: Quick start guide
- **docs/architecture-rationale.md**: Why this architecture
- **docs/customization-guide.md**: How to customize
- **docs/language-overlays.md**: Language-specific guidance
- **examples/**: Example configurations
- **hooks/README.md**: Hook documentation

## Summary

This configuration kit provides:

✓ **Complete structure** for AI-assisted development
✓ **Generic-first design** for reusability
✓ **Clear separation** of concerns
✓ **Comprehensive documentation**
✓ **Production-ready** components
✓ **Easy customization**

**Start simple, iterate based on usage, keep AGENTS.md up to date.**

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**License:** MIT
