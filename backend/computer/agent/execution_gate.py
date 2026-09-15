"""
ISMAIL AI - Computer Agent Safety / Execution Gate
Task 12C
This module is the final safety gate before execution.
IMPORTANT:
Actual computer execution is intentionally disabled.
"""
from backend.computer.agent.decision import evaluate_agent_request
def check_execution_gate(query, user_confirmed=False):
    """
    Check whether an action may proceed toward execution.
    Actual execution is NOT performed.
    user_confirmed:
        Explicit confirmation supplied by the caller.
    """
    decision_result = evaluate_agent_request(query)
    decision = decision_result.get("decision", "block")
    execution_allowed = decision_result.get(
        "execution_allowed",
        False
    )
    requires_confirmation = decision_result.get(
        "requires_confirmation",
        False
    )
    gate_status = "blocked"
    gate_reason = ""
    if decision == "block":
        gate_status = "blocked"
        gate_reason = (
            "Action is blocked by the agent safety decision."
        )
    elif decision == "confirm":
        if not user_confirmed:
            gate_status = "confirmation_required"
            gate_reason = (
                "Explicit user confirmation is required."
            )
        else:
            gate_status = "ready"
            gate_reason = (
                "Confirmation received, but execution remains disabled."
            )
    elif decision == "allow":
        gate_status = "ready"
        gate_reason = (
            "Action passed the planning safety gate, "
            "but execution remains disabled."
        )
    else:
        gate_status = "blocked"
        gate_reason = (
            "Unknown agent decision."
        )
    # HARD SAFETY RULE:
    # Task 12C never enables actual computer execution.
    actual_execution_allowed = False
    return {
        "request": decision_result.get("request", ""),
        "decision": decision,
        "gate_status": gate_status,
        "gate_reason": gate_reason,
        "requires_confirmation": requires_confirmation,
        "user_confirmed": bool(user_confirmed),
        "execution_allowed": actual_execution_allowed,
        "plan": decision_result.get("plan"),
        "safety_checks": decision_result.get(
            "safety_checks",
            []
        ),
    }
def get_execution_gate_summary(query, user_confirmed=False):
    """
    Return a human-readable execution-gate report.
    """
    result = check_execution_gate(
        query,
        user_confirmed=user_confirmed
    )
    lines = [
        "Computer Agent Execution Gate",
        "Request: " + result.get("request", ""),
        "Decision: " + result.get("decision", ""),
        "Gate Status: " + result.get("gate_status", ""),
        "Gate Reason: " + result.get("gate_reason", ""),
        "User Confirmed: "
        + str(result.get("user_confirmed", False)),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
    ]
    checks = result.get("safety_checks", [])
    if checks:
        lines.append("Safety Checks:")
        for index, check in enumerate(checks, 1):
            lines.append(
                str(index) + ". " + str(check)
            )
    return "\n".join(lines)
