"""
ISMAIL AI - Computer Agent Decision Engine
Task 12B
This module performs decision analysis only.
It does NOT execute computer actions.
"""
from backend.computer.agent.core import create_agent_decision
VALID_DECISIONS = {
    "allow",
    "confirm",
    "block",
}
def evaluate_agent_request(query):
    """
    Evaluate a computer request and return a structured
    safety decision.
    No computer action is executed.
    """
    result = create_agent_decision(query)
    decision = result.get("decision", "block")
    if decision not in VALID_DECISIONS:
        decision = "block"
    plan = result.get("plan")
    if plan is None:
        return {
            **result,
            "decision": "block",
            "status": "blocked",
            "execution_allowed": False,
            "safety_checks": [
                "No valid action plan found."
            ],
        }
    safety_checks = []
    risk = plan.get("risk", "high")
    safety_checks.append(
        "Action plan detected."
    )
    safety_checks.append(
        "Risk level classified as: " + str(risk)
    )
    if decision == "allow":
        safety_checks.append(
            "Action is allowed for planning, but execution remains disabled."
        )
    elif decision == "confirm":
        safety_checks.append(
            "Explicit user confirmation is required before execution."
        )
    else:
        safety_checks.append(
            "Action is blocked by the safety layer."
        )
    safety_checks.append(
        "Computer execution is disabled in Task 12B."
    )
    return {
        **result,
        "decision": decision,
        "status": "evaluated",
        "execution_allowed": False,
        "safety_checks": safety_checks,
    }
def get_decision_summary(query):
    """
    Return a human-readable decision report.
    """
    result = evaluate_agent_request(query)
    lines = [
        "Computer Agent Decision",
        "Request: " + result.get("request", ""),
        "Decision: " + result.get("decision", "block"),
        "Status: " + result.get("status", ""),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
        "Requires Confirmation: "
        + str(result.get("requires_confirmation", False)),
        "Reason: " + result.get("reason", ""),
    ]
    safety_checks = result.get("safety_checks", [])
    if safety_checks:
        lines.append("Safety Checks:")
        for index, check in enumerate(safety_checks, 1):
            lines.append(
                str(index) + ". " + str(check)
            )
    return "\n".join(lines)
