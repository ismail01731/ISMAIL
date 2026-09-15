def build_scenarios(
    question: str,
    evidence: list[dict],
    horizon_days: int,
    context: dict,
) -> list[dict]:
    """
    Task 1 baseline scenario generator.
    Later this function will consume:
    - historical data
    - live data
    - external APIs
    - existing AI reasoning
    - domain-specific prediction models
    """
    return [
        {
            "name": "Base case",
            "probability": 0.55,
            "description": (
                "Current conditions continue without a major change."
            ),
        },
        {
            "name": "Positive scenario",
            "probability": 0.25,
            "description": (
                "Conditions improve and the main trend becomes stronger."
            ),
        },
        {
            "name": "Negative scenario",
            "probability": 0.20,
            "description": (
                "An unexpected negative event changes the current trend."
            ),
        },
    ]
