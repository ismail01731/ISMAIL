from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
message = "Write a Python program to calculate factorial."
result = engine.understand_question(message)
assert isinstance(result, dict)
plan = result["task_plan"]
programming_steps = [
    step
    for step in plan
    if isinstance(step, TaskStep)
    and step.capability == "programming"
]
assert programming_steps, "Programming step missing from task plan."
planner_step = programming_steps[0]
resolved_action = engine._detect_programming_action(message)
print("MESSAGE:", message)
print("TASK_PLAN:", plan)
print("PROGRAMMING_STEP:", planner_step)
print("PLANNER_ACTION:", planner_step.action)
print("RESOLVED_ACTION:", resolved_action)
assert planner_step.capability == "programming"
assert planner_step.action == "analyze_or_execute"
assert resolved_action == "generate_code"
print("TASK4_STEP30_PLANNER_PROGRAMMING_INTEGRATION_BOUNDARY_OK")
