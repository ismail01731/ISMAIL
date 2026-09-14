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
        action="generate_code",
        reason="A Python solution is required.",
        order=2,
    ),
]
def executor(step):
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability="research",
            action="research",
            success=False,
            result=[],
            reason="No evidence is available.",
            order=step.order,
        )
    if step.capability == "programming":
        return CapabilityExecutionResult(
            capability="programming",
            action="generate_code",
            success=True,
            result="generated-code",
            reason="Code generated successfully.",
            order=step.order,
        )
    raise ValueError("Unexpected capability")
results = orchestrator.execute(
    plan,
    executor,
)
assert len(results) == 2
research_result = results[0]
programming_result = results[1]
assert research_result.capability == "research"
assert research_result.action == "research"
assert research_result.success is False
assert research_result.result == []
assert research_result.reason == "No evidence is available."
assert research_result.order == 1
assert programming_result.capability == "programming"
assert programming_result.action == "generate_code"
assert programming_result.success is True
assert programming_result.result == "generated-code"
assert programming_result.reason == "Code generated successfully."
assert programming_result.order == 2
print("RESEARCH_RESULT:", research_result)
print("PROGRAMMING_RESULT:", programming_result)
print("RESULT_COUNT:", len(results))
print("RESULT_FIELDS_INTACT: True")
print("TASK4_STEP56_RESULT_COLLECTION_OK")
