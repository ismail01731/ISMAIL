from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
@dataclass(frozen=True)
class LanguageInfo:
    name: str
    extensions: tuple[str, ...]
    aliases: tuple[str, ...]
    category: str
    executable: str | None = None
class LanguageRegistry:
    """
    Task 5.1: Programming Language Registry.
    Provides:
    - supported language metadata
    - alias lookup
    - file-extension detection
    - language-name normalization
    This module does NOT execute code.
    """
    def __init__(self) -> None:
        self._languages: tuple[LanguageInfo, ...] = (
            LanguageInfo(
                name="Python",
                extensions=(".py", ".pyw", ".pyi"),
                aliases=("python", "py", "python3"),
                category="general-purpose",
                executable="python",
            ),
            LanguageInfo(
                name="JavaScript",
                extensions=(".js", ".mjs", ".cjs"),
                aliases=("javascript", "js", "node", "nodejs"),
                category="web/general-purpose",
                executable="node",
            ),
            LanguageInfo(
                name="TypeScript",
                extensions=(".ts", ".mts", ".cts"),
                aliases=("typescript", "ts"),
                category="web/general-purpose",
                executable="node",
            ),
            LanguageInfo(
                name="HTML",
                extensions=(".html", ".htm"),
                aliases=("html",),
                category="web",
            ),
            LanguageInfo(
                name="CSS",
                extensions=(".css",),
                aliases=("css",),
                category="web",
            ),
            LanguageInfo(
                name="SQL",
                extensions=(".sql",),
                aliases=("sql",),
                category="database",
            ),
            LanguageInfo(
                name="Bash",
                extensions=(".sh", ".bash"),
                aliases=("bash", "sh", "shell"),
                category="shell",
                executable="bash",
            ),
            LanguageInfo(
                name="PowerShell",
                extensions=(".ps1", ".psm1", ".psd1"),
                aliases=("powershell", "pwsh", "ps1"),
                category="shell",
                executable="pwsh",
            ),
            LanguageInfo(
                name="Java",
                extensions=(".java",),
                aliases=("java",),
                category="general-purpose",
                executable="java",
            ),
            LanguageInfo(
                name="C",
                extensions=(".c", ".h"),
                aliases=("c",),
                category="systems",
                executable="gcc",
            ),
            LanguageInfo(
                name="C++",
                extensions=(".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx"),
                aliases=("c++", "cpp", "cplusplus"),
                category="systems",
                executable="g++",
            ),
            LanguageInfo(
                name="C#",
                extensions=(".cs",),
                aliases=("c#", "csharp", "cs"),
                category="general-purpose",
                executable="dotnet",
            ),
            LanguageInfo(
                name="Go",
                extensions=(".go",),
                aliases=("go", "golang"),
                category="systems/backend",
                executable="go",
            ),
            LanguageInfo(
                name="Rust",
                extensions=(".rs",),
                aliases=("rust", "rs"),
                category="systems/backend",
                executable="rustc",
            ),
            LanguageInfo(
                name="PHP",
                extensions=(".php",),
                aliases=("php",),
                category="web/backend",
                executable="php",
            ),
            LanguageInfo(
                name="Ruby",
                extensions=(".rb",),
                aliases=("ruby", "rb"),
                category="general-purpose",
                executable="ruby",
            ),
            LanguageInfo(
                name="Kotlin",
                extensions=(".kt", ".kts"),
                aliases=("kotlin", "kt"),
                category="android/general-purpose",
                executable="kotlinc",
            ),
            LanguageInfo(
                name="Swift",
                extensions=(".swift",),
                aliases=("swift",),
                category="ios/general-purpose",
                executable="swift",
            ),
            LanguageInfo(
                name="Dart",
                extensions=(".dart",),
                aliases=("dart",),
                category="mobile/general-purpose",
                executable="dart",
            ),
        )
        self._by_alias: dict[str, LanguageInfo] = {}
        for language in self._languages:
            for alias in language.aliases:
                self._by_alias[alias.lower().strip()] = language
        self._by_extension: dict[str, LanguageInfo] = {}
        for language in self._languages:
            for extension in language.extensions:
                self._by_extension[extension.lower()] = language
    def all_languages(self) -> list[LanguageInfo]:
        return list(self._languages)
    def get_by_name(self, name: Any) -> LanguageInfo | None:
        if not isinstance(name, str):
            return None
        return self._by_alias.get(
            name.lower().strip()
        )
    def detect_from_file(self, file_path: str | Path) -> LanguageInfo | None:
        try:
            suffix = Path(file_path).suffix.lower()
        except Exception:
            return None
        if not suffix:
            return None
        return self._by_extension.get(suffix)
    def detect(self, value: Any) -> LanguageInfo | None:
        """
        Detect a language from either:
        - language name/alias
        - filename/path
        """
        if not isinstance(value, (str, Path)):
            return None
        text = str(value).strip()
        if not text:
            return None
        by_name = self.get_by_name(text)
        if by_name is not None:
            return by_name
        return self.detect_from_file(text)
language_registry = LanguageRegistry()
