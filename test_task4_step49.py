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
def wrap_result(
    step: TaskStep,
    *,
    success: bool,
    result=None,
    reason: str = "",
) -> CapabilityExecutionResult:
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=success,
        result=result,
        reason=reason,
        order=step.order,
    )
failed_research = TaskStep(
    capability="research",
    action="research",
    reason="Current information is required.",
    order=1,
)
failed_programming = TaskStep(
    capability="programming",
    action="analyze_or_execute",
    reason="A Python solution is required.",
    order=2,
)
research_result = wrap_result(
    failed_research,
    success=False,
    result=[],
    reason="No evidence is available.",
)
programming_result = wrap_result(
    failed_programming,
    success=False,
    result=None,
    reason="Execution failed.",
)
assert research_result.success is False
assert research_result.result == []
assert research_result.reason == "No evidence is available."
assert research_result.order == 1
assert programming_result.success is False
assert programming_result.result is None
assert programming_result.reason == "Execution failed."
assert programming_result.order == 2
results = [research_result, programming_result]
assert len(results) == 2
assert all(isinstance(item, CapabilityExecutionResult) for item in results)
assert all(isinstance(item.success, bool) for item in results)
assert all(isinstance(item.reason, str) for item in results)
print("FAILED_RESEARCH:", research_result)
print("FAILED_PROGRAMMING:", programming_result)
print("FAILURE_RESULTS_SAFE:", True)
print("TASK4_STEP49_FAILURE_RESULT_CONTRACT_OK")
