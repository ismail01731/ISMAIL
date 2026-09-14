from __future__ import annotations
import ast

from typing import Any

from .analysis_types import CodeAnalysisResult
from .javascript_code_analyzer import JavaScriptCodeAnalyzer
from .html_code_analyzer import HTMLCodeAnalyzer
from .css_code_analyzer import CSSCodeAnalyzer
from .sql_code_analyzer import SQLCodeAnalyzer
from .bash_code_analyzer import BashCodeAnalyzer
from .powershell_code_analyzer import PowerShellCodeAnalyzer
class PythonCodeAnalyzer:
    """
    Task 5.2: Python Code Understanding.
    Uses Python AST instead of executing the supplied code.
    This analyzer:
    - parses Python source
    - identifies imports
    - identifies functions and classes
    - identifies assigned variables
    - identifies exception handlers
    - identifies async functions
    - detects basic API/database indicators
    It NEVER executes the analyzed source code.
    """
    API_MODULES = {
        "fastapi",
        "flask",
        "django",
        "requests",
        "httpx",
        "aiohttp",
        "urllib",
        "websocket",
    }
    DATABASE_MODULES = {
        "sqlite3",
        "sqlalchemy",
        "psycopg",
        "psycopg2",
        "pymysql",
        "mysql",
        "asyncpg",
        "mongodb",
        "pymongo",
    }
    def analyze(self, source: Any) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language="Python",
                valid=False,
                syntax_error="Source code must be a string.",
            )
        try:
            tree = ast.parse(source)
        except SyntaxError as exc:
            return CodeAnalysisResult(
                language="Python",
                valid=False,
                syntax_error=self._format_syntax_error(exc),
            )
        except Exception as exc:
            return CodeAnalysisResult(
                language="Python",
                valid=False,
                syntax_error=str(exc),
            )
        result = CodeAnalysisResult(
            language="Python",
            valid=True,
        )
        for node in ast.walk(tree):
            self._inspect_node(node, result)
        result.imports = self._unique(result.imports)
        result.functions = self._unique(result.functions)
        result.classes = self._unique(result.classes)
        result.variables = self._unique(result.variables)
        result.exceptions = self._unique(result.exceptions)
        result.async_functions = self._unique(result.async_functions)
        result.api_indicators = self._unique(result.api_indicators)
        result.database_indicators = self._unique(
            result.database_indicators
        )
        return result
    def _inspect_node(
        self,
        node: ast.AST,
        result: CodeAnalysisResult,
    ) -> None:
        if isinstance(node, ast.Import):
            for alias in node.names:
                result.imports.append(alias.name)
                self._check_module_indicators(alias.name, result)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module:
                result.imports.append(module)
                self._check_module_indicators(module, result)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result.functions.append(node.name)
            if isinstance(node, ast.AsyncFunctionDef):
                result.async_functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            result.classes.append(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                result.variables.extend(
                    self._assignment_names(target)
                )
        elif isinstance(node, ast.AnnAssign):
            result.variables.extend(
                self._assignment_names(node.target)
            )
        elif isinstance(node, ast.AugAssign):
            result.variables.extend(
                self._assignment_names(node.target)
            )
        elif isinstance(node, ast.ExceptHandler):
            if node.type is not None:
                exception_name = self._exception_name(node.type)
                if exception_name:
                    result.exceptions.append(exception_name)
        elif isinstance(node, ast.Raise):
            if node.exc is not None:
                exception_name = self._exception_name(node.exc)
                if exception_name:
                    result.exceptions.append(exception_name)
    def _check_module_indicators(
        self,
        module: str,
        result: CodeAnalysisResult,
    ) -> None:
        root = module.split(".")[0].lower()
        if root in self.API_MODULES:
            result.api_indicators.append(module)
        if root in self.DATABASE_MODULES:
            result.database_indicators.append(module)
    @staticmethod
    def _assignment_names(node: ast.AST) -> list[str]:
        names = []
        if isinstance(node, ast.Name):
            names.append(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for element in node.elts:
                names.extend(
                    PythonCodeAnalyzer._assignment_names(element)
                )
        return names
    @staticmethod
    def _exception_name(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            parts = []
            current: ast.AST | None = node
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return ".".join(reversed(parts))
        if isinstance(node, ast.Call):
            return PythonCodeAnalyzer._exception_name(node.func)
        return ""
    @staticmethod
    def _format_syntax_error(exc: SyntaxError) -> str:
        message = str(exc).strip()
        if exc.lineno:
            return f"Line {exc.lineno}: {message}"
        return message
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
class MultiLanguageCodeAnalyzer:
    """
    Task 6.2 integration layer.
    Routes each supported language to its dedicated analyzer:
    Python, JavaScript, TypeScript, HTML, and CSS.
    """
    SUPPORTED_LANGUAGES = {
        "python",
        "javascript",
        "typescript",
        "html",
        "css",
        "sql",
        "bash",
        "powershell",
    }
    def __init__(self) -> None:
        self.python_analyzer = PythonCodeAnalyzer()
        self.javascript_analyzer = JavaScriptCodeAnalyzer()
        self.html_analyzer = HTMLCodeAnalyzer()
        self.css_analyzer = CSSCodeAnalyzer()
        self.sql_analyzer = SQLCodeAnalyzer()
        self.bash_analyzer = BashCodeAnalyzer()
        self.powershell_analyzer = PowerShellCodeAnalyzer()
    def analyze(
        self,
        source: Any,
        language: str = "Python",
    ) -> CodeAnalysisResult:
        normalized = (language or "Python").strip().lower()
        if normalized == "python":
            return self.python_analyzer.analyze(source)
        if normalized in {"javascript", "typescript"}:
            return self.javascript_analyzer.analyze(
                source,
                language=language,
            )
        if normalized == "html":
            return self.html_analyzer.analyze(
                source,
                language=language,
            )
        if normalized == "css":
            return self.css_analyzer.analyze(
                source,
                language=language,
            )
        if normalized == "sql":
            return self.sql_analyzer.analyze(
                source,
                language=language,
            )
        if normalized == "bash":
            return self.bash_analyzer.analyze(
                source,
                language=language,
            )
        if normalized in {"powershell", "pwsh", "ps1"}:
            return self.powershell_analyzer.analyze(
                source,
                language=language,
            )
        return CodeAnalysisResult(
            language=language,
            valid=False,
            syntax_error=(
                "Supported languages: "
                "Python, JavaScript, TypeScript, HTML, CSS, SQL, Bash, PowerShell."
            ),
        )
code_analyzer = MultiLanguageCodeAnalyzer()








