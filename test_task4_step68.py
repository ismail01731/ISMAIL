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
        reason="Research step.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="Programming step.",
        order=2,
    ),
    TaskStep(
        capability="medical",
        action="assess",
        reason="Medical step.",
        order=3,
    ),
]
execution_trace = []
def mixed_executor(step):
    execution_trace.append(step.capability)
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result=["research-result"],
            reason="Research completed.",
            order=step.order,
        )
    if step.capability == "programming":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=False,
            result=None,
            reason="Programming execution failed.",
            order=step.order,
        )
    if step.capability == "medical":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="medical-result",
            reason="Medical step completed.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    mixed_executor,
)
assert len(results) == 3
assert execution_trace == [
    "research",
    "programming",
    "medical",
]
assert [result.order for result in results] == [1, 2, 3]
assert [result.capability for result in results] == [
    "research",
    "programming",
    "medical",
]
assert [result.success for result in results] == [
    True,
    False,
    True,
]
assert results[0].result == ["research-result"]
assert results[1].result is None
assert results[2].result == "medical-result"
assert results[0].reason == "Research completed."
assert results[1].reason == "Programming execution failed."
assert results[2].reason == "Medical step completed."
print("EXECUTION_TRACE:", execution_trace)
print("RESULT_COUNT:", len(results))
print("ORDERS:", [result.order for result in results])
print(
    "CAPABILITIES:",
    [result.capability for result in results],
)
print(
    "SUCCESS_FLAGS:",
    [result.success for result in results],
)
print("TASK4_STEP68_MIXED_EXECUTION_REGRESSION_OK")
