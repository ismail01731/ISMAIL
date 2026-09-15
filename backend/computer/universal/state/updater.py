"""
ISMAIL AI - Computer State Updater
Task 14E-D
This module updates logical/planned computer state
after a computer action or planned step.
IMPORTANT:
- This module does NOT execute computer actions.
- This module does NOT inspect the real computer.
- State represents logical/planned context only.
- execution_allowed is ALWAYS False.
"""
from typing import Any, Dict, Optional
from backend.computer.universal.state.model import ComputerState
ACTION_TO_STATE = {
    "open_application": "application",
    "close_application": "application",
    "open_website": "website",
    "search_web": "website",
    "create_folder": "folder",
    "create_file": "file",
    "read_file": "file",
    "delete_file": "file",
    "copy_file": "file",
    "move_file": "file",
    "rename_file": "file",
}
def _normalize_text(value: Any) -> str:
    return str(value or "").strip()
def _add_unique(items, value: Optional[str]) -> None:
    value = _normalize_text(value)
    if value and value not in items:
        items.append(value)
def update_state_from_action(
    state: ComputerState,
    action: str,
    value: Optional[str] = None,
    request: Optional[str] = None,
    step: Optional[int] = None,
) -> ComputerState:
    """
    Update logical computer state from an action.
    No real computer action is performed.
    """
    if state is None:
        state = ComputerState()
    action_name = _normalize_text(action).lower()
    target = _normalize_text(value)
    request_text = _normalize_text(request)
    if action_name == "open_application":
        if target:
            state.active_application = target
    elif action_name == "close_application":
        if target:
            if state.active_application == target:
                state.active_application = None
        else:
            state.active_application = None
    elif action_name == "open_website":
        if target:
            state.active_website = target
    elif action_name == "search_web":
        if target:
            state.active_website = target
    elif action_name == "create_folder":
        if target:
            _add_unique(state.known_folders, target)
            state.current_folder = target
    elif action_name == "create_file":
        if target:
            _add_unique(state.known_files, target)
            state.active_file = target
    elif action_name == "read_file":
        if target:
            _add_unique(state.known_files, target)
            state.active_file = target
    elif action_name == "delete_file":
        if target:
            state.known_files = [
                item
                for item in state.known_files
                if item != target
            ]
            if state.active_file == target:
                state.active_file = None
    elif action_name == "copy_file":
        if target:
            _add_unique(state.known_files, target)
            state.active_file = target
    elif action_name == "move_file":
        if target:
            _add_unique(state.known_files, target)
            state.active_file = target
    elif action_name == "rename_file":
        if target:
            old_value = state.active_file
            if old_value and old_value != target:
                state.known_files = [
                    target if item == old_value else item
                    for item in state.known_files
                ]
            _add_unique(state.known_files, target)
            state.active_file = target
    state.last_action = action_name or None
    state.last_request = request_text or None
    state.last_step = step
    state.execution_allowed = False
    return state
def update_state_from_result(
    state: ComputerState,
    result: Optional[Dict[str, Any]],
) -> ComputerState:
    """
    Update state from a structured planner/agent result.
    This function only reads logical result data.
    It never executes anything.
    """
    if state is None:
        state = ComputerState()
    result = result or {}
    action = result.get("action")
    if not action:
        plan = result.get("plan") or {}
        action = plan.get("name")
    if not action:
        classification = result.get("classification") or {}
        action = classification.get("plan_name")
    value = (
        result.get("value")
        or result.get("target")
        or result.get("name")
    )
    request = result.get("request")
    step = result.get("step")
    return update_state_from_action(
        state=state,
        action=action,
        value=value,
        request=request,
        step=step,
    )
def set_reference(
    state: ComputerState,
    reference: str,
    value: Any,
) -> ComputerState:
    """
    Store a logical reference for future steps.
    """
    if state is None:
        state = ComputerState()
    key = _normalize_text(reference).lower()
    target = _normalize_text(value)
    if key and target:
        state.references[key] = target
    state.execution_allowed = False
    return state
def get_state_update_summary(state: ComputerState) -> Dict[str, Any]:
    """
    Return a compact state summary.
    """
    if state is None:
        state = ComputerState()
    return {
        "active_application": state.active_application,
        "active_website": state.active_website,
        "current_folder": state.current_folder,
        "active_file": state.active_file,
        "known_files": list(state.known_files),
        "known_folders": list(state.known_folders),
        "last_action": state.last_action,
        "last_request": state.last_request,
        "last_step": state.last_step,
        "references": dict(state.references),
        "execution_allowed": False,
    }
