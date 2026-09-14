from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
test_cases = [
    ("Write a Python program to calculate factorial.", "generate_code"),
    ("Debug this Python code.", "debug_code"),
    ("Run this Python code.", "execute"),
    ("Run the unit tests for this project.", "run_tests"),
    ("Analyze this Python code.", "analyze_code"),
    ("Analyze this project.", "analyze_project"),
    ("Create documentation for this Python API.", "documentation"),
]
for message, expected_action in test_cases:
    result = engine.understand_question(message)
    plan = result["task_plan"]
    programming_steps = [
        step for step in plan
        if isinstance(step, TaskStep)
        and step.capability == "programming"
    ]
    assert programming_steps, (
        f"No programming task step found: {message}"
    )
    resolved_action = engine._detect_programming_action(message)
    print(
        f"MESSAGE: {message}\n"
        f"PLANNER_ACTION: {programming_steps[0].action}\n"
        f"RESOLVED_ACTION: {resolved_action}\n"
        f"EXPECTED_ACTION: {expected_action}\n"
    )
    assert resolved_action == expected_action
print("TASK4_STEP29_PROGRAMMING_ACTION_BOUNDARY_OK")
