from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskPlanner
from backend.task_planner import TaskStep
# --------------------------------------------------
# 1. Planner priority regression
# --------------------------------------------------
planner = TaskPlanner()
plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Programming task.",
        },
        {
            "capability": "research",
            "reason": "Research task.",
        },
        {
            "capability": "knowledge",
            "reason": "Knowledge task.",
        },
    ]
)
assert [
    step.capability
    for step in plan
] == [
    "knowledge",
    "research",
    "programming",
]
# --------------------------------------------------
# 2. Planner dependency regression
# --------------------------------------------------
dependency_plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Programming depends on research.",
            "depends_on": ["research"],
        },
        {
            "capability": "research",
            "reason": "Research prerequisite.",
        },
    ]
)
assert [
    step.capability
    for step in dependency_plan
] == [
    "research",
    "programming",
]
# --------------------------------------------------
# 3. Orchestrator execution regression
# --------------------------------------------------
orchestrator = CapabilityOrchestrator()
execution_plan = [
    TaskStep(
        capability="research",
        action="research",
        reason="Research.",
        order=1,
    ),
    TaskStep(
        capability="programming",
        action="generate_code",
        reason="Programming.",
        order=2,
    ),
]
execution_trace = []
def executor(step):
    execution_trace.append(step.capability)
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="research-result",
            reason="Research completed.",
            order=step.order,
        )
    return CapabilityExecutionResult(
        capability=step.capability,
        action=step.action,
        success=False,
        result=None,
        reason="Programming failed.",
        order=step.order,
    )
results = orchestrator.execute(
    execution_plan,
    executor,
)
assert execution_trace == [
    "research",
    "programming",
]
assert len(results) == 2
assert results[0].success is True
assert results[1].success is False
assert [result.order for result in results] == [1, 2]
# --------------------------------------------------
# 4. Invalid executor result regression
# --------------------------------------------------
def invalid_executor(step):
    return {
        "capability": step.capability,
        "success": True,
    }
try:
    orchestrator.execute(
        [
            TaskStep(
                capability="programming",
                action="generate_code",
                reason="Invalid result test.",
                order=1,
            )
        ],
        invalid_executor,
    )
except TypeError as exc:
    assert (
        "Capability executor must return "
        "CapabilityExecutionResult."
        in str(exc)
    )
else:
    raise AssertionError(
        "Invalid executor result was not rejected."
    )
# --------------------------------------------------
# 5. AIEngine planner integration regression
# --------------------------------------------------
engine = AIEngine()
question_info = engine.understand_question(
    "Write a Python function that adds two numbers."
)
assert question_info["intent"] == "programming"
assert question_info["capabilities"]
assert question_info["task_plan"]
assert (
    question_info["task_plan"][0].capability
    == "programming"
)
# --------------------------------------------------
# 6. AIEngine generate regression
# --------------------------------------------------
response = engine.generate(
    "Write a Python function named add that returns "
    "the sum of two numbers."
)
assert response is not None
assert bool(response)
response_text = str(response)
assert "programming" in response_text
assert "success" in response_text
# --------------------------------------------------
# Final regression output
# --------------------------------------------------
print("PLANNER_PRIORITY_OK: True")
print("PLANNER_DEPENDENCY_OK: True")
print("ORCHESTRATOR_EXECUTION_OK: True")
print("MIXED_SUCCESS_FAILURE_OK: True")
print("INVALID_RESULT_VALIDATION_OK: True")
print("AIENGINE_PLANNER_INTEGRATION_OK: True")
print("AIENGINE_GENERATE_OK: True")
print("TASK4_STEP75_FULL_REGRESSION_OK")
