from __future__ import annotations
from copy import copy
from dataclasses import dataclass
from typing import Any, Iterable
from urllib.parse import urlparse
import re
@dataclass
class EvidenceIntelligenceResult:
    evidence: list[Any]
    claims: list[str]
    duplicate_count: int
    source_count: int
    reason: str
class Task3EvidenceIntelligenceLayer:
    """
    Task 3: Evidence Intelligence Layer.
    Responsibilities:
    - prepare reliable evidence for answer synthesis
    - remove obvious duplicate evidence
    - preserve independent sources
    - extract concise claim candidates
    - never mutate original evidence objects
    """
    MIN_CLAIM_LENGTH = 20
    MAX_CLAIMS_PER_EVIDENCE = 3
    def analyze(
        self,
        evidence: Iterable[Any] | None,
    ) -> EvidenceIntelligenceResult:
        items = [
            copy(item)
            for item in (evidence or [])
            if item is not None
        ]
        if not items:
            return EvidenceIntelligenceResult(
                evidence=[],
                claims=[],
                duplicate_count=0,
                source_count=0,
                reason="No evidence is available for intelligence analysis.",
            )
        unique_items = []
        seen_keys = set()
        duplicate_count = 0
        for item in items:
            key = self._dedup_key(item)
            if key and key in seen_keys:
                duplicate_count += 1
                continue
            if key:
                seen_keys.add(key)
            unique_items.append(item)
        claims = []
        for item in unique_items:
            claims.extend(
                self._extract_claims(item)
            )
        claims = self._deduplicate_claims(claims)
        domains = {
            self._domain(item)
            for item in unique_items
            if self._domain(item)
        }
        return EvidenceIntelligenceResult(
            evidence=unique_items,
            claims=claims,
            duplicate_count=duplicate_count,
            source_count=len(domains),
            reason=(
                "Evidence passed Task 3 intelligence analysis."
            ),
        )
    def _domain(self, item: Any) -> str:
        url = str(
            getattr(item, "source_url", "")
            or getattr(item, "url", "")
            or ""
        ).strip()
        if not url:
            return ""
        try:
            hostname = urlparse(url).hostname or ""
        except Exception:
            return ""
        return hostname.lower().removeprefix("www.").strip()
    def _dedup_key(self, item: Any) -> str:
        title = self._normalize(
            getattr(item, "title", "")
        )
        url = str(
            getattr(item, "url", "")
            or getattr(item, "source_url", "")
            or ""
        ).strip()
        if url:
            return f"url:{url.lower()}"
        if title:
            return f"title:{title}"
        content = self._normalize(
            getattr(item, "content", "")
            or getattr(item, "snippet", "")
        )
        if content:
            return f"content:{content[:300]}"
        return ""
    def _extract_claims(self, item: Any) -> list[str]:
        content = str(
            getattr(item, "content", "")
            or getattr(item, "snippet", "")
            or ""
        ).strip()
        if not content:
            return []
        sentences = re.split(
            r"(?<=[.!?।])\s+|\n+",
            content,
        )
        claims = []
        for sentence in sentences:
            sentence = re.sub(
                r"\s+",
                " ",
                sentence,
            ).strip()
            if len(sentence) < self.MIN_CLAIM_LENGTH:
                continue
            claims.append(sentence)
            if len(claims) >= self.MAX_CLAIMS_PER_EVIDENCE:
                break
        return claims
    def _deduplicate_claims(
        self,
        claims: list[str],
    ) -> list[str]:
        unique = []
        seen = set()
        for claim in claims:
            normalized = self._normalize(claim)
            if not normalized:
                continue
            if normalized in seen:
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
