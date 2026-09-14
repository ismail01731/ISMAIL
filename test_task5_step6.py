from dataclasses import dataclass, field
@dataclass(frozen=True)
class RequiredInformationDetection:
    required_information: list[str] = field(default_factory=list)
    confidence: str = "medium"
def detect_required_information(
    message: str,
) -> RequiredInformationDetection:
    text = message.strip()
    lower = text.lower()
    if not text:
        return RequiredInformationDetection(
            required_information=[],
            confidence="low",
        )
    required = []
    if "error" in lower and "python" in lower:
        required.extend([
            "error_message",
            "relevant_code",
            "python_version",
        ])
    if "weather" in lower:
        required.extend([
            "location",
            "current_weather_data",
        ])
    if "electrical" in lower and "python" in lower:
        required.extend([
            "electrical_values",
            "formula",
            "units",
            "calculation_requirements",
            "python_requirements",
        ])
    return RequiredInformationDetection(
        required_information=required,
        confidence="high" if required else "medium",
    )
test_cases = [
    (
        "Python-এ এই error কেন হচ্ছে?",
        [
            "error_message",
            "relevant_code",
            "python_version",
        ],
        "high",
    ),
    (
        "আজকের বাংলাদেশের weather কেমন?",
        [
            "location",
            "current_weather_data",
        ],
        "high",
    ),
    (
        "এই electrical calculation করে "
        "একটা Python calculator বানিয়ে দাও.",
        [
            "electrical_values",
            "formula",
            "units",
            "calculation_requirements",
            "python_requirements",
        ],
        "high",
    ),
]
print("=" * 70)
print("TASK 5 - STEP 6")
print("REQUIRED INFORMATION DETECTION CONTRACT")
print("=" * 70)
for index, (
    message,
    expected_information,
    expected_confidence,
) in enumerate(test_cases, start=1):
    result = detect_required_information(message)
    print()
    print("CASE:", index)
    print("QUESTION:", message)
    print(
        "REQUIRED_INFORMATION:",
        result.required_information,
    )
    print("CONFIDENCE:", result.confidence)
    assert isinstance(
        result,
        RequiredInformationDetection,
    )
    assert (
        result.required_information
        == expected_information
    )
    assert (
        result.confidence
        == expected_confidence
    )
empty_result = detect_required_information("")
assert empty_result.required_information == []
assert empty_result.confidence == "low"
no_information_result = detect_required_information(
    "Hello ISMAIL."
)
assert no_information_result.required_information == []
assert no_information_result.confidence == "medium"
print()
print("REQUIRED_INFORMATION_CASES_OK: True")
print("EMPTY_INPUT_HANDLING_OK: True")
print("NO_INFORMATION_HANDLING_OK: True")
print(
    "TASK5_STEP6_REQUIRED_INFORMATION_CONTRACT_OK"
)
print("=" * 70)
