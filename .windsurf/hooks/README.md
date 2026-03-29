# Windsurf Cascade Hooks

This directory contains hook scripts for Windsurf Cascade enforcement and auditing.

## Overview

Hooks provide lightweight validation, enforcement, and auditing without blocking the development workflow.

## Available Hooks

### quality_gate.py

Runs lightweight quality checks on modified files after code is written.

**Features:**
- Checks for debug statements (print, console.log, debugger)
- Checks for TODO comments without issue references
- Checks for large files
- Language-specific checks (Python, JavaScript/TypeScript)
- Cooldown mechanism to avoid running too frequently

**Environment variables:**
- `WINDSURF_STRICT_MODE=1`: Treat warnings as errors
- `WINDSURF_SKIP_QUALITY_GATE=1`: Skip quality gate
- `WINDSURF_MODIFIED_FILES`: Comma-separated list of modified files

**Usage:**
```bash
python3 hooks/quality_gate.py
```

### block_dangerous_commands.py

Prevents dangerous commands from running automatically.

**Features:**
- Blocks destructive file operations (rm -rf, etc.)
- Blocks dangerous system modifications
- Blocks piping untrusted sources to shell
- Blocks dangerous database operations
- Requires confirmation for publishing operations

**Environment variables:**
- `WINDSURF_COMMAND`: The command to be executed
- `WINDSURF_ALLOW_DANGEROUS=1`: Allow dangerous commands (use with caution)

**Usage:**
```bash
WINDSURF_COMMAND="rm -rf /" python3 hooks/block_dangerous_commands.py
```

### audit_log.py

Logs command execution for audit trail and analysis.

**Features:**
- Logs all commands executed
- Records timestamp, user, exit code
- Automatic log rotation
- Non-blocking (doesn't fail if logging fails)

**Environment variables:**
- `WINDSURF_COMMAND`: The command that was executed
- `WINDSURF_COMMAND_EXIT_CODE`: Exit code of the command
- `WINDSURF_SKIP_AUDIT=1`: Skip audit logging

**Audit log location:** `.windsurf/audit.log`

**Usage:**
```bash
WINDSURF_COMMAND="npm test" WINDSURF_COMMAND_EXIT_CODE="0" python3 hooks/audit_log.py
```

## Hook Configuration

Hooks are configured in `.windsurf/hooks.json`:

```json
{
  "hooks": {
    "post_write_code": [
      {
        "command": "python3 hooks/quality_gate.py",
        "show_output": true,
        "description": "Run lightweight quality checks"
      }
    ],
    "pre_run_command": [
      {
        "command": "python3 hooks/block_dangerous_commands.py",
        "show_output": true,
        "description": "Block dangerous commands"
      }
    ],
    "post_run_command": [
      {
        "command": "python3 hooks/audit_log.py",
        "show_output": false,
        "description": "Log command execution"
      }
    ]
  },
  "config": {
    "enabled": true,
    "timeout_seconds": 30,
    "fail_on_error": false
  }
}
```

## Customizing Hooks

### Adding Project-Specific Checks

Edit `quality_gate.py` to add project-specific checks:

```python
def run_project_checks(files: List[str]) -> Dict[str, Any]:
    """Run project-specific checks."""
    checks = []
    
    # Add your custom checks here
    for filepath in files:
        # Example: check for specific patterns
        if "deprecated_function()" in Path(filepath).read_text():
            checks.append({
                "file": filepath,
                "type": "warning",
                "message": "Use of deprecated function"
            })
    
    return {"passed": True, "checks": checks}
```

### Adding Dangerous Command Patterns

Edit `block_dangerous_commands.py` to add patterns:

```python
DANGEROUS_PATTERNS = [
    # Add your patterns here
    (r"your_pattern", "Description"),
]
```

### Customizing Audit Log

Edit `audit_log.py` to customize what gets logged:

```python
def get_command_info():
    """Get command information from environment."""
    return {
        "command": os.getenv("WINDSURF_COMMAND", ""),
        # Add more fields here
        "project": "my-project",
        "environment": os.getenv("ENV", "dev"),
    }
```

## Best Practices

### Do:
- Keep hooks fast (< 5 seconds)
- Make hooks non-blocking by default
- Use environment variables for configuration
- Log errors but don't fail on logging issues
- Use cooldown mechanisms for expensive checks
- Provide clear error messages

### Don't:
- Run full test suites in hooks (too slow)
- Run expensive type checking on every edit
- Block the workflow for non-critical issues
- Assume specific project structure
- Hardcode project-specific values

## Disabling Hooks

### Temporarily disable all hooks

Set in `.windsurf/hooks.json`:
```json
{
  "config": {
    "enabled": false
  }
}
```

### Disable specific hook

Comment out in `.windsurf/hooks.json`:
```json
{
  "hooks": {
    "post_write_code": [
      // {
      //   "command": "python3 hooks/quality_gate.py",
      //   "show_output": true
      // }
    ]
  }
}
```

### Skip via environment variable

```bash
WINDSURF_SKIP_QUALITY_GATE=1  # Skip quality gate
WINDSURF_SKIP_AUDIT=1         # Skip audit logging
```

## Troubleshooting

### Hook times out

Increase timeout in `.windsurf/hooks.json`:
```json
{
  "config": {
    "timeout_seconds": 60
  }
}
```

### Hook fails

Check hook output and logs. Set `fail_on_error: false` to make hooks non-blocking.

### Hook runs too frequently

Adjust cooldown in `quality_gate.py`:
```python
COOLDOWN_SECONDS = 120  # 2 minutes
```

## Security Considerations

- Review hook scripts before running
- Be cautious with `WINDSURF_ALLOW_DANGEROUS=1`
- Audit logs may contain sensitive information
- Hooks run with your user permissions
- Keep hook scripts in version control

## Examples

### Run quality gate manually

```bash
WINDSURF_MODIFIED_FILES="src/user.py,src/auth.py" python3 hooks/quality_gate.py
```

### Run in strict mode

```bash
WINDSURF_STRICT_MODE=1 python3 hooks/quality_gate.py
```

### Test dangerous command blocking

```bash
WINDSURF_COMMAND="rm -rf /" python3 hooks/block_dangerous_commands.py
```

### View audit log

```bash
cat .windsurf/audit.log | jq .
```

## Notes

- Hooks are optional but recommended
- Start with lightweight checks
- Add more checks as needed
- Monitor hook performance
- Adjust based on team feedback
