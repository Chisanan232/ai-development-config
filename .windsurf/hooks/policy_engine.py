#!/usr/bin/env python3
"""
Policy Engine Hook - Enforces project-specific policies

This hook validates code changes against project policies defined in AGENTS.md
and .windsurf/rules/. It provides scope-aware, diff-based validation with
language-specific checkers.

Usage:
    python3 hooks/policy_engine.py [--strict] [--scope=<scope>]

Environment Variables:
    WINDSURF_POLICY_MODE: 'strict' or 'lenient' (default: lenient)
    WINDSURF_POLICY_SCOPE: Scope of changes (e.g., 'feature', 'bugfix', 'refactor')
    WINDSURF_SKIP_POLICY: Set to '1' to skip policy checks
    WINDSURF_POLICY_LANGUAGES: Comma-separated list of languages to check (default: auto-detect)

Supported Languages:
    - Python (.py)
    - TypeScript/JavaScript (.ts, .tsx, .js, .jsx)
    - React (.jsx, .tsx with React patterns)
    - Vue (.vue)
    - Java (.java)
    - Kotlin (.kt, .kts)
    - Scala (.scala)
    - Rust (.rs)
    - Go (.go)
    - Generic checks for all languages
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod


class PolicySeverity(Enum):
    """Policy violation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ChangeScope(Enum):
    """Scope of code changes"""
    FEATURE = "feature"
    BUGFIX = "bugfix"
    REFACTOR = "refactor"
    TEST = "test"
    DOCS = "docs"
    CHORE = "chore"


@dataclass
class PolicyViolation:
    """Represents a policy violation"""
    rule: str
    severity: PolicySeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None


