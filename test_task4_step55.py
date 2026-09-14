from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskPlanner
planner = TaskPlanner()
orchestrator = CapabilityOrchestrator()
capabilities = [
    {
        "capability": "programming",
        "reason": "A Python solution is required.",
        "depends_on": ["research"],
    },
    {
        "capability": "research",
        "reason": "Current information is required.",
    },
]
plan = planner.create_plan(
    capabilities=capabilities
)
assert [step.capability for step in plan] == [
    "research",
    "programming",
]
assert [step.order for step in plan] == [1, 2]
execution_trace = []
def trace_executor(step):
    execution_trace.append(step.capability)
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=True,
        result=f"{step.capability}-result",
        reason="Executed.",
        order=step.order,
    )
results = orchestrator.execute(
    plan,
    trace_executor,
)
assert execution_trace == [
    "research",
    "programming",
]
assert [result.capability for result in results] == [
    "research",
    "programming",
]
assert [result.order for result in results] == [1, 2]
print(
    "PLAN:",
    [(step.capability, step.order) for step in plan]
)
print("EXECUTION_TRACE:", execution_trace)
print(
    "RESULT_ORDER:",
    [result.order for result in results]
)
print(
    "RESULT_CAPABILITIES:",
    [result.capability for result in results]
)
print("TASK4_STEP55_DEPENDENCY_EXECUTION_ORDER_OK")
