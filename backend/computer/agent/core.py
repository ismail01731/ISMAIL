"""
ISMAIL AI - Computer Agent Core
Task 12A
This module converts an action plan into a safe agent decision.
IMPORTANT:
This module does NOT execute computer actions.
"""
from backend.computer.planner.generator import generate_action_plan
ALLOWED_DECISIONS = {
    "allow",
    "confirm",
    "block",
}
def create_agent_decision(query):
    """
    Create a structured computer-agent decision.
    No computer action is executed here.
    """
    text = str(query or "").strip()
    if not text:
        return {
            "request": "",
            "status": "block",
            "decision": "block",
            "reason": "Empty request.",
            "execution_allowed": False,
            "requires_confirmation": False,
            "plan": None,
        }
    plan = generate_action_plan(text)
    if not plan:
        return {
            "request": text,
            "status": "block",
            "decision": "block",
            "reason": "No supported computer action plan was found.",
            "execution_allowed": False,
            "requires_confirmation": False,
            "plan": None,
        }
    risk = plan.get("risk", "high")
    requires_confirmation = bool(
        plan.get("requires_confirmation", False)
    )
    if risk == "critical":
        decision = "confirm"
        reason = "Critical computer action requires explicit confirmation."
    elif requires_confirmation:
        decision = "confirm"
        reason = "This computer action requires explicit confirmation."
    elif risk in {"low", "medium"}:
        decision = "allow"
        reason = "The action is currently classified as safe for agent planning."
    else:
        decision = "block"
        reason = "Unknown or unsupported risk level."
    execution_allowed = False
    return {
        "request": text,
        "status": "ready",
        "decision": decision,
        "reason": reason,
        "execution_allowed": execution_allowed,
        "requires_confirmation": requires_confirmation,
        "plan": plan,
    }
def get_agent_decision_summary(query):
    """
    Return a human-readable computer-agent decision summary.
    """
    result = create_agent_decision(query)
    lines = [
        "Computer Agent",
        "Request: " + result.get("request", ""),
        "Decision: " + result.get("decision", "block"),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
        "Requires Confirmation: "
        + str(result.get("requires_confirmation", False)),
        "Reason: " + result.get("reason", ""),
    ]
    plan = result.get("plan")
    if plan:
        lines.append(
            "Plan: " + plan.get("plan_name", "")
        )
        actions = plan.get("actions", [])
        if actions:
            lines.append("Steps:")
            for index, action in enumerate(actions, 1):
                lines.append(
                    str(index) + ". " + str(action)
                )
    return "\n".join(lines)
