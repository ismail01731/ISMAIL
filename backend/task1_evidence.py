"""
ISMAIL AI - Task 1 Evidence Layer
This module provides a separate, non-destructive processing layer
for evidence collected by the existing web_research system.
Important:
- Does NOT perform web searches.
- Does NOT duplicate WebEvidence.
- Does NOT replace the existing verification algorithm.
- Does NOT modify the original evidence objects.
"""
from __future__ import annotations
from typing import Any, Iterable, List
import copy
from urllib.parse import urlparse
class Task1EvidenceLayer:
    """Prepare existing evidence for the Task 1 pipeline."""
    def prepare(
        self,
        evidence: Iterable[Any],
        max_items: int = 15,
    ) -> List[Any]:
        """
        Return a clean, bounded evidence list.
        The original evidence objects are preserved unchanged.
        """
        if evidence is None:
            return []
        try:
            limit = int(max_items)
        except (TypeError, ValueError):
            limit = 15
        limit = max(1, min(limit, 50))
        prepared: List[Any] = []
        seen_urls: set[str] = set()
        for item in evidence:
            if item is None:
                continue
            url = str(getattr(item, "url", "") or "").strip()
            if url:
                normalized_url = url.lower().rstrip("/")
                if normalized_url in seen_urls:
                    continue
                seen_urls.add(normalized_url)
            prepared.append(item)
            if len(prepared) >= limit:
                break
        return prepared
    def count_usable(
        self,
        evidence: Iterable[Any],
    ) -> int:
        """Count non-empty evidence objects."""
        if evidence is None:
            return 0
        return sum(1 for item in evidence if item is not None)
    def improve_source_quality(
        self,
        evidence: Iterable[Any],
    ) -> List[Any]:
        """
        Apply Task 1 source-quality overrides without changing the
        original evidence objects.
        This does not verify the actual claim. It only improves the
        source classification used by the existing verification layer.
        """
        if evidence is None:
            return []
        # Trusted/established publishers and organizations.
        # Values are intentionally conservative.
        trusted_domains = {
            "dw.com": (0.85, "high"),
            "reuters.com": (0.90, "high"),
            "apnews.com": (0.90, "high"),
            "bbc.com": (0.90, "high"),
            "bbc.co.uk": (0.90, "high"),
            "aljazeera.com": (0.85, "high"),
            "nytimes.com": (0.85, "high"),
            "theguardian.com": (0.85, "high"),
            "jagonews24.com": (0.75, "medium"),
            "bangladeshtoday.net": (0.75, "medium"),
            "thebangladeshtoday.com": (0.75, "medium"),
        }
        improved: List[Any] = []
        for item in evidence:
            if item is None:
                continue
            url = str(getattr(item, "source_url", "") or "").strip()
            if not url:
                url = str(getattr(item, "url", "") or "").strip()
            hostname = ""
            if url:
                try:
                    hostname = urlparse(url).hostname or ""
                except Exception:
                    hostname = ""
            hostname = hostname.lower().strip().removeprefix("www.")
            match = None
            for domain, quality in trusted_domains.items():
                if hostname == domain or hostname.endswith("." + domain):
                    match = quality
                    break
            if match is None:
                improved.append(item)
                continue
            # Work on a shallow copy so the original evidence object
            # remains untouched.
            updated = copy.copy(item)
            score, level = match
            current_score = float(
                getattr(updated, "reliability_score", 0.0) or 0.0
            )
            # Never reduce an already stronger source score.
            if score > current_score:
                updated.reliability_score = score
                updated.reliability_level = level
            improved.append(updated)
        return improved
    def enforce_claim_verification(
        self,
        question: str,
        evidence: Iterable[Any],
    ) -> List[Any]:
        """
        Require independent-source agreement for live/current claims.
        Source reputation alone is never treated as proof of a live claim.
        Independent publisher domains must provide meaningful textual
        agreement before an item can be marked corroborated.
        """
        if evidence is None:
            return []
        items = [item for item in evidence if item is not None]
        # Detect live/current intent directly from the original question.
        # Do not use _meaningful_words() here because that method removes
        # several of these words as comparison stopwords.
        live_markers = (
            "latest", "breaking", "today", "current", "recent",
            "news", "happening", "status", "update",
            "???????", "?????", "???????", "??????????",
            "???", "???????", "????",
        )
        question_text = str(question or "").lower()
        is_live = any(marker in question_text for marker in live_markers)
        if not is_live:
            return items
        updated_items: List[Any] = []
        for item in items:
            # Keep the original evidence object untouched.
            current = copy.copy(item)
            item_text = " ".join(
                str(getattr(item, field, "") or "")
                for field in ("title", "snippet", "content")
            )
            item_words = self._meaningful_words(item_text)
            item_domain = self._domain_for(item)
            corroborated = False
            if item_domain and item_words:
                for other in items:
                    if other is item:
                        continue
                    other_domain = self._domain_for(other)
                    if not other_domain or other_domain == item_domain:
                        continue
                    other_text = " ".join(
                        str(getattr(other, field, "") or "")
                        for field in ("title", "snippet", "content")
                    )
                    other_words = self._meaningful_words(other_text)
                    if not other_words:
                        continue
                    shared = item_words & other_words
                    if len(shared) < 3:
                        continue
                    smaller = min(len(item_words), len(other_words))
                    overlap = len(shared) / max(smaller, 1)
                    if overlap >= 0.30:
                        corroborated = True
                        break
            if corroborated:
                current.verification_status = "corroborated"
            else:
                # Live claims cannot become verified/high-confidence solely
                # because the publisher itself is considered reputable.
                current.verification_status = "unverified"
            updated_items.append(current)
        return updated_items
    @staticmethod
    def _meaningful_words(text: str) -> set[str]:
        """Return normalized words suitable for conservative comparison."""
        import re
        if not text:
            return set()
        words = re.findall(r"[A-Za-z0-9ঀ-৿]{4,}", text.lower())
        stopwords = {
            "what", "when", "where", "which", "that", "this",
            "latest", "news", "today", "current", "recent",
            "bangladesh", "about", "with", "from",
            "???", "???", "???", "????", "?????",
        }
        return {
            word
            for word in words
            if word not in stopwords
        }
    @staticmethod
    def _domain_for(item: Any) -> str:
        """Extract the publisher domain from an evidence object."""
        from urllib.parse import urlparse
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
        return hostname.lower().strip().removeprefix("www.")
