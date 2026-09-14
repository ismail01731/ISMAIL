from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .language_registry import LanguageRegistry
@dataclass
class ProjectFile:
    path: str
    relative_path: str
    name: str
    extension: str
    language: str | None
    category: str
@dataclass
class ProjectAnalysisResult:
    root: str
    exists: bool
    total_files: int
    analyzed_files: int
    skipped_files: int
    directories: list[str] = field(default_factory=list)
    files: list[ProjectFile] = field(default_factory=list)
    languages: dict[str, int] = field(default_factory=dict)
    categories: dict[str, int] = field(default_factory=dict)
    reason: str = ""
class ProjectAnalyzer:
    """
    Task 5.3: Project Awareness / Project Analyzer.
    Responsibilities:
    - inspect project structure
    - classify relevant files
    - detect programming languages
    - identify project categories
    - ignore generated/dependency directories
    - produce a safe read-only project summary
    This module NEVER:
    - executes project code
    - modifies files
    - deletes files
    - installs packages
    """
    DEFAULT_IGNORED_DIRECTORIES = {
        ".git",
        ".gradle",
        ".idea",
        ".kotlin",

        # Python virtual environments
        ".venv",
        ".venv312",
        "venv",
        "env",
        ".env",
        "__pycache__",
        "site-packages",
        "__pypackages__",

        # Build / dependency / cache directories
        "build",
        "dist",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
        ".cache",

        # Backup directories
        "backup",
        "backups",
        "universalai_backup",
    }
    CATEGORY_MAP = {
        "backend": "backend",
        "frontend": "frontend",
        "app": "mobile",
        "mobile": "mobile",
        "desktop": "desktop",
        "config": "config",
        "data": "data",
        "programming": "programming",
        "voice": "voice",
        "vision": "vision",
        "llm": "ai",
        "medical": "medical",
        "live_intelligence": "ai",
    }
    CONFIG_EXTENSIONS = {
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".env",
        ".properties",
        ".xml",
        ".gradle",
    }
    DATA_EXTENSIONS = {
        ".csv",
        ".jsonl",
        ".db",
        ".sqlite",
        ".sqlite3",
    }
    def __init__(
        self,
        language_registry: LanguageRegistry | None = None,
        ignored_directories: set[str] | None = None,
    ) -> None:
        self.language_registry = (
            language_registry
            or LanguageRegistry()
        )
        self.ignored_directories = {
            value.lower()
            for value in (
                ignored_directories
                or self.DEFAULT_IGNORED_DIRECTORIES
            )
        }
    def analyze(
        self,
        root: str | Path,
    ) -> ProjectAnalysisResult:
        project_root = Path(root)
        if not project_root.exists():
            return ProjectAnalysisResult(
                root=str(project_root),
                exists=False,
                total_files=0,
                analyzed_files=0,
                skipped_files=0,
                reason="Project root does not exist.",
            )
        if not project_root.is_dir():
            return ProjectAnalysisResult(
                root=str(project_root),
                exists=False,
                total_files=0,
                analyzed_files=0,
                skipped_files=0,
                reason="Project root is not a directory.",
            )
        directories = []
        files = []
        total_files = 0
        skipped_files = 0
        languages: dict[str, int] = {}
        categories: dict[str, int] = {}
        for current_root, dir_names, file_names in self._walk(
            project_root
        ):
            relative_dir = self._relative_path(
                project_root,
                current_root,
            )
            if relative_dir:
                directories.append(relative_dir)
            for file_name in file_names:
                total_files += 1
                file_path = Path(current_root) / file_name
                if self._should_skip_file(file_path):
                    skipped_files += 1
                    continue
                project_file = self._classify_file(
                    project_root,
                    file_path,
                )
                if project_file is None:
                    skipped_files += 1
                    continue
                files.append(project_file)
                if project_file.language:
                    languages[project_file.language] = (
                        languages.get(
                            project_file.language,
                            0,
                        )
                        + 1
                    )
                categories[project_file.category] = (
                    categories.get(
                        project_file.category,
                        0,
                    )
                    + 1
                )
        return ProjectAnalysisResult(
            root=str(project_root.resolve()),
            exists=True,
            total_files=total_files,
            analyzed_files=len(files),
            skipped_files=skipped_files,
            directories=sorted(set(directories)),
            files=files,
            languages=dict(
                sorted(
                    languages.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ),
            categories=dict(
                sorted(
                    categories.items(),
                    key=lambda item: (-item[1], item[0]),
                )
            ),
            reason="Project structure analyzed successfully.",
        )
    def _walk(
        self,
        root: Path,
    ):
        for current_root, dir_names, file_names in __import__(
            "os"
        ).walk(root):
            dir_names[:] = [
                name
                for name in dir_names
                if name.lower()
                not in self.ignored_directories
            ]
            yield current_root, dir_names, file_names
    def _classify_file(
        self,
        root: Path,
        file_path: Path,
    ) -> ProjectFile | None:
        try:
            relative_path = file_path.relative_to(root)
        except ValueError:
            return None
        extension = file_path.suffix.lower()
        language_info = (
            self.language_registry.detect_from_file(
                file_path
            )
        )
        language = (
            language_info.name
            if language_info is not None
            else None
        )
        category = self._category(
            relative_path,
            extension,
            language,
        )
        if language is None and extension not in (
            self.CONFIG_EXTENSIONS
            | self.DATA_EXTENSIONS
        ):
            return None
        return ProjectFile(
            path=str(file_path.resolve()),
            relative_path=str(relative_path),
            name=file_path.name,
            extension=extension,
            language=language,
            category=category,
        )
    def _category(
        self,
        relative_path: Path,
        extension: str,
        language: str | None,
    ) -> str:
        parts = [
            part.lower()
            for part in relative_path.parts[:-1]
        ]
        for part in parts:
            if part in self.CATEGORY_MAP:
                return self.CATEGORY_MAP[part]
        if extension in self.DATA_EXTENSIONS:
            return "data"
        if extension in self.CONFIG_EXTENSIONS:
            return "config"
        if language in {
            "HTML",
            "CSS",
            "JavaScript",
            "TypeScript",
        }:
            return "frontend"
        if language in {
            "Python",
            "Java",
            "Kotlin",
            "Swift",
            "Dart",
            "C",
            "C++",
            "C#",
            "Go",
            "Rust",
            "PHP",
            "Ruby",
        }:
            return "source"
        if language in {
            "SQL",
        }:
            return "database"
        if language in {
            "Bash",
            "PowerShell",
        }:
            return "shell"
        return "other"
    def _should_skip_file(
        self,
        file_path: Path,
    ) -> bool:
        name = file_path.name.lower()
        if name.endswith((
            ".pyc",
            ".pyo",
            ".class",
        )):
            return True
        if name.startswith("~$"):
            return True
        return False
    @staticmethod
    def _relative_path(
        root: Path,
        current_root: str,
    ) -> str:
        try:
            relative = Path(current_root).relative_to(root)
        except ValueError:
            return ""
        if str(relative) == ".":
            return ""
        return str(relative)
project_analyzer = ProjectAnalyzer()
