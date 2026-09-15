"""
ISMAIL AI - Universal Computer Request Classifier
Task 14B
This layer converts the existing Computer Action Planner
result into a universal computer-request category.
IMPORTANT:
This module does NOT execute any computer action.
"""
from backend.computer.planner.knowledge import (
    search_computer_action_plan,
)
PLAN_CATEGORY_MAP = {
    "create_folder": "file",
    "create_file": "file",
    "read_file": "file",
    "delete_file": "file",
    "copy_file": "file",
    "move_file": "file",
    "rename_file": "file",
    "open_application": "application",
    "close_application": "application",
    "open_website": "website",
    "search_web": "web_search",
    "run_command": "command",
    "check_system": "system",
    "shutdown_computer": "system",
    "restart_computer": "system",
    "check_network": "network",
    "install_software": "software",
    "uninstall_software": "software",
}
VALID_CATEGORIES = {
    "file",
    "application",
    "website",
    "web_search",
    "command",
    "system",
    "network",
    "software",
    "computer_control",
    "unknown",
}
def classify_computer_request(query):
    """
    Classify a computer request using the existing planner.
    Returns a structured result and never executes an action.
    """
    text = str(query or "").strip()
    if not text:
        return {
            "request": "",
            "category": "unknown",
            "plan_name": None,
            "matched": False,
            "execution_allowed": False,
        }
    plans = search_computer_action_plan(text)
    if not plans:
        return {
            "request": text,
            "category": "unknown",
            "plan_name": None,
            "matched": False,
            "execution_allowed": False,
        }
    plan = plans[0]
    plan_name = plan.get("name")
    category = PLAN_CATEGORY_MAP.get(
        plan_name,
        "computer_control"
    )
    if category not in VALID_CATEGORIES:
        category = "unknown"
    return {
        "request": text,
        "category": category,
        "plan_name": plan_name,
        "intent": plan.get("intent"),
        "risk": plan.get("risk"),
        "matched": True,
        "execution_allowed": False,
    }
def get_classification_summary(query):
    """
    Return a compact classification summary.
    """
    result = classify_computer_request(query)
    return {
        "request": result.get("request", ""),
        "category": result.get("category", "unknown"),
        "plan_name": result.get("plan_name"),
        "risk": result.get("risk"),
        "matched": result.get("matched", False),
        "execution_allowed": False,
    }
