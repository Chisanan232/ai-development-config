# SKILL.md — post-merge-close

## Purpose
After a PR is merged, perform all required close-out actions: transition the
ticket to Done, delete the feature branch, post a completion comment, and
notify the reporter. Leaves no dangling branches or open tickets.

## Type
Auto-used. Invoked by `dev-lead-agent` immediately after a PR merge is confirmed.

## Do Not Assume
- Do not assume the PR was actually merged — verify the merge status before acting.
- Do not assume the ticket reference is in the PR title — check the description too.
- Do not delete the branch before confirming the merge was recorded by the tracker.
- Do not assume the reporter and the assignee are the same person.

## Steps

### Phase 1 — Confirm merge
1. Fetch the PR's current state using `code_repository` MCP.
2. Confirm the PR status is "merged" (not just "closed").
3. Record: merge commit SHA, merged-at timestamp, base branch.
4. If the PR was closed without merging: stop. Do not transition the ticket or
   delete the branch. Report the closure reason to `dev-lead-agent`.

### Phase 2 — Close the ticket
5. Fetch the linked ticket reference from the PR description
   (look for `Closes #`, `Fixes #`, `Refs #` patterns, or a ClickUp/JIRA URL).
6. If a ticket reference is found:
   a. Transition the ticket state to "Done" / "Closed".
   b. Post a close comment on the ticket:
      ```
      Merged via [PR reference] ([merge commit SHA]).
      All acceptance criteria verified by qa-agent.
      ```
7. If no ticket reference is found: log the gap and notify `dev-lead-agent`.
   Do not proceed to branch deletion until the ticket is resolved.

### Phase 3 — Branch cleanup
8. Delete the remote feature branch:
   ```bash
   git push origin --delete [feature-branch-name]
   ```
   Do not delete protected branches (`main`, `master`, `release/*`).
9. Delete the local tracking branch if it exists:
   ```bash
   git branch -d [feature-branch-name]
   ```
   Use `-d` (safe delete), not `-D` (force delete). If `-d` fails because
   the branch is not fully merged, report to `dev-lead-agent` and stop.

### Phase 4 — Notify reporter
10. Identify the ticket reporter (the person who originally filed the ticket,
    not the implementer).
11. If the reporter is different from the assignee, post a notification comment
    on the ticket tagging the reporter:
    ```
    @[reporter] — this item has been implemented and merged.
    Summary: [one sentence from the PR description]
    ```
12. If `communication` MCP (Slack) is configured and the project uses Slack
    notifications, post to the configured project channel:
    ```
    ✅ [ticket-ref]: [ticket title] — merged and closed.
    PR: [PR URL] | Commit: [merge SHA]
    ```

### Phase 5 — Update workflow state
13. Write final workflow state:
    ```bash
    bash ~/.claude/hooks/workflow-state.sh write \
      "[ticket-ref]" "post-merge-close" "done" "done" "complete"
    ```
14. Archive or clean up the local workflow state file for this ticket:
    ```bash
    bash ~/.claude/hooks/workflow-state.sh archive "[ticket-ref]"
    ```

## Output

```
## Post-merge close — [PR reference]

| Action | Result |
|---|---|
| Merge confirmed | ✅ SHA [sha] at [timestamp] |
| Ticket closed | ✅ [ticket-ref] → Done / ❌ No ticket found |
| Branch deleted | ✅ [branch-name] / ❌ [reason] |
| Reporter notified | ✅ @[reporter] / ℹ️ Same as assignee |
| Slack notified | ✅ / ℹ️ Not configured |
| Workflow state | complete |
```

## Safe-Fix Guidance
- Never delete the branch before the ticket is confirmed closed in the tracker.
- If the branch delete fails (another open PR targets it), stop and report.
- Do not close a ticket as Done if the PR was reverted — escalate instead.
- Do not notify reporter via Slack if the project channel is not configured;
  the ticket comment is sufficient.
