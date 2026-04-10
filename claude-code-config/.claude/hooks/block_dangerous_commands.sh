#!/usr/bin/env bash
# block_dangerous_commands.sh
# Fires: PreToolUse[Bash]
# Purpose: Block or warn on commands that could cause irreversible damage.
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

# --- Absolute blocks (exit code 2 = block the tool call) ---

BLOCKED_PATTERNS=(
    "rm -rf /"
    "rm -rf ~"
    "mkfs"
    "fdisk"
    "dd if="
    "curl.*|.*sh"
    "wget.*|.*sh"
    "DROP TABLE"
    "DROP DATABASE"
    "TRUNCATE TABLE"
    "git push --force"
    "git push -f"
    "git reset --hard"
    "git clean -fd"
    "git clean -f"
    "kill -9 -1"
    "killall"
    ":(){:|:&};:"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$pattern"; then
        echo "[HOOK] BLOCKED: Dangerous command pattern detected: $pattern" >&2
        echo "[HOOK] Command: $COMMAND" >&2
        echo "[HOOK] This command requires explicit user confirmation. Do not retry automatically." >&2
        exit 2
    fi
done

# --- Confirmation-required patterns (warn, do not block) ---

WARN_PATTERNS=(
    "npm publish"
    "cargo publish"
    "pip upload"
    "twine upload"
    "docker push"
    "git tag"
    "heroku"
    "terraform apply"
    "terraform destroy"
)

for pattern in "${WARN_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$pattern"; then
        echo "[HOOK] WARNING: High-impact command requires explicit confirmation: $pattern" >&2
        echo "[HOOK] Command: $COMMAND" >&2
        exit 0
    fi
done

exit 0
