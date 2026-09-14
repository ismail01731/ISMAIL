from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.programming.programming_intelligence import (
    ProgrammingRequest,
)
engine = AIEngine()
orchestrator = CapabilityOrchestrator()
from backend.task_planner import TaskStep
plan = [
    TaskStep(
        capability="programming",
        action="execute",
        reason="Execute invalid Python command.",
        order=1,
    ),
]
def real_executor(step):
    request = ProgrammingRequest(
        action="execute",
        language="Python",
        requirement="Run a failing Python command.",
        code="raise ValueError('test failure')",
        project_path="",
        command=[
            "python",
            "-c",
            "raise ValueError('test failure')",
        ],
        error_message="",
        file_path="",
        context="",
        timeout_seconds=10,
    )
    programming_result = (
        engine.programming_intelligence.handle(request)
    )
    assert programming_result.success is False
    verification = engine.result_verifier.verify_execution(
        programming_result.result
    )
    assert verification.verified is False
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
assert result.success is False
assert result.order == 1
assert isinstance(result.reason, str)
assert result.reason
print("RESULT_TYPE:", type(result).__name__)
print(
    "INNER_RESULT_TYPE:",
    type(result.result).__name__
    if result.result is not None
    else "None",
)
print("SUCCESS:", result.success)
print("VERIFIED: False")
print("REASON:", result.reason)
print("TASK4_STEP66_VERIFICATION_FAILURE_BOUNDARY_OK")
