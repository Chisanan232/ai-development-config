#!/usr/bin/env python3
"""
Dangerous command blocker for Windsurf Cascade.

This hook prevents dangerous commands from running automatically.
It checks commands against a blocklist and requires user confirmation.

Environment variables:
- WINDSURF_COMMAND: The command to be executed
- WINDSURF_ALLOW_DANGEROUS: Set to "1" to allow dangerous commands (use with caution)
"""

import os
import sys
import re
from typing import List, Tuple

# Configuration
ALLOW_DANGEROUS = os.getenv("WINDSURF_ALLOW_DANGEROUS", "0") == "1"

# Dangerous command patterns
DANGEROUS_PATTERNS = [
    # Destructive file operations
    (r"rm\s+-rf\s+/", "Recursive delete from root"),
    (r"rm\s+-rf\s+\*", "Recursive delete with wildcard"),
    (r"rm\s+-rf\s+~", "Recursive delete from home"),
    (r"rm\s+-rf\s+\.", "Recursive delete from current directory"),
    
    # System modifications
    (r"sudo\s+rm", "Sudo delete"),
    (r"sudo\s+dd", "Sudo disk operations"),
    (r"mkfs\.", "Format filesystem"),
    (r"fdisk", "Disk partitioning"),
    
    # Network operations
    (r"curl\s+.*\|\s*bash", "Pipe curl to bash"),
    (r"wget\s+.*\|\s*bash", "Pipe wget to bash"),
    (r"curl\s+.*\|\s*sh", "Pipe curl to sh"),
    (r"wget\s+.*\|\s*sh", "Pipe wget to sh"),
    
    # Database operations
    (r"DROP\s+DATABASE", "Drop database"),
    (r"DROP\s+TABLE", "Drop table"),
    (r"TRUNCATE\s+TABLE", "Truncate table"),
    (r"DELETE\s+FROM\s+\w+\s*;", "Delete all rows"),
    
    # Git operations
    (r"git\s+push\s+.*--force", "Force push"),
    (r"git\s+reset\s+--hard", "Hard reset"),
    (r"git\s+clean\s+-fd", "Clean untracked files"),
    
    # Process operations
    (r"kill\s+-9\s+-1", "Kill all processes"),
    (r"killall\s+-9", "Kill all by name"),
    
    # Package operations
    (r"pip\s+install\s+.*--no-verify", "Pip install without verification"),
    (r"npm\s+install\s+.*--ignore-scripts", "NPM install ignoring scripts"),
]

# Commands that require confirmation
CONFIRMATION_PATTERNS = [
    (r"npm\s+publish", "Publish to npm"),
    (r"cargo\s+publish", "Publish to crates.io"),
    (r"pip\s+upload", "Upload to PyPI"),
    (r"docker\s+rmi\s+.*-f", "Force remove Docker images"),
    (r"docker\s+system\s+prune", "Prune Docker system"),
]


def get_command() -> str:
    """Get command from environment."""
    return os.getenv("WINDSURF_COMMAND", "")


def check_dangerous_patterns(command: str) -> List[Tuple[str, str]]:
    """Check if command matches dangerous patterns."""
    matches = []
    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            matches.append((pattern, description))
    return matches


def check_confirmation_patterns(command: str) -> List[Tuple[str, str]]:
    """Check if command requires confirmation."""
    matches = []
    for pattern, description in CONFIRMATION_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            matches.append((pattern, description))
    return matches


def is_safe_command(command: str) -> bool:
    """Check if command is in safe list."""
    safe_prefixes = [
        "ls", "cat", "echo", "pwd", "cd",
        "git status", "git log", "git diff",
        "npm test", "npm run test",
        "pytest", "cargo test",
        "python -m", "node",
    ]
    
    for prefix in safe_prefixes:
        if command.strip().startswith(prefix):
            return True
    
    return False


def main():
    """Main entry point."""
    command = get_command()
    
    if not command:
        print("No command to check")
        return 0
    
    # Allow dangerous commands if explicitly enabled
    if ALLOW_DANGEROUS:
        print("⚠️  Dangerous commands allowed (WINDSURF_ALLOW_DANGEROUS=1)")
        return 0
    
    # Check if command is safe
    if is_safe_command(command):
        return 0
    
    # Check for dangerous patterns
    dangerous_matches = check_dangerous_patterns(command)
    if dangerous_matches:
        print("\n" + "=" * 60)
        print("🚫 DANGEROUS COMMAND BLOCKED")
        print("=" * 60)
        print(f"\nCommand: {command}")
        print("\nMatched patterns:")
        for pattern, description in dangerous_matches:
            print(f"  - {description}")
        print("\nThis command is blocked for safety.")
        print("If you need to run this command:")
        print("  1. Review the command carefully")
        print("  2. Run it manually in the terminal")
        print("  3. Or set WINDSURF_ALLOW_DANGEROUS=1 (use with extreme caution)")
        print("=" * 60)
        return 1
    
    # Check for confirmation patterns
    confirmation_matches = check_confirmation_patterns(command)
    if confirmation_matches:
        print("\n" + "=" * 60)
        print("⚠️  COMMAND REQUIRES CONFIRMATION")
        print("=" * 60)
        print(f"\nCommand: {command}")
        print("\nThis command requires manual confirmation:")
        for pattern, description in confirmation_matches:
            print(f"  - {description}")
        print("\nPlease run this command manually after reviewing.")
        print("=" * 60)
        return 1
    
    # Command is allowed
    return 0


if __name__ == "__main__":
    sys.exit(main())
