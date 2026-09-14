from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.programming.programming_intelligence import ProgrammingRequest
engine = AIEngine()
orchestrator = CapabilityOrchestrator()
plan = [
    __import__("backend.task_planner", fromlist=["TaskStep"]).TaskStep(
        capability="programming",
        action="analyze_or_execute",
        reason="A Python solution is required.",
        order=1,
    ),
]
def real_programming_executor(
    step,
) -> CapabilityExecutionResult:
    assert step.capability == "programming"
    resolved_action = engine._detect_programming_action(
        "Write a Python program to calculate factorial."
    )
    assert resolved_action == "generate_code"
    request = ProgrammingRequest(
        action=resolved_action,
        language="Python",
        requirement="Write a Python program to calculate factorial.",
        code="",
        project_path="",
        command=[],
        error_message="",
        file_path="",
        context="",
        timeout_seconds=10,
    )
    programming_result = engine.programming_intelligence.handle(
        request
    )
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=programming_result.success,
        result=programming_result.result,
        reason=programming_result.reason,
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    real_programming_executor,
)
assert len(results) == 1
result = results[0]
assert isinstance(result, CapabilityExecutionResult)
assert result.capability == "programming"
assert result.action == "analyze_or_execute"
assert result.success is True
assert result.result is not None
assert isinstance(result.reason, str)
assert result.order == 1
print("RESULT:", result)
print("RESULT_TYPE:", type(result.result).__name__)
print("SUCCESS:", result.success)
print("PLANNER_ACTION:", result.action)
print("RESOLVED_ACTION: generate_code")
print("TASK4_STEP53_REAL_PROGRAMMING_BOUNDARY_OK")
