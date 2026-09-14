from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class ResearchFreshnessDecision:
    needs_research: bool
    freshness_required: bool
    reason: str
    confidence: str = "medium"
class ResearchFreshnessRouter:
    """
    Decides whether a question requires fresh external research.
    This module only makes the routing decision.
    It does not perform web research, knowledge lookup,
    or freshness calculation.
    """
    LIVE_INTENTS = {
        "live_information",
    }
    LIVE_ROUTES = {
        "live",
        "research",
    }
    FRESH_DOMAINS = {
        "live_information",
        "research",
    }
    def decide(
        self,
        *,
        intent: str | None = None,
        route: str | None = None,
        domains: list[dict] | None = None,
    ) -> ResearchFreshnessDecision:
        normalized_intent = (
            intent.strip().lower()
            if isinstance(intent, str)
            else ""
        )
        normalized_route = (
            route.strip().lower()
            if isinstance(route, str)
            else ""
        )
        if (
            normalized_intent in self.LIVE_INTENTS
            or normalized_route in self.LIVE_ROUTES
        ):
            return ResearchFreshnessDecision(
                needs_research=True,
                freshness_required=True,
                reason=(
                    "The request requires current or time-sensitive "
                    "information."
                ),
                confidence="high",
            )
        for domain_info in domains or []:
            if not isinstance(domain_info, dict):
                continue
            domain = domain_info.get("domain")
            if not isinstance(domain, str):
                continue
            if domain.strip().lower() in self.FRESH_DOMAINS:
                return ResearchFreshnessDecision(
                    needs_research=True,
                    freshness_required=True,
                    reason=(
                        "The detected domain requires fresh external "
                        "information."
                    ),
                    confidence="high",
                )
        return ResearchFreshnessDecision(
            needs_research=False,
            freshness_required=False,
            reason=(
                "The request does not currently require fresh "
                "external research."
            ),
            confidence="medium",
        )
