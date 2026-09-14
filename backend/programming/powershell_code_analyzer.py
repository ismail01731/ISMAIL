from __future__ import annotations
import re
from typing import Any
from .analysis_types import CodeAnalysisResult
class PowerShellCodeAnalyzer:
    """
    Task 6.4: PowerShell Code Understanding.
    Performs dependency-free structural analysis of PowerShell source.
    It NEVER executes the supplied source code.
    """
    API_INDICATORS = {
        "Invoke-WebRequest",
        "Invoke-RestMethod",
        "Invoke-RestMethod",
        "Start-BitsTransfer",
        "Test-Connection",
    }
    DATABASE_INDICATORS = {
        "Invoke-Sqlcmd",
        "sqlcmd",
        "System.Data.SqlClient",
        "Microsoft.Data.SqlClient",
        "SQLite",
    }
    FUNCTION_PATTERN = re.compile(
        r"^\s*function\s+([A-Za-z_][A-Za-z0-9_-]*)",
        re.IGNORECASE | re.MULTILINE,
    )
    VARIABLE_PATTERN = re.compile(
        r"\$([A-Za-z_][A-Za-z0-9_]*)",
    )
    PARAM_PATTERN = re.compile(
        r"^\s*param\s*\((.*?)\)",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    CMDLET_PATTERN = re.compile(
        r"(?<![\w-])([A-Za-z][A-Za-z0-9]+-[A-Za-z][A-Za-z0-9]+)(?![\w-])"
    )
    IMPORT_PATTERN = re.compile(
        r"\b(?:Import-Module|Using\s+Module)\s+['\"]?([^'\"\s;]+)",
        re.IGNORECASE,
    )
    CONTROL_PATTERNS = {
        "if": r"\bif\s*\(",
        "elseif": r"\belseif\s*\(",
        "else": r"\belse\b",
        "foreach": r"\bforeach\s*\(",
        "for": r"\bfor\s*\(",
        "while": r"\bwhile\s*\(",
        "do": r"\bdo\b",
        "switch": r"\bswitch\s*\(",
        "try": r"\btry\s*\{",
        "catch": r"\bcatch\s*\{",
        "finally": r"\bfinally\s*\{",
    }
    EXCEPTION_PATTERN = re.compile(
        r"\b(?:throw|catch)\b",
        re.IGNORECASE,
    )
    def analyze(
        self,
        source: Any,
        language: str = "PowerShell",
    ) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="Source code must be a string.",
            )
        cleaned = self._strip_comments(source)
        if not cleaned.strip():
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="PowerShell source is empty.",
            )
        syntax_error = self._validate_structure(cleaned)
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
        self._extract_functions(cleaned, result)
        self._extract_variables(cleaned, result)
        self._extract_parameters(cleaned, result)
        self._extract_imports(cleaned, result)
        self._extract_cmdlets(cleaned, result)
        self._extract_control_flow(cleaned, result)
        self._extract_indicators(cleaned, result)
        self._extract_exceptions(cleaned, result)
        result.imports = self._unique(result.imports)
        result.functions = self._unique(result.functions)
        result.variables = self._unique(result.variables)
        result.classes = self._unique(result.classes)
        result.exceptions = self._unique(result.exceptions)
        result.async_functions = self._unique(result.async_functions)
        result.api_indicators = self._unique(result.api_indicators)
        result.database_indicators = self._unique(
            result.database_indicators
        )
        return result
    def _extract_functions(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for match in self.FUNCTION_PATTERN.finditer(source):
            result.functions.append(match.group(1))
    def _extract_variables(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        excluded = {
            "true",
            "false",
            "null",
            "args",
            "input",
            "this",
        }
        for match in self.VARIABLE_PATTERN.finditer(source):
            name = match.group(1)
            if name.lower() in excluded:
                continue
            result.variables.append(name)
    def _extract_parameters(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for match in self.PARAM_PATTERN.finditer(source):
            block = match.group(1)
            for name in re.findall(
                r"\$([A-Za-z_][A-Za-z0-9_]*)",
                block,
            ):
                result.variables.append(name)
    def _extract_imports(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for match in self.IMPORT_PATTERN.finditer(source):
            result.imports.append(match.group(1))
    def _extract_cmdlets(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        excluded = {
            "Where-Object",
            "ForEach-Object",
            "Select-Object",
            "Sort-Object",
            "Group-Object",
            "Measure-Object",
        }
        for match in self.CMDLET_PATTERN.finditer(source):
            cmdlet = match.group(1)
            if cmdlet in excluded:
                continue
            result.classes.append(cmdlet)
    def _extract_control_flow(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for name, pattern in self.CONTROL_PATTERNS.items():
            if re.search(
                pattern,
                source,
                flags=re.IGNORECASE,
            ):
                result.exceptions.append(
                    f"control:{name}"
                )
    def _extract_indicators(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        lowered = source.lower()
        for indicator in self.API_INDICATORS:
            if indicator.lower() in lowered:
                result.api_indicators.append(indicator)
        for indicator in self.DATABASE_INDICATORS:
            if indicator.lower() in lowered:
                result.database_indicators.append(indicator)
        if "|" in source:
            result.api_indicators.append("pipeline")
    def _extract_exceptions(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        if self.EXCEPTION_PATTERN.search(source):
            result.exceptions.append("exception_handling")
    @staticmethod
    def _strip_comments(source: str) -> str:
        lines = []
        for line in source.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#"):
                lines.append("")
                continue
            output = []
            quote = None
            escaped = False
            index = 0
            while index < len(line):
                char = line[index]
                if escaped:
                    output.append(char)
                    escaped = False
                    index += 1
                    continue
                if char == "`" and quote == '"':
                    output.append(char)
                    if index + 1 < len(line):
                        output.append(line[index + 1])
                        index += 2
                        continue
                if char in {"'", '"'}:
                    if quote is None:
                        quote = char
                    elif quote == char:
                        quote = None
                    output.append(char)
                    index += 1
                    continue
                if char == "#" and quote is None:
                    break
                output.append(char)
                index += 1
            lines.append("".join(output))
        return "\n".join(lines)
    @staticmethod
    def _validate_structure(source: str) -> str:
        stack = []
        quote = None
        escaped = False
        for char in source:
            if escaped:
                escaped = False
                continue
            if char == "`" and quote == '"':
                escaped = True
                continue
            if char in {"'", '"'}:
                if quote is None:
                    quote = char
                elif quote == char:
                    quote = None
                continue
            if quote is not None:
                continue
            if char in "({[":
                stack.append(char)
            elif char in ")}]":
                if not stack:
                    return (
                        "PowerShell syntax error: "
                        "unmatched closing delimiter."
                    )
                opening = stack.pop()
                expected = {
                    "(": ")",
                    "{": "}",
                    "[": "]",
                }[opening]
                if char != expected:
                    return (
                        "PowerShell syntax error: "
                        "mismatched delimiters."
                    )
        if quote is not None:
            return (
                "PowerShell syntax error: "
                "unterminated quote."
            )
        if stack:
            return (
                "PowerShell syntax error: "
                "unmatched opening delimiter."
            )
        return ""
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
powershell_code_analyzer = PowerShellCodeAnalyzer()