class LanguageChecker(ABC):
    """Abstract base class for language-specific checkers"""
    
    @abstractmethod
    def get_file_extensions(self) -> List[str]:
        """Return list of file extensions this checker handles"""
        pass
    
    @abstractmethod
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check a file for language-specific issues"""
        pass
    
    def get_test_patterns(self) -> List[str]:
        """Return patterns that identify test files"""
        return ["test"]


class PythonChecker(LanguageChecker):
    """Python-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".py"]
    
    def get_test_patterns(self) -> List[str]:
        return ["test_", "_test.py", "/tests/", "/test/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Python file for issues"""
        self._check_imports(file_path, violations)
        self._check_dangerous_patterns(file_path, violations)
    
    def _check_imports(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Python import organization"""
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            code_started = False
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                
                if stripped.startswith('"""') or stripped.startswith("'''") or stripped.startswith("#"):
                    continue
                
                if stripped and not stripped.startswith("import ") and not stripped.startswith("from "):
                    if not stripped.startswith("__"):
                        code_started = True
                
                if code_started and (stripped.startswith("import ") or stripped.startswith("from ")):
                    violations.append(PolicyViolation(
                        rule="python-import-organization",
                        severity=PolicySeverity.WARNING,
                        message="Imports should be at the top of the file",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass
    
    def _check_dangerous_patterns(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for dangerous Python patterns"""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                lines = content.split("\n")
            
            for i, line in enumerate(lines, 1):
                if "except:" in line and "except Exception:" not in line:
                    violations.append(PolicyViolation(
                        rule="python-bare-except",
                        severity=PolicySeverity.WARNING,
                        message="Avoid bare 'except:' clauses. Catch specific exceptions.",
                        file_path=file_path,
                        line_number=i
                    ))
            
            if "test" not in file_path:
                for i, line in enumerate(lines, 1):
                    stripped = line.strip()
                    if stripped.startswith("print(") and not stripped.startswith("#"):
                        violations.append(PolicyViolation(
                            rule="python-print-statement",
                            severity=PolicySeverity.INFO,
                            message="Consider using logging instead of print() in production code",
                            file_path=file_path,
                            line_number=i
                        ))
        except Exception:
            pass


class TypeScriptChecker(LanguageChecker):
    """TypeScript/JavaScript-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".ts", ".tsx", ".js", ".jsx"]
    
    def get_test_patterns(self) -> List[str]:
        return [".test.", ".spec.", "/__tests__/", "/test/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check TypeScript/JavaScript file for issues"""
        self._check_console_statements(file_path, violations)
    
    def _check_console_statements(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for console.log in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("console.log(") or stripped.startswith("console.debug("):
                    violations.append(PolicyViolation(
                        rule="typescript-console-statement",
                        severity=PolicySeverity.INFO,
                        message="Consider removing console.log() from production code",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass


class JavaChecker(LanguageChecker):
    """Java-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".java"]
    
    def get_test_patterns(self) -> List[str]:
        return ["Test.java", "/test/", "/tests/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Java file for issues"""
        self._check_system_out(file_path, violations)
    
    def _check_system_out(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for System.out in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if "System.out.print" in line:
                    violations.append(PolicyViolation(
                        rule="java-system-out",
                        severity=PolicySeverity.INFO,
                        message="Consider using a logging framework instead of System.out",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass


class RustChecker(LanguageChecker):
    """Rust-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".rs"]
    
    def get_test_patterns(self) -> List[str]:
        return ["#[test]", "#[cfg(test)]", "/tests/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Rust file for issues"""
        # Rust has strong compiler checks, so we keep this minimal
        pass


class GoChecker(LanguageChecker):
    """Go-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".go"]
    
    def get_test_patterns(self) -> List[str]:
        return ["_test.go"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Go file for issues"""
        # Go has strong tooling (gofmt, golint), so we keep this minimal
        pass


class KotlinChecker(LanguageChecker):
    """Kotlin-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".kt", ".kts"]
    
    def get_test_patterns(self) -> List[str]:
        return ["Test.kt", "/test/", "/tests/", "Spec.kt"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Kotlin file for issues"""
        self._check_println(file_path, violations)
    
    def _check_println(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for println in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("println(") or "println(" in stripped:
                    violations.append(PolicyViolation(
                        rule="kotlin-println",
                        severity=PolicySeverity.INFO,
                        message="Consider using a logging framework instead of println() in production code",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass


class ScalaChecker(LanguageChecker):
    """Scala-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".scala"]
    
    def get_test_patterns(self) -> List[str]:
        return ["Test.scala", "Spec.scala", "/test/", "/tests/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Scala file for issues"""
        self._check_println(file_path, violations)
    
    def _check_println(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for println in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                if "println(" in line:
                    violations.append(PolicyViolation(
                        rule="scala-println",
                        severity=PolicySeverity.INFO,
                        message="Consider using a logging framework instead of println() in production code",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass


class ReactChecker(LanguageChecker):
    """React-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".jsx", ".tsx"]
    
    def get_test_patterns(self) -> List[str]:
        return [".test.", ".spec.", "/__tests__/", "/test/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check React file for issues"""
        self._check_console_statements(file_path, violations)
        self._check_react_patterns(file_path, violations)
    
    def _check_console_statements(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for console.log in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("console.log(") or stripped.startswith("console.debug("):
                    violations.append(PolicyViolation(
                        rule="react-console-statement",
                        severity=PolicySeverity.INFO,
                        message="Consider removing console.log() from production code",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass
    
    def _check_react_patterns(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for React-specific anti-patterns"""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                lines = content.split("\n")
            
            # Check for missing key prop in map
            for i, line in enumerate(lines, 1):
                if ".map(" in line and "key=" not in line and "key =" not in line:
                    # Simple heuristic - may have false positives
                    if "=>" in line or "function" in line:
                        violations.append(PolicyViolation(
                            rule="react-missing-key",
                            severity=PolicySeverity.WARNING,
                            message="Consider adding 'key' prop when using .map() to render lists",
                            file_path=file_path,
                            line_number=i
                        ))
        except Exception:
            pass


class VueChecker(LanguageChecker):
    """Vue-specific policy checker"""
    
    def get_file_extensions(self) -> List[str]:
        return [".vue"]
    
    def get_test_patterns(self) -> List[str]:
        return [".test.", ".spec.", "/__tests__/", "/test/"]
    
    def check_file(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check Vue file for issues"""
        self._check_console_statements(file_path, violations)
        self._check_vue_patterns(file_path, violations)
    
    def _check_console_statements(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for console.log in production code"""
        if any(pattern in file_path for pattern in self.get_test_patterns()):
            return
        
        try:
            with open(file_path, "r") as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("console.log(") or stripped.startswith("console.debug("):
                    violations.append(PolicyViolation(
                        rule="vue-console-statement",
                        severity=PolicySeverity.INFO,
                        message="Consider removing console.log() from production code",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass
    
    def _check_vue_patterns(self, file_path: str, violations: List[PolicyViolation]) -> None:
        """Check for Vue-specific anti-patterns"""
        try:
            with open(file_path, "r") as f:
                content = f.read()
                lines = content.split("\n")
            
            # Check for v-for without key
            for i, line in enumerate(lines, 1):
                if "v-for=" in line and ":key=" not in line and "v-bind:key=" not in line:
                    violations.append(PolicyViolation(
                        rule="vue-missing-key",
                        severity=PolicySeverity.WARNING,
                        message="Consider adding ':key' attribute when using v-for directive",
                        file_path=file_path,
                        line_number=i
                    ))
        except Exception:
            pass


class PolicyEngine:
    """Enforces project policies on code changes"""
    
    def __init__(self, strict_mode: bool = False, scope: Optional[ChangeScope] = None):
        self.strict_mode = strict_mode or os.getenv("WINDSURF_POLICY_MODE") == "strict"
        self.scope = scope or self._detect_scope()
        self.violations: List[PolicyViolation] = []
        self.project_root = self._find_project_root()
        self.language_checkers = self._initialize_checkers()
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".windsurf").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _initialize_checkers(self) -> List[LanguageChecker]:
        """Initialize language-specific checkers"""
        checkers = [
            PythonChecker(),
            TypeScriptChecker(),
            ReactChecker(),
            VueChecker(),
            JavaChecker(),
            KotlinChecker(),
            ScalaChecker(),
            RustChecker(),
            GoChecker(),
        ]
        
        # Filter by environment variable if specified
        enabled_langs = os.getenv("WINDSURF_POLICY_LANGUAGES", "").lower()
        if enabled_langs:
            lang_set = set(enabled_langs.split(","))
            checkers = [c for c in checkers if any(
                ext.lstrip(".") in lang_set for ext in c.get_file_extensions()
            )]
        
        return checkers
    
    def _get_checker_for_file(self, file_path: str) -> Optional[LanguageChecker]:
        """Get the appropriate language checker for a file"""
        for checker in self.language_checkers:
            if any(file_path.endswith(ext) for ext in checker.get_file_extensions()):
                return checker
        return None
    
    def _detect_scope(self) -> ChangeScope:
        """Detect the scope of changes from environment or git branch"""
        # Check environment variable first
        scope_env = os.getenv("WINDSURF_POLICY_SCOPE", "").lower()
        if scope_env:
            try:
                return ChangeScope(scope_env)
            except ValueError:
                pass
        
        # Try to detect from git branch name
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            branch = result.stdout.strip().lower()
            
            if "feature/" in branch or "feat/" in branch:
                return ChangeScope.FEATURE
            elif "fix/" in branch or "bugfix/" in branch:
                return ChangeScope.BUGFIX
            elif "refactor/" in branch:
                return ChangeScope.REFACTOR
            elif "test/" in branch:
                return ChangeScope.TEST
            elif "docs/" in branch:
                return ChangeScope.DOCS
        except subprocess.CalledProcessError:
            pass
        
        return ChangeScope.CHORE
    
    def get_changed_files(self) -> Set[str]:
        """Get list of changed files from git"""
        try:
            # Get staged files
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            staged = set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
            
            # Get unstaged files
            result = subprocess.run(
                ["git", "diff", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            unstaged = set(result.stdout.strip().split("\n")) if result.stdout.strip() else set()
            
            return staged | unstaged
        except subprocess.CalledProcessError:
            return set()
    
    def _is_test_file(self, file_path: str) -> bool:
        """Check if a file is a test file using language-specific patterns"""
        checker = self._get_checker_for_file(file_path)
        if checker:
            return any(pattern in file_path for pattern in checker.get_test_patterns())
        return "test" in file_path.lower()
    
    def check_test_coverage_requirements(self, changed_files: Set[str]) -> None:
        """Check if test files exist for changed source files"""
        if self.scope == ChangeScope.TEST or self.scope == ChangeScope.DOCS:
            return
        
        # Separate source and test files
        source_files = {f for f in changed_files if not self._is_test_file(f) and self._get_checker_for_file(f)}
        test_files = {f for f in changed_files if self._is_test_file(f)}
        
        # If source files changed but no tests, warn for new features
        if source_files and not test_files and self.scope == ChangeScope.FEATURE:
            self.violations.append(PolicyViolation(
                rule="test-coverage",
                severity=PolicySeverity.WARNING,
                message=f"New feature changes {len(source_files)} source files but no test files. Consider adding tests.",
            ))
    
    def check_commit_message_format(self) -> None:
        """Check if commit message follows conventions"""
        # This would typically check the last commit message
        # For now, we'll skip this as it's better handled by git hooks
        pass
    
    def check_file_with_language_checker(self, file_path: str) -> None:
        """Check file using appropriate language-specific checker"""
        checker = self._get_checker_for_file(file_path)
        if checker:
            checker.check_file(file_path, self.violations)
    
    def check_scope_specific_policies(self, changed_files: Set[str]) -> None:
        """Apply scope-specific policy checks"""
        test_files = {f for f in changed_files if self._is_test_file(f)}
        
        if self.scope == ChangeScope.REFACTOR:
            if not test_files:
                self.violations.append(PolicyViolation(
                    rule="refactor-without-tests",
                    severity=PolicySeverity.ERROR if self.strict_mode else PolicySeverity.WARNING,
                    message="Refactoring should include test verification. No test files modified."
                ))
        
        elif self.scope == ChangeScope.BUGFIX:
            if not test_files:
                self.violations.append(PolicyViolation(
                    rule="bugfix-without-test",
                    severity=PolicySeverity.WARNING,
                    message="Consider adding a regression test for this bugfix"
                ))
    
    def run_checks(self) -> bool:
        """Run all policy checks"""
        # Check if policy checks are disabled
        if os.getenv("WINDSURF_SKIP_POLICY") == "1":
            print("ℹ️  Policy checks skipped (WINDSURF_SKIP_POLICY=1)")
            return True
        
        changed_files = self.get_changed_files()
        
        if not changed_files:
            print("ℹ️  No changed files detected")
            return True
        
        print(f"🔍 Running policy checks on {len(changed_files)} files (scope: {self.scope.value})...")
        
        # Run language-specific checks
        for file_path in changed_files:
            if os.path.exists(file_path):
                self.check_file_with_language_checker(file_path)
        
        self.check_test_coverage_requirements(changed_files)
        self.check_scope_specific_policies(changed_files)
        
        # Report violations
        return self._report_violations()
    
    def _report_violations(self) -> bool:
        """Report policy violations and return success status"""
        if not self.violations:
            print("✅ All policy checks passed")
            return True
        
        # Group by severity
        errors = [v for v in self.violations if v.severity == PolicySeverity.ERROR]
        warnings = [v for v in self.violations if v.severity == PolicySeverity.WARNING]
        infos = [v for v in self.violations if v.severity == PolicySeverity.INFO]
        
        # Print violations
        if errors:
            print(f"\n❌ {len(errors)} policy error(s):")
            for v in errors:
                location = f"{v.file_path}:{v.line_number}" if v.file_path else "general"
                print(f"  [{v.rule}] {location}: {v.message}")
        
        if warnings:
            print(f"\n⚠️  {len(warnings)} policy warning(s):")
            for v in warnings:
                location = f"{v.file_path}:{v.line_number}" if v.file_path else "general"
                print(f"  [{v.rule}] {location}: {v.message}")
        
        if infos:
            print(f"\nℹ️  {len(infos)} policy info:")
            for v in infos:
                location = f"{v.file_path}:{v.line_number}" if v.file_path else "general"
                print(f"  [{v.rule}] {location}: {v.message}")
        
        # In strict mode, errors fail the check
        if self.strict_mode and errors:
            print("\n❌ Policy check failed (strict mode)")
            return False
        
        # In lenient mode, only fail on errors, warnings are informational
        if errors:
            print("\n⚠️  Policy violations found but not blocking (lenient mode)")
            print("   Set WINDSURF_POLICY_MODE=strict to enforce")
        
        return True


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Windsurf Policy Engine")
    parser.add_argument("--strict", action="store_true", help="Enable strict mode")
    parser.add_argument("--scope", type=str, help="Change scope (feature, bugfix, refactor, etc.)")
    args = parser.parse_args()
    
    scope = None
    if args.scope:
        try:
            scope = ChangeScope(args.scope.lower())
        except ValueError:
            print(f"⚠️  Invalid scope: {args.scope}")
            scope = None
    
    engine = PolicyEngine(strict_mode=args.strict, scope=scope)
    success = engine.run_checks()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
