# Global Rules

These rules apply to all projects on your machine.

**Location**: `~/.codeium/memories/global_rules.md`

---

## Detailed Policy References

For comprehensive policy details, see the rules in `~/.codeium/memories/rules/`:

- **Coding Standards**: See `rules/coding-standards.md` for code quality expectations
- **Testing Policy**: See `rules/testing-policy.md` for test requirements and coverage
- **Commit Policy**: See `rules/commit-policy.md` for commit message format and hygiene
- **PR Policy**: See `rules/pr-policy.md` for pull request preparation and review
- **CI Policy**: See `rules/ci-policy.md` for CI/CD expectations and failure handling
- **Typing Policy**: See `rules/typing-policy.md` for type hint standards (Python projects)

**Note**: Copy your workspace rules from `.windsurf/rules/` to `~/.codeium/memories/rules/` to use them globally across all projects if you need.

---

## General Coding Principles

- Prefer explicit over implicit
- Write code for humans first, computers second
- Keep functions small and focused (< 50 lines when possible)
- Use meaningful, descriptive names for variables and functions

## Code Quality

- Use early returns to reduce nesting
- Avoid deep nesting (> 3 levels)
- Remove unused imports and dead code
- Add comments for non-obvious logic, not obvious code

## Testing

- Write tests for new features before or alongside implementation
- Update tests when changing behavior
- Mock external dependencies (APIs, databases, file systems)
- Test edge cases and error conditions
- Use descriptive test names that explain what is being tested

## Git Commits

- Write clear, descriptive commit messages
- Keep commits atomic and focused on a single change
- Reference issue numbers when applicable (e.g., "Fixes #123")
- Don't commit commented-out code or debug statements
- Review your own changes before committing

## Code Review

- Review your own code before submitting for review
- Check for edge cases and error handling
- Ensure tests cover new functionality
- Update documentation when behavior changes
- Respond to review comments promptly and constructively

## Documentation

- Add docstrings to all public functions and classes
- Keep README files up to date
- Document non-obvious decisions and trade-offs
- Include usage examples in documentation
- Update documentation when code behavior changes

## Error Handling

- Handle errors explicitly, don't silently ignore them
- Provide helpful error messages with context
- Fail fast with clear validation errors
- Log errors with sufficient context for debugging
- Use specific exception types, not generic ones

## Security

- Never commit secrets, API keys, or passwords
- Validate and sanitize all user input
- Use environment variables for configuration
- Be cautious with user-provided data
- Follow principle of least privilege

---

## Customization Instructions

1. **Copy this template** to `~/.codeium/memories/global_rules.md`
2. **Edit the rules** to match your personal preferences
3. **Remove sections** that don't apply to you
4. **Add new sections** for your specific needs
5. **Keep it concise** - rules should be short and actionable

## Tips

- Don't duplicate rules that are already in Cascade's training data (e.g., "write good code")
- Be specific rather than vague
- Use bullet points for easy scanning
- Group related rules together
- Update regularly as your preferences evolve

## Example: Adding Language-Specific Rules

You can add language-specific sections:

```markdown
## Python-Specific

- Use type hints for function signatures
- Prefer f-strings over .format() or %
- Use pathlib instead of os.path
- Follow PEP 8 style guidelines

## JavaScript/TypeScript-Specific

- Use const by default, let when needed, avoid var
- Prefer async/await over raw promises
- Use TypeScript strict mode
- Destructure objects and arrays when appropriate
```

## Example: Adding Project-Type Rules

You can add rules for specific project types:

```markdown
## API Development

- Validate all input parameters
- Return consistent error response formats
- Add proper HTTP status codes
- Include request/response examples in docs
- Implement rate limiting considerations

## Frontend Development

- Ensure accessibility (ARIA labels, keyboard navigation)
- Optimize for performance (lazy loading, code splitting)
- Handle loading and error states
- Make UI responsive for different screen sizes
```

---

**Remember**: Global rules apply to ALL your projects. For project-specific rules, use `.windsurf/rules/*.md` in your repository instead.
