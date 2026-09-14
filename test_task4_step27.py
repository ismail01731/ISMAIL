from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
result = engine.understand_question(
    "Write a Python program and use current information if needed."
)
plan = result["task_plan"]
assert isinstance(plan, list)
assert plan
for step in plan:
    assert isinstance(step, TaskStep)
capabilities = [step.capability for step in plan]
actions = [step.action for step in plan]
print("ROUTE:", result.get("route"))
print("CAPABILITIES:", capabilities)
print("ACTIONS:", actions)
print("TASK_PLAN:", plan)
assert "programming" in capabilities
print("TASK4_STEP27_EXECUTION_FEASIBILITY_OK")
