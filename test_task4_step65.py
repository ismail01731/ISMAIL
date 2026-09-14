from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.programming.programming_intelligence import (
    ProgrammingRequest,
)
from backend.task_planner import TaskStep
engine = AIEngine()
orchestrator = CapabilityOrchestrator()
plan = [
    TaskStep(
        capability="programming",
        action="execute",
        reason="Execute and verify Python code.",
        order=1,
    ),
]
def real_executor(step):
    assert step.capability == "programming"
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
    assert verification.verified is True
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=verification.verified,
        result=programming_result.result,
        reason=verification.reason,
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    real_executor,
)
assert len(results) == 1
result = results[0]
assert isinstance(
    result,
    CapabilityExecutionResult,
)
assert result.capability == "programming"
assert result.action == "execute"
assert result.success is True
assert result.result is not None
assert result.order == 1
assert (
    result.reason
    == "Code execution result passed consistency verification."
)
print(
    "RESULT_TYPE:",
    type(result).__name__,
)
print(
    "INNER_RESULT_TYPE:",
    type(result.result).__name__,
)
print("SUCCESS:", result.success)
print("VERIFIED: True")
print("REASON:", result.reason)
print("TASK4_STEP65_ORCHESTRATOR_VERIFICATION_CHAIN_OK")
