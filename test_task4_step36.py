from backend.ai_engine import AIEngine
from backend.programming.programming_intelligence import ProgrammingRequest
engine = AIEngine()
cases = [
    (
        "Write a Python program to calculate factorial.",
        "generate_code",
    ),
    (
        "Debug this Python code: print(x)",
        "debug_code",
    ),
    (
        "Run this Python code: print(2+3)",
        "execute",
    ),
    (
        "Run unit tests for this Python project.",
        "run_tests",
    ),
    (
        "Analyze this Python code for problems.",
        "analyze_code",
    ),
    (
        "Analyze this Python project.",
        "analyze_project",
    ),
    (
        "Write documentation for this Python project.",
        "documentation",
    ),
    (
        "Check the Python version.",
        "check_version",
    ),
]
for message, expected_action in cases:
    resolved_action = engine._detect_programming_action(message)
    print(
        f"MESSAGE: {message}\n"
        f"EXPECTED: {expected_action}\n"
        f"RESOLVED: {resolved_action}"
    )
    assert resolved_action == expected_action, (
        f"Action mismatch: expected {expected_action}, "
        f"got {resolved_action}"
    )
    request = ProgrammingRequest(
        action=resolved_action,
        language="Python",
        requirement=message,
        code="",
        project_path="",
        command=[],
        error_message="",
        context="",
        timeout_seconds=10,
    )
    assert request.action == expected_action
    print("REQUEST_ACTION:", request.action)
    print("---")
print("TASK4_STEP36_ACTION_RESOLUTION_CONTRACT_OK")
