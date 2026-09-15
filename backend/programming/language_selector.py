from __future__ import annotations
from dataclasses import dataclass
from .language_registry import LanguageInfo, LanguageRegistry
@dataclass(frozen=True)
class LanguageSelection:
    language: str
    reason: str
    confidence: str = "medium"
class LanguageSelector:
    """
    Selects a suitable programming language from task context.
    This module only selects and normalizes a language.
    It does not generate, execute, debug, or analyze code.
    """
    def __init__(self, registry: LanguageRegistry | None = None) -> None:
        self.registry = registry or LanguageRegistry()
    def select(
        self,
        *,
        language: str | None = None,
        requirement: str = "",
        domain: str | None = None,
    ) -> LanguageSelection | None:
        explicit = self._detect_explicit_language(language)
        if explicit is not None:
            return LanguageSelection(
                language=explicit.name,
                reason="The requested programming language was explicitly identified.",
                confidence="high",
            )
        detected = self._detect_from_requirement(requirement)
        if detected is not None:
            return LanguageSelection(
                language=detected.name,
                reason="The programming language was identified from the task requirement.",
                confidence="high",
            )
        default = self._select_by_domain(domain)
        if default is not None:
            return LanguageSelection(
                language=default.name,
                reason="The language was selected from the programming task domain.",
                confidence="medium",
            )
        return None
    def _detect_explicit_language(
        self,
        language: str | None,
    ) -> LanguageInfo | None:
        if not isinstance(language, str) or not language.strip():
            return None
        return self.registry.detect(language)
    def _detect_from_requirement(
        self,
        requirement: str,
    ) -> LanguageInfo | None:
        if not isinstance(requirement, str) or not requirement.strip():
            return None

        
        words = requirement.lower()

        import re

        languages = sorted(
            self.registry.all_languages(),
            key=lambda language: max(
                (len(alias) for alias in language.aliases),
                default=0,
            ),
            reverse=True,
        )

        for language in languages:
            for alias in language.aliases:
                normalized_alias = alias.lower().strip()

                if not normalized_alias:
                    continue

                pattern = rf"(?<!\w){re.escape(normalized_alias)}(?!\w)"

                if re.search(pattern, words):
                    return language

                
        return None
    def _select_by_domain(
        self,
        domain: str | None,
    ) -> LanguageInfo | None:
        if not isinstance(domain, str):
            return None
        normalized = domain.strip().lower()
        preferred = {
    "programming": "javascript",
            "web": "javascript",
            "frontend": "javascript",
            "backend": "python",
            "data": "python",
            "data_science": "python",
            "machine_learning": "python",
            "android": "kotlin",
            "ios": "swift",
            "systems": "c++",
            "database": "sql",
            "shell": "bash",
        }
        alias = preferred.get(normalized)
        if alias is None:
            return None
        return self.registry.get_by_name(alias)
