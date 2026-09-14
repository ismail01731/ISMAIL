from backend.ai_engine import AIEngine
engine = AIEngine()
tests = [
    "Python code লিখে দাও",
    "এই Python code-এর error ঠিক করো",
    "এই Python code analyze করো",
]
for message in tests:
    info = engine.understand_question(message)
    print("\nMESSAGE:", message)
    print("INTENT:", info["intent"])
    print("ROUTE:", info["route"])
    print("CAPABILITIES:", info["capabilities"])
    print("TASK_PLAN:", info["task_plan"])
    action = engine._detect_programming_action(message)
    print("PROGRAMMING_ACTION:", action)
    assert info["route"] == "programming"
    assert any(
        item["capability"] == "programming"
        for item in info["capabilities"]
    )
    assert info["task_plan"]
    assert action in {
        "generate_code",
        "debug_code",
        "analyze_code",
    }
print("\nTASK4_STEP41_PROGRAMMING_ORCHESTRATION_OK")
