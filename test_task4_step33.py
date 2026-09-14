from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
message = "Write a Python program to calculate factorial."
result = engine.understand_question(message)
plan = result["task_plan"]
programming_steps = [
    step
    for step in plan
    if isinstance(step, TaskStep)
    and step.capability == "programming"
]
assert programming_steps, "Programming step was not found."
programming_step = programming_steps[0]
resolved_action = engine._detect_programming_action(message)
print("TASK_PLAN:", plan)
print("PROGRAMMING_STEP:", programming_step)
print("PLANNER_ACTION:", programming_step.action)
print("RESOLVED_ACTION:", resolved_action)
assert programming_step.action == "analyze_or_execute"
assert resolved_action == "generate_code"
print("TASK4_STEP33_PLANNER_TO_PROGRAMMING_BOUNDARY_OK")
