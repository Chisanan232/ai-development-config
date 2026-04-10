# SKILL.md — task-decomposition

## Purpose
Translate a high-level ticket or requirement into a concrete, ordered list of
implementation steps with clear dependency relationships and agent assignments.

## Type
Auto-used. `dev-lead-agent` invokes this skill when a new ticket or task arrives.

## Do Not Assume
- Do not assume the requirement is self-contained — check for cross-cutting concerns.
- Do not assume the current implementation is correct — read the relevant code first.
- Do not assume dependencies between tasks are obvious — make them explicit.
- Do not assume a single agent should handle everything — assign appropriately.

## Steps

### Phase 1 — Requirement intake
1. Read the ticket description in full.
2. Identify the acceptance criteria. If none are stated, draft them and confirm
   with the engineer before continuing.
3. Identify the affected system areas (services, packages, files, APIs).
4. Identify external dependencies: APIs, data stores, infrastructure, third-party services.

### Phase 2 — Constraint mapping
5. Check the CLAUDE.md Architecture Constraints section for any rules that apply.
6. Identify any performance, security, or compatibility constraints not stated in the ticket.
7. Identify any configuration or environment changes required (new env vars, flags, etc.).
8. Note any migrations, schema changes, or breaking API changes.

### Phase 3 — Task breakdown
9. Break the work into the smallest logical steps that can each be implemented and
   tested independently.
10. Order the steps by dependency: no step should depend on a later step.
11. For each step, state:
    - What changes
    - What tests will be added
    - Which agent should execute it (`dev-agent`, `qa-agent`, or direct action)
    - Whether it can be parallelized with any other step

### Phase 4 — Output
12. Produce the decomposition as a numbered task list.
13. Mark each task with its assigned agent.
14. Identify the critical path (the minimum sequence required to reach a shippable state).
15. Post the decomposition as a comment on the ticket if issue-tracking MCP is available.

## Output format

```
## Task decomposition — [ticket reference]

### Acceptance criteria
- [ ] [criterion 1]
- [ ] [criterion 2]

### Tasks
1. [dev-agent] [task description] — depends on: none
2. [dev-agent] [task description] — depends on: 1
3. [qa-agent] [validate behavior X] — depends on: 2
4. [dev-lead-agent] [PR review and merge decision] — depends on: 3

### Critical path
1 → 2 → 3 → 4

### Parallelizable
Tasks [X] and [Y] can run concurrently after task [Z] completes.
```

## Safe-Fix Guidance
- If the requirement is ambiguous, stop and ask. Do not decompose an ambiguous ticket.
- If the decomposition reveals a hidden dependency on an incomplete feature, surface it
  to the engineer before handing off to `dev-agent`.
