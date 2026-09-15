"""
ISMAIL AI - Universal Computer Request Decomposer
Task 14D
This module decomposes a computer request into ordered
sub-requests and validates each step through the existing
Universal Computer Request Classifier.
IMPORTANT:
This module does NOT execute computer actions.
"""
from backend.computer.universal.classifier import (
    classify_computer_request,
)
SEPARATORS = [
    " তারপর ",
    " এরপর ",
    " এবং তারপর ",
    " তারপর ",
    " then ",
    " and then ",
    " after that ",
]
def _split_request(text):
    """
    Split a request into ordered sub-requests.
    Only explicit sequential connectors are used.
    This avoids blindly splitting normal sentences.
    """
    parts = [text]
    changed = True
    while changed:
        changed = False
        new_parts = []
        for part in parts:
            current = [part]
            for separator in SEPARATORS:
                next_parts = []
                for item in current:
                    if separator.lower() in item.lower():
                        pieces = item.lower().split(
                            separator.lower()
                        )
                        if len(pieces) > 1:
                            next_parts.extend(pieces)
                            changed = True
                        else:
                            next_parts.append(item)
                    else:
                        next_parts.append(item)
                current = next_parts
            new_parts.extend(current)
        parts = new_parts
    cleaned = []
    for part in parts:
        value = part.strip(" ,.!?;")
        if value:
            cleaned.append(value)
    return cleaned
def decompose_computer_request(query):
    """
    Decompose a computer request into ordered steps.
    Each step is classified using the existing Task 14B
    classifier. No computer action is executed.
    """
    text = str(query or "").strip()
    if not text:
        return {
            "request": "",
            "decomposed": False,
            "step_count": 0,
            "steps": [],
            "execution_allowed": False,
        }
    parts = _split_request(text)
    steps = []
    for index, part in enumerate(parts, 1):
        classification = classify_computer_request(part)
        steps.append({
            "step": index,
            "request": part,
            "classification": classification,
            "execution_allowed": False,
        })
    return {
        "request": text,
        "decomposed": len(steps) > 1,
        "step_count": len(steps),
        "steps": steps,
        "execution_allowed": False,
    }
def get_decomposition_summary(query):
    """
    Return a compact decomposition summary.
    """
    result = decompose_computer_request(query)
    return {
        "request": result.get("request", ""),
        "decomposed": result.get("decomposed", False),
        "step_count": result.get("step_count", 0),
        "steps": [
            {
                "step": item.get("step"),
                "request": item.get("request"),
                "category": item.get(
                    "classification", {}
                ).get("category", "unknown"),
                "plan_name": item.get(
                    "classification", {}
                ).get("plan_name"),
            }
            for item in result.get("steps", [])
        ],
        "execution_allowed": False,
    }
