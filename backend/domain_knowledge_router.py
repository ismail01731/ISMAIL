from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class KnowledgeRoute:
    domain: str
    source: str
    reason: str
    confidence: str = "medium"
class DomainKnowledgeRouter:
    """
    Selects the appropriate knowledge source for a detected domain.
    This module only routes.
    It does not perform database lookup, web research,
    or specialized capability execution.
    """
    DOMAIN_SOURCES: dict[str, str] = {
        "medical": "medical",
        "health": "medical",
        "electronics": "knowledge",
        "education": "knowledge",
        "mathematics": "knowledge",
        "science": "knowledge",
        "programming": "programming",
        "software": "programming",
        "web": "programming",
        "development": "programming",
    }
    def route(
        self,
        *,
        domains: list[dict] | None = None,
    ) -> list[KnowledgeRoute]:
        routes: list[KnowledgeRoute] = []
        for domain_info in domains or []:
            if not isinstance(domain_info, dict):
                continue
            domain = domain_info.get("domain")
            if not isinstance(domain, str):
                continue
            normalized = domain.strip().lower()
            source = self.DOMAIN_SOURCES.get(normalized)
            if source is None:
                continue
            confidence = domain_info.get("confidence", "medium")
            if not isinstance(confidence, str):
                confidence = "medium"
            routes.append(
                KnowledgeRoute(
                    domain=normalized,
                    source=source,
                    reason=(
                        f"The {normalized} domain is routed "
                        f"to the {source} knowledge source."
                    ),
                    confidence=confidence,
                )
            )
        unique_routes: list[KnowledgeRoute] = []
        seen: set[tuple[str, str]] = set()
        for route in routes:
            key = (route.domain, route.source)
            if key in seen:
                continue
            seen.add(key)
            unique_routes.append(route)
        return unique_routes
