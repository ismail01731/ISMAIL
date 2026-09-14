from backend.ai_engine import AIEngine
engine = AIEngine()
message = (
    "Write a Python function named add that returns "
    "the sum of two numbers."
)
question_info = engine.understand_question(message)
assert isinstance(question_info, dict)
assert "intent" in question_info
assert "capabilities" in question_info
assert "task_plan" in question_info
assert question_info["capabilities"]
assert question_info["task_plan"]
print("INTENT:", question_info.get("intent"))
print("ROUTE:", question_info.get("route"))
print(
    "CAPABILITIES:",
    [
        item.get("capability")
        for item in question_info["capabilities"]
    ],
)
print(
    "TASK_PLAN:",
    [
        (
            step.capability,
            step.action,
            step.order,
        )
        for step in question_info["task_plan"]
    ],
)
response = engine.generate(message)
assert response is not None
print("GENERATE_RESULT_TYPE:", type(response).__name__)
print("GENERATE_RESULT_PRESENT:", bool(response))
print("GENERATE_RESULT_PREVIEW:", str(response)[:500])
print("TASK4_STEP74_AIENGINE_GENERATE_BOUNDARY_OK")
