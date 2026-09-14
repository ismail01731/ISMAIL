from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskPlanner
engine = AIEngine()
planner = TaskPlanner()
orchestrator = CapabilityOrchestrator()
capabilities = [
    {
        "capability": "research",
        "reason": "Research prerequisite.",
    },
    {
        "capability": "programming",
        "reason": "Programming depends on research.",
        "depends_on": ["research"],
    },
]
plan = planner.create_plan(
    capabilities=capabilities
)
assert len(plan) == 2
assert plan[0].capability == "research"
assert plan[1].capability == "programming"
execution_trace = []
def dependency_failure_executor(step):
    execution_trace.append(step.capability)
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=False,
            result=[],
            reason="Research failed: no evidence available.",
            order=step.order,
        )
    if step.capability == "programming":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="programming-result",
            reason="Programming executed despite failed prerequisite.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    dependency_failure_executor,
)
assert len(results) == 2
assert execution_trace == [
    "research",
    "programming",
]
assert results[0].capability == "research"
assert results[0].success is False
assert results[0].order == 1
assert results[1].capability == "programming"
assert results[1].success is True
assert results[1].order == 2
print(
    "PLAN:",
    [
        (step.capability, step.action, step.order)
        for step in plan
    ],
)
print("EXECUTION_TRACE:", execution_trace)
print("RESULT_COUNT:", len(results))
print("RESEARCH_SUCCESS:", results[0].success)
print("PROGRAMMING_SUCCESS:", results[1].success)
print("PROGRAMMING_EXECUTED_AFTER_RESEARCH_FAILURE: True")
print("TASK4_STEP69_DEPENDENCY_FAILURE_BEHAVIOR_OK")
