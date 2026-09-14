from backend.ai_engine import AIEngine
from backend.programming.programming_intelligence import ProgrammingRequest
engine = AIEngine()
request = ProgrammingRequest(
    action="execute",
    language="Python",
    requirement="",
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
programming_result = engine.programming_intelligence.handle(request)
print("PROGRAMMING_SUCCESS:", programming_result.success)
print("PROGRAMMING_ACTION:", programming_result.action)
print("PROGRAMMING_RESULT:", programming_result.result)
print("PROGRAMMING_REASON:", programming_result.reason)
assert programming_result.success is True
assert programming_result.action == "execute"
assert programming_result.result is not None
verification = engine.result_verifier.verify_execution(
    programming_result.result
)
print("VERIFICATION_TYPE:", type(verification).__name__)
print("VERIFIED:", verification.verified)
print("VERIFICATION_REASON:", verification.reason)
assert isinstance(verification.verified, bool)
assert isinstance(verification.reason, str)
print("TASK4_STEP47_EXECUTION_VERIFICATION_OK")
