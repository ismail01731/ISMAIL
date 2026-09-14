from backend.programming.programming_intelligence import ProgrammingRequest
request = ProgrammingRequest(
    action="generate_code",
    language="Python",
    requirement="Write a Python program to calculate factorial.",
    code="",
    project_path="",
    command=[],
    error_message="",
    context="",
    timeout_seconds=10,
)
required_fields = [
    "action",
    "language",
    "requirement",
    "code",
    "project_path",
    "command",
    "error_message",
    "context",
    "timeout_seconds",
]
for field in required_fields:
    assert hasattr(request, field), f"Missing field: {field}"
print("VALID_ACTION:", request.action)
print("REQUIRED_FIELDS_OK")
try:
    invalid_request = ProgrammingRequest(
        action="analyze_or_execute",
        language="Python",
        requirement="Write a Python program.",
        code="",
        project_path="",
        command=[],
        error_message="",
        context="",
        timeout_seconds=10,
    )
    print("GENERIC_ACTION_ACCEPTED:", invalid_request.action)
except Exception as exc:
    print("GENERIC_ACTION_REJECTED:", type(exc).__name__, str(exc))
print("TASK4_STEP35_PROGRAMMING_REQUEST_CONTRACT_OK")
