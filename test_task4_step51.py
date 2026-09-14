from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskStep
orchestrator = CapabilityOrchestrator()
plan = [
    TaskStep(
        capability="research",
        action="research",
        reason="Current information is required.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="analyze_or_execute",
        reason="A Python solution is required.",
        order=2,
    ),
]
def fake_executor(step: TaskStep) -> CapabilityExecutionResult:
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=False,
            result=[],
            reason="No evidence is available.",
            order=step.order,
        )
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result="programming-result",
        reason="Execution completed.",
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    fake_executor,
)
assert len(results) == 2
assert results[0].capability == "research"
assert results[0].success is False
assert results[0].result == []
assert results[0].reason == "No evidence is available."
assert results[1].capability == "programming"
assert results[1].success is True
assert results[1].result == "programming-result"
assert [result.order for result in results] == [1, 2]
print("RESULTS:", results)
print("SUCCESS_FLAGS:", [result.success for result in results])
print("EXECUTION_ORDER:", [result.order for result in results])
print("TASK4_STEP51_ORCHESTRATOR_FAILURE_HANDLING_OK")
