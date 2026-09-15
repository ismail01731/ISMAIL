"""
ISMAIL AI - Universal Computer Intelligence
Task 14C + Task 14D Integration
"""
from backend.computer.universal.state.manager import get_computer_state_manager
from backend.computer.universal.state.resolver import resolve_reference
from backend.computer.universal.state.updater import (
    update_state_from_action,
    set_reference,
)
from backend.computer.universal.classifier import (
    classify_computer_request,
)
from backend.computer.universal.decomposer import (
    decompose_computer_request,
)
from backend.computer.context.knowledge import (
    search_computer_context,
)
from backend.computer.planner.generator import (
    generate_action_plan,
)
from backend.computer.agent.decision import (
    evaluate_agent_request,
)
from backend.computer.safety.decision import (
    evaluate_permission,
)
from backend.computer.safety.guard import (
    apply_safety_guard,
)
from backend.computer.agent.execution_gate import (
    check_execution_gate,
)
from backend.computer.agent.dry_run import (
    dry_run_action,
)
from backend.computer.agent.verification import (
    verify_agent_result,
)
def _resolve_state_references(text, state):
    """
    Resolve logical references found in a request.
    This only uses planned/logical state.
    It never inspects the real computer.
    """
    normalized = str(text or "").strip().lower()
    candidates = [
        "this application",
        "that application",
        "the application",
        "this app",
        "that app",
        "the app",
        "this website",
        "that website",
        "the website",
        "this folder",
        "that folder",
        "the folder",
        "this file",
        "that file",
        "the file",
        "it",
        "\u098f\u099f\u09be",
        "\u0993\u099f\u09be",
        "\u09b8\u09c7\u099f\u09be",
        "\u098f\u0987 \u0985\u09cd\u09af\u09be\u09aa",
        "\u0993\u0987 \u0985\u09cd\u09af\u09be\u09aa",
        "\u098f\u0987 \u0985\u09cd\u09af\u09be\u09aa\u099f\u09bf",
        "\u0993\u0987 \u0985\u09cd\u09af\u09be\u09aa\u099f\u09bf",
        "\u098f\u0987 \u09ab\u09be\u0987\u09b2",
        "\u0993\u0987 \u09ab\u09be\u0987\u09b2",
        "\u098f\u0987 \u09ab\u09be\u0987\u09b2\u099f\u09bf",
        "\u0993\u0987 \u09ab\u09be\u0987\u09b2\u099f\u09bf",
        "\u098f\u0987 \u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0",
        "\u0993\u0987 \u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0",
        "\u098f\u0987 \u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0\u099f\u09bf",
        "\u0993\u0987 \u09ab\u09cb\u09b2\u09cd\u09a1\u09be\u09b0\u099f\u09bf",
        "\u098f\u0987 \u0993\u09df\u09c7\u09ac\u09b8\u09be\u0987\u099f",
        "\u0993\u0987 \u0993\u09df\u09c7\u09ac\u09b8\u09be\u0987\u099f",
    ]
    references = []
    for candidate in candidates:
        if candidate in normalized and candidate not in references:
            references.append(candidate)
    return [
        resolve_reference(reference, state)
        for reference in references
    ]
def _get_action_name(plan, classification):
    """
    Get the logical action name from the existing pipeline.
    """
    if isinstance(plan, dict):
        name = plan.get("name")
        if name:
            return str(name).strip().lower()
    if isinstance(classification, dict):
        name = classification.get("plan_name")
        if name:
            return str(name).strip().lower()
    return ""
def _extract_logical_target(text, action):
    """
    Extract a simple logical target from a request.
    This is only for planned/context state.
    It does not inspect or control the real computer.
    """
    value = str(text or "").strip()
    action_name = str(action or "").strip().lower()
    prefixes = {
        "open_application": [
            "open ",
            "launch ",
            "start ",
            "\u0996\u09c1\u09b2\u09c7 ",
            "\u0996\u09cb\u09b2\u09be ",
        ],
        "close_application": [
            "close ",
            "exit ",
            "stop ",
        ],
        "open_website": [
            "open ",
            "visit ",
            "go to ",
            "\u0996\u09c1\u09b2\u09c7 ",
            "\u0996\u09cb\u09b2\u09be ",
        ],
        "search_web": [
            "search ",
            "search for ",
        ],
        "create_folder": [
            "create folder ",
            "create a folder ",
            "make folder ",
            "make a folder ",
        ],
        "create_file": [
            "create file ",
            "create a file ",
            "make file ",
            "make a file ",
        ],
    }
    bengali_suffixes = {
        "open_application": [
            " \u0996\u09c1\u09b2\u09c7 \u09a6\u09be\u0993",
            " \u0996\u09c1\u09b2\u09c7 \u09a6\u09be\u0993\u0964",
            " \u0996\u09cb\u09b2\u09cb",
            " \u0996\u09cb\u09b2\u09be \u0995\u09b0\u09cb",
        ],
        "open_website": [
            " \u0996\u09c1\u09b2\u09c7 \u09a6\u09be\u0993",
            " \u0996\u09c1\u09b2\u09c7 \u09a6\u09be\u0993\u0964",
            " \u0996\u09cb\u09b2\u09be \u0995\u09b0\u09cb",
        ],
    }
    lower_value = value.lower()
    for prefix in prefixes.get(action_name, []):
        if lower_value.startswith(prefix):
            target = value[len(prefix):].strip()
            if target:
                return target
    for suffix in bengali_suffixes.get(action_name, []):
        if lower_value.endswith(suffix):
            target = value[:-len(suffix)].strip()
            if target:
                return target
    return None
