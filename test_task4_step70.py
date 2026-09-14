from backend.capability_orchestrator import CapabilityOrchestrator
from backend.task_planner import TaskStep
orchestrator = CapabilityOrchestrator()
plan = [
    TaskStep(
        capability="research",
        action="research",
        reason="First step succeeds.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="execute",
        reason="Second step raises an exception.",
        order=2,
    ),
    TaskStep(
        capability="medical",
        action="assess",
        reason="Third step must not execute.",
        order=3,
    ),
]
execution_trace = []
def exception_executor(step):
    execution_trace.append(step.capability)
    if step.capability == "research":
        return __import__(
            "backend.capability_orchestrator",
            fromlist=["CapabilityExecutionResult"],
        ).CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="research-result",
            reason="Research completed.",
            order=step.order,
        )
    if step.capability == "programming":
        raise RuntimeError(
            "Simulated programming capability exception."
        )
    raise AssertionError(
        "Medical step should not execute after exception."
    )
try:
    orchestrator.execute(
        plan,
        exception_executor,
    )
except RuntimeError as exc:
    print("EXCEPTION_PROPAGATED: True")
    print("EXCEPTION_TYPE:", type(exc).__name__)
    print("EXCEPTION_MESSAGE:", str(exc))
else:
    raise AssertionError(
        "Expected RuntimeError was not propagated."
    )
assert execution_trace == [
    "research",
    "programming",
]
assert "medical" not in execution_trace
print("EXECUTION_TRACE:", execution_trace)
print("MEDICAL_EXECUTED: False")
print("EXCEPTION_STOPS_REMAINING_STEPS: True")
print("TASK4_STEP70_EXCEPTION_STOP_BOUNDARY_OK")
