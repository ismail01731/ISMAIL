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
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result=f"executed:{step.capability}",
        reason="Execution completed.",
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    fake_executor,
)
assert isinstance(results, list)
assert len(results) == 2
assert all(
    isinstance(result, CapabilityExecutionResult)
    for result in results
)
assert [result.capability for result in results] == [
    "research",
    "programming",
]
assert [result.order for result in results] == [1, 2]
assert results[0].result == "executed:research"
assert results[1].result == "executed:programming"
print("PLAN:", plan)
print("RESULTS:", results)
print("EXECUTION_ORDER:", [result.order for result in results])
print("TASK4_STEP50_ORCHESTRATOR_CONTRACT_OK")
