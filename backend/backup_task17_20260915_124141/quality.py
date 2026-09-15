class DataQualityEngine:
    def score(
        self,
        values: list[float],
    ) -> dict:
        if not values:
            return {
                "score": 0.0,
                "level": "none",
                "count": 0,
            }
        count = len(values)
        missing = sum(
            1
            for value in values
            if value is None
        )
        valid = count - missing
        completeness = (
            valid / count
        )
        if valid >= 100:
            level = "excellent"
        elif valid >= 50:
            level = "good"
        elif valid >= 10:
            level = "fair"
        else:
            level = "low"
        return {
            "score": round(
                completeness,
                4,
            ),
            "level": level,
            "count": count,
            "valid": valid,
            "missing": missing,
        }
