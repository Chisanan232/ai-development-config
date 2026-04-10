# SKILL.md — dev-impl-loop

## Purpose
Drive a single ticket through the full implementation cycle using a ralph loop:
implement → run relative tests → iterate until green → full test suite →
pre-commit → explicit QA handoff. Provides a defined entry point, exit
condition, and circuit breaker threshold for every iteration phase.

## Type
Auto-used. Invoked by `dev-agent` immediately after `ticket-pickup-check` passes.

## Do Not Assume
- Do not assume the branch is current — pull before writing any code.
- Do not assume relative tests passing means the full suite passes.
- Do not assume a passing full suite means pre-commit will pass.
- Do not assume implementation is done until QA verdict is "ready".

## Steps

### Phase 0 — Environment verification (before the loop starts)
1. Confirm the circuit breaker for this ticket is in "closed" state
   (enforced automatically by `circuit-breaker-gate.sh`).
2. Run `git fetch origin && git pull --rebase` on the working branch.
3. Confirm working directory is clean (no stale changes from a previous session).
4. Update workflow state: step 1 of 5.
   ```bash
   bash ~/.claude/hooks/workflow-state.sh write \
     "[ticket-ref]" "dev-impl-loop" "1" "5" "in_progress"
   ```

### Phase 1 — Implementation ralph loop (relative tests)
5. Start `/ralph-loop` for the implementation cycle.
6. Within each loop iteration:
   a. Implement the next logical unit of work for this ticket.
      Follow all conventions in CLAUDE.md (naming, structure, type hints).
   b. Run **relative tests only** — tests in the affected module or package.
      Do not run the full suite here (too slow for iteration).
   c. If relative tests pass → commit the change with a GitEmoji message.
      Example: `✨ feat(module): Implement [specific behavior]`
   d. If relative tests fail:
      - Analyze the root cause (do not guess — read the failure output).
      - Apply the minimal fix.
      - Re-run relative tests. Repeat from (b).
      - The circuit breaker counts each consecutive failure; if it trips,
        stop the loop and escalate to `dev-lead-agent`.
7. Continue iterations until all ticket acceptance criteria are implemented
   and relative tests are green.
8. Stop `/ralph-loop`. Do not proceed until the loop exits cleanly.

### Phase 2 — Full test suite
9. Run the complete test suite (all modules, not just relative).
   Update workflow state: step 2 of 5.
   ```bash
   bash ~/.claude/hooks/workflow-state.sh write \
     "[ticket-ref]" "dev-impl-loop" "2" "5" "in_progress"
   ```
10. If any test fails:
    a. Determine: is the failure in code I changed, or pre-existing?
    b. Pre-existing failure → document it, report to `dev-lead-agent`, do not fix.
    c. Failure in changed code → one ralph loop iteration to fix
       (circuit breaker applies — do not iterate without limit).
11. All tests must pass before proceeding to Phase 3.

### Phase 3 — Pre-commit checks
12. Run `pre-commit run --all-files`.
    Update workflow state: step 3 of 5.
    ```bash
    bash ~/.claude/hooks/workflow-state.sh write \
      "[ticket-ref]" "dev-impl-loop" "3" "5" "in_progress"
    ```
13. If any check fails: use `python-precommit-repair` or `python-ruff-fixing`
    skill. Re-run after repair. Do not use `--no-verify`.
14. When all checks pass: write the test sentinel.
    ```bash
    touch ~/.claude/hooks/.last-test-pass
    ```

### Phase 4 — QA handoff (explicit trigger)
15. Update ticket state to "Ready for QA" in the issue tracker.
    Update workflow state: step 4 of 5.
    ```bash
    bash ~/.claude/hooks/workflow-state.sh write \
      "[ticket-ref]" "dev-impl-loop" "4" "5" "in_progress"
    ```
16. Post a QA handoff comment on the ticket:
    ```
    ## Implementation complete — ready for QA

    ### What was implemented
    [one paragraph summary]

    ### Tests added/changed
    - [test file]: [what it covers]

    ### Known edge cases or concerns
    - [any area that needs extra attention during QA]

    Requesting qa-agent to begin acceptance-validation.
    ```
17. **Explicitly signal `qa-agent`** to begin `acceptance-validation`.
    Do not proceed until the qa-agent verdict arrives.

### Phase 5 — Post-QA resolution
18. If qa-agent verdict is "ready":
    a. Update workflow state: step 5 of 5, status "complete".
       ```bash
       bash ~/.claude/hooks/workflow-state.sh write \
         "[ticket-ref]" "dev-impl-loop" "5" "5" "complete"
       ```
    b. Open a PR using `code-review-prep` and `pr-readiness` skills.
    c. Link the PR to the ticket.
19. If qa-agent verdict is "blocked":
    a. Read the blocking items from the verdict output.
    b. Re-enter Phase 1 ralph loop to address each item.
       Circuit breaker applies — max attempts before escalating.
    c. After fixes: re-run Phase 2 (full suite) and Phase 3 (pre-commit)
       before signaling QA again.

## Circuit breaker thresholds
- Phase 1 (relative tests): max **5 consecutive failures** or **60 min** elapsed.
- Phase 2 (full suite repair): max **3 consecutive failures** or **30 min** elapsed.
- Phase 5 (post-QA repair): max **3 QA rejection cycles** before escalating.

When the circuit breaker trips: stop the loop, write state as "circuit_open",
report to `dev-lead-agent` with the failure summary.

## Output
On successful completion: PR opened, linked to ticket, workflow state = complete.

## Safe-Fix Guidance
- Do not skip Phase 2 (full suite) even if Phase 1 relative tests are green.
- Do not open the PR before qa-agent produces a "ready" verdict.
- Do not mark work complete while the circuit breaker is open.
- If the ralph loop exits without all acceptance criteria met, that is a
  decomposition problem — escalate to `dev-lead-agent`.
