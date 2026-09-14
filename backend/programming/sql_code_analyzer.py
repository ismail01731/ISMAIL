from __future__ import annotations
import re
from typing import Any
from .analysis_types import CodeAnalysisResult
class SQLCodeAnalyzer:
    """
    Task 6.3: SQL Code Understanding.
    Dependency-free structural SQL analyzer.
    Does not execute SQL or modify databases/files.
    """
    API_INDICATORS = (
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "CREATE",
        "ALTER",
        "DROP",
        "JOIN",
        "TRANSACTION",
    )
    DATABASE_INDICATORS = (
        "POSTGRESQL",
        "POSTGRES",
        "MYSQL",
        "SQLITE",
        "MSSQL",
        "SQL SERVER",
        "ORACLE",
    )
    SQL_KEYWORDS = {
        "SELECT",
        "FROM",
        "WHERE",
        "INSERT",
        "INTO",
        "VALUES",
        "UPDATE",
        "SET",
        "DELETE",
        "CREATE",
        "ALTER",
        "DROP",
        "TABLE",
        "VIEW",
        "INDEX",
        "DATABASE",
        "SCHEMA",
        "JOIN",
        "INNER",
        "LEFT",
        "RIGHT",
        "FULL",
        "OUTER",
        "ON",
        "GROUP",
        "BY",
        "ORDER",
        "HAVING",
        "LIMIT",
        "OFFSET",
        "UNION",
        "ALL",
        "DISTINCT",
        "AS",
        "AND",
        "OR",
        "NOT",
        "NULL",
        "IS",
        "IN",
        "EXISTS",
        "CASE",
        "WHEN",
        "THEN",
        "ELSE",
        "END",
        "PRIMARY",
        "KEY",
        "FOREIGN",
        "REFERENCES",
        "UNIQUE",
        "CHECK",
        "DEFAULT",
        "CONSTRAINT",
        "BEGIN",
        "COMMIT",
        "ROLLBACK",
        "TRANSACTION",
    }
    def analyze(
        self,
        source: Any,
        language: str = "SQL",
    ) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="Source code must be a string.",
            )
        cleaned = self._remove_comments(source).strip()
        if not cleaned:
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="SQL source is empty.",
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
        result.imports = self._extract_tables(cleaned)
        result.functions = self._extract_sql_functions(cleaned)
        result.classes = self._extract_statement_types(cleaned)
        result.variables = self._extract_columns(cleaned)
        result.exceptions = []
        result.async_functions = []
        result.api_indicators = self._extract_api_indicators(cleaned)
        result.database_indicators = self._extract_database_indicators(
            cleaned
        )
        return result
    @staticmethod
    def _remove_comments(source: str) -> str:
        source = re.sub(
            r"/\*.*?\*/",
            "",
            source,
            flags=re.DOTALL,
        )
        source = re.sub(
            r"--[^\r\n]*",
            "",
            source,
        )
        return source
    @staticmethod
    def _validate_structure(source: str) -> str | None:
        single_quote_open = False
        double_quote_open = False
        parentheses = 0
        index = 0
        while index < len(source):
            character = source[index]
            if character == "'" and not double_quote_open:
                if (
                    index + 1 < len(source)
                    and source[index + 1] == "'"
                ):
                    index += 2
                    continue
                single_quote_open = not single_quote_open
            elif character == '"' and not single_quote_open:
                if (
                    index + 1 < len(source)
                    and source[index + 1] == '"'
                ):
                    index += 2
                    continue
                double_quote_open = not double_quote_open
            elif not single_quote_open and not double_quote_open:
                if character == "(":
                    parentheses += 1
                elif character == ")":
                    parentheses -= 1
                    if parentheses < 0:
                        return (
                            "SQL syntax error: unexpected closing "
                            "parenthesis."
                        )
            index += 1
        if single_quote_open:
            return "SQL syntax error: unmatched single quote."
        if double_quote_open:
            return "SQL syntax error: unmatched double quote."
        if parentheses != 0:
            return "SQL syntax error: unmatched parentheses."
        statement = source.lstrip().upper()
        if not re.match(
            r"^(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|"
            r"WITH|BEGIN|COMMIT|ROLLBACK|TRUNCATE|REPLACE)\b",
            statement,
        ):
            return (
                "SQL syntax error: unsupported or unrecognized "
                "statement."
            )
        return None
    @classmethod
    def _extract_tables(cls, source: str) -> list[str]:
        values = []
        patterns = (
            r"\bFROM\s+([A-Za-z_][A-Za-z0-9_.]*)",
            r"\bJOIN\s+([A-Za-z_][A-Za-z0-9_.]*)",
            r"\bINTO\s+([A-Za-z_][A-Za-z0-9_.]*)",
            r"\bUPDATE\s+([A-Za-z_][A-Za-z0-9_.]*)",
        )
        for pattern in patterns:
            for match in re.finditer(
                pattern,
                source,
                flags=re.IGNORECASE,
            ):
                value = match.group(1)
                if value.upper() not in cls.SQL_KEYWORDS:
                    values.append(value)
        return cls._unique(values)
    @staticmethod
    def _extract_sql_functions(source: str) -> list[str]:
        values = []
        for match in re.finditer(
            r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(",
            source,
        ):
            name = match.group(1)
            if name.upper() in SQLCodeAnalyzer.SQL_KEYWORDS:
                continue
            values.append(name)
        return SQLCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_statement_types(source: str) -> list[str]:
        values = []
        pattern = (
            r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|"
            r"DROP|WITH|BEGIN|COMMIT|ROLLBACK|TRUNCATE|REPLACE)\b"
        )
        for match in re.finditer(
            pattern,
            source,
            flags=re.IGNORECASE,
        ):
            values.append(match.group(1).upper())
        return SQLCodeAnalyzer._unique(values)
    @classmethod
    def _extract_columns(cls, source: str) -> list[str]:
        values = []
        select_match = re.search(
            r"\bSELECT\s+(.*?)\s+\bFROM\b",
            source,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if not select_match:
            return values
        section = select_match.group(1)
        for item in section.split(","):
            item = item.strip()
            alias_match = re.match(
                r"(.+?)\s+\bAS\s+([A-Za-z_][A-Za-z0-9_]*)$",
                item,
                flags=re.IGNORECASE,
            )
            if alias_match:
                item = alias_match.group(2)
            item = item.strip()
            if re.fullmatch(
                r"[A-Za-z_][A-Za-z0-9_.]*",
                item,
            ):
                values.append(item)
        return cls._unique(values)
    @classmethod
    def _extract_api_indicators(cls, source: str) -> list[str]:
        upper = source.upper()
        values = []
        for indicator in cls.API_INDICATORS:
            if re.search(
                rf"\b{re.escape(indicator)}\b",
                upper,
            ):
                values.append(indicator)
        return values
    @classmethod
    def _extract_database_indicators(cls, source: str) -> list[str]:
        upper = source.upper()
        values = []
        for indicator in cls.DATABASE_INDICATORS:
            if indicator in upper:
                values.append(indicator)
        return values
    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        seen = set()
        result = []
        for value in values:
            normalized = value.lower()
            if normalized in seen:
                continue
            seen.add(normalized)
            result.append(value)
        return result
sql_code_analyzer = SQLCodeAnalyzer()
