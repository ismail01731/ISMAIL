"""
ISMAIL AI - Computer Context / Reference Resolver
Task 14E-C
This module resolves contextual references against the
logical ComputerState.
IMPORTANT:
This module does NOT inspect or modify the real computer.
It only resolves references from known logical state.
"""
from typing import Any, Dict, Optional
from backend.computer.universal.state.model import (
    ComputerState,
)
REFERENCE_ALIASES = {
    "it": "it",
    "this": "it",
    "that": "it",
    "\u098f\u099f\u09be": "it",
    "\u0993\u099f\u09be": "it",
    "\u09b8\u09c7\u099f\u09be": "it",
    "\u098f\u0987": "it",
    "\u0993\u0987": "it",
    "this": "it",
    "that": "it",
    "the file": "the file",
    "this file": "the file",
    "that file": "the file",
    "the folder": "the folder",
    "this folder": "the folder",
    "that folder": "the folder",
    "the application": "the application",
    "this application": "the application",
    "that application": "the application",
    "the app": "the application",
    "this app": "the application",
    "that app": "the application",
    "\u098f\u0987 \u0985\u09cd\u09af\u09be\u09aa": "the application",
    "\u0993\u0987 \u0985\u09cd\u09af\u09be\u09aa": "the application",
    "\u098f\u0987 \u0985\u09cd\u09af\u09be\u09aa\u099f\u09bf": "the application",
    "\u0993\u0987 \u0985\u09cd\u09af\u09be\u09aa\u099f\u09bf": "the application",
    "the website": "the website",
    "this website": "the website",
    "that website": "the website",
}
def _normalize_reference(reference: Optional[str]) -> str:
    """
    Normalize a reference phrase.
    """
    return " ".join(
        str(reference or "")
        .strip()
        .lower()
        .split()
    )
def _get_reference_key(reference: str) -> str:
    """
    Convert a user-facing reference into a canonical key.
    """
    normalized = _normalize_reference(reference)
    return REFERENCE_ALIASES.get(
        normalized,
        normalized,
    )
def _resolve_from_state(
    state: ComputerState,
    reference_key: str,
) -> Any:
    """
    Resolve a canonical reference key against state.
    """
    if reference_key == "it":
        if state.references.get("it") is not None:
            return state.references.get("it")
        if state.active_file is not None:
            return state.active_file
        if state.current_folder is not None:
            return state.current_folder
        if state.active_application is not None:
            return state.active_application
        if state.active_website is not None:
            return state.active_website
        return None
    if reference_key == "the file":
        if state.references.get("the file") is not None:
            return state.references.get("the file")
        if state.active_file is not None:
            return state.active_file
        if state.known_files:
            return state.known_files[-1]
        return None
    if reference_key == "the folder":
        if state.references.get("the folder") is not None:
            return state.references.get("the folder")
        if state.current_folder is not None:
            return state.current_folder
        if state.known_folders:
            return state.known_folders[-1]
        return None
    if reference_key == "the application":
        if state.references.get("the application") is not None:
            return state.references.get(
                "the application"
            )
        if state.active_application is not None:
            return state.active_application
        return None
    if reference_key == "the website":
        if state.references.get("the website") is not None:
            return state.references.get(
                "the website"
            )
        if state.active_website is not None:
            return state.active_website
        return None
    if state.references.get(reference_key) is not None:
        return state.references.get(reference_key)
    return None
def resolve_reference(
    reference: str,
    state: ComputerState,
) -> Dict[str, Any]:
    """
    Resolve one contextual reference against a ComputerState.
    No computer action is performed.
    """
    normalized = _normalize_reference(reference)
    if not normalized:
        return {
            "reference": str(reference or ""),
            "normalized_reference": "",
            "resolved": False,
            "value": None,
            "source": None,
            "execution_allowed": False,
        }
    reference_key = _get_reference_key(
        normalized
    )
    value = _resolve_from_state(
        state,
        reference_key,
    )
    if value is None:
        return {
            "reference": reference,
            "normalized_reference": normalized,
            "reference_key": reference_key,
            "resolved": False,
            "value": None,
            "source": None,
            "execution_allowed": False,
        }
    if state.references.get(reference_key) is not None:
        source = "explicit_reference"
    elif reference_key == "the file":
        source = (
            "active_file"
            if state.active_file is not None
            else "known_files"
        )
    elif reference_key == "the folder":
        source = (
            "current_folder"
            if state.current_folder is not None
            else "known_folders"
        )
    elif reference_key == "the application":
        source = "active_application"
    elif reference_key == "the website":
        source = "active_website"
    elif reference_key == "it":
        source = "context_fallback"
    else:
        source = "state_reference"
    return {
        "reference": reference,
        "normalized_reference": normalized,
        "reference_key": reference_key,
        "resolved": True,
        "value": value,
        "source": source,
        "execution_allowed": False,
    }
def resolve_references(
    references,
    state: ComputerState,
):
    """
    Resolve multiple contextual references.
    """
    results = []
    for reference in references or []:
        results.append(
            resolve_reference(
                reference,
                state,
            )
        )
    return results
def get_reference_value(
    reference: str,
    state: ComputerState,
):
    """
    Return only the resolved value.
    Returns None when unresolved.
    """
    result = resolve_reference(
        reference,
        state,
    )
    return result.get("value")
def is_reference_resolved(
    reference: str,
    state: ComputerState,
) -> bool:
    """
    Check whether a reference can be resolved.
    """
    result = resolve_reference(
        reference,
        state,
    )
    return result.get("resolved", False)
