# SKILL.md — ticket-pickup-check

## Purpose
Before a dev-agent begins any implementation work, verify the target ticket
is in an acceptable state: correct workflow state ("Accepted"), no unresolved
blockers, no assignee conflict. Self-assign the ticket if all checks pass.

## Type
Auto-used. Invoked by `dev-agent` as the first action before any implementation
task. Must pass before `dev-impl-loop` begins.

## Do Not Assume
- Do not assume a ticket is ready just because it was handed to you.
- Do not assume no one else is working on it — always check the assignee field.
- Do not assume dependencies are resolved — check linked blocker tickets explicitly.
- Do not assume the ticket state is current — fetch fresh state from the tracker.

## Steps

### Check 1 — Ticket workflow state
1. Fetch the ticket's current state from the issue tracker (GitHub MCP or ClickUp MCP).
2. Acceptable states: "Accepted", "Ready for Dev", "In Sprint".
3. Unacceptable states: "New", "Open", "Backlog", "Blocked", "In Review", "Done", "Closed".
4. If the state is not acceptable: **stop immediately**.
   - Report to `dev-lead-agent` with the current state.
   - Do not begin implementation.

### Check 2 — Blocking dependencies
5. Fetch all "blocks" / "depends on" relationships from the ticket.
6. For each linked blocker ticket, check its current state.
7. If any blocker is not "Done" or "Closed": **stop immediately**.
   - List the specific blocking tickets and their states.
   - Report to `dev-lead-agent` to resolve the dependency.

### Check 3 — Assignee conflict
8. Read the ticket's current assignee field.
9. If the ticket is assigned to a named developer or another agent:
   - **Stop immediately.** Do not pick up a ticket already owned by someone else.
   - Report the conflict to `dev-lead-agent`.
10. If the ticket is unassigned: proceed to Check 4.

### Check 4 — Self-assign and state transition
11. Assign the ticket to the current agent session / developer identity.
12. Transition the ticket state to "In Progress".
13. Post a brief start comment on the ticket:
    ```
    Starting implementation — dev-agent session [timestamp].
    Branch: [branch-name]
    ```
14. **Bind the ticket reference** to the current session so all subsequent
    skills can resolve it without requiring the engineer to re-state it:
    ```bash
    # Write to the repo-local context file (committed to .gitignore)
    echo "[ticket-ref]" > .claude/.current-ticket

    # Also export for the current shell session
    export CLAUDE_CURRENT_TICKET="[ticket-ref]"
    ```
    If `CLAUDE_CURRENT_TICKET` is already set in the environment (e.g., from
    a CI pipeline), skip the file write — the env var takes precedence.
15. Write the initial workflow state file:
    ```bash
    bash ~/.claude/hooks/workflow-state.sh write \
      "[ticket-ref]" "dev-impl-loop" "0" "5" "in_progress"
    ```

## Output

```
## Ticket pickup check — [ticket reference]

| Check | Result | Detail |
|---|---|---|
| Workflow state | ✅ Accepted / ❌ [state] | [acceptable / reason blocked] |
| Blocker check | ✅ No blockers / ❌ Blocked | [blocker ticket refs if any] |
| Assignee check | ✅ Unassigned → self-assigned / ❌ Assigned to [name] | |

### Decision
- Proceed with implementation: yes / no
- Reason (if no): [reason]
- Next action (if no): escalate to dev-lead-agent
```

## Ticket context resolution (for all skills)

All skills that need the ticket reference resolve it in this order:
1. `$CLAUDE_CURRENT_TICKET` environment variable (set by CI or the engineer)
2. `.claude/.current-ticket` file in the repository root (written by this skill)
3. Prompt the engineer if neither is set

Skills should never hardcode a ticket ref. Use this pattern:
```bash
TICKET="${CLAUDE_CURRENT_TICKET:-$(cat .claude/.current-ticket 2>/dev/null || echo '')}"
if [[ -z "$TICKET" ]]; then
  echo "No active ticket context. Run ticket-pickup-check first." >&2
  exit 1
fi
```

Ensure `.claude/.current-ticket` is listed in `.gitignore` — it is session
state, not source code.

## Safe-Fix Guidance
- Never bypass the state check — implementing a "New" or "Backlog" ticket
  skips intake and decomposition, producing unreviewed work.
- If the assignee field shows a stale assignment (inactive user, old session),
  escalate to `dev-lead-agent` to resolve before self-assigning.
- If two parallel dev-agent instances attempt the same ticket simultaneously,
  the one that loses the assignee race must stop and report the conflict.
