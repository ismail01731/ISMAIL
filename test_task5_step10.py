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
@dataclass(frozen=True)
class IntegrationContext:
    message: str
    goal: str
    task_type: str
    constraints: list[str]
    required_information: list[str]
    confidence: str
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
def validate_task_understanding(
    result: TaskUnderstanding,
) -> bool:
    if not isinstance(result, TaskUnderstanding):
        return False
    if not isinstance(result.message, str):
        return False
    if not isinstance(result.goal, str):
        return False
    if not isinstance(result.task_type, str):
        return False
    if not isinstance(result.constraints, list):
        return False
    if not isinstance(
        result.required_information,
        list,
    ):
        return False
    if not isinstance(result.confidence, str):
        return False
    if result.task_type not in VALID_TASK_TYPES:
        return False
    if result.confidence not in VALID_CONFIDENCE:
        return False
    return True
def create_integration_context(
    result: TaskUnderstanding,
) -> IntegrationContext:
    return IntegrationContext(
        message=result.message,
        goal=result.goal,
        task_type=result.task_type,
        constraints=list(result.constraints),
        required_information=list(
            result.required_information
        ),
        confidence=result.confidence,
    )
def check_complete_chain(
    result: TaskUnderstanding,
) -> bool:
    if not validate_task_understanding(result):
        return False
    context = create_integration_context(result)
    assert context.message == result.message
    assert context.goal == result.goal
    assert context.task_type == result.task_type
    assert context.constraints == result.constraints
    assert (
        context.required_information
        == result.required_information
    )
    assert context.confidence == result.confidence
    return True
print("=" * 70)
print("TASK 5 - STEP 10")
print("FULL TASK UNDERSTANDING CONTRACT")
print("=" * 70)
# ------------------------------------------------------------------
# CASE 1: Python code generation
# ------------------------------------------------------------------
result = build_task_understanding(
    message="Python-এ calculator বানাও, কোনো external library ব্যবহার করবে না.",
    goal="Create a Python calculator.",
    task_type="code_generation",
    constraints=[
        "no_external_libraries",
    ],
    required_information=[
        "calculation_requirements",
        "python_requirements",
    ],
    confidence="high",
)
assert result.message
assert result.goal
assert result.task_type == "code_generation"
assert result.constraints == [
    "no_external_libraries"
]
assert result.required_information == [
    "calculation_requirements",
    "python_requirements",
]
assert result.confidence == "high"
assert check_complete_chain(result)
print()
print("CASE 1: CODE_GENERATION_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 2: Debugging
# ------------------------------------------------------------------
result = build_task_understanding(
    message="এই Python code-এ error হচ্ছে, ঠিক করে দাও.",
    goal="Fix the Python code error.",
    task_type="debugging",
    constraints=[
        "preserve_existing_function_names",
    ],
    required_information=[
        "error_message",
        "relevant_code",
        "python_version",
    ],
    confidence="high",
)
assert result.task_type == "debugging"
assert result.constraints == [
    "preserve_existing_function_names"
]
assert result.required_information == [
    "error_message",
    "relevant_code",
    "python_version",
]
assert check_complete_chain(result)
print("CASE 2: DEBUGGING_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 3: Weather / current information
# ------------------------------------------------------------------
result = build_task_understanding(
    message="আজ Noakhali-এর weather কেমন?",
    goal="Get the current weather information.",
    task_type="information_retrieval",
    constraints=[],
    required_information=[
        "location",
        "current_weather_data",
    ],
    confidence="high",
)
assert result.task_type == "information_retrieval"
assert result.required_information == [
    "location",
    "current_weather_data",
]
assert check_complete_chain(result)
print("CASE 3: INFORMATION_RETRIEVAL_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 4: Electrical calculation
# ------------------------------------------------------------------
result = build_task_understanding(
    message="12V এবং 6Ω হলে current কত?",
    goal="Calculate the electrical current.",
    task_type="calculation",
    constraints=[],
    required_information=[
        "electrical_values",
        "formula",
        "units",
        "calculation_requirements",
    ],
    confidence="high",
)
assert result.task_type == "calculation"
assert result.required_information == [
    "electrical_values",
    "formula",
    "units",
    "calculation_requirements",
]
assert check_complete_chain(result)
print("CASE 4: CALCULATION_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 5: Troubleshooting
# ------------------------------------------------------------------
result = build_task_understanding(
    message="Wi-Fi বারবার disconnect হচ্ছে.",
    goal="Troubleshoot recurring Wi-Fi disconnections.",
    task_type="troubleshooting",
    constraints=[
        "preserve_existing_network_settings",
    ],
    required_information=[
        "device_information",
        "network_information",
        "error_details",
    ],
    confidence="high",
)
assert result.task_type == "troubleshooting"
assert result.constraints == [
    "preserve_existing_network_settings"
]
assert result.required_information == [
    "device_information",
    "network_information",
    "error_details",
]
assert check_complete_chain(result)
print("CASE 5: TROUBLESHOOTING_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 6: Unknown / incomplete input
# ------------------------------------------------------------------
result = build_task_understanding(
    message="",
    goal="",
    task_type="",
    constraints=None,
    required_information=None,
    confidence="invalid",
)
assert result.message == ""
assert result.goal == ""
assert result.task_type == "unknown"
assert result.constraints == []
assert result.required_information == []
assert result.confidence == "low"
assert validate_task_understanding(result)
assert check_complete_chain(result)
print("CASE 6: UNKNOWN_INPUT_END_TO_END_OK")
# ------------------------------------------------------------------
# CASE 7: No constraints / no required information
# ------------------------------------------------------------------
result = build_task_understanding(
    message="Hello ISMAIL.",
    goal="Respond to the greeting.",
    task_type="unknown",
    confidence="medium",
)
assert result.constraints == []
assert result.required_information == []
assert result.confidence == "medium"
assert check_complete_chain(result)
print("CASE 7: OPTIONAL_FIELDS_HANDLING_OK")
# ------------------------------------------------------------------
# CASE 8: Data isolation
# ------------------------------------------------------------------
original_constraints = [
    "no_external_libraries"
]
original_information = [
    "python_requirements"
]
result = build_task_understanding(
    message="Build Python tool.",
    goal="Build the requested Python tool.",
    task_type="code_generation",
    constraints=original_constraints,
    required_information=original_information,
    confidence="high",
)
original_constraints.append(
    "changed_after_build"
)
original_information.append(
    "changed_after_build"
)
assert result.constraints == [
    "no_external_libraries"
]
assert result.required_information == [
    "python_requirements"
]
print("CASE 8: DATA_ISOLATION_OK")
# ------------------------------------------------------------------
# CASE 9: Required final structure
# ------------------------------------------------------------------
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
print("CASE 9: FINAL_STRUCTURE_OK")
# ------------------------------------------------------------------
# FINAL ASSERTIONS
# ------------------------------------------------------------------
print()
print("MESSAGE_OK: True")
print("GOAL_OK: True")
print("TASK_TYPE_OK: True")
print("CONSTRAINTS_OK: True")
print("REQUIRED_INFORMATION_OK: True")
print("CONFIDENCE_OK: True")
print("VALIDATION_OK: True")
print("INTEGRATION_OK: True")
print("DATA_ISOLATION_OK: True")
print("TASK5_STEP10_FULL_TASK_UNDERSTANDING_CONTRACT_OK")
print("=" * 70)
