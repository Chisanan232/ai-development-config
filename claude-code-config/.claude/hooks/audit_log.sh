#!/usr/bin/env bash
# audit_log.sh
# Fires: PostToolUse[Bash]
# Purpose: Log every shell command Claude Code executes for traceability.

set -euo pipefail

LOG_DIR="${CLAUDE_AUDIT_LOG_DIR:-$HOME/.claude/audit}"
LOG_FILE="$LOG_DIR/commands.jsonl"
MAX_LOG_SIZE_BYTES=10485760  # 10 MB

# Skip if audit is disabled
if [ "${CLAUDE_SKIP_AUDIT:-0}" = "1" ]; then
    exit 0
fi

mkdir -p "$LOG_DIR"

# Rotate log if it exceeds max size
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(wc -c < "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$LOG_SIZE" -gt "$MAX_LOG_SIZE_BYTES" ]; then
        mv "$LOG_FILE" "${LOG_FILE}.$(date +%Y%m%d_%H%M%S).bak"
    fi
fi

# Extract command from tool input
COMMAND=$(echo "${CLAUDE_TOOL_INPUT:-}" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except Exception:
    print('')
" 2>/dev/null || echo "")

EXIT_CODE="${CLAUDE_TOOL_EXIT_CODE:-0}"
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
USER=$(whoami 2>/dev/null || echo "unknown")
PWD_VAL=$(pwd 2>/dev/null || echo "unknown")

# Write JSON log entry (audit failures must never block execution)
python3 -c "
import json
entry = {
    'timestamp': '$TIMESTAMP',
    'user': '$USER',
    'working_directory': '$PWD_VAL',
    'command': r'''$COMMAND''',
    'exit_code': $EXIT_CODE
}
print(json.dumps(entry))
" >> "$LOG_FILE" 2>/dev/null || true

exit 0
