#!/usr/bin/env bash
# workflow-state.sh — Read, write, and archive per-ticket workflow state.
#
# Usage:
#   workflow-state.sh write  <ticket> <workflow> <step> <total> <status>
#   workflow-state.sh read   <ticket>
#   workflow-state.sh archive <ticket>
#
# State is stored as JSON in ~/.claude/workflow-state/<ticket>.json
# This script is NOT a hook — it is a utility called by skills.

set -euo pipefail

STATE_DIR="${HOME}/.claude/workflow-state"
ARCHIVE_DIR="${STATE_DIR}/archive"

cmd="${1:-}"
ticket="${2:-}"

if [[ -z "$cmd" || -z "$ticket" ]]; then
  echo "Usage: workflow-state.sh <write|read|archive> <ticket> [workflow] [step] [total] [status]" >&2
  exit 1
fi

mkdir -p "$STATE_DIR" "$ARCHIVE_DIR"

STATE_FILE="${STATE_DIR}/${ticket}.json"

case "$cmd" in
  write)
    workflow="${3:-}"
    step="${4:-}"
    total="${5:-}"
    status="${6:-}"

    if [[ -z "$workflow" || -z "$step" || -z "$total" || -z "$status" ]]; then
      echo "workflow-state write: missing arguments (workflow step total status)" >&2
      exit 1
    fi

    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    cat > "$STATE_FILE" <<JSON
{
  "ticket": "${ticket}",
  "workflow": "${workflow}",
  "step": "${step}",
  "total_steps": "${total}",
  "status": "${status}",
  "timestamp": "${timestamp}"
}
JSON

    echo "[workflow-state] wrote: ${ticket} | ${workflow} | step ${step}/${total} | ${status} | ${timestamp}"
    ;;

  read)
    if [[ ! -f "$STATE_FILE" ]]; then
      echo "[workflow-state] no state file found for ticket: ${ticket}" >&2
      exit 1
    fi
    cat "$STATE_FILE"
    ;;

  archive)
    if [[ ! -f "$STATE_FILE" ]]; then
      echo "[workflow-state] nothing to archive for ticket: ${ticket}" >&2
      exit 0
    fi
    timestamp="$(date -u +"%Y%m%dT%H%M%SZ")"
    archive_path="${ARCHIVE_DIR}/${ticket}_${timestamp}.json"
    mv "$STATE_FILE" "$archive_path"
    echo "[workflow-state] archived: ${ticket} → ${archive_path}"
    ;;

  *)
    echo "workflow-state: unknown command '${cmd}'. Use write, read, or archive." >&2
    exit 1
    ;;
esac
