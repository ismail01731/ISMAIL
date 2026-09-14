from backend.ai_engine import AIEngine
engine = AIEngine()
message = "Write a Python program to calculate factorial."
question_info = engine.understand_question(message)
assert isinstance(question_info, dict)
assert question_info.get("route") == "programming"
task_plan = question_info.get("task_plan")
assert isinstance(task_plan, list)
assert task_plan
programming_steps = [
    step
    for step in task_plan
    if step.capability == "programming"
]
assert programming_steps
print("ROUTE:", question_info["route"])
print("TASK_PLAN:", task_plan)
print("PROGRAMMING_STEP:", programming_steps[0])
print("TASK4_STEP34_GENERATE_PLANNER_REGRESSION_OK")
