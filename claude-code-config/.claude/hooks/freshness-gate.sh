#!/usr/bin/env bash
# freshness-gate.sh
# Fires: PreToolUse[Bash] — before significant git or file-mutation commands
# Purpose: Verify the local branch is not stale relative to the remote base.
# Blocks if the current branch is behind its upstream by more than 0 commits.
# Reads the command from CLAUDE_TOOL_INPUT environment variable (JSON).

set -euo pipefail

COMMAND=$(echo "${CLAUDE_TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

if [ -z "$COMMAND" ]; then
    exit 0
fi

# Only run freshness check before remote-mutation commands.
# git commit is intentionally excluded — committing local work while behind
# remote is the normal workflow (commit → pull --rebase → push). Adding a
# network fetch on every local commit adds latency and blocks offline work.
MUTATION_PATTERNS=(
    "git push"
    "git checkout -b"
    "git switch -c"
)

IS_MUTATION=0
for pattern in "${MUTATION_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$pattern"; then
        IS_MUTATION=1
        break
    fi
done

if [ "$IS_MUTATION" -eq 0 ]; then
    exit 0
fi

# Resolve the tracking remote for the current branch (not hardcoded 'origin').
REMOTE=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null \
    | cut -d'/' -f1)

if [ -z "$REMOTE" ]; then
    # No upstream configured — cannot check freshness, proceed.
    exit 0
fi

# Fetch remote state without modifying local refs.
git fetch "$REMOTE" --quiet 2>/dev/null || {
    echo "[HOOK] freshness-gate: Could not reach remote '$REMOTE'. Proceeding without freshness check." >&2
    exit 0
}

# Determine the full upstream tracking branch (remote/branch).
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "")

BEHIND=$(git rev-list --count HEAD.."$UPSTREAM" 2>/dev/null || echo "0")

if [ "$BEHIND" -gt 0 ]; then
    echo "[HOOK] BLOCKED: freshness-gate — local branch is $BEHIND commit(s) behind $UPSTREAM." >&2
    echo "[HOOK] Run 'git pull --rebase' or 'git merge $UPSTREAM' before proceeding." >&2
    echo "[HOOK] Do not bypass this check — working on a stale branch risks conflicts and lost work." >&2
    exit 2
fi

exit 0
