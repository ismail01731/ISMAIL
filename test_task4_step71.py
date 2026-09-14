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
        reason="Gather research context first.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="Use research result for programming.",
        order=2,
    ),
]
execution_trace = []
research_result = None
programming_context = None
def chained_executor(step):
    global research_result
    global programming_context
    execution_trace.append(step.capability)
    if step.capability == "research":
        research_result = {
            "title": "Python Example",
            "content": "Python is a programming language.",
        }
        return CapabilityExecutionResult(
            capability="research",
            action="research",
            success=True,
            result=research_result,
            reason="Research completed.",
            order=step.order,
        )
    if step.capability == "programming":
        assert research_result is not None
        programming_context = research_result
        return CapabilityExecutionResult(
            capability="programming",
            action="generate_code",
            success=True,
            result={
                "generated": True,
                "context_used": programming_context,
            },
            reason="Programming used research context.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    chained_executor,
)
assert len(results) == 2
assert execution_trace == [
    "research",
    "programming",
]
assert results[0].success is True
assert results[1].success is True
assert programming_context == research_result
assert results[1].result["context_used"] == research_result
print("EXECUTION_TRACE:", execution_trace)
print("RESEARCH_SUCCESS:", results[0].success)
print("PROGRAMMING_SUCCESS:", results[1].success)
print("RESEARCH_RESULT_PASSED_TO_PROGRAMMING: True")
print("CONTEXT_INTACT:", programming_context == research_result)
print("TASK4_STEP71_RESEARCH_PROGRAMMING_CONTEXT_CHAIN_OK")
