from __future__ import annotations
import re
from typing import Any
from .analysis_types import CodeAnalysisResult
class CSSCodeAnalyzer:
    """
    Task 6.2: CSS Code Understanding.
    Dependency-free structural CSS analyzer.
    Does not execute CSS or modify files.
    """
    API_INDICATORS = (
        "url(",
        "@import",
        "@font-face",
    )
    def analyze(
        self,
        source: Any,
        language: str = "CSS",
    ) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="Source code must be a string.",
            )
        cleaned = self._remove_comments(source)
        syntax_error = self._validate_braces(cleaned)
        if syntax_error:
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error=syntax_error,
            )
        result = CodeAnalysisResult(
            language=language,
            valid=True,
        )
        result.imports = self._extract_imports(cleaned)
        result.functions = self._extract_at_rules(cleaned)
        result.classes = self._extract_class_selectors(cleaned)
        result.variables = self._extract_custom_properties(cleaned)
        result.exceptions = []
        result.async_functions = []
        result.api_indicators = self._extract_api_indicators(cleaned)
        result.database_indicators = []
        return result
    @staticmethod
    def _remove_comments(source: str) -> str:
        return re.sub(
            r"/\*.*?\*/",
            "",
            source,
            flags=re.DOTALL,
        )
    @staticmethod
    def _validate_braces(source: str) -> str | None:
        depth = 0
        for index, character in enumerate(source):
            if character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth < 0:
                    return (
                        "CSS syntax error: unexpected closing brace "
                        f"at position {index}."
                    )
        if depth != 0:
            return "CSS syntax error: unmatched braces."
        return None
    @staticmethod
    def _extract_imports(source: str) -> list[str]:
        values = []
        for match in re.finditer(
            r"@import\s+(?:url\(\s*)?[\"']?([^\"'\s\);]+)",
            source,
            flags=re.IGNORECASE,
        ):
            values.append(match.group(1))
        return CSSCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_at_rules(source: str) -> list[str]:
        values = []
        for match in re.finditer(
            r"@([a-zA-Z-]+)",
            source,
        ):
            values.append("@" + match.group(1).lower())
        return CSSCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_class_selectors(source: str) -> list[str]:
        values = []
        # Remove quoted strings so file names and URLs such as
        # "theme.css", "bg.png", and "font.woff2" are not
        # mistaken for CSS class selectors.
        cleaned = re.sub(
            r"""(["'])(?:\\.|(?!\1).)*\1""",
            "",
            source,
            flags=re.DOTALL,
        )
        # CSS class selectors begin with "." followed by a valid
        # identifier and are normally selector tokens.
        for match in re.finditer(
            r"(?<![a-zA-Z0-9_-])\.([a-zA-Z_][a-zA-Z0-9_-]*)",
            cleaned,
        ):
            values.append(match.group(1))
        return CSSCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_custom_properties(source: str) -> list[str]:
        values = []
        for match in re.finditer(
            r"(--[a-zA-Z0-9_-]+)\s*:",
            source,
        ):
            values.append(match.group(1))
        return CSSCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_api_indicators(source: str) -> list[str]:
        values = []
        lowered = source.lower()
        if "url(" in lowered:
            values.append("url")
        if "@import" in lowered:
            values.append("@import")
        if "@font-face" in lowered:
            values.append("@font-face")
        return CSSCodeAnalyzer._unique(values)
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
css_code_analyzer = CSSCodeAnalyzer()

