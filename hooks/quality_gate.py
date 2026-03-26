#!/usr/bin/env python3
"""
Quality gate hook for Windsurf Cascade.

This hook runs lightweight quality checks on modified files after code is written.
It is designed to be fast and provide quick feedback without blocking the workflow.

Environment variables:
- WINDSURF_STRICT_MODE: Set to "1" to enable strict mode (fail on warnings)
- WINDSURF_SKIP_QUALITY_GATE: Set to "1" to skip quality gate
- WINDSURF_MODIFIED_FILES: Comma-separated list of modified files
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any
import time

# Configuration
STRICT_MODE = os.getenv("WINDSURF_STRICT_MODE", "0") == "1"
SKIP_QUALITY_GATE = os.getenv("WINDSURF_SKIP_QUALITY_GATE", "0") == "1"
COOLDOWN_SECONDS = 60  # Don't run more than once per minute
COOLDOWN_FILE = Path(".windsurf/.quality_gate_last_run")


def get_modified_files() -> List[str]:
    """Get list of modified files from environment or git."""
    # Try environment variable first
    env_files = os.getenv("WINDSURF_MODIFIED_FILES", "")
    if env_files:
        return [f.strip() for f in env_files.split(",") if f.strip()]
    
    # Fall back to git diff
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        return [f.strip() for f in result.stdout.split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        return []


def check_cooldown() -> bool:
    """Check if we're in cooldown period."""
    if not COOLDOWN_FILE.exists():
        return False
    
    last_run = COOLDOWN_FILE.stat().st_mtime
    elapsed = time.time() - last_run
    return elapsed < COOLDOWN_SECONDS


def update_cooldown():
    """Update cooldown timestamp."""
    COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
    COOLDOWN_FILE.touch()


def is_python_file(filepath: str) -> bool:
    """Check if file is a Python file."""
    return filepath.endswith(".py")


def is_javascript_file(filepath: str) -> bool:
    """Check if file is a JavaScript/TypeScript file."""
    return filepath.endswith((".js", ".jsx", ".ts", ".tsx"))


def run_python_checks(files: List[str]) -> Dict[str, Any]:
    """Run Python-specific checks."""
    python_files = [f for f in files if is_python_file(f)]
    if not python_files:
        return {"passed": True, "checks": []}
    
    checks = []
    
    # Check for common issues
    for filepath in python_files:
        if not Path(filepath).exists():
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check for debug statements
        if "print(" in content or "pdb.set_trace()" in content:
            checks.append({
                "file": filepath,
                "type": "warning",
                "message": "Debug statements found (print, pdb)"
            })
        
        # Check for TODO without issue reference
        if "TODO" in content and "#" not in content[content.find("TODO"):content.find("TODO")+50]:
            checks.append({
                "file": filepath,
                "type": "info",
                "message": "TODO comment without issue reference"
            })
    
    passed = all(c["type"] != "error" for c in checks)
    if STRICT_MODE:
        passed = passed and all(c["type"] not in ["error", "warning"] for c in checks)
    
    return {"passed": passed, "checks": checks}


def run_javascript_checks(files: List[str]) -> Dict[str, Any]:
    """Run JavaScript/TypeScript-specific checks."""
    js_files = [f for f in files if is_javascript_file(f)]
    if not js_files:
        return {"passed": True, "checks": []}
    
    checks = []
    
    # Check for common issues
    for filepath in js_files:
        if not Path(filepath).exists():
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check for debug statements
        if "console.log(" in content or "debugger" in content:
            checks.append({
                "file": filepath,
                "type": "warning",
                "message": "Debug statements found (console.log, debugger)"
            })
        
        # Check for TODO without issue reference
        if "TODO" in content and "#" not in content[content.find("TODO"):content.find("TODO")+50]:
            checks.append({
                "file": filepath,
                "type": "info",
                "message": "TODO comment without issue reference"
            })
    
    passed = all(c["type"] != "error" for c in checks)
    if STRICT_MODE:
        passed = passed and all(c["type"] not in ["error", "warning"] for c in checks)
    
    return {"passed": passed, "checks": checks}


def run_general_checks(files: List[str]) -> Dict[str, Any]:
    """Run general checks applicable to all files."""
    checks = []
    
    for filepath in files:
        if not Path(filepath).exists():
            continue
        
        # Check file size
        file_size = Path(filepath).stat().st_size
        if file_size > 1_000_000:  # 1 MB
            checks.append({
                "file": filepath,
                "type": "warning",
                "message": f"Large file ({file_size / 1_000_000:.1f} MB)"
            })
    
    passed = all(c["type"] != "error" for c in checks)
    if STRICT_MODE:
        passed = passed and all(c["type"] not in ["error", "warning"] for c in checks)
    
    return {"passed": passed, "checks": checks}


def print_results(results: List[Dict[str, Any]]):
    """Print check results."""
    all_checks = []
    for result in results:
        all_checks.extend(result["checks"])
    
    if not all_checks:
        print("✓ Quality gate: All checks passed")
        return
    
    print("\n" + "=" * 60)
    print("Quality Gate Results")
    print("=" * 60)
    
    errors = [c for c in all_checks if c["type"] == "error"]
    warnings = [c for c in all_checks if c["type"] == "warning"]
    infos = [c for c in all_checks if c["type"] == "info"]
    
    if errors:
        print(f"\n❌ Errors ({len(errors)}):")
        for check in errors:
            print(f"  {check['file']}: {check['message']}")
    
    if warnings:
        print(f"\n⚠️  Warnings ({len(warnings)}):")
        for check in warnings:
            print(f"  {check['file']}: {check['message']}")
    
    if infos:
        print(f"\nℹ️  Info ({len(infos)}):")
        for check in infos:
            print(f"  {check['file']}: {check['message']}")
    
    print("\n" + "=" * 60)
    
    if STRICT_MODE:
        print("Running in STRICT MODE - warnings treated as errors")
    else:
        print("Tip: Set WINDSURF_STRICT_MODE=1 for strict checking")


def main():
    """Main entry point."""
    # Check if quality gate is disabled
    if SKIP_QUALITY_GATE:
        print("Quality gate skipped (WINDSURF_SKIP_QUALITY_GATE=1)")
        return 0
    
    # Check cooldown
    if check_cooldown():
        print("Quality gate skipped (cooldown period)")
        return 0
    
    # Get modified files
    modified_files = get_modified_files()
    if not modified_files:
        print("No modified files to check")
        return 0
    
    print(f"Running quality gate on {len(modified_files)} file(s)...")
    
    # Run checks
    results = [
        run_general_checks(modified_files),
        run_python_checks(modified_files),
        run_javascript_checks(modified_files),
    ]
    
    # Print results
    print_results(results)
    
    # Update cooldown
    update_cooldown()
    
    # Determine exit code
    all_passed = all(r["passed"] for r in results)
    if not all_passed:
        print("\n⚠️  Quality gate found issues (not blocking)")
        return 0  # Don't block workflow
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
