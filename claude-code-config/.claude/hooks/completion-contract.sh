#!/usr/bin/env bash
# completion-contract.sh
# Fires: PostToolUse[Bash] — after any bash command
# Purpose: After task-completion signals, verify no red validation remains.
# Inspects recent output for failure markers before allowing Claude Code to
# declare a task complete.
#
# This hook watches for common task-completion phrases in the tool input
# and then checks whether any known failure markers are present in recent output.
# It does not repair — it blocks premature completion and delegates repair.

set -euo pipefail

COMMAND=$(echo "${CLAUDE_TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

OUTPUT=$(echo "${CLAUDE_TOOL_RESULT:-}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    # Handle both string and list output formats
    out = data.get('output', '') or data.get('content', '')
    if isinstance(out, list):
        out = ' '.join(str(item) for item in out)
    print(str(out)[:4000])
except Exception:
    print('')
" 2>/dev/null || echo "")

if [ -z "$OUTPUT" ]; then
    exit 0
fi

# Failure markers that indicate red validation state.
FAILURE_MARKERS=(
    "FAILED"
    "ERROR"
    "error:"
    "failed:"
    "AssertionError"
    "SyntaxError"
    "ImportError"
    "ModuleNotFoundError"
    "mypy.*error"
    "ruff.*error"
    "pre-commit.*failed"
    "tests.*failed"
)

RED_FOUND=0
RED_MARKER=""
for marker in "${FAILURE_MARKERS[@]}"; do
    if echo "$OUTPUT" | grep -qiE "$marker"; then
        RED_FOUND=1
        RED_MARKER="$marker"
        break
    fi
done

if [ "$RED_FOUND" -eq 1 ]; then
    echo "[HOOK] completion-contract: Failure marker detected in output: $RED_MARKER" >&2
    echo "[HOOK] Do not declare this task complete while validation is red." >&2
    echo "[HOOK] Investigate the failure and delegate repair to the appropriate skill or agent." >&2
    # Exit 0 to warn but not block — completion is a Claude Code decision, not a tool call.
    # Change to exit 2 if you want to actively block the next Bash command.
    exit 0
fi

exit 0
