from backend.ai_engine import AIEngine
from backend.programming.programming_intelligence import (
    ProgrammingRequest,
)
from backend.result_verifier import VerificationResult
engine = AIEngine()
request = ProgrammingRequest(
    action="execute",
    language="Python",
    requirement="Run a simple Python calculation.",
    code="print(2 + 3)",
    project_path="",
    command=[
        "python",
        "-c",
        "print(2 + 3)",
    ],
    error_message="",
    file_path="",
    context="",
    timeout_seconds=10,
)
programming_result = (
    engine.programming_intelligence.handle(request)
)
assert programming_result.success is True
assert programming_result.result is not None
verification = engine.result_verifier.verify_execution(
    programming_result.result
)
assert isinstance(
    verification,
    VerificationResult,
)
assert verification.verified is True
assert isinstance(verification.reason, str)
assert verification.reason
print(
    "PROGRAMMING_SUCCESS:",
    programming_result.success,
)
print(
    "PROGRAMMING_RESULT_TYPE:",
    type(programming_result.result).__name__,
)
print(
    "VERIFICATION_TYPE:",
    type(verification).__name__,
)
print(
    "VERIFIED:",
    verification.verified,
)
print(
    "VERIFICATION_REASON:",
    verification.reason,
)
print("TASK4_STEP64_RESULT_VERIFICATION_BOUNDARY_OK")
