# Claude Code Engineering Agent System — Design Reference

This document covers the design rationale, architectural decisions, and known
trade-offs behind the Claude Code engineering agent system introduced in the
`claude-code-config/` upgrade. It is a companion to `CONFIGURATION-OVERVIEW.md`.

---

## 1. Design Philosophy

### Why a five-layer model?

The Claude Code kit mirrors the same engineering philosophy as the Windsurf Cascade
kit, but expressed in Claude Code's native vocabulary:

| Windsurf Layer | Claude Code Equivalent | Purpose |
|---|---|---|
| AGENTS.md | CLAUDE.md | Project truth + durable policy |
| Rules | CLAUDE.md sections | Behavioral constraints |
| Skills | `.claude/skills/` | Reusable multi-step procedures |
| MCP config | `.mcp.json` | External capability access |
| Hooks | `.claude/hooks/` + `settings.json` | Automated enforcement |

The Claude Code kit adds a **sixth layer not present in the Windsurf kit**: the
**role layer** (`.claude/agents/`), which provides sub-agent specialization for
complex multi-step engineering tasks.

### Core design concerns

**Concern 1 — Responsibility collapse**
When a single AI session handles ticket intake, implementation, testing, PR
management, and release, it inevitably makes trade-offs that collapse into
"just get it done." Specialized agents enforce strict scope boundaries, making
collapses visible as explicit delegation failures rather than silent drift.

**Concern 2 — Context contamination**
A session that has written 500 lines of implementation code thinks differently
about acceptance criteria than one that reads only the requirement and tests.
The `qa-agent` is deliberately isolated from implementation context.

**Concern 3 — Feedback loop safety**
Automated loops (PR polling, bot PR maintenance, release watching) can become
infinite self-repair cycles if agents are allowed to trigger other agents or
invoke repair skills without human checkpoints. The skill-first polling design
and hook gate-not-loop principle address this directly.

---

## 2. Agent Design Rationale

### Why four agents?

The split is derived from the four distinct cognitive modes in software engineering:

```
┌─────────────────┬────────────────────────────────────────────────┐
│ Agent           │ Cognitive mode                                  │
├─────────────────┼────────────────────────────────────────────────┤
│ dev-lead-agent  │ Strategic: what to build, when, in what order  │
│ dev-agent       │ Tactical: how to build it correctly            │
│ qa-agent        │ Skeptical: does it actually work as expected?  │
│ release-agent   │ Observational: did the automation succeed?     │
└─────────────────┴────────────────────────────────────────────────┘
```

Each mode is adversarial to the others in healthy engineering:
- The strategist wants to ship fast; the skeptic wants to slow down and verify.
- The implementer believes the code is correct; the skeptic assumes it is not.
- The observer doesn't care how the code was written; it only cares about outcomes.

Collapsing these modes into one session removes the natural tension.

### dev-lead-agent — design rationale

**Why it exists:** Complex tickets arrive as ambiguous intent. Without a
dedicated decomposition step, Claude Code starts writing code based on the
first plausible interpretation. The `dev-lead-agent` forces a clarification
and planning step before any code is written.

**Key design decision:** `dev-lead-agent` is the only agent that may make merge
decisions. This creates a single authorization point for repository mutation.

**Design concern — authority creep:** If `dev-lead-agent` starts writing code
"just to unblock" `dev-agent`, it defeats the separation. The agent's "What this
agent must not do" section enforces this boundary explicitly.

**Design concern — stale decomposition:** Task decompositions can go stale if
a dependency changes mid-sprint. `dev-lead-agent` should be re-invoked (not
`dev-agent`) when the plan needs replanning.

### dev-agent — design rationale

**Why it exists:** Implementation is a focused, narrow task. Giving an implementer
agent access to orchestration decisions (ticket state, PR merges) creates
temptation to shortcut: "I'll just merge this myself since it looks fine."

**Key design decision:** `dev-agent` runs the full validation sequence before
marking work done. It does not hand off to `qa-agent` prematurely.

**Design concern — validation skipping:** Under time pressure, `dev-agent` may
try to skip steps 1–3 of the validation sequence and jump to "done." The
`full-test-gate.sh` and `precommit-gate.sh` hooks enforce this mechanically.

**Design concern — scope creep during repair:** When CI fails, `dev-agent` may
expand the fix beyond the minimal change. The skill's Safe-Fix Guidance section
constrains this explicitly.

### qa-agent — design rationale

