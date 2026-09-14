from backend.ai_engine import AIEngine
from backend.programming.programming_intelligence import (
    ProgrammingRequest,
    ProgrammingResult,
)
engine = AIEngine()
programming = engine.programming_intelligence
assert hasattr(programming, "handle")
assert callable(programming.handle)
print("PROGRAMMING_METHOD:", programming.handle.__name__)
request = ProgrammingRequest(
    action="generate_code",
    language="Python",
    requirement="Write a Python program that returns the factorial of 5.",
    code="",
    project_path="",
    command=[],
    error_message="",
    file_path="",
    context="",
    timeout_seconds=10,
)
result = programming.handle(request)
assert isinstance(result, ProgrammingResult)
print("RESULT_TYPE:", type(result).__name__)
print("SUCCESS:", result.success)
print("ACTION:", result.action)
print("REASON:", result.reason)
print("RESULT_PRESENT:", result.result is not None)
assert isinstance(result.success, bool)
assert isinstance(result.action, str)
assert isinstance(result.reason, str)
print("PROGRAMMING_RESULT_CONTRACT_OK")
print("TASK4_STEP45_PROGRAMMING_EXECUTION_BOUNDARY_OK")
