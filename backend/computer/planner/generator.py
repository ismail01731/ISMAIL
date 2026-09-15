from backend.computer.planner.knowledge import search_computer_action_plan
def generate_action_plan(query):
    """
    Convert a user computer-action request into a structured
    action plan.
    This module only creates a plan.
    It does NOT execute any computer action.
    """
    if not query:
        return None
    text = str(query).strip()
    if not text:
        return None
    results = search_computer_action_plan(text)
    if not results:
        return None
    best_plan = results[0]
    risk = best_plan.get("risk", "unknown")
    return {
        "request": text,
        "intent": best_plan.get("intent", ""),
        "plan_name": best_plan.get("name", ""),
        "actions": list(best_plan.get("actions", [])),
        "risk": risk,
        "requires_confirmation": risk in {
            "high",
            "critical"
        },
        "execution_allowed": False
    }
def get_action_plan_summary(query):
    """
    Return a human-readable summary of the generated plan.
    """
    plan = generate_action_plan(query)
    if plan is None:
        return None
    lines = [
        "Action Plan",
        "Intent: " + plan["intent"],
        "Plan: " + plan["plan_name"],
        "Risk: " + plan["risk"],
        "Requires Confirmation: " + str(
            plan["requires_confirmation"]
        ),
        "Execution Allowed: " + str(
            plan["execution_allowed"]
        ),
        "Steps:"
    ]
    for index, action in enumerate(
        plan["actions"],
        1
    ):
        lines.append(
            str(index) + ". " + action
        )
    return "\n".join(lines)
