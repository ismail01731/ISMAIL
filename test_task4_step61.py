from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
engine = AIEngine()
orchestrator = CapabilityOrchestrator()
question_info = engine.understand_question(
    "Write a Python program to calculate factorial."
)
task_plan = question_info["task_plan"]
assert len(task_plan) == 1
assert task_plan[0].capability == "programming"
assert task_plan[0].order == 1
def boundary_executor(step):
    assert step.capability == "programming"
    assert step.action == "analyze_or_execute"
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result="boundary-result",
        reason="Boundary execution successful.",
        order=step.order,
    )
results = orchestrator.execute(
    task_plan,
    boundary_executor,
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
assert result.result == "boundary-result"
assert result.reason == "Boundary execution successful."
assert result.order == 1
print("TASK_PLAN:", [
    (step.capability, step.action, step.order)
    for step in task_plan
])
print("ORCHESTRATOR_RESULTS:", results)
print("RESULT_TYPE:", type(result).__name__)
print("TASK4_STEP61_AIENGINE_PLAN_TO_ORCHESTRATOR_OK")