**Why it exists:** An agent that just implemented a feature will subconsciously
validate the implementation rather than the requirement. `qa-agent` reads the
requirement first and derives expected behavior independently.

**Key design decision:** `qa-agent` produces a structured verdict (ready/blocked
with reasons), not a vague "looks good." `dev-lead-agent` acts on the verdict,
not on `qa-agent`'s judgment about whether to merge.

**Design concern — happy-path bias:** Without explicit adversarial and boundary
scenarios in the skill, `qa-agent` will default to validating only the happy path.
The `acceptance-validation` skill forces adversarial scenario coverage.

**Design concern — blocking without action:** If `qa-agent` produces a "blocked"
verdict with uncovered edge cases, `dev-agent` needs a concrete list to act on.
The structured output format in `acceptance-validation` enforces this.

### release-agent — design rationale

**Why it is thin by design:** The external release workflow (automated tag
creation, version bumping, changelog generation) owns the release mechanics.
A thick release agent would duplicate and potentially conflict with that workflow.

**Key design decision:** `release-agent` observes and summarizes. It does not
pull levers. This makes it safe to run in a loop during a release window without
risk of double-triggering.

**Design concern — false confidence:** If the pipeline is stuck (no progress for
30+ minutes), a naive observer may report "in progress" indefinitely. The
`release-watch` skill has an explicit timeout threshold and escalation rule.

**Design concern — premature summary:** `release-agent` must not produce a
success summary until the tag is confirmed and artifacts are accessible. Checking
only that the pipeline completed is not sufficient.

---

## 3. Skill Design Rationale

### Why skills rather than agent capabilities?

Skills are reusable across agents. `dev-lead-agent` uses `pr-health-check`,
but so can an engineer invoking `/pr-health-check` directly. If PR health-check
logic lived inside the agent definition, it would be unreachable from the command
interface.

Skills also isolate concerns better: the skill carries the "how," the agent
carries the "who decides what to do with the result."

### New skill design concerns

**`task-decomposition`**
- Concern: Decomposition is only as good as the acceptance criteria. If criteria
  are missing, the skill must stop and ask rather than infer. Inferring wrong
  acceptance criteria leads to technically complete but behaviorally wrong work.
- Concern: Dependency ordering is easy to get wrong. The output format enforces
  explicit "depends on: N" markers rather than leaving ordering implicit.

**`acceptance-validation`**
- Concern: "All tests pass" is not the same as "acceptance criteria are met."
  Tests often verify implementation assumptions, not requirement fulfillment.
  The skill forces re-derivation of expected behavior from the requirement, not
  from the test suite.
- Concern: Adversarial scenarios are easy to skip. The skill makes them a
  named mandatory phase, not an optional afterthought.

**`pr-health-check`**
- Concern: Classification must be deterministic. A PR classified as
  `ready-to-merge` must meet all Auto-Merge Policy conditions, not a subjective
  assessment of "looks ready."
- Concern: Stale PR handling requires a comment before closure. Silent closures
  break contributor trust.

**`bot-pr-maintainer`**
- Concern: The two-rebase-attempt limit prevents infinite rebase loops. After
  two failures, the bot PR is escalated to the engineer.
- Concern: A bot PR with CI failure caused by the update itself must never be
  merged, even if it later becomes green through unrelated CI flakiness. The
  skill requires re-classification at each poll cycle.

**`release-preparation`**
- Concern: The skill must not create a git tag. The automated workflow owns
  tagging. If the skill creates a tag, the workflow will either fail (tag exists)
  or produce a duplicate.

**`release-watch`**
- Concern: "Pipeline completed" is not the same as "release succeeded." The skill
  must verify the tag was created and artifacts are accessible before declaring
  success.

---

## 4. Further Reading

| Document | What it covers |
|---|---|
| `CONFIGURATION-OVERVIEW.md` | Full directory structure, hook wiring, MCP map |
| `claude-code-config/CLAUDE.md` | All 20 policy sections — the durable constitution |
| `claude-code-config/.claude/agents/dev-lead-agent.md` | Full dev-lead-agent responsibilities |
| `claude-code-config/.claude/agents/dev-agent.md` | Full dev-agent responsibilities |
| `claude-code-config/.claude/agents/qa-agent.md` | Full qa-agent responsibilities |
| `claude-code-config/.claude/agents/release-agent.md` | Full release-agent responsibilities |
| `docs/architecture-rationale.md` | Windsurf Cascade layer model rationale |
| `docs/mcp-integration.md` | MCP capability model and integration guidance |
