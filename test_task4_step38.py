from backend.ai_engine import AIEngine
engine = AIEngine()
cases = [
    ("Write a Python program to calculate factorial.", "generate_code"),
    ("Debug this Python code: print(x)", "debug_code"),
    ("Run this Python code: print(2+3)", "execute"),
    ("Run unit tests for this Python project.", "run_tests"),
    ("Analyze this Python code for problems.", "analyze_code"),
    ("Analyze this Python project.", "analyze_project"),
    ("Documentation for this Python project.", "documentation"),
    ("Check the Python version.", "check_version"),
]
for message, expected in cases:
    actual = engine._detect_programming_action(message)
    print(f"MESSAGE: {message}")
    print(f"EXPECTED: {expected}")
    print(f"RESOLVED: {actual}")
    assert actual == expected, (
        f"Expected {expected}, got {actual} for: {message}"
    )
    print("---")
print("TASK4_STEP38_PROGRAMMING_ACTION_FIX_OK")
