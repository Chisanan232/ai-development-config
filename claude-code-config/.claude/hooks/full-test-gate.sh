#!/usr/bin/env bash
# full-test-gate.sh
# Fires: PreToolUse[Bash] — before git push commands
# Purpose: Block push unless the full test suite has passed after the most
# recent source file change.
#
# Sentinel is scoped per-repository and per-branch using the git remote URL
# as a stable key — prevents a sentinel from one project clearing the gate
# in another. Uses `git diff` (git index) instead of `find` for freshness
# checking — O(1) via git, git-aware, does not traverse node_modules etc.
#
# IMPORTANT: This hook gates, not loops. It does not run tests itself.

set -euo pipefail

[ -f "${HOME}/.claude/config.env" ] && source "${HOME}/.claude/config.env"

# ── Extract command ───────────────────────────────────────────────────────────

COMMAND=$(echo "${CLAUDE_TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

[[ -z "$COMMAND" ]] && exit 0

# Only gate on push commands.
echo "$COMMAND" | grep -qiE "git push" || exit 0

# ── Compute per-repo, per-branch sentinel path ────────────────────────────────

SENTINEL_BASE="${CLAUDE_SENTINEL_DIR:-${HOME}/.claude/sentinels}"

REPO_REMOTE=$(git remote get-url origin 2>/dev/null \
    || git remote get-url remote 2>/dev/null \
    || echo "unknown")

# Portable SHA-256: shasum (macOS/BSD) with fallback to sha256sum (Linux/GNU)
_sha256() { shasum -a 256 2>/dev/null || sha256sum; }
REPO_KEY=$(echo "$REPO_REMOTE" | _sha256 | cut -c1-12)

BRANCH=$(git branch --show-current 2>/dev/null | tr '/' '_' || echo "unknown")

SENTINEL_DIR="${SENTINEL_BASE}/${REPO_KEY}/${BRANCH}"
SENTINEL_FILE="${SENTINEL_DIR}/.last-test-pass"

mkdir -p "$SENTINEL_DIR"

# ── Check sentinel exists ─────────────────────────────────────────────────────

if [[ ! -f "$SENTINEL_FILE" ]]; then
    echo "[HOOK] BLOCKED: full-test-gate — no passing test run recorded for this repo/branch." >&2
    echo "[HOOK] Run the full test suite. The gate clears automatically after a clean run." >&2
    echo "[HOOK] Sentinel expected at: ${SENTINEL_FILE}" >&2
    exit 2
fi

# ── Check for source changes since last sentinel (via git) ────────────────────
# git diff checks both staged and unstaged changes against HEAD.
# git diff HEAD --name-only shows all files modified since last commit.
# We compare the sentinel mtime against each changed file's mtime.

SENTINEL_MTIME=$(stat -f "%m" "$SENTINEL_FILE" 2>/dev/null \
    || stat -c "%Y" "$SENTINEL_FILE" 2>/dev/null \
    || echo "0")

# Get files changed since the sentinel was written.
# Check: uncommitted changes (index + worktree) and commits after sentinel.
CHANGED_FILES=$(git diff HEAD --name-only 2>/dev/null || echo "")

if [[ -z "$CHANGED_FILES" ]]; then
    # No uncommitted changes. Check if any new commits landed after sentinel.
    LAST_COMMIT_MTIME=$(git log -1 --format="%ct" 2>/dev/null || echo "0")
    if [[ "$LAST_COMMIT_MTIME" -gt "$SENTINEL_MTIME" ]]; then
        echo "[HOOK] BLOCKED: full-test-gate — commits added after last passing test run." >&2
        echo "[HOOK] Run the full test suite again before pushing." >&2
        exit 2
    fi
else
    echo "[HOOK] BLOCKED: full-test-gate — uncommitted source changes since last passing test run." >&2
    echo "[HOOK] Changed files:" >&2
    echo "$CHANGED_FILES" | head -5 | sed 's/^/[HOOK]   /' >&2
    echo "[HOOK] Run the full test suite again, then push." >&2
    exit 2
fi

echo "[HOOK] full-test-gate: sentinel current for ${REPO_KEY}/${BRANCH}. Proceeding." >&2
exit 0