def _get_logical_state_value(text, action, resolved_references):
    """
    Get a value suitable for logical state tracking.
    Reference resolution is preferred when a request explicitly
    refers to an existing logical object.
    This function never performs a real computer operation.
    """
    action = str(action or "").strip().lower()
    reference_actions = {
        "rename_file",
        "delete_file",
        "read_file",
        "copy_file",
        "move_file",
        "close_application",
    }
    if action in reference_actions:
        for item in resolved_references:
            if item.get("resolved") and item.get("value"):
                return item.get("value")
    return None
def _process_single_computer_request(
    text,
    user_confirmed=False,
    step_number=None,
    session_key=None,
):
    """
    Process exactly one computer request through
    the existing Task 14C pipeline.
    This function does NOT execute real computer actions.
    """
    state_manager = get_computer_state_manager()
    state = state_manager.get_state(session_key)
    resolved_references = _resolve_state_references(
        text,
        state,
    )
    classification = classify_computer_request(text)
    context = search_computer_context(text)
    plan = generate_action_plan(text)
    agent_decision = evaluate_agent_request(text)
    permission = evaluate_permission(
        text,
        user_confirmed=user_confirmed,
    )
    safety = apply_safety_guard(
        text,
        user_confirmed=user_confirmed,
    )
    if safety.get("decision") == "block":
        return {
            "request": text,
            "status": "blocked",
            "stage": "safety",
            "classification": classification,
            "context": context,
            "plan": plan,
            "agent_decision": agent_decision,
            "permission": permission,
            "safety": safety,
            "execution_gate": None,
            "dry_run": None,
            "verification": None,
            "state": state.to_dict(),
            "resolved_references": resolved_references,
            "execution_allowed": False,
            "reason": safety.get(
                "reason",
                "Request blocked by safety guard.",
            ),
        }
    gate = check_execution_gate(
        text,
        user_confirmed=user_confirmed,
    )
    dry_run = dry_run_action(
        text,
        user_confirmed=user_confirmed,
    )
    verification = verify_agent_result(
        text,
        user_confirmed=user_confirmed,
    )
    action_name = _get_action_name(
        plan,
        classification,
    )
    logical_value = _get_logical_state_value(
        text,
        action_name,
        resolved_references,
    )
    if logical_value is None:
        logical_value = _extract_logical_target(
            text,
            action_name,
        )
    if logical_value:
        set_reference(
            state,
            "it",
            logical_value,
        )
    if action_name:
        update_state_from_action(
            state=state,
            action=action_name,
            value=logical_value,
            request=text,
            step=step_number,
        )
        state_manager.update_state(
            session_key=session_key,
            active_application=state.active_application,
            active_website=state.active_website,
            current_folder=state.current_folder,
            active_file=state.active_file,
            known_files=list(state.known_files),
            known_folders=list(state.known_folders),
            last_action=state.last_action,
            last_request=state.last_request,
            last_step=state.last_step,
            references=dict(state.references),
        )
    return {
        "request": text,
        "status": "reviewed",
        "stage": "complete",
        "classification": classification,
        "context": context,
        "plan": plan,
        "agent_decision": agent_decision,
        "permission": permission,
        "safety": safety,
        "execution_gate": gate,
        "dry_run": dry_run,
        "verification": verification,
        "state": state.to_dict(),
        "resolved_references": resolved_references,
        "execution_allowed": False,
        "reason": (
            "Computer request was processed through the "
            "Universal Computer Intelligence pipeline."
        ),
    }
