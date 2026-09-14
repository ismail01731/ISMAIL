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
        reason="Collect source information.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="Generate code using research context.",
        order=2,
    ),
    TaskStep(
        capability="verification",
        action="verify",
        reason="Verify the programming result.",
        order=3,
    ),
]
execution_trace = []
research_result = None
programming_result = None
programming_context = None
verification_context = None
def chained_executor(step):
    global research_result
    global programming_result
    global programming_context
    global verification_context
    execution_trace.append(step.capability)
    if step.capability == "research":
        research_result = {
            "source": "Python documentation",
            "fact": "Python supports functions.",
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
        programming_context = {
            "research": research_result,
        }
        programming_result = {
            "code": "def add(a, b): return a + b",
            "context": programming_context,
        }
        return CapabilityExecutionResult(
            capability="programming",
            action="generate_code",
            success=True,
            result=programming_result,
            reason="Programming completed using research context.",
            order=step.order,
        )
    if step.capability == "verification":
        assert programming_result is not None
        verification_context = {
            "programming": programming_result,
            "research": research_result,
        }
        return CapabilityExecutionResult(
            capability="verification",
            action="verify",
            success=True,
            result={
                "verified": True,
                "context": verification_context,
            },
            reason="Programming result verified.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    plan,
    chained_executor,
)
assert len(results) == 3
assert execution_trace == [
    "research",
    "programming",
    "verification",
]
assert results[0].success is True
assert results[1].success is True
assert results[2].success is True
assert programming_context["research"] == research_result
assert (
    verification_context["programming"]
    == programming_result
)
assert (
    verification_context["research"]
    == research_result
)
assert (
    results[2].result["context"]["programming"]
    == programming_result
)
assert (
    results[2].result["context"]["research"]
    == research_result
)
print("EXECUTION_TRACE:", execution_trace)
print("RESULT_COUNT:", len(results))
print(
    "SUCCESS_FLAGS:",
    [result.success for result in results],
)
print("RESEARCH_TO_PROGRAMMING_CONTEXT: True")
print("PROGRAMMING_TO_VERIFICATION_CONTEXT: True")
print("RESEARCH_CONTEXT_RETAINED: True")
print("TASK4_STEP72_MULTI_CAPABILITY_CONTEXT_PASSING_OK")
