def normalize_probabilities(scenarios: list[dict]) -> list[dict]:
    """
    Ensures all scenario probabilities add up to 1.0.
    """
    if not scenarios:
        return []
    total = sum(
        max(0.0, float(item.get("probability", 0.0)))
        for item in scenarios
    )
    if total <= 0:
        equal = 1.0 / len(scenarios)
        for item in scenarios:
            item["probability"] = round(equal, 4)
        return scenarios
    for item in scenarios:
        value = max(0.0, float(item.get("probability", 0.0)))
        item["probability"] = round(value / total, 4)
    # Correct rounding difference.
    difference = round(
        1.0 - sum(item["probability"] for item in scenarios),
        4,
    )
    scenarios[0]["probability"] = round(
        scenarios[0]["probability"] + difference,
        4,
    )
    return scenarios
