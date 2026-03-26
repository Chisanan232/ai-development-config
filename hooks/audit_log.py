#!/usr/bin/env python3
"""
Audit log hook for Windsurf Cascade.

This hook logs command execution for audit trail and analysis.

Environment variables:
- WINDSURF_COMMAND: The command that was executed
- WINDSURF_COMMAND_EXIT_CODE: Exit code of the command
- WINDSURF_SKIP_AUDIT: Set to "1" to skip audit logging
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Configuration
SKIP_AUDIT = os.getenv("WINDSURF_SKIP_AUDIT", "0") == "1"
AUDIT_LOG_FILE = Path(".windsurf/audit.log")
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB


def get_command_info():
    """Get command information from environment."""
    return {
        "command": os.getenv("WINDSURF_COMMAND", ""),
        "exit_code": os.getenv("WINDSURF_COMMAND_EXIT_CODE", ""),
        "timestamp": datetime.utcnow().isoformat(),
        "user": os.getenv("USER", "unknown"),
        "cwd": os.getcwd(),
    }


def rotate_log_if_needed():
    """Rotate log file if it's too large."""
    if not AUDIT_LOG_FILE.exists():
        return
    
    if AUDIT_LOG_FILE.stat().st_size > MAX_LOG_SIZE:
        # Rotate: audit.log -> audit.log.1
        backup = AUDIT_LOG_FILE.with_suffix(".log.1")
        if backup.exists():
            backup.unlink()
        AUDIT_LOG_FILE.rename(backup)


def log_command(info):
    """Log command to audit file."""
    AUDIT_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    rotate_log_if_needed()
    
    with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(info) + "\n")


def main():
    """Main entry point."""
    if SKIP_AUDIT:
        return 0
    
    info = get_command_info()
    
    if not info["command"]:
        return 0
    
    try:
        log_command(info)
    except Exception as e:
        # Don't fail if logging fails
        print(f"Warning: Failed to write audit log: {e}", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
