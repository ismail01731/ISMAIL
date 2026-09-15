"""
ISMAIL AI - Computer Safety Guard
Task 13C
Final safety guard for computer-agent requests.
IMPORTANT:
This module does NOT execute computer actions.
It only validates and blocks unsafe requests.
"""
from backend.computer.safety.decision import evaluate_permission
DANGEROUS_PATTERNS = [
    "format disk",
    "format drive",
    "delete system32",
    "delete windows",
    "remove system32",
    "remove windows",
    "disable firewall",
    "turn off firewall",
    "disable antivirus",
    "turn off antivirus",
    "disable security",
    "bypass security",
    "bypass permission",
    "bypass administrator",
    "steal password",
    "steal passwords",
    "dump passwords",
    "delete boot",
    "destroy boot",
]
def detect_dangerous_request(query):
    """
    Detect explicitly dangerous computer requests.
    Returns a list of matched dangerous patterns.
    """
    text = str(query or "").strip().lower()
    if not text:
        return []
    normalized = (
        text
        .replace("-", " ")
        .replace("_", " ")
    )
    matches = []
    for pattern in DANGEROUS_PATTERNS:
        if pattern in normalized:
            matches.append(pattern)
    return matches
def apply_safety_guard(
    query,
    user_confirmed=False,
):
    """
    Apply the final safety guard to a computer request.
    """
    text = str(query or "").strip()
    dangerous_matches = detect_dangerous_request(text)
    if dangerous_matches:
        return {
            "request": text,
            "status": "blocked",
            "decision": "block",
            "permission": "critical",
            "requires_confirmation": True,
            "user_confirmed": bool(user_confirmed),
            "execution_allowed": False,
            "dangerous_matches": dangerous_matches,
            "reason": (
                "The request matches a dangerous computer-operation "
                "pattern and is blocked by the safety guard."
            ),
            "permission_result": None,
        }
    permission_result = evaluate_permission(
        text,
        user_confirmed=user_confirmed
    )
    decision = permission_result.get(
        "decision",
        "block"
    )
    if decision not in {
        "allow",
        "confirm",
        "block",
    }:
        decision = "block"
    execution_allowed = False
    return {
        "request": text,
        "status": "safe_reviewed",
        "decision": decision,
        "permission": permission_result.get(
            "permission",
            "critical"
        ),
        "requires_confirmation": permission_result.get(
            "requires_confirmation",
            True
        ),
        "user_confirmed": bool(user_confirmed),
        "execution_allowed": execution_allowed,
        "dangerous_matches": [],
        "reason": permission_result.get(
            "reason",
            "Safety review completed."
        ),
        "permission_result": permission_result,
    }
def get_safety_guard_summary(
    query,
    user_confirmed=False,
):
    """
    Return a human-readable safety guard report.
    """
    result = apply_safety_guard(
        query,
        user_confirmed=user_confirmed
    )
    lines = [
        "Computer Safety Guard",
        "Request: " + result.get("request", ""),
        "Status: " + result.get("status", ""),
        "Decision: " + result.get("decision", ""),
        "Permission: " + result.get("permission", ""),
        "Requires Confirmation: "
        + str(result.get("requires_confirmation", False)),
        "User Confirmed: "
        + str(result.get("user_confirmed", False)),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
        "Reason: " + result.get("reason", ""),
    ]
    dangerous_matches = result.get(
        "dangerous_matches",
        []
    )
    if dangerous_matches:
        lines.append(
            "Dangerous Patterns: "
            + ", ".join(dangerous_matches)
        )
    return "\n".join(lines)
