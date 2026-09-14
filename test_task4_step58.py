from backend.capability_orchestrator import CapabilityOrchestrator
orchestrator = CapabilityOrchestrator()
executor_called = False
def executor(step):
    global executor_called
    executor_called = True
    raise AssertionError(
        "Executor must not be called for an empty plan."
    )
results = orchestrator.execute(
    [],
    executor,
)
assert results == []
assert executor_called is False
print("RESULTS:", results)
print("EXECUTOR_CALLED:", executor_called)
print("TASK4_STEP58_EMPTY_PLAN_BOUNDARY_OK")
