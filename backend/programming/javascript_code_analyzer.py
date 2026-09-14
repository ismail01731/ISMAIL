from __future__ import annotations
import re
import subprocess
import tempfile
from pathlib import Path
from .analysis_types import CodeAnalysisResult
class JavaScriptCodeAnalyzer:
    """
    Task 6.1: JavaScript / TypeScript Code Understanding.
    This foundation performs structural source analysis without executing
    the supplied program.
    JavaScript syntax can optionally be validated through Node.js
    using `node --check`. TypeScript syntax validation is not delegated
    to Node because Node does not natively type-check TypeScript source.
    """
    API_INDICATORS = (
        "fetch",
        "axios",
        "express",
        "http",
        "https",
        "websocket",
    )
    DATABASE_INDICATORS = (
        "mongoose",
        "sequelize",
        "prisma",
        "pg",
        "mysql",
        "mysql2",
        "mongodb",
    )
    def analyze(
        self,
        source: object,
        language: str = "JavaScript",
    ) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="Source code must be a string.",
            )
        normalized_language = language.strip() or "JavaScript"
        if normalized_language.lower() not in {
            "javascript",
            "typescript",
        }:
            return CodeAnalysisResult(
                language=normalized_language,
                valid=False,
                syntax_error=(
                    "Supported languages: JavaScript, TypeScript."
                ),
            )
        syntax_error = None
        if normalized_language.lower() == "javascript":
            syntax_error = self._validate_javascript_syntax(source)
        result = CodeAnalysisResult(
            language=normalized_language,
            valid=syntax_error is None,
        )
        if syntax_error is not None:
            result.syntax_error = syntax_error
        result.imports = self._extract_imports(source)
        result.functions = self._extract_functions(source)
        result.classes = self._extract_classes(source)
        result.variables = self._extract_variables(source)
        result.exceptions = self._extract_exceptions(source)
        result.async_functions = self._extract_async_functions(source)
        result.api_indicators = self._extract_indicators(
            source,
            self.API_INDICATORS,
        )
        result.database_indicators = self._extract_indicators(
            source,
            self.DATABASE_INDICATORS,
        )
        return result
    @staticmethod
    def _extract_imports(source: str) -> list[str]:
        values = []
        patterns = (
            r"\bimport\s+(?:[^;]+?\s+from\s+)?['\"]([^'\"]+)['\"]",
            r"\brequire\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        )
        for pattern in patterns:
            values.extend(re.findall(pattern, source))
        return JavaScriptCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_functions(source: str) -> list[str]:
        values = []
        patterns = (
            r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(",
            r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>",
            r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s+)?[A-Za-z_$][\w$]*\s*=>",
        )
        for pattern in patterns:
            values.extend(re.findall(pattern, source))
        return JavaScriptCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_async_functions(source: str) -> list[str]:
        values = []
        patterns = (
            r"\basync\s+function\s+([A-Za-z_$][\w$]*)\s*\(",
            r"\b(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*async\b",
        )
        for pattern in patterns:
            values.extend(re.findall(pattern, source))
        return JavaScriptCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_classes(source: str) -> list[str]:
        return JavaScriptCodeAnalyzer._unique(
            re.findall(
                r"\bclass\s+([A-Za-z_$][\w$]*)",
                source,
            )
        )
    @staticmethod
    def _extract_variables(source: str) -> list[str]:
        values = []
        pattern = (
            r"\b(?:const|let|var)\s+"
            r"([A-Za-z_$][\w$]*)"
        )
        values.extend(re.findall(pattern, source))
        return JavaScriptCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_exceptions(source: str) -> list[str]:
        values = []
        values.extend(
            re.findall(
                r"\bcatch\s*\(\s*([A-Za-z_$][\w$]*)\s*\)",
                source,
            )
        )
        values.extend(
            re.findall(
                r"\bthrow\s+new\s+([A-Za-z_$][\w$]*)",
                source,
            )
        )
        return JavaScriptCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_indicators(
        source: str,
        indicators: tuple[str, ...],
    ) -> list[str]:
        lowered = source.lower()
        return [
            item
            for item in indicators
            if re.search(rf"\b{re.escape(item)}\b", lowered)
        ]
    @staticmethod
    def _validate_javascript_syntax(
        source: str,
    ) -> str | None:
        temp_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".js",
                encoding="utf-8",
                delete=False,
            ) as handle:
                handle.write(source)
                temp_path = Path(handle.name)
            completed = subprocess.run(
                ["node", "--check", str(temp_path)],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False,
            )
            if completed.returncode == 0:
                return None
            error = (
                completed.stderr.strip()
                or completed.stdout.strip()
                or "JavaScript syntax validation failed."
            )
            return error
        except FileNotFoundError:
            return "Node.js is not available for JavaScript syntax validation."
        except subprocess.TimeoutExpired:
            return "JavaScript syntax validation timed out."
        except Exception as exc:
            return str(exc)
        finally:
            if temp_path is not None:
                try:
                    temp_path.unlink(missing_ok=True)
                except OSError:
                    pass
    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        seen = set()
        result = []
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result
javascript_code_analyzer = JavaScriptCodeAnalyzer()

