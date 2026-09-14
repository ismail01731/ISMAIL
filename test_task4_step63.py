from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.programming.programming_intelligence import (
    ProgrammingRequest,
)
engine = AIEngine()
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
question_info = engine.understand_question(
    "Research Python and then write a Python program to calculate factorial."
)
task_plan = engine.task_planner.create_plan(
    capabilities=capabilities
)
assert [step.capability for step in task_plan] == [
    "research",
    "programming",
]
assert [step.order for step in task_plan] == [1, 2]
def real_executor(step):
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
        assert resolved_action == "generate_code"
        request = ProgrammingRequest(
            action=resolved_action,
            language="Python",
            requirement=(
                "Write a Python program to calculate factorial."
            ),
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
    task_plan,
    real_executor,
)
assert len(results) == 2
research_result = results[0]
programming_result = results[1]
assert research_result.capability == "research"
assert research_result.order == 1
assert isinstance(research_result.result, list)
assert programming_result.capability == "programming"
assert programming_result.order == 2
assert programming_result.success is True
assert programming_result.result is not None
assert type(programming_result.result).__name__ == (
    "CodeGenerationResult"
)
assert [result.order for result in results] == [1, 2]
print(
    "TASK_PLAN:",
    [
        (step.capability, step.action, step.order)
        for step in task_plan
    ],
)
print(
    "RESULT_CAPABILITIES:",
    [result.capability for result in results],
)
print(
    "RESULT_ORDERS:",
    [result.order for result in results],
)
print(
    "RESULT_SUCCESS_FLAGS:",
    [result.success for result in results],
)
print(
    "PROGRAMMING_RESULT_TYPE:",
    type(programming_result.result).__name__,
)
print("TASK4_STEP63_REAL_MULTI_CAPABILITY_OK")
