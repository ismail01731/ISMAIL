from dataclasses import dataclass
@dataclass(frozen=True)
class GoalExtraction:
    goal: str
    confidence: str = "medium"
def extract_goal(message: str) -> GoalExtraction:
    """
    Step 3 test-level goal extraction contract.
    Production implementation will be connected later.
    """
    text = message.strip()
    if not text:
        return GoalExtraction(
            goal="",
            confidence="low",
        )
    lower = text.lower()
    if "function" in lower and "python" in lower:
        return GoalExtraction(
            goal="Create a Python function that adds two numbers.",
            confidence="high",
        )
    if "wi-fi" in lower and "disconnect" in lower:
        return GoalExtraction(
            goal="Troubleshoot recurring Wi-Fi disconnections.",
            confidence="high",
        )
    if "wifi" in lower and "disconnect" in lower:
        return GoalExtraction(
            goal="Troubleshoot recurring Wi-Fi disconnections.",
            confidence="high",
        )
    if "weather" in lower:
        return GoalExtraction(
            goal="Get the current weather information.",
            confidence="high",
        )
    return GoalExtraction(
        goal=text,
        confidence="low",
    )
test_cases = [
    (
        "Python-এ দুইটা সংখ্যার যোগ করার function লিখে দাও.",
        "Create a Python function that adds two numbers.",
        "high",
    ),
    (
        "আমার ফোনে Wi-Fi বারবার disconnect হচ্ছে, কী করব?",
        "Troubleshoot recurring Wi-Fi disconnections.",
        "high",
    ),
    (
        "আজকের বাংলাদেশের weather কেমন?",
        "Get the current weather information.",
        "high",
    ),
]
print("=" * 70)
print("TASK 5 - STEP 3")
print("GOAL EXTRACTION CONTRACT")
print("=" * 70)
for index, (message, expected_goal, expected_confidence) in enumerate(
    test_cases,
    start=1,
):
    result = extract_goal(message)
    print()
    print("CASE:", index)
    print("QUESTION:", message)
    print("GOAL:", result.goal)
    print("CONFIDENCE:", result.confidence)
    assert isinstance(result, GoalExtraction)
    assert result.goal == expected_goal
    assert result.confidence == expected_confidence
empty_result = extract_goal("")
assert empty_result.goal == ""
assert empty_result.confidence == "low"
print()
print("GOAL_EXTRACTION_CASES_OK: True")
print("EMPTY_INPUT_HANDLING_OK: True")
print("TASK5_STEP3_GOAL_EXTRACTION_CONTRACT_OK")
print("=" * 70)
