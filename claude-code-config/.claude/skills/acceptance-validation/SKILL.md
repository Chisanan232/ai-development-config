# SKILL.md — acceptance-validation

## Purpose
Validate that a delivered implementation meets its acceptance criteria from an
external tester perspective, covering happy paths, edge cases, and regressions.

## Type
Auto-used. `qa-agent` invokes this skill before producing a pre-merge validation report.

## Do Not Assume
- Do not assume the stated acceptance criteria are complete — look for implicit requirements.
- Do not assume the implementation is correct just because tests pass.
- Do not assume happy-path coverage means edge cases are handled.
- Do not assume regressions are impossible — check what could have been affected.

## Steps

### Phase 1 — Criteria extraction
1. Read the ticket or PR description to identify acceptance criteria.
2. If acceptance criteria are missing, derive them from the stated purpose and scope.
3. Confirm with `dev-lead-agent` before proceeding if criteria cannot be determined.

### Phase 2 — Happy path validation
4. For each acceptance criterion, identify the primary scenario that should satisfy it.
5. Verify that scenario works as expected using the available implementation.
6. Record: criterion → scenario → result (pass / fail / not verifiable).

### Phase 3 — Adversarial and boundary validation
7. For each changed behavior, identify:
   - Boundary values (min, max, empty, zero, null, overflow)
   - Invalid inputs (wrong types, missing required fields, malformed data)
   - Error paths (what happens when dependencies fail)
   - Concurrent or race condition scenarios (if applicable)
8. Verify each adversarial scenario produces the correct outcome.

### Phase 4 — Regression check
9. Identify the existing behaviors that could be affected by the change.
10. Run the existing test suite and check for failures.
11. If failures are found, report them — do not fix them directly.
12. Identify behavioral regressions that the test suite does not catch.

### Phase 5 — Validation report
13. Produce the structured validation report (see Output format).
14. If any blocking items are found, report them to `dev-lead-agent` with detail.
15. Do not declare the work ready if any criterion fails or any blocking regression exists.

## Output format

```
## Acceptance validation report — [PR or ticket reference]

### Acceptance criteria
| Criterion | Scenario tested | Result |
|---|---|---|
| [criterion 1] | [scenario description] | ✅ Pass / ❌ Fail / ⚠️ Not verifiable |

### Adversarial scenarios
| Scenario | Expected behavior | Actual behavior | Result |
|---|---|---|---|
| [scenario] | [expected] | [actual] | ✅ / ❌ |

### Regression check
- Existing tests: ✅ all pass / ❌ N failures (list below)
- Behavioral regressions not caught by tests: [none / list]

### Uncovered edge cases
- [edge case that has no test and no verification]

### Verdict
[ ] Ready to merge
[ ] Not ready — blocking items:
  - [item 1]
  - [item 2]
```

## Safe-Fix Guidance
- If a criterion fails, report it. Do not modify tests or code to make it pass.
- If the test suite is red, stop and escalate to `dev-lead-agent` — do not proceed
  with validation on a broken baseline.
