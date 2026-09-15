"""
ISMAIL AI - Computer Agent Dry-Run Executor
Task 12D
This module simulates computer actions.
IMPORTANT:
NO real computer action is executed.
"""
from backend.computer.agent.execution_gate import check_execution_gate
def dry_run_action(query, user_confirmed=False):
    """
    Simulate the action plan without executing it.
    """
    gate = check_execution_gate(
        query,
        user_confirmed=user_confirmed
    )
    gate_status = gate.get("gate_status", "blocked")
    plan = gate.get("plan")
    if gate_status == "blocked":
        return {
            "request": gate.get("request", ""),
            "status": "blocked",
            "mode": "dry_run",
            "simulated": False,
            "execution_allowed": False,
            "message": gate.get("gate_reason", ""),
            "plan": plan,
        }
    if gate_status == "confirmation_required":
        return {
            "request": gate.get("request", ""),
            "status": "confirmation_required",
            "mode": "dry_run",
            "simulated": False,
            "execution_allowed": False,
            "message": gate.get("gate_reason", ""),
            "plan": plan,
        }
    if gate_status == "ready":
        actions = []
        if plan:
            actions = list(
                plan.get("actions", [])
            )
        return {
            "request": gate.get("request", ""),
            "status": "simulated",
            "mode": "dry_run",
            "simulated": True,
            "execution_allowed": False,
            "message": (
                "Action simulated successfully. "
                "No real computer action was executed."
            ),
            "plan": plan,
            "simulated_actions": actions,
        }
    return {
        "request": gate.get("request", ""),
        "status": "blocked",
        "mode": "dry_run",
        "simulated": False,
        "execution_allowed": False,
        "message": "Unknown execution-gate status.",
        "plan": plan,
    }
def get_dry_run_summary(query, user_confirmed=False):
    """
    Return a human-readable dry-run report.
    """
    result = dry_run_action(
        query,
        user_confirmed=user_confirmed
    )
    lines = [
        "Computer Agent Dry Run",
        "Request: " + result.get("request", ""),
        "Mode: " + result.get("mode", ""),
        "Status: " + result.get("status", ""),
        "Simulated: " + str(result.get("simulated", False)),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
        "Message: " + result.get("message", ""),
    ]
    simulated_actions = result.get(
        "simulated_actions",
        []
    )
    if simulated_actions:
        lines.append("Simulated Steps:")
        for index, action in enumerate(
            simulated_actions,
            1
        ):
            lines.append(
                str(index) + ". " + str(action)
            )
    return "\n".join(lines)
