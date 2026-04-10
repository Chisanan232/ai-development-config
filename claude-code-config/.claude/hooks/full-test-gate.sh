#!/usr/bin/env bash
# full-test-gate.sh
# Fires: PreToolUse[Bash] — before git push commands
# Purpose: Require the full test suite to pass before any push.
# Does not run the tests itself — it checks whether the last test run was clean.
# If the last test run is stale or unknown, it blocks and instructs Claude Code
# to run the full test suite first.
#
# IMPORTANT: This hook gates, not loops. It does not run tests itself.
# If tests fail, delegate repair to the appropriate skill or agent.

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

# Only gate on push commands.
if ! echo "$COMMAND" | grep -qiE "git push"; then
    exit 0
fi

# Check for a sentinel file written by the test runner after a clean run.
# The sentinel must be newer than the most recently modified source file.
SENTINEL_FILE="${HOME}/.claude/hooks/.last-test-pass"
SOURCE_DIR="${CLAUDE_REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || echo ".")}"

if [ ! -f "$SENTINEL_FILE" ]; then
    echo "[HOOK] BLOCKED: full-test-gate — no record of a passing test run found." >&2
    echo "[HOOK] Run the full test suite before pushing. After a clean run, the gate will clear." >&2
    echo "[HOOK] Do not bypass this gate with --no-verify." >&2
    exit 2
fi

# Find the most recently modified source file (excluding hidden dirs, build outputs, venv).
NEWEST_SOURCE=$(find "$SOURCE_DIR" \
    -not -path "*/\.*" \
    -not -path "*/node_modules/*" \
    -not -path "*/__pycache__/*" \
    -not -path "*/.venv/*" \
    -not -path "*/dist/*" \
    -not -path "*/build/*" \
    -type f \
    -newer "$SENTINEL_FILE" \
    -print -quit 2>/dev/null || echo "")

if [ -n "$NEWEST_SOURCE" ]; then
    echo "[HOOK] BLOCKED: full-test-gate — source files changed since the last passing test run." >&2
    echo "[HOOK] Changed since last test pass: $NEWEST_SOURCE" >&2
    echo "[HOOK] Run the full test suite again before pushing." >&2
    exit 2
fi

echo "[HOOK] full-test-gate: Test sentinel is current. Proceeding." >&2
exit 0
