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

# Write JSON log entry (audit failures must never block execution).
# Pass free-text fields via env vars to prevent shell-interpolation injection
# into the Python source. If COMMAND contains ''', r'''$COMMAND''' terminates
# prematurely and the audit entry is silently dropped.
_AL_COMMAND="$COMMAND" \
_AL_TIMESTAMP="$TIMESTAMP" \
_AL_USER="$USER" \
_AL_PWD="$PWD_VAL" \
_AL_EXIT_CODE="$EXIT_CODE" \
python3 -c "
import json, os
entry = {
    'timestamp': os.environ['_AL_TIMESTAMP'],
    'user': os.environ['_AL_USER'],
    'working_directory': os.environ['_AL_PWD'],
    'command': os.environ.get('_AL_COMMAND', ''),
    'exit_code': int(os.environ.get('_AL_EXIT_CODE', '0') or '0'),
}
print(json.dumps(entry))
" >> "$LOG_FILE" 2>/dev/null || true

exit 0
