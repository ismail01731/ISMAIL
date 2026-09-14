from __future__ import annotations
from copy import copy
from dataclasses import dataclass
from typing import Any, Iterable
import re
@dataclass
class AnswerSynthesisResult:
    evidence: list[Any]
    claims: list[str]
    answer_points: list[str]
    source_count: int
    reason: str
class Task4AnswerSynthesisLayer:
    """
    Task 4: Answer Synthesis Layer.
    Responsibilities:
    - prepare evidence and claims for final answer generation
    - preserve only supported claim text
    - remove duplicate answer points
    - keep independent source information available
    - never mutate original evidence objects
    - never invent facts or missing values
    """
    MAX_ANSWER_POINTS = 8
    def synthesize(
        self,
        evidence: Iterable[Any] | None = None,
        claims: Iterable[str] | None = None,
    ) -> AnswerSynthesisResult:
        items = [
            copy(item)
            for item in (evidence or [])
            if item is not None
        ]
        claim_list = [
            str(claim).strip()
            for claim in (claims or [])
            if str(claim).strip()
        ]
        claim_list = self._deduplicate_claims(claim_list)
        answer_points = self._build_answer_points(
            items,
            claim_list,
        )
        domains = {
            self._domain(item)
            for item in items
            if self._domain(item)
        }
        if not items and not claim_list:
            return AnswerSynthesisResult(
                evidence=[],
                claims=[],
                answer_points=[],
                source_count=0,
                reason="No evidence or claims are available for synthesis.",
            )
        return AnswerSynthesisResult(
            evidence=items,
            claims=claim_list,
            answer_points=answer_points,
            source_count=len(domains),
            reason="Evidence and claims passed Task 4 synthesis preparation.",
        )
    def _build_answer_points(
        self,
        evidence: list[Any],
        claims: list[str],
    ) -> list[str]:
        points = []
        for claim in claims:
            normalized = self._normalize(claim)
            if not normalized:
                continue
            if any(
                self._normalize(existing) == normalized
                for existing in points
            ):
                continue
            points.append(claim)
            if len(points) >= self.MAX_ANSWER_POINTS:
                break
        if points:
            return points
        for item in evidence:
            content = str(
                getattr(item, "content", "")
                or getattr(item, "snippet", "")
                or ""
            ).strip()
            if not content:
                continue
            sentences = re.split(
                r"(?<=[.!?।])\s+|\n+",
                content,
            )
            for sentence in sentences:
                sentence = re.sub(
                    r"\s+",
                    " ",
                    sentence,
                ).strip()
                if len(sentence) < 20:
                    continue
                normalized = self._normalize(sentence)
                if not normalized:
                    continue
                if any(
                    self._normalize(existing) == normalized
                    for existing in points
                ):
                    continue
                points.append(sentence)
                if len(points) >= self.MAX_ANSWER_POINTS:
                    return points
        return points
    def _domain(self, item: Any) -> str:
        url = str(
            getattr(item, "source_url", "")
            or getattr(item, "url", "")
            or ""
        ).strip()
        if not url:
            return ""
        try:
            from urllib.parse import urlparse
            hostname = urlparse(url).hostname or ""
        except Exception:
            return ""
        return hostname.lower().removeprefix("www.").strip()
    @staticmethod
    def _deduplicate_claims(
        claims: list[str],
    ) -> list[str]:
        unique = []
        seen = set()
        for claim in claims:
            normalized = Task4AnswerSynthesisLayer._normalize(
                claim
            )
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            unique.append(claim)
        return unique
    @staticmethod
    def _normalize(value: Any) -> str:
        text = str(value or "").lower()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip()
