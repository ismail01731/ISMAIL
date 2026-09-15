"""
ISMAIL AI - Computer Permission & Safety Policy
Task 13A
This module defines permission and safety rules
for computer actions.
IMPORTANT:
This module does NOT execute computer actions.
"""
PERMISSION_LEVELS = {
    "low",
    "medium",
    "high",
    "critical",
}
SAFETY_DECISIONS = {
    "allow",
    "confirm",
    "block",
}
COMPUTER_SAFETY_POLICIES = {
    "create_folder": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Creating a folder is normally a low-risk computer action.",
    },
    "create_file": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Creating a file is normally a low-risk computer action.",
    },
    "read_file": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Reading a file does not normally modify the computer.",
    },
    "open_application": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Opening an application is normally low risk.",
    },
    "open_website": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Opening a website is normally low risk.",
    },
    "search_web": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Web search does not normally modify the local computer.",
    },
    "check_system": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "System inspection is normally read-only.",
    },
    "check_network": {
        "permission": "low",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Network inspection is normally read-only.",
    },
    "copy_file": {
        "permission": "medium",
        "decision": "allow",
        "requires_confirmation": False,
        "reason": "Copying creates another file but normally does not destroy data.",
    },
    "move_file": {
        "permission": "medium",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Moving a file changes its location and may affect workflows.",
    },
    "rename_file": {
        "permission": "medium",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Renaming changes an existing file reference.",
    },
    "close_application": {
        "permission": "medium",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Closing an application may discard unsaved work.",
    },
    "delete_file": {
        "permission": "high",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Deleting a file can cause data loss.",
    },
    "run_command": {
        "permission": "high",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "A command may modify the system or execute unintended operations.",
    },
    "install_software": {
        "permission": "high",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Software installation changes the system.",
    },
    "uninstall_software": {
        "permission": "high",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Software removal changes the system and may remove data.",
    },
    "shutdown_computer": {
        "permission": "critical",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Shutting down the computer interrupts active work.",
    },
    "restart_computer": {
        "permission": "critical",
        "decision": "confirm",
        "requires_confirmation": True,
        "reason": "Restarting the computer interrupts active work.",
    },
}
def get_permission_policy(intent):
    """
    Return the safety policy for a computer action intent.
    """
    key = str(intent or "").strip().lower()
    policy = COMPUTER_SAFETY_POLICIES.get(key)
    if policy is None:
        return {
            "intent": key,
            "permission": "critical",
            "decision": "block",
            "requires_confirmation": True,
            "reason": (
                "Unknown computer action intent is blocked "
                "by default for safety."
            ),
        }
    return {
        "intent": key,
        "permission": policy["permission"],
        "decision": policy["decision"],
        "requires_confirmation": policy["requires_confirmation"],
        "reason": policy["reason"],
    }
def is_known_permission_level(level):
    return str(level or "").strip().lower() in PERMISSION_LEVELS
def is_known_safety_decision(decision):
    return str(decision or "").strip().lower() in SAFETY_DECISIONS
def get_all_permission_policies():
    return dict(COMPUTER_SAFETY_POLICIES)
