from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.programming.programming_intelligence import ProgrammingRequest
from backend.task_planner import TaskStep
engine = AIEngine()
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
        action="analyze_or_execute",
        reason="A Python solution is required.",
        order=2,
    ),
]
def real_executor(step: TaskStep) -> CapabilityExecutionResult:
    if step.capability == "research":
        evidence = engine.web_research.research(
            "What is Python?",
            max_sources=1,
        )
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=bool(evidence),
            result=evidence,
            reason=(
                "Research completed."
                if evidence
                else "No evidence is available."
            ),
            order=step.order,
        )
    if step.capability == "programming":
        resolved_action = engine._detect_programming_action(
            "Write a Python program to calculate factorial."
        )
        request = ProgrammingRequest(
            action=resolved_action,
            language="Python",
            requirement="Write a Python program to calculate factorial.",
            code="",
            project_path="",
            command=[],
            error_message="",
            file_path="",
            context="",
            timeout_seconds=10,
        )
        programming_result = (
            engine.programming_intelligence.handle(request)
        )
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=programming_result.success,
            result=programming_result.result,
            reason=programming_result.reason,
            order=step.order,
        )
    raise ValueError(
        f"Unsupported capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    real_executor,
)
assert len(results) == 2
assert results[0].capability == "research"
assert results[0].order == 1
assert isinstance(results[0].result, list)
assert results[1].capability == "programming"
assert results[1].order == 2
assert results[1].success is True
assert results[1].result is not None
assert [item.order for item in results] == [1, 2]
assert [item.capability for item in results] == [
    "research",
    "programming",
]
print("RESULTS:", results)
print("CAPABILITIES:", [item.capability for item in results])
print("ORDERS:", [item.order for item in results])
print("SUCCESS_FLAGS:", [item.success for item in results])
print("TASK4_STEP54_MULTI_CAPABILITY_EXECUTION_OK")
