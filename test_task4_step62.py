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
message = "Write a Python program to calculate factorial."
question_info = engine.understand_question(message)
task_plan = question_info["task_plan"]
assert len(task_plan) == 1
assert task_plan[0].capability == "programming"
assert task_plan[0].order == 1
def real_executor(step):
    assert step.capability == "programming"
    resolved_action = engine._detect_programming_action(
        message
    )
    assert resolved_action == "generate_code"
    request = ProgrammingRequest(
        action=resolved_action,
        language="Python",
        requirement=message,
        code="",
        project_path="",
        command=[],
        error_message="",
        file_path="",
        context="",
        timeout_seconds=10,
    )
    programming_result = (
        engine.programming_intelligence.handle(request)
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
    task_plan,
    real_executor,
)
assert len(results) == 1
result = results[0]
assert isinstance(
    result,
    CapabilityExecutionResult,
)
assert result.capability == "programming"
assert result.action == "analyze_or_execute"
assert result.success is True
assert result.result is not None
assert type(result.result).__name__ == "CodeGenerationResult"
assert result.reason == "Code generated successfully."
assert result.order == 1
print(
    "TASK_PLAN:",
    [
        (step.capability, step.action, step.order)
        for step in task_plan
    ],
)
print("RESULT_TYPE:", type(result.result).__name__)
print("SUCCESS:", result.success)
print("ACTION:", result.action)
print("REASON:", result.reason)
print("TASK4_STEP62_REAL_PROGRAMMING_VIA_PLAN_OK")
