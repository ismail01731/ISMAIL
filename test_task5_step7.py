from dataclasses import dataclass, field
@dataclass(frozen=True)
class TaskUnderstanding:
    message: str
    goal: str
    task_type: str
    constraints: list[str] = field(default_factory=list)
    required_information: list[str] = field(default_factory=list)
    confidence: str = "medium"
def build_task_understanding(
    message: str,
    goal: str,
    task_type: str,
    constraints: list[str] | None = None,
    required_information: list[str] | None = None,
    confidence: str = "medium",
) -> TaskUnderstanding:
    return TaskUnderstanding(
        message=message.strip(),
        goal=goal.strip(),
        task_type=task_type.strip(),
        constraints=list(constraints or []),
        required_information=list(
            required_information or []
        ),
        confidence=confidence,
    )
test_cases = [
    {
        "message": (
            "Python-এ একটা calculator বানাও, "
            "কোনো external library ব্যবহার করবে না।"
        ),
        "goal": "Create a Python calculator.",
        "task_type": "code_generation",
        "constraints": [
            "no_external_libraries",
        ],
        "required_information": [
            "calculation_requirements",
            "python_requirements",
        ],
        "confidence": "high",
    },
    {
        "message": (
            "Python-এ এই error কেন হচ্ছে?"
        ),
        "goal": "Troubleshoot the Python error.",
        "task_type": "debugging",
        "constraints": [],
        "required_information": [
            "error_message",
            "relevant_code",
            "python_version",
        ],
        "confidence": "high",
    },
    {
        "message": (
            "আজকের বাংলাদেশের weather কেমন?"
        ),
        "goal": "Get the current weather information.",
        "task_type": "information_retrieval",
        "constraints": [],
        "required_information": [
            "location",
            "current_weather_data",
        ],
        "confidence": "high",
    },
]
print("=" * 70)
print("TASK 5 - STEP 7")
print("TASK UNDERSTANDING ASSEMBLY CONTRACT")
print("=" * 70)
for index, case in enumerate(test_cases, start=1):
    result = build_task_understanding(
        message=case["message"],
        goal=case["goal"],
        task_type=case["task_type"],
        constraints=case["constraints"],
        required_information=case[
            "required_information"
        ],
        confidence=case["confidence"],
    )
    print()
    print("CASE:", index)
    print("MESSAGE:", result.message)
    print("GOAL:", result.goal)
    print("TASK_TYPE:", result.task_type)
    print("CONSTRAINTS:", result.constraints)
    print(
        "REQUIRED_INFORMATION:",
        result.required_information,
    )
    print("CONFIDENCE:", result.confidence)
    assert isinstance(result, TaskUnderstanding)
    assert result.message == case["message"]
    assert result.goal == case["goal"]
    assert result.task_type == case["task_type"]
    assert result.constraints == case["constraints"]
    assert (
        result.required_information
        == case["required_information"]
    )
    assert result.confidence == case["confidence"]
empty_result = build_task_understanding(
    message="",
    goal="",
    task_type="unknown",
    constraints=[],
    required_information=[],
    confidence="low",
)
assert isinstance(empty_result, TaskUnderstanding)
assert empty_result.message == ""
assert empty_result.goal == ""
assert empty_result.task_type == "unknown"
assert empty_result.constraints == []
assert empty_result.required_information == []
assert empty_result.confidence == "low"
# Verify input lists are copied rather than shared.
constraints = ["no_external_libraries"]
required_information = ["python_requirements"]
result = build_task_understanding(
    message="Build a Python calculator.",
    goal="Create a Python calculator.",
    task_type="code_generation",
    constraints=constraints,
    required_information=required_information,
)
constraints.append("maximum_20_lines")
required_information.append("calculation_requirements")
assert result.constraints == [
    "no_external_libraries"
]
assert result.required_information == [
    "python_requirements"
]
print()
print("TASK_UNDERSTANDING_CASES_OK: True")
print("EMPTY_INPUT_HANDLING_OK: True")
print("INPUT_LIST_ISOLATION_OK: True")
print(
    "TASK5_STEP7_TASK_UNDERSTANDING_ASSEMBLY_CONTRACT_OK"
)
print("=" * 70)
