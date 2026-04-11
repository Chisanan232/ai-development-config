#!/usr/bin/env bash
# workflow-state.sh — Read, write, and archive per-ticket workflow state.
#
# Usage:
#   workflow-state.sh write  <ticket> <workflow> <step> <total> <status>
#   workflow-state.sh read   <ticket>
#   workflow-state.sh archive <ticket>
#
# Writes are atomic (mktemp + mv) — partial writes from crashes leave no
# corrupt state. Reads validate JSON before returning; exits 1 on corruption.
#
# State: ${CLAUDE_WORKFLOW_STATE_DIR}/<ticket>.json

set -euo pipefail

[ -f "${HOME}/.claude/config.env" ] && source "${HOME}/.claude/config.env"

STATE_DIR="${CLAUDE_WORKFLOW_STATE_DIR:-${HOME}/.claude/workflow-state}"
ARCHIVE_DIR="${STATE_DIR}/archive"

cmd="${1:-}"
ticket="${2:-}"

if [[ -z "$cmd" || -z "$ticket" ]]; then
    echo "Usage: workflow-state.sh <write|read|archive> <ticket> [workflow step total status]" >&2
    exit 1
fi

mkdir -p "$STATE_DIR" "$ARCHIVE_DIR"

STATE_FILE="${STATE_DIR}/${ticket}.json"

# ── Shared JSON validation ────────────────────────────────────────────────────

_validate_json() {
    local file="$1"
    # Pass file and ticket via env vars — never interpolate free-text paths or
    # ticket refs directly into Python source (single quotes in values break syntax).
    _WS_FILE="$file" _WS_TICKET="$ticket" python3 -c "
import json, sys, os
f = os.environ['_WS_FILE']
t = os.environ['_WS_TICKET']
try:
    with open(f) as fh:
        json.load(fh)
    sys.exit(0)
except json.JSONDecodeError as e:
    print(f'[workflow-state] CORRUPT state file for ticket: {t} — {e}', file=sys.stderr)
    sys.exit(1)
except FileNotFoundError:
    print(f'[workflow-state] state file not found: {f}', file=sys.stderr)
    sys.exit(1)
" 2>&1
}

# ── write ─────────────────────────────────────────────────────────────────────

if [[ "$cmd" == "write" ]]; then
    workflow="${3:-}"
    step="${4:-}"
    total="${5:-}"
    status="${6:-}"

    if [[ -z "$workflow" || -z "$step" || -z "$total" || -z "$status" ]]; then
        echo "workflow-state write: missing arguments (workflow step total status)" >&2
        exit 1
    fi

    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    # Atomic write: write to temp file, then mv (POSIX-atomic on same filesystem)
    tmp="$(mktemp "${STATE_FILE}.XXXXXX")"
    cat > "$tmp" <<JSON
{
  "ticket": "${ticket}",
  "workflow": "${workflow}",
  "step": "${step}",
  "total_steps": "${total}",
  "status": "${status}",
  "timestamp": "${timestamp}"
}
JSON
    mv "$tmp" "$STATE_FILE"

    echo "[workflow-state] wrote: ${ticket} | ${workflow} | step ${step}/${total} | ${status} | ${timestamp}"
    exit 0
fi

# ── read ──────────────────────────────────────────────────────────────────────

if [[ "$cmd" == "read" ]]; then
    if [[ ! -f "$STATE_FILE" ]]; then
        echo "[workflow-state] no state file found for ticket: ${ticket}" >&2
        exit 1
    fi

    validation_output="$(_validate_json "$STATE_FILE")"
    if [[ $? -ne 0 ]]; then
        echo "$validation_output" >&2
        echo "[workflow-state] Delete the corrupt file and restart from ticket-pickup-check:" >&2
        echo "  rm ${STATE_FILE}" >&2
        exit 1
    fi

    cat "$STATE_FILE"
    exit 0
fi

# ── archive ───────────────────────────────────────────────────────────────────

if [[ "$cmd" == "archive" ]]; then
    if [[ ! -f "$STATE_FILE" ]]; then
        echo "[workflow-state] nothing to archive for ticket: ${ticket}" >&2
        exit 0
    fi

    timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
    archive_path="${ARCHIVE_DIR}/${ticket}_${timestamp}.json"
    mv "$STATE_FILE" "$archive_path"
    echo "[workflow-state] archived: ${ticket} → ${archive_path}"
    exit 0
fi

echo "workflow-state: unknown command '${cmd}'. Use write, read, or archive." >&2
exit 1
