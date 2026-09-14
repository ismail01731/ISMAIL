from dataclasses import dataclass
@dataclass(frozen=True)
class TaskTypeClassification:
    task_type: str
    confidence: str = "medium"
def classify_task_type(message: str) -> TaskTypeClassification:
    text = message.strip()
    if not text:
        return TaskTypeClassification(
            task_type="unknown",
            confidence="low",
        )
    lower = text.lower()
    if "function" in lower and "python" in lower:
        return TaskTypeClassification(
            task_type="code_generation",
            confidence="high",
        )
    if "error" in lower and "python" in lower:
        return TaskTypeClassification(
            task_type="debugging",
            confidence="high",
        )
    if "wi-fi" in lower and "disconnect" in lower:
        return TaskTypeClassification(
            task_type="troubleshooting",
            confidence="high",
        )
    if "wifi" in lower and "disconnect" in lower:
        return TaskTypeClassification(
            task_type="troubleshooting",
            confidence="high",
        )
    if "weather" in lower:
        return TaskTypeClassification(
            task_type="information_retrieval",
            confidence="high",
        )
    if "calculation" in lower:
        return TaskTypeClassification(
            task_type="calculation",
            confidence="high",
        )
    return TaskTypeClassification(
        task_type="unknown",
        confidence="low",
    )
test_cases = [
    (
        "Python-এ দুইটা সংখ্যার যোগ করার function লিখে দাও.",
        "code_generation",
        "high",
    ),
    (
        "Python-এ এই error কেন হচ্ছে?",
        "debugging",
        "high",
    ),
    (
        "আমার ফোনে Wi-Fi বারবার disconnect হচ্ছে, কী করব?",
        "troubleshooting",
        "high",
    ),
    (
        "আজকের বাংলাদেশের weather কেমন?",
        "information_retrieval",
        "high",
    ),
    (
        "এই electrical calculation করে দাও.",
        "calculation",
        "high",
    ),
]
print("=" * 70)
print("TASK 5 - STEP 4")
print("TASK TYPE CLASSIFICATION CONTRACT")
print("=" * 70)
for index, (
    message,
    expected_type,
    expected_confidence,
) in enumerate(test_cases, start=1):
    result = classify_task_type(message)
    print()
    print("CASE:", index)
    print("QUESTION:", message)
    print("TASK_TYPE:", result.task_type)
    print("CONFIDENCE:", result.confidence)
    assert isinstance(result, TaskTypeClassification)
    assert result.task_type == expected_type
    assert result.confidence == expected_confidence
empty_result = classify_task_type("")
assert empty_result.task_type == "unknown"
assert empty_result.confidence == "low"
print()
print("TASK_TYPE_CASES_OK: True")
print("UNKNOWN_INPUT_HANDLING_OK: True")
print("TASK5_STEP4_TASK_TYPE_CLASSIFICATION_CONTRACT_OK")
print("=" * 70)
