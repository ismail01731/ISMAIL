from datetime import datetime, timezone
class EvidenceScorer:
    SOURCE_RELIABILITY = {
        "official": 0.95,
        "government": 0.95,
        "scientific": 0.95,
        "academic": 0.90,
        "major_news": 0.80,
        "database": 0.85,
        "api": 0.80,
        "expert": 0.75,
        "social": 0.40,
        "unknown": 0.50,
    }
    def source_score(self, source_type: str) -> float:
        return self.SOURCE_RELIABILITY.get(
            source_type.lower(),
            self.SOURCE_RELIABILITY["unknown"],
        )
    def freshness_score(
        self,
        timestamp: str,
        half_life_hours: float = 168,
    ) -> float:
        try:
            created = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
            now = datetime.now(timezone.utc)
            age_hours = max(
                0,
                (now - created).total_seconds() / 3600,
            )
            # Exponential decay.
            score = 0.5 ** (
                age_hours / half_life_hours
            )
            return round(
                min(max(score, 0.0), 1.0),
                4,
            )
        except Exception:
            return 0.25
    def calculate(
        self,
        source_type: str,
        relevance: float,
        timestamp: str,
    ) -> float:
        reliability = self.source_score(source_type)
        freshness = self.freshness_score(timestamp)
        score = (
            reliability * 0.45
            + relevance * 0.35
            + freshness * 0.20
        )
        return round(
            min(max(score, 0.0), 1.0),
            4,
        )
