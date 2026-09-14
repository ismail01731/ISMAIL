from __future__ import annotations
from copy import copy
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse
@dataclass
class ReliabilityResult:
    evidence: list[Any]
    reliable: bool
    confidence: float
    reason: str
    contradiction_detected: bool = False
class Task2ReliabilityLayer:
    """
    Task 2: Reliability Layer.
    Responsibilities:
    - evaluate evidence quality
    - detect contradictory evidence
    - calculate a conservative confidence score
    - reject weak/insufficient evidence
    - never mutate the original evidence objects
    """
    MIN_RELIABLE_SCORE = 0.75
    MIN_RELIABLE_SOURCES = 2
    def evaluate(self, evidence: Iterable[Any] | None) -> ReliabilityResult:
        items = [item for item in (evidence or []) if item is not None]
        if not items:
            return ReliabilityResult(
                evidence=[],
                reliable=False,
                confidence=0.0,
                reason="No evidence is available.",
            )
        prepared = [copy(item) for item in items]
        reliable_items = [
            item
            for item in prepared
            if self._score(item) >= self.MIN_RELIABLE_SCORE
        ]
        domains = {
            domain
            for domain in (self._domain(item) for item in reliable_items)
            if domain
        }
        contradiction = self._has_contradiction(reliable_items)
        if contradiction:
            return ReliabilityResult(
                evidence=prepared,
                reliable=False,
                confidence=self._calculate_confidence(reliable_items, domains),
                reason="Contradictory evidence was detected.",
                contradiction_detected=True,
            )
        if len(reliable_items) < self.MIN_RELIABLE_SOURCES:
            return ReliabilityResult(
                evidence=prepared,
                reliable=False,
                confidence=self._calculate_confidence(reliable_items, domains),
                reason="Insufficient reliable independent evidence.",
            )
        if len(domains) < self.MIN_RELIABLE_SOURCES:
            return ReliabilityResult(
                evidence=prepared,
                reliable=False,
                confidence=self._calculate_confidence(reliable_items, domains),
                reason="Reliable evidence does not come from enough independent sources.",
            )
        corroborated = [
            item
            for item in reliable_items
            if getattr(item, "verification_status", "") in (
                "corroborated",
                "verified",
            )
        ]
        if not corroborated:
            return ReliabilityResult(
                evidence=prepared,
                reliable=False,
                confidence=self._calculate_confidence(reliable_items, domains),
                reason="Evidence has not passed the required verification gate.",
            )
        confidence = self._calculate_confidence(reliable_items, domains)
        return ReliabilityResult(
            evidence=reliable_items,
            reliable=confidence >= self.MIN_RELIABLE_SCORE,
            confidence=confidence,
            reason=(
                "Evidence passed the reliability gate."
                if confidence >= self.MIN_RELIABLE_SCORE
                else "Evidence confidence is below the reliability threshold."
            ),
            contradiction_detected=False,
        )
    def _score(self, item: Any) -> float:
        try:
            return float(getattr(item, "reliability_score", 0.0) or 0.0)
        except (TypeError, ValueError):
            return 0.0
    def _domain(self, item: Any) -> str:
        url = str(getattr(item, "url", "") or "").strip()
        if not url:
            return ""
        try:
            hostname = urlparse(url).hostname or ""
        except Exception:
            return ""
        return hostname.lower().removeprefix("www.").strip()
    def _calculate_confidence(
        self,
        items: list[Any],
        domains: set[str],
    ) -> float:
        if not items:
            return 0.0
        scores = [self._score(item) for item in items]
        average = sum(scores) / len(scores)
        source_bonus = min(0.10, max(0, len(domains) - 1) * 0.05)
        confidence = average + source_bonus
        return round(min(1.0, max(0.0, confidence)), 3)
    def _has_contradiction(self, items: list[Any]) -> bool:
        """
        Conservative contradiction detector.
        It only flags explicit opposing verification states.
        It does not guess semantic contradictions from unrelated text.
        """
        statuses = {
            str(getattr(item, "verification_status", "") or "").lower()
            for item in items
        }
        opposing_statuses = {
            "contradicted",
            "conflicting",
            "disputed",
        }
        return bool(statuses & opposing_statuses)
