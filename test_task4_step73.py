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
        reason="Research information.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="Generate code.",
        order=2,
    ),
    TaskStep(
        capability="verification",
        action="verify",
        reason="Verify result.",
        order=3,
    ),
]
def aggregation_executor(step):
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability="research",
            action="research",
            success=True,
            result=["source-A", "source-B"],
            reason="Research completed.",
            order=step.order,
        )
    if step.capability == "programming":
        return CapabilityExecutionResult(
            capability="programming",
            action="generate_code",
            success=False,
            result=None,
            reason="Code generation failed.",
            order=step.order,
        )
    if step.capability == "verification":
        return CapabilityExecutionResult(
            capability="verification",
            action="verify",
            success=True,
            result={"verified": True},
            reason="Verification completed.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    aggregation_executor,
)
assert len(results) == 3
# Ordered aggregation
assert [result.order for result in results] == [1, 2, 3]
# Capability aggregation
assert [result.capability for result in results] == [
    "research",
    "programming",
    "verification",
]
# Success/failure aggregation
assert [result.success for result in results] == [
    True,
    False,
    True,
]
# Result preservation
assert results[0].result == [
    "source-A",
    "source-B",
]
assert results[1].result is None
assert results[2].result == {
    "verified": True,
}
# Reason preservation
assert results[0].reason == "Research completed."
assert results[1].reason == "Code generation failed."
assert results[2].reason == "Verification completed."
# Final aggregation object must remain a list
assert isinstance(results, list)
# Every item must retain the common contract
assert all(
    isinstance(
        result,
        CapabilityExecutionResult,
    )
    for result in results
)
print("RESULT_TYPE:", type(results).__name__)
print("RESULT_COUNT:", len(results))
print(
    "ORDERS:",
    [result.order for result in results],
)
print(
    "CAPABILITIES:",
    [result.capability for result in results],
)
print(
    "SUCCESS_FLAGS:",
    [result.success for result in results],
)
print(
    "REASONS:",
    [result.reason for result in results],
)
print("ALL_RESULT_FIELDS_PRESERVED: True")
print("TASK4_STEP73_FINAL_RESULT_AGGREGATION_OK")
