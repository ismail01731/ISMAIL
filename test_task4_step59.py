from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskStep
orchestrator = CapabilityOrchestrator()
plan = [
    {
        "capability": "invalid",
        "action": "invalid",
        "order": 0,
    },
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="A Python solution is required.",
        order=1,
    ),
]
executed = []
def executor(step):
    executed.append(step.capability)
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result="ok",
        reason="Executed.",
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    executor,
)
assert executed == ["programming"]
assert len(results) == 1
assert results[0].capability == "programming"
assert results[0].order == 1
print("EXECUTED:", executed)
print("RESULTS:", results)
print("INVALID_STEP_SKIPPED: True")
print("TASK4_STEP59_INVALID_TASKSTEP_HANDLING_OK")
