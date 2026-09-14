from dataclasses import dataclass, field
VALID_TASK_TYPES = {
    "code_generation",
    "debugging",
    "troubleshooting",
    "information_retrieval",
    "calculation",
    "unknown",
}
VALID_CONFIDENCE = {
    "low",
    "medium",
    "high",
}
@dataclass(frozen=True)
class TaskUnderstanding:
    message: str
    goal: str
    task_type: str
    constraints: list[str] = field(default_factory=list)
    required_information: list[str] = field(
        default_factory=list
    )
    confidence: str = "medium"
def build_task_understanding(
    message: str,
    goal: str,
    task_type: str,
    constraints: list[str] | None = None,
    required_information: list[str] | None = None,
    confidence: str = "medium",
) -> TaskUnderstanding:
    normalized_message = (
        message.strip()
        if isinstance(message, str)
        else ""
    )
    normalized_goal = (
        goal.strip()
        if isinstance(goal, str)
        else ""
    )
    normalized_task_type = (
        task_type.strip().lower()
        if isinstance(task_type, str)
        else "unknown"
    )
    normalized_confidence = (
        confidence.strip().lower()
        if isinstance(confidence, str)
        else "low"
    )
    if not normalized_task_type:
        normalized_task_type = "unknown"
    if normalized_task_type not in VALID_TASK_TYPES:
        normalized_task_type = "unknown"
    if normalized_confidence not in VALID_CONFIDENCE:
        normalized_confidence = "low"
    normalized_constraints = [
        item.strip()
        for item in (constraints or [])
        if isinstance(item, str)
        and item.strip()
    ]
    normalized_information = [
        item.strip()
        for item in (required_information or [])
        if isinstance(item, str)
        and item.strip()
    ]
    return TaskUnderstanding(
        message=normalized_message,
        goal=normalized_goal,
        task_type=normalized_task_type,
        constraints=normalized_constraints,
        required_information=normalized_information,
        confidence=normalized_confidence,
    )
print("=" * 70)
print("TASK 5 - STEP 8")
print("TASK UNDERSTANDING COMPLETENESS / FINAL CONTRACT")
print("=" * 70)
# CASE 1: Complete valid input
result = build_task_understanding(
    message="Python-এ calculator বানাও.",
    goal="Create a Python calculator.",
    task_type="code_generation",
    constraints=["no_external_libraries"],
    required_information=[
        "calculation_requirements",
        "python_requirements",
    ],
    confidence="high",
)
assert result.message == (
    "Python-এ calculator বানাও."
)
assert result.goal == (
    "Create a Python calculator."
)
assert result.task_type == "code_generation"
assert result.constraints == [
    "no_external_libraries"
]
assert result.required_information == [
    "calculation_requirements",
    "python_requirements",
]
assert result.confidence == "high"
print()
print("CASE 1: COMPLETE_VALID_INPUT_OK")
# CASE 2: Blank / invalid goal
result = build_task_understanding(
    message="Hello ISMAIL.",
    goal="   ",
    task_type="unknown",
    confidence="low",
)
assert result.message == "Hello ISMAIL."
assert result.goal == ""
assert result.task_type == "unknown"
assert result.confidence == "low"
assert result.constraints == []
assert result.required_information == []
print("CASE 2: EMPTY_GOAL_HANDLING_OK")
# CASE 3: Invalid task type
result = build_task_understanding(
    message="Some request.",
    goal="Handle the request.",
    task_type="something_invalid",
    confidence="medium",
)
assert result.task_type == "unknown"
print("CASE 3: INVALID_TASK_TYPE_HANDLING_OK")
# CASE 4: Invalid confidence
result = build_task_understanding(
    message="Some request.",
    goal="Handle the request.",
    task_type="unknown",
    confidence="very_high",
)
assert result.confidence == "low"
print("CASE 4: INVALID_CONFIDENCE_HANDLING_OK")
# CASE 5: Invalid / empty list entries
result = build_task_understanding(
    message="Build something.",
    goal="Build the requested system.",
    task_type="code_generation",
    constraints=[
        "valid_constraint",
        "",
        "   ",
        123,
    ],
    required_information=[
        "valid_information",
        "",
        None,
        "   ",
    ],
)
assert result.constraints == [
    "valid_constraint"
]
assert result.required_information == [
    "valid_information"
]
print("CASE 5: LIST_NORMALIZATION_OK")
# CASE 6: Non-string primary inputs
result = build_task_understanding(
    message=None,
    goal=None,
    task_type=None,
    confidence=None,
)
assert result.message == ""
assert result.goal == ""
assert result.task_type == "unknown"
assert result.confidence == "low"
assert result.constraints == []
assert result.required_information == []
print("CASE 6: INVALID_PRIMARY_INPUT_HANDLING_OK")
# CASE 7: Case normalization
result = build_task_understanding(
    message=" Test request ",
    goal=" Test goal ",
    task_type="  CODE_GENERATION  ",
    confidence="  HIGH  ",
)
assert result.message == "Test request"
assert result.goal == "Test goal"
assert result.task_type == "code_generation"
assert result.confidence == "high"
print("CASE 7: NORMALIZATION_OK")
# Final structural completeness check
required_fields = {
    "message",
    "goal",
    "task_type",
    "constraints",
    "required_information",
    "confidence",
}
actual_fields = set(
    TaskUnderstanding.__dataclass_fields__.keys()
)
assert actual_fields == required_fields
print()
print("REQUIRED_FIELDS_COMPLETE_OK: True")
print("INVALID_INPUT_HANDLING_OK: True")
print("NORMALIZATION_OK: True")
print("TASK_UNDERSTANDING_FINAL_CONTRACT_OK: True")
print(
    "TASK5_STEP8_TASK_UNDERSTANDING_COMPLETENESS_CONTRACT_OK"
)
print("=" * 70)
