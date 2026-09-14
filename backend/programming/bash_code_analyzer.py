from __future__ import annotations
import re
from typing import Any
from .analysis_types import CodeAnalysisResult
class BashCodeAnalyzer:
    """
    Task 6.4: Bash Code Understanding.
    Performs dependency-free structural analysis of Bash/shell source.
    It NEVER executes the supplied source code.
    """
    API_INDICATOR_PATTERNS = {
        "curl": r"\bcurl\b",
        "wget": r"\bwget\b",
        "ssh": r"\bssh\b",
        "scp": r"\bscp\b",
        "nc": r"\bnc\b",
        "netcat": r"\bnetcat\b",
    }
    DATABASE_INDICATOR_PATTERNS = {
        "sqlite3": r"\bsqlite3\b",
        "psql": r"\bpsql\b",
        "mysql": r"\bmysql\b",
        "mariadb": r"\bmariadb\b",
        "sqlcmd": r"\bsqlcmd\b",
        "mongo": r"\bmongo(?:sh)?\b",
    }
    COMMAND_PATTERN = re.compile(
        r"(?<![\w.-])"
        r"(?:sudo\s+)?"
        r"([A-Za-z_][A-Za-z0-9_.-]*)"
        r"(?![\w.-])"
    )
    FUNCTION_PATTERNS = (
        re.compile(
            r"^\s*(?:function\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*\))?\s*\{",
            re.MULTILINE,
        ),
        re.compile(
            r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(\s*\)\s*\{",
            re.MULTILINE,
        ),
    )
    VARIABLE_PATTERN = re.compile(
        r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=",
        re.MULTILINE,
    )
    IMPORT_PATTERN = re.compile(
        r"^\s*(?:source|\.)\s+(.+?)\s*$",
        re.MULTILINE,
    )
    SHEBANG_PATTERN = re.compile(
        r"^\s*#!\s*(?:/usr/bin/env\s+)?([^\s]+)"
    )
    CONTROL_KEYWORDS = {
        "if",
        "then",
        "elif",
        "else",
        "fi",
        "for",
        "while",
        "until",
        "do",
        "done",
        "case",
        "esac",
        "in",
        "select",
        "function",
        "time",
    }
    def analyze(
        self,
        source: Any,
        language: str = "Bash",
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
                syntax_error="Bash source is empty.",
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
        self._extract_shebang(cleaned, result)
        self._extract_functions(cleaned, result)
        self._extract_variables(cleaned, result)
        self._extract_imports(cleaned, result)
        self._extract_commands(cleaned, result)
        self._extract_indicators(cleaned, result)
        self._extract_control_flow(cleaned, result)
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
    def _extract_shebang(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        match = self.SHEBANG_PATTERN.search(source)
        if match:
            interpreter = match.group(1)
            result.imports.append(f"shebang:{interpreter}")
    def _extract_functions(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        seen = set()
        for pattern in self.FUNCTION_PATTERNS:
            for match in pattern.finditer(source):
                name = match.group(1)
                if name not in seen:
                    seen.add(name)
                    result.functions.append(name)
    def _extract_variables(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for match in self.VARIABLE_PATTERN.finditer(source):
            result.variables.append(match.group(1))
    def _extract_imports(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        for match in self.IMPORT_PATTERN.finditer(source):
            value = match.group(1).strip()
            if value:
                result.imports.append(value)
    def _extract_commands(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        control_words = self.CONTROL_KEYWORDS
        for line in source.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            stripped = re.sub(
                r"^(if|while|until|for)\b.*?\b(?:in|do)\b",
                "",
                stripped,
                flags=re.IGNORECASE,
            )
            parts = re.split(
                r"[|;&]+",
                stripped,
            )
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                part = re.sub(
                    r"^(then|do|else|elif)\b\s*",
                    "",
                    part,
                    flags=re.IGNORECASE,
                )
                match = self.COMMAND_PATTERN.match(part)
                if not match:
                    continue
                command = match.group(1)
                if command.lower() in control_words:
                    continue
                result.classes.append(command)
    def _extract_indicators(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        lowered = source.lower()
        for name, pattern in self.API_INDICATOR_PATTERNS.items():
            if re.search(pattern, lowered):
                result.api_indicators.append(name)
        for name, pattern in self.DATABASE_INDICATOR_PATTERNS.items():
            if re.search(pattern, lowered):
                result.database_indicators.append(name)
        if "|" in source:
            result.api_indicators.append("pipeline")
        if ">" in source or ">>" in source or "<" in source:
            result.api_indicators.append("redirection")
    def _extract_control_flow(
        self,
        source: str,
        result: CodeAnalysisResult,
    ) -> None:
        keywords = (
            "if",
            "for",
            "while",
            "until",
            "case",
            "select",
        )
        for keyword in keywords:
            if re.search(
                rf"^\s*{keyword}\b",
                source,
                flags=re.MULTILINE,
            ):
                result.exceptions.append(f"control:{keyword}")
    @staticmethod
    def _strip_comments(source: str) -> str:
        lines = []
        for line in source.splitlines():
            stripped = line.lstrip()
            if stripped.startswith("#!"):
                lines.append(line)
                continue
            if stripped.startswith("#"):
                lines.append("")
                continue
            quote = None
            output = []
            index = 0
            while index < len(line):
                char = line[index]
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
            if char == "\\" and quote == '"':
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
            if char in "{([":
                stack.append(char)
            elif char in "})]":
                if not stack:
                    return "Bash syntax error: unmatched closing delimiter."
                opening = stack.pop()
                expected = {
                    "(": ")",
                    "[": "]",
                    "{": "}",
                }[opening]
                if char != expected:
                    return "Bash syntax error: mismatched delimiters."
        if quote is not None:
            return "Bash syntax error: unterminated quote."
        if stack:
            return "Bash syntax error: unmatched opening delimiter."
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
bash_code_analyzer = BashCodeAnalyzer()
