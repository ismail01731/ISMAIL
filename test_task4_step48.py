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
research_step = TaskStep(
    capability="research",
    action="research",
    reason="Current information is required.",
    order=1,
)
programming_step = TaskStep(
    capability="programming",
    action="analyze_or_execute",
    reason="A Python solution is required.",
    order=2,
)
research_result = wrap_result(
    research_step,
    success=True,
    result=["research-evidence"],
    reason="Research completed.",
)
programming_result = wrap_result(
    programming_step,
    success=True,
    result={"generated_code": "print(5)"},
    reason="Programming completed.",
)
assert isinstance(research_result, CapabilityExecutionResult)
assert isinstance(programming_result, CapabilityExecutionResult)
assert research_result.capability == "research"
assert research_result.action == "research"
assert research_result.success is True
assert research_result.result == ["research-evidence"]
assert research_result.order == 1
assert programming_result.capability == "programming"
assert programming_result.action == "analyze_or_execute"
assert programming_result.success is True
assert programming_result.result == {"generated_code": "print(5)"}
assert programming_result.order == 2
results = [research_result, programming_result]
assert [item.order for item in results] == [1, 2]
assert [item.capability for item in results] == [
    "research",
    "programming",
]
print("RESEARCH_WRAPPED:", research_result)
print("PROGRAMMING_WRAPPED:", programming_result)
print("COMMON_RESULT_TYPE:", CapabilityExecutionResult.__name__)
print("TASK4_STEP48_COMMON_RESULT_WRAPPER_OK")
