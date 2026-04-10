#!/usr/bin/env bash
# decision-log.sh — Structured decision log for skills and agents.
#
# Records WHY the system made a decision, not just WHAT it ran.
# Complements the audit log (what commands ran) and workflow state (what phase).
#
# Usage:
#   decision-log.sh record \
#     --ticket   "PROJ-123"     \
#     --agent    "dev-agent"    \
#     --skill    "dev-impl-loop" \
#     --phase    "2"            \
#     --decision "proceed"      \
#     --reason   "47 tests pass after fix" \
#     --context  "pytest: 47 passed, 0 failed"
#
#   decision-log.sh tail [N]   — show last N entries (default: 20)
#   decision-log.sh query --ticket "PROJ-123"  — show entries for a ticket
#
# Output: ${CLAUDE_DECISION_LOG_DIR}/<YYYY-MM-DD>.jsonl (one JSON object per line)

set -euo pipefail

[ -f "${HOME}/.claude/config.env" ] && source "${HOME}/.claude/config.env"

# Bail out silently if logging is disabled
ENABLED="${CLAUDE_DECISION_LOG_ENABLED:-1}"
[[ "$ENABLED" == "0" ]] && exit 0

LOG_DIR="${CLAUDE_DECISION_LOG_DIR:-${HOME}/.claude/decisions}"
MAX_CONTEXT="${CLAUDE_DECISION_LOG_MAX_CONTEXT:-500}"
mkdir -p "$LOG_DIR"

DATE_KEY="$(date -u +"%Y-%m-%d")"
LOG_FILE="${LOG_DIR}/${DATE_KEY}.jsonl"

# ── record ────────────────────────────────────────────────────────────────────

if [[ "${1:-}" == "record" ]]; then
    shift
    ticket="" agent="" skill="" phase="" decision="" reason="" context=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --ticket)   ticket="$2";   shift 2 ;;
            --agent)    agent="$2";    shift 2 ;;
            --skill)    skill="$2";    shift 2 ;;
            --phase)    phase="$2";    shift 2 ;;
            --decision) decision="$2"; shift 2 ;;
            --reason)   reason="$2";   shift 2 ;;
            --context)  context="$2";  shift 2 ;;
            *) echo "decision-log record: unknown flag '$1'" >&2; exit 1 ;;
        esac
    done

    if [[ -z "$decision" || -z "$reason" ]]; then
        echo "decision-log record: --decision and --reason are required" >&2
        exit 1
    fi

    # Truncate context to MAX_CONTEXT characters
    if [[ ${#context} -gt $MAX_CONTEXT ]]; then
        context="${context:0:$MAX_CONTEXT}…"
    fi

    timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    # Escape strings for JSON using python3 (handles quotes, newlines, etc.)
    python3 -c "
import json, sys
entry = {
    'timestamp': '${timestamp}',
    'ticket':    '${ticket}',
    'agent':     '${agent}',
    'skill':     '${skill}',
    'phase':     '${phase}',
    'decision':  '${decision}',
    'reason':    ${reason!r},
    'context':   ${context!r},
}
print(json.dumps(entry))
" >> "$LOG_FILE"

    echo "[decision-log] recorded: ${ticket:-?} | ${skill:-?} phase ${phase:-?} | ${decision}"
    exit 0
fi

# ── tail ─────────────────────────────────────────────────────────────────────

if [[ "${1:-}" == "tail" ]]; then
    n="${2:-20}"
    # Concatenate all daily logs sorted by name (date order), show last N lines
    find "$LOG_DIR" -name "*.jsonl" | sort | xargs cat 2>/dev/null | tail -n "$n" \
    | python3 -c "
import json, sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        print(f\"{d.get('timestamp','?')}  {d.get('ticket','?'):12}  {d.get('agent','?'):15}  {d.get('skill','?'):20}  ph={d.get('phase','?'):2}  [{d.get('decision','?')}]  {d.get('reason','?')[:80]}\")
    except Exception:
        print(line)
"
    exit 0
fi

# ── query ─────────────────────────────────────────────────────────────────────

if [[ "${1:-}" == "query" ]]; then
    shift
    filter_ticket=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --ticket) filter_ticket="$2"; shift 2 ;;
            *) echo "decision-log query: unknown flag '$1'" >&2; exit 1 ;;
        esac
    done

    find "$LOG_DIR" -name "*.jsonl" | sort | xargs cat 2>/dev/null \
    | python3 -c "
import json, sys
filter_ticket = '${filter_ticket}'
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
        if filter_ticket and d.get('ticket','') != filter_ticket:
            continue
        print(json.dumps(d, indent=2))
    except Exception:
        pass
"
    exit 0
fi

echo "decision-log: unknown sub-command '${1:-}'.
Usage:
  decision-log.sh record --ticket T --agent A --skill S --phase P --decision D --reason R [--context C]
  decision-log.sh tail [N]
  decision-log.sh query --ticket T" >&2
exit 1
