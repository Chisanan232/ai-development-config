#!/usr/bin/env bash
# circuit-breaker-gate.sh — Track consecutive failures per ticket/loop context
# and block execution when the threshold is exceeded (circuit open).
#
# Usage (as hook — receives JSON via stdin from Claude Code):
#   Input: {"tool_name": "Bash", "tool_input": {"command": "..."}}
#   Exit 0: circuit closed — allow execution
#   Exit 1 + message: circuit open — block execution
#
# Usage (as utility check from skills):
#   circuit-breaker-gate.sh check <ticket> [threshold]
#   Exit 0: circuit closed
#   Exit 1: circuit open
#
# State files: ~/.claude/circuit-breaker/<ticket>.json
# Format: {"ticket": "...", "consecutive_failures": N, "state": "closed|open", "timestamp": "..."}

set -euo pipefail

BREAKER_DIR="${HOME}/.claude/circuit-breaker"
mkdir -p "$BREAKER_DIR"

DEFAULT_THRESHOLD=5

# ── Utility check mode ──────────────────────────────────────────────────────
if [[ "${1:-}" == "check" ]]; then
  ticket="${2:-}"
  threshold="${3:-$DEFAULT_THRESHOLD}"

  if [[ -z "$ticket" ]]; then
    echo "circuit-breaker check: ticket argument required" >&2
    exit 1
  fi

  state_file="${BREAKER_DIR}/${ticket}.json"

  if [[ ! -f "$state_file" ]]; then
    echo "[circuit-breaker] no state for ${ticket} — circuit closed"
    exit 0
  fi

  state="$(python3 -c "import json,sys; d=json.load(open('${state_file}')); print(d.get('state','closed'))" 2>/dev/null || echo "closed")"
  failures="$(python3 -c "import json,sys; d=json.load(open('${state_file}')); print(d.get('consecutive_failures',0))" 2>/dev/null || echo "0")"

  if [[ "$state" == "open" ]]; then
    echo "[circuit-breaker] OPEN for ${ticket} — ${failures} consecutive failures (threshold: ${threshold})" >&2
    echo "Escalate to dev-lead-agent. Reset with: circuit-breaker-gate.sh reset ${ticket}" >&2
    exit 1
  fi

  echo "[circuit-breaker] closed for ${ticket} — ${failures} consecutive failures"
  exit 0
fi

# ── Reset mode ──────────────────────────────────────────────────────────────
if [[ "${1:-}" == "reset" ]]; then
  ticket="${2:-}"
  if [[ -z "$ticket" ]]; then
    echo "circuit-breaker reset: ticket argument required" >&2
    exit 1
  fi
  state_file="${BREAKER_DIR}/${ticket}.json"
  rm -f "$state_file"
  echo "[circuit-breaker] reset for ${ticket}"
  exit 0
fi

# ── Record failure mode ──────────────────────────────────────────────────────
if [[ "${1:-}" == "record-failure" ]]; then
  ticket="${2:-}"
  threshold="${3:-$DEFAULT_THRESHOLD}"

  if [[ -z "$ticket" ]]; then
    echo "circuit-breaker record-failure: ticket argument required" >&2
    exit 1
  fi

  state_file="${BREAKER_DIR}/${ticket}.json"
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  if [[ -f "$state_file" ]]; then
    failures="$(python3 -c "import json; d=json.load(open('${state_file}')); print(d.get('consecutive_failures',0))" 2>/dev/null || echo "0")"
  else
    failures=0
  fi

  failures=$((failures + 1))

  if [[ "$failures" -ge "$threshold" ]]; then
    new_state="open"
  else
    new_state="closed"
  fi

  cat > "$state_file" <<JSON
{
  "ticket": "${ticket}",
  "consecutive_failures": ${failures},
  "state": "${new_state}",
  "threshold": ${threshold},
  "timestamp": "${timestamp}"
}
JSON

  echo "[circuit-breaker] recorded failure for ${ticket}: ${failures}/${threshold} — state: ${new_state}"

  if [[ "$new_state" == "open" ]]; then
    echo "[circuit-breaker] CIRCUIT OPEN for ${ticket} — escalate to dev-lead-agent" >&2
    exit 1
  fi

  exit 0
fi

# ── Record success mode ──────────────────────────────────────────────────────
if [[ "${1:-}" == "record-success" ]]; then
  ticket="${2:-}"
  if [[ -z "$ticket" ]]; then
    echo "circuit-breaker record-success: ticket argument required" >&2
    exit 1
  fi

  state_file="${BREAKER_DIR}/${ticket}.json"
  timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  cat > "$state_file" <<JSON
{
  "ticket": "${ticket}",
  "consecutive_failures": 0,
  "state": "closed",
  "threshold": ${DEFAULT_THRESHOLD},
  "timestamp": "${timestamp}"
}
JSON

  echo "[circuit-breaker] reset to closed for ${ticket} after success"
  exit 0
fi

# ── Hook mode (stdin JSON from Claude Code) ──────────────────────────────────
# When wired as PostToolUse[Bash], read stdin and check for failure markers.
# If failures detected, record them against the current ticket context.

if [[ ! -t 0 ]]; then
  input="$(cat)"

  # Extract command output if available
  output="$(echo "$input" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('tool_response', {}).get('content', '') if isinstance(data.get('tool_response', {}), dict) else '')
" 2>/dev/null || echo "")"

  # Detect failure markers in output
  if echo "$output" | grep -qiE "(FAILED|ERROR|error:|fatal:|test.*failed|[0-9]+ failed)"; then
    # Try to find ticket context from workflow state
    if compgen -G "${BREAKER_DIR}/*.json" > /dev/null 2>&1; then
      # Find most recently modified open ticket state
      latest_ticket="$(ls -t "${BREAKER_DIR}"/*.json 2>/dev/null | head -1 | xargs -I{} python3 -c "
import json; d=json.load(open('{}'))
if d.get('state','closed') != 'open': print(d.get('ticket',''))
" 2>/dev/null || echo "")"

      if [[ -n "$latest_ticket" ]]; then
        bash "$0" record-failure "$latest_ticket" "$DEFAULT_THRESHOLD" || true
      fi
    fi
  fi
fi

# Hook mode always exits 0 (warn, do not block generically).
# Blocking only happens via explicit `check` or `record-failure` sub-commands.
exit 0
