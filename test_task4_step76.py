from backend.ai_engine import AIEngine
from backend.capability_orchestrator import (
    CapabilityExecutionResult,
    CapabilityOrchestrator,
)
from backend.task_planner import TaskPlanner
from backend.task_planner import TaskStep
# ==================================================
# INITIALIZE
# ==================================================
engine = AIEngine()
planner = TaskPlanner()
orchestrator = CapabilityOrchestrator()
# ==================================================
# 1. SINGLE CAPABILITY
# ==================================================
single_plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Single programming task.",
        }
    ]
)
assert len(single_plan) == 1
assert single_plan[0].capability == "programming"
# ==================================================
# 2. MULTI-CAPABILITY + DEPENDENCY
# ==================================================
multi_plan = planner.create_plan(
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
        {
            "capability": "knowledge",
            "reason": "Independent knowledge capability.",
        },
    ]
)
assert [
    step.capability
    for step in multi_plan
] == [
    "knowledge",
    "research",
    "programming",
]
# ==================================================
# 3. MIXED SUCCESS / FAILURE
# ==================================================
execution_trace = []
def acceptance_executor(step):
    execution_trace.append(step.capability)
    if step.capability == "knowledge":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="knowledge-result",
            reason="Knowledge completed.",
            order=step.order,
        )
    if step.capability == "research":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=False,
            result=[],
            reason="No research evidence available.",
            order=step.order,
        )
    if step.capability == "programming":
        return CapabilityExecutionResult(
            capability=step.capability,
            action=step.action,
            success=True,
            result="programming-result",
            reason="Programming completed.",
            order=step.order,
        )
    raise AssertionError(
        f"Unexpected capability: {step.capability}"
    )
results = orchestrator.execute(
    multi_plan,
    acceptance_executor,
)
assert len(results) == 3
assert execution_trace == [
    "knowledge",
    "research",
    "programming",
]
assert [result.order for result in results] == [
    1,
    2,
    3,
]
assert [result.success for result in results] == [
    True,
    False,
    True,
]
# ==================================================
# 4. RESULT CONTRACT
# ==================================================
assert all(
    isinstance(
        result,
        CapabilityExecutionResult,
    )
    for result in results
)
assert results[0].result == "knowledge-result"
assert results[1].result == []
assert results[2].result == "programming-result"
assert results[1].reason == (
    "No research evidence available."
)
# ==================================================
# 5. VERIFICATION ACCEPTANCE
# ==================================================
programming_request = (
    "Run this Python code: print(2 + 3)"
)
programming_response = engine.generate(
    programming_request
)
assert programming_response is not None
verification_text = str(programming_response)
assert "programming" in verification_text
assert "success" in verification_text
# ==================================================
# 6. AIENGINE PLANNER ACCEPTANCE
# ==================================================
question_info = engine.understand_question(
    "Write a Python function that returns "
    "the factorial of a number."
)
assert question_info["intent"] == "programming"
assert question_info["capabilities"]
assert question_info["task_plan"]
assert (
    question_info["task_plan"][0].capability
    == "programming"
)
# ==================================================
# 7. EXCEPTION BOUNDARY
# ==================================================
exception_plan = [
    TaskStep(
        capability="programming",
        action="execute",
        reason="Exception boundary.",
        order=1,
    ),
    TaskStep(
        capability="knowledge",
        action="lookup",
        reason="Must not execute after exception.",
        order=2,
    ),
]
exception_trace = []
def exception_executor(step):
    exception_trace.append(step.capability)
    if step.capability == "programming":
        raise RuntimeError(
            "Final acceptance exception test."
        )
    raise AssertionError(
        "Remaining step executed after exception."
    )
try:
    orchestrator.execute(
        exception_plan,
        exception_executor,
    )
except RuntimeError as exc:
    assert str(exc) == (
        "Final acceptance exception test."
    )
else:
    raise AssertionError(
        "Expected exception was not propagated."
    )
assert exception_trace == [
    "programming",
]
# ==================================================
# FINAL ACCEPTANCE
# ==================================================
print("SINGLE_CAPABILITY_OK: True")
print("MULTI_CAPABILITY_OK: True")
print("DEPENDENCY_ORDER_OK: True")
print("MIXED_SUCCESS_FAILURE_OK: True")
print("RESULT_CONTRACT_OK: True")
print("VERIFICATION_BOUNDARY_OK: True")
print("AIENGINE_PLANNER_OK: True")
print("EXCEPTION_BOUNDARY_OK: True")
print("TASK4_STEP76_FINAL_ACCEPTANCE_OK")
