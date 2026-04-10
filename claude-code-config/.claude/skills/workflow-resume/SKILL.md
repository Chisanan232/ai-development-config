# SKILL.md — workflow-resume

## Purpose
Recover an interrupted agent session. Read the persisted workflow state file,
determine which phase was interrupted, validate the current environment matches
the expected state, and re-enter the workflow at the correct point.

## Type
Command-like. Invoked explicitly via `/workflow-resume [ticket-ref]` when a
session is interrupted (crash, context limit, manual stop) and needs to continue.

## Do Not Assume
- Do not assume the last-written workflow state reflects actual file system state.
  Verify both.
- Do not assume the branch is clean — check git status before resuming.
- Do not re-run completed phases — read the state file to find the resume point.
- Do not resume if the circuit breaker is open — check first.

## Steps

### Phase 1 — Read persisted state
1. Resolve the ticket reference:
   ```bash
   TICKET="${CLAUDE_CURRENT_TICKET:-$(cat .claude/.current-ticket 2>/dev/null || echo '[ticket-ref]')}"
   ```
2. Read the workflow state file for the target ticket:
   ```bash
   bash ~/.claude/hooks/workflow-state.sh read "$TICKET"
   ```
   Expected output fields: `workflow`, `step`, `total_steps`, `status`, `timestamp`.
3. If no state file exists:
   - Report: "No workflow state found for $TICKET."
   - Do not guess the resume point. Ask the engineer which phase to enter.
4. If `status` is "complete":
   - Report: "Workflow for $TICKET is already marked complete."
   - Verify the PR was opened and ticket was closed. If not, escalate.
5. **If `status` is "escalated"**: surface this prominently before any other step.
   ```
   ⚠️  UNRESOLVED ESCALATION — do not resume until this is addressed.

   Ticket:       $TICKET
   Escalated at: [timestamp from state file]
   Reason:       [escalation_reason from state file]

   Required action before resuming:
   1. Read the escalation reason above.
   2. Resolve the root cause (e.g., reset circuit breaker, clarify requirements).
   3. Run: bash ~/.claude/hooks/circuit-breaker-gate.sh reset $TICKET
   4. Then re-run /workflow-resume $TICKET
   ```
   Do NOT proceed past this step until the engineer confirms resolution.
6. If `status` is "circuit_open":
   - Surface the same block as above.
   - Confirm circuit breaker has been manually reset before resuming.

### Phase 2 — Environment verification
7. Confirm the circuit breaker for this ticket is in "closed" state:
   ```bash
   bash ~/.claude/hooks/circuit-breaker-gate.sh check "$TICKET"
   ```
   If open: stop. Surface the same escalation block from Phase 1, step 5.
8. Confirm the git branch matches the ticket's expected branch:
   ```bash
   git branch --show-current
   ```
9. Run `git fetch && git status` to confirm the branch is clean and not behind.
10. If the working tree is dirty: identify the uncommitted changes.
    - If they look like in-progress work from the interrupted session:
      review with the engineer before discarding or committing.
    - Do not run `git clean` or `git reset --hard` without explicit confirmation.

### Phase 3 — Determine resume point
8. Map the recorded `step` and `workflow` to the correct phase:

   For `dev-impl-loop`:
   | step | Resume action |
   |---|---|
   | 0 | Re-enter Phase 0 (env verify) |
   | 1 | Re-enter Phase 1 (ralph loop — check what's implemented vs acceptance criteria) |
   | 2 | Re-enter Phase 2 (full test suite) |
   | 3 | Re-enter Phase 3 (pre-commit) |
   | 4 | Re-enter Phase 4 (QA handoff — check if QA verdict arrived) |
   | 5 | Re-enter Phase 5 (post-QA: open PR or re-loop) |

   For other workflows: use the workflow's own phase-to-step mapping.

9. Before re-entering, list what was already completed in this session:
   ```
   Resuming [ticket-ref] at step [N] of [total].
   Completed: phases 0..N-1
   Resuming: phase [N] — [phase description]
   ```

### Phase 4 — Resume execution
10. Re-invoke the appropriate skill or phase directly.
    Do not restart from Phase 0 unless the environment check (Phase 2 of this
    skill) revealed the branch has been reset or re-created.
11. Update the workflow state to reflect the resumed session:
    ```bash
    bash ~/.claude/hooks/workflow-state.sh write \
      "[ticket-ref]" "[workflow]" "[step]" "[total]" "in_progress"
    ```

## Output

```
## Workflow resume — [ticket-ref]

| Check | Result |
|---|---|
| State file found | ✅ / ❌ not found |
| Circuit breaker | ✅ closed / ❌ open |
| Branch | ✅ [branch-name] / ❌ mismatch |
| Working tree | ✅ clean / ⚠️ dirty — [files] |

### Resume point
- Workflow: [workflow name]
- Step: [N] of [total]
- Phase: [phase description]
- Action: re-entering phase [N]
```

## Safe-Fix Guidance
- If the state file says step 2 but no tests were committed, re-enter at step 1
  after confirming with the engineer — state files can be stale if a crash
  happened mid-write.
- If the branch was deleted or recreated, treat this as a fresh start and run
  `ticket-pickup-check` again.
- Do not resume a workflow if the ticket has been reassigned to another developer
  — report the conflict to `dev-lead-agent`.
