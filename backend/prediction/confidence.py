def calculate_confidence(
    evidence: list[dict],
    scenarios: list[dict],
) -> float:
    """
    Calculates a baseline confidence score.
    More reliable evidence will be added in later tasks.
    """
    if not evidence:
        return 0.30
    evidence_count = min(len(evidence), 10)
    evidence_score = evidence_count / 10.0
    scenario_quality = 0.20
    score = (
        evidence_score * 0.80
        + scenario_quality * 0.20
    )
    return round(min(max(score, 0.0), 1.0), 4)
