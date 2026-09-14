from dataclasses import dataclass, field
@dataclass(frozen=True)
class ConstraintDetection:
    constraints: list[str] = field(default_factory=list)
    confidence: str = "medium"
def detect_constraints(message: str) -> ConstraintDetection:
    text = message.strip()
    lower = text.lower()
    if not text:
        return ConstraintDetection(
            constraints=[],
            confidence="low",
        )
    constraints = []
    if (
        "no external library" in lower
        or "without external library" in lower
        or "external library ব্যবহার করবে না" in lower
    ):
        constraints.append("no_external_libraries")
    if (
        "function names" in lower
        and (
            "don't change" in lower
            or "do not change" in lower
            or "পরিবর্তন করো না" in lower
        )
    ):
        constraints.append("preserve_existing_function_names")
    if (
        "20 lines" in lower
        or "20 লাইনের" in lower
    ):
        constraints.append("maximum_20_lines")
    return ConstraintDetection(
        constraints=constraints,
        confidence="high" if constraints else "medium",
    )
test_cases = [
    (
        "Python-এ একটা calculator বানাও, "
        "কোনো external library ব্যবহার করবে না।",
        ["no_external_libraries"],
        "high",
    ),
    (
        "এই code-টা ঠিক করে দাও, "
        "কিন্তু existing function names পরিবর্তন করো না।",
        ["preserve_existing_function_names"],
        "high",
    ),
    (
        "একটা ছোট Python program বানাও, "
        "20 লাইনের মধ্যে।",
        ["maximum_20_lines"],
        "high",
    ),
]
print("=" * 70)
print("TASK 5 - STEP 5")
print("CONSTRAINT DETECTION CONTRACT")
print("=" * 70)
for index, (
    message,
    expected_constraints,
    expected_confidence,
) in enumerate(test_cases, start=1):
    result = detect_constraints(message)
    print()
    print("CASE:", index)
    print("QUESTION:", message)
    print("CONSTRAINTS:", result.constraints)
    print("CONFIDENCE:", result.confidence)
    assert isinstance(result, ConstraintDetection)
    assert result.constraints == expected_constraints
    assert result.confidence == expected_confidence
empty_result = detect_constraints("")
assert empty_result.constraints == []
assert empty_result.confidence == "low"
no_constraint_result = detect_constraints(
    "Python-এ একটি function লিখে দাও."
)
assert no_constraint_result.constraints == []
assert no_constraint_result.confidence == "medium"
print()
print("CONSTRAINT_CASES_OK: True")
print("EMPTY_INPUT_HANDLING_OK: True")
print("NO_CONSTRAINT_HANDLING_OK: True")
print("TASK5_STEP5_CONSTRAINT_DETECTION_CONTRACT_OK")
print("=" * 70)