def process_computer_request(
    query,
    user_confirmed=False,
    session_key=None,
):
    """
    Process a computer request through Task 14D
    decomposition and the existing Task 14C pipeline.
    IMPORTANT:
    This function does NOT execute real computer actions.
    """
    text = str(query or "").strip()
    if not text:
        return {
            "request": "",
            "status": "blocked",
            "stage": "input",
            "classification": {
                "request": "",
                "category": "unknown",
                "plan_name": None,
                "matched": False,
                "execution_allowed": False,
            },
            "decomposition": {
                "request": "",
                "decomposed": False,
                "step_count": 0,
                "steps": [],
                "execution_allowed": False,
            },
            "execution_allowed": False,
            "reason": "Computer request cannot be empty.",
        }
    decomposition = decompose_computer_request(text)
    steps = decomposition.get("steps", [])
    if not steps:
        return {
            "request": text,
            "status": "blocked",
            "stage": "decomposition",
            "classification": {
                "request": text,
                "category": "unknown",
                "plan_name": None,
                "matched": False,
                "execution_allowed": False,
            },
            "decomposition": decomposition,
            "steps": [],
            "execution_allowed": False,
            "reason": "No valid computer request steps found.",
        }
    # Single-step request:
    # preserve the existing Task 14C behavior.
    if len(steps) == 1:
        single_result = _process_single_computer_request(
            text,
            user_confirmed=user_confirmed,
              session_key=session_key,
            step_number=steps[0].get("step"),
        )
        single_result["decomposition"] = decomposition
        single_result["steps"] = [
            single_result.copy()
        ]
        single_result["execution_allowed"] = False
        return single_result
    # Multi-step request:
    # process every decomposed step through the
    # existing Task 14C pipeline.
    state_manager = get_computer_state_manager()
    state = state_manager.get_state(session_key)
    processed_steps = []
    overall_status = "reviewed"
    overall_stage = "complete"
    overall_reason = (
        "All decomposed computer request steps were "
        "processed through the Universal Computer "
        "Intelligence pipeline."
    )
    for step in steps:
        step_request = step.get("request", "").strip()
        step_result = _process_single_computer_request(
            step_request,
            user_confirmed=user_confirmed,
              session_key=session_key,
            step_number=step.get("step"),
        )
        processed_steps.append({
            "step": step.get("step"),
            "request": step_request,
            "classification": step_result.get(
                "classification",
                {},
            ),
            "context": step_result.get(
                "context",
                [],
            ),
            "plan": step_result.get(
                "plan",
            ),
            "agent_decision": step_result.get(
                "agent_decision",
            ),
            "permission": step_result.get(
                "permission",
            ),
            "safety": step_result.get(
                "safety",
            ),
            "execution_gate": step_result.get(
                "execution_gate",
            ),
            "dry_run": step_result.get(
                "dry_run",
            ),
            "verification": step_result.get(
                "verification",
            ),
            "state": step_result.get(
                "state",
                state.to_dict(),
            ),
            "resolved_references": step_result.get(
                "resolved_references",
                [],
            ),
            "status": step_result.get(
                "status",
                "blocked",
            ),
            "stage": step_result.get(
                "stage",
                "",
            ),
            "execution_allowed": False,
            "reason": step_result.get(
                "reason",
                "",
            ),
        })
        if step_result.get("status") == "blocked":
            overall_status = "blocked"
            overall_stage = "step"
            overall_reason = (
                "One or more decomposed computer "
                "request steps were blocked."
            )
    return {
        "request": text,
        "status": overall_status,
        "stage": overall_stage,
        "classification": {
            "request": text,
            "category": "computer_control",
            "plan_name": None,
            "matched": True,
            "execution_allowed": False,
        },
        "decomposition": decomposition,
        "steps": processed_steps,
        "state": state.to_dict(),
        "execution_allowed": False,
        "reason": overall_reason,
    }
def get_universal_computer_summary(
    query,
    user_confirmed=False,
):
    result = process_computer_request(
        query,
        user_confirmed=user_confirmed,
    )
    return {
        "request": result.get(
            "request",
            "",
        ),
        "status": result.get(
            "status",
            "",
        ),
        "stage": result.get(
            "stage",
            "",
        ),
        "decision": result.get(
            "safety",
            {},
        ).get(
            "decision",
            result.get(
                "steps",
                [{}],
            )[0].get(
                "safety",
                {},
            ).get(
                "decision",
                result.get(
                    "classification",
                    {},
                ).get(
                    "category",
                    "unknown",
                ),
            )
            if result.get("steps")
            else result.get(
                "classification",
                {},
            ).get(
                "category",
                "unknown",
            ),
        ),
        "permission": result.get(
            "permission",
            {},
        ).get(
            "permission",
            "critical",
        ),
        "execution_allowed": False,
        "reason": result.get(
            "reason",
            "",
        ),
    }
