from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
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
]
def real_research_executor(
    step: TaskStep,
) -> CapabilityExecutionResult:
    assert step.capability == "research"
    assert step.action == "research"
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
results = orchestrator.execute(
    plan,
    real_research_executor,
)
assert len(results) == 1
assert isinstance(results[0], CapabilityExecutionResult)
assert results[0].capability == "research"
assert results[0].action == "research"
assert isinstance(results[0].success, bool)
assert isinstance(results[0].result, list)
assert isinstance(results[0].reason, str)
assert results[0].order == 1
print("RESULT:", results[0])
print("RESULT_TYPE:", type(results[0].result).__name__)
print("EVIDENCE_COUNT:", len(results[0].result))
print("SUCCESS:", results[0].success)
print("TASK4_STEP52_REAL_RESEARCH_BOUNDARY_OK")
