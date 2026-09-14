from backend.capability_orchestrator import CapabilityOrchestrator
from backend.task_planner import TaskStep
orchestrator = CapabilityOrchestrator()
plan = [
    TaskStep(
        capability="programming",
        action="execute",
        reason="Test executor exception.",
        order=1,
    ),
]
def failing_executor(step):
    raise RuntimeError(
        "Simulated capability execution failure."
    )
try:
    orchestrator.execute(
        plan,
        failing_executor,
    )
except RuntimeError as exc:
    print("EXCEPTION_PROPAGATED: True")
    print("EXCEPTION_TYPE:", type(exc).__name__)
    print("EXCEPTION_MESSAGE:", str(exc))
else:
    raise AssertionError(
        "Executor exception was unexpectedly swallowed."
    )
print("TASK4_STEP67_EXECUTOR_EXCEPTION_BOUNDARY_OK")
