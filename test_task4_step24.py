from dataclasses import is_dataclass
from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
result = engine.understand_question(
    "Write a Python program and use current information if needed."
)
assert isinstance(result, dict)
assert "capabilities" in result
assert isinstance(result["capabilities"], list)
# Step 24 target contract:
# understand_question() should expose the planner output.
assert "task_plan" in result, (
    "understand_question() does not expose task_plan yet."
)
assert isinstance(result["task_plan"], list)
for step in result["task_plan"]:
    assert isinstance(step, TaskStep)
    assert is_dataclass(step)
    assert isinstance(step.capability, str)
    assert isinstance(step.action, str)
    assert isinstance(step.reason, str)
    assert isinstance(step.order, int)
    assert step.order >= 1
print("CAPABILITIES:", result["capabilities"])
print("TASK_PLAN:", result["task_plan"])
print("TASK4_STEP24_PLANNER_CONTRACT_OK")
