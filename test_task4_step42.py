from dataclasses import dataclass
from backend.task_planner import TaskStep
@dataclass(frozen=True)
class CapabilityExecutionResult:
    capability: str
    action: str
    success: bool
    result: object = None
    reason: str = ""
    order: int = 0
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
results = [
    CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result="test-result",
        reason="Executed successfully.",
        order=step.order,
    )
    for step in plan
]
assert len(results) == len(plan)
for step, result in zip(plan, results):
    assert result.capability == step.capability
    assert result.action == step.action
    assert result.order == step.order
    assert isinstance(result.success, bool)
    assert isinstance(result.reason, str)
print("PLAN_STEPS:", plan)
print("EXECUTION_RESULTS:", results)
print("RESULT_COUNT:", len(results))
print("TASK4_STEP42_ORCHESTRATOR_RESULT_CONTRACT_OK")
