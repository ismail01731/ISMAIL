from dataclasses import dataclass, field
@dataclass(frozen=True)
class TaskUnderstanding:
    message: str
    goal: str
    task_type: str
    constraints: list[str] = field(default_factory=list)
    required_information: list[str] = field(default_factory=list)
    confidence: str = "medium"
@dataclass(frozen=True)
class IntegrationContext:
    message: str
    goal: str
    task_type: str
    constraints: list[str]
    required_information: list[str]
    confidence: str
@dataclass(frozen=True)
class IntentContext:
    intent: str
    route: str
    confidence: str
    task_understanding: IntegrationContext
@dataclass(frozen=True)
class DomainContext:
    domains: list[dict]
    task_understanding: IntegrationContext
@dataclass(frozen=True)
class CapabilityContext:
    capabilities: list[dict]
    task_understanding: IntegrationContext
@dataclass(frozen=True)
class TaskPlanContext:
    plan: list[dict]
    task_understanding: IntegrationContext
def create_integration_context(
    understanding: TaskUnderstanding,
) -> IntegrationContext:
    return IntegrationContext(
        message=understanding.message,
        goal=understanding.goal,
        task_type=understanding.task_type,
        constraints=list(understanding.constraints),
        required_information=list(
            understanding.required_information
        ),
        confidence=understanding.confidence,
    )
def build_intent_context(
    understanding: TaskUnderstanding,
) -> IntentContext:
    context = create_integration_context(understanding)
    intent_map = {
        "code_generation": "programming",
        "debugging": "programming",
        "troubleshooting": "knowledge",
        "information_retrieval": "live_information",
        "calculation": "calculation",
        "unknown": "knowledge",
    }
    route_map = {
        "code_generation": "programming",
        "debugging": "programming",
        "troubleshooting": "knowledge",
        "information_retrieval": "research",
        "calculation": "calculation",
        "unknown": "knowledge",
    }
    return IntentContext(
        intent=intent_map.get(
            understanding.task_type,
            "knowledge",
        ),
        route=route_map.get(
            understanding.task_type,
            "knowledge",
        ),
        confidence=understanding.confidence,
        task_understanding=context,
    )
def build_domain_context(
    understanding: TaskUnderstanding,
) -> DomainContext:
    context = create_integration_context(understanding)
    domains = []
    if understanding.task_type in {
        "code_generation",
        "debugging",
    }:
        domains.append({
            "domain": "programming",
            "confidence": understanding.confidence,
        })
    elif understanding.task_type == "troubleshooting":
        domains.append({
            "domain": "electronics",
            "confidence": "medium",
        })
    elif understanding.task_type == "calculation":
        domains.append({
            "domain": "mathematics",
            "confidence": understanding.confidence,
        })
    elif understanding.task_type == "information_retrieval":
        domains.append({
            "domain": "research",
            "confidence": understanding.confidence,
        })
    return DomainContext(
        domains=domains,
        task_understanding=context,
    )
def build_capability_context(
    understanding: TaskUnderstanding,
) -> CapabilityContext:
    context = create_integration_context(understanding)
    capabilities = []
    if understanding.task_type in {
        "code_generation",
        "debugging",
    }:
        capabilities.append({
            "capability": "programming",
            "reason": understanding.goal,
            "confidence": understanding.confidence,
        })
    elif understanding.task_type == "information_retrieval":
        capabilities.append({
            "capability": "research",
            "reason": understanding.goal,
            "confidence": understanding.confidence,
        })
    elif understanding.task_type == "troubleshooting":
        capabilities.append({
            "capability": "knowledge",
            "reason": understanding.goal,
            "confidence": understanding.confidence,
        })
    elif understanding.task_type == "calculation":
        capabilities.append({
            "capability": "knowledge",
            "reason": understanding.goal,
            "confidence": understanding.confidence,
        })
    return CapabilityContext(
        capabilities=capabilities,
        task_understanding=context,
    )
def build_task_plan_context(
    understanding: TaskUnderstanding,
) -> TaskPlanContext:
    context = create_integration_context(understanding)
    capability_context = build_capability_context(
        understanding
    )
    plan = []
    for index, capability in enumerate(
        capability_context.capabilities,
        start=1,
    ):
        plan.append({
            "order": index,
            "capability": capability["capability"],
            "action": understanding.task_type,
            "goal": understanding.goal,
            "constraints": list(
                understanding.constraints
            ),
            "required_information": list(
                understanding.required_information
            ),
            "confidence": understanding.confidence,
        })
    return TaskPlanContext(
        plan=plan,
        task_understanding=context,
    )
print("=" * 70)
print("TASK 5 - STEP 9")
print("CONTRACT INTEGRATION BOUNDARY")
print("=" * 70)
# CASE 1: Programming task
understanding = TaskUnderstanding(
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
intent = build_intent_context(understanding)
domain = build_domain_context(understanding)
capability = build_capability_context(understanding)
plan = build_task_plan_context(understanding)
assert intent.intent == "programming"
assert intent.route == "programming"
assert domain.domains[0]["domain"] == "programming"
assert capability.capabilities[0]["capability"] == "programming"
assert plan.plan[0]["goal"] == understanding.goal
assert plan.plan[0]["constraints"] == understanding.constraints
assert (
    plan.plan[0]["required_information"]
    == understanding.required_information
)
print()
print("CASE 1: PROGRAMMING_CHAIN_OK")
# CASE 2: Weather / information retrieval
understanding = TaskUnderstanding(
    message="বাংলাদেশের আজকের আবহাওয়া কেমন?",
    goal="Get the current weather information.",
    task_type="information_retrieval",
    constraints=[],
    required_information=[
        "location",
        "current_weather_data",
    ],
    confidence="high",
)
intent = build_intent_context(understanding)
domain = build_domain_context(understanding)
capability = build_capability_context(understanding)
plan = build_task_plan_context(understanding)
assert intent.intent == "live_information"
assert intent.route == "research"
assert domain.domains[0]["domain"] == "research"
assert capability.capabilities[0]["capability"] == "research"
assert plan.plan[0]["goal"] == understanding.goal
assert plan.plan[0]["required_information"] == [
    "location",
    "current_weather_data",
]
print("CASE 2: RESEARCH_CHAIN_OK")
# CASE 3: Calculation
understanding = TaskUnderstanding(
    message="100/4 কত?",
    goal="Calculate the requested expression.",
    task_type="calculation",
    constraints=[],
    required_information=[
        "calculation_requirements",
    ],
    confidence="high",
)
intent = build_intent_context(understanding)
domain = build_domain_context(understanding)
capability = build_capability_context(understanding)
plan = build_task_plan_context(understanding)
assert intent.intent == "calculation"
assert intent.route == "calculation"
assert domain.domains[0]["domain"] == "mathematics"
assert capability.capabilities[0]["capability"] == "knowledge"
print("CASE 3: CALCULATION_CHAIN_OK")
# CASE 4: Constraints preserved
understanding = TaskUnderstanding(
    message="Existing function ঠিক করো.",
    goal="Fix the existing function.",
    task_type="debugging",
    constraints=[
        "preserve_existing_function_names",
        "no_external_libraries",
    ],
    required_information=[
        "error_message",
        "relevant_code",
        "python_version",
    ],
    confidence="high",
)
plan = build_task_plan_context(understanding)
assert plan.plan[0]["constraints"] == [
    "preserve_existing_function_names",
    "no_external_libraries",
]
assert plan.plan[0]["required_information"] == [
    "error_message",
    "relevant_code",
    "python_version",
]
print("CASE 4: CONSTRAINT_INFORMATION_PRESERVATION_OK")
# CASE 5: Confidence preserved through all layers
understanding = TaskUnderstanding(
    message="Test request",
    goal="Handle the request.",
    task_type="code_generation",
    confidence="medium",
)
intent = build_intent_context(understanding)
domain = build_domain_context(understanding)
capability = build_capability_context(understanding)
plan = build_task_plan_context(understanding)
assert intent.confidence == "medium"
assert domain.domains[0]["confidence"] == "medium"
assert capability.capabilities[0]["confidence"] == "medium"
assert plan.plan[0]["confidence"] == "medium"
print("CASE 5: CONFIDENCE_PRESERVATION_OK")
# CASE 6: Input list isolation
understanding = TaskUnderstanding(
    message="Build something.",
    goal="Build the requested system.",
    task_type="code_generation",
    constraints=["original_constraint"],
    required_information=["original_information"],
    confidence="high",
)
plan = build_task_plan_context(understanding)
plan.plan[0]["constraints"].append(
    "new_constraint"
)
plan.plan[0]["required_information"].append(
    "new_information"
)
assert understanding.constraints == [
    "original_constraint"
]
assert understanding.required_information == [
    "original_information"
]
print("CASE 6: INPUT_ISOLATION_OK")
# CASE 7: Required integration fields
required_fields = {
    "message",
    "goal",
    "task_type",
    "constraints",
    "required_information",
    "confidence",
}
assert set(
    IntegrationContext.__dataclass_fields__.keys()
) == required_fields
print("CASE 7: INTEGRATION_FIELDS_COMPLETE_OK")
print()
print("GOAL_PRESERVATION_OK: True")
print("CONSTRAINT_PRESERVATION_OK: True")
print("REQUIRED_INFORMATION_PRESERVATION_OK: True")
print("CONFIDENCE_PRESERVATION_OK: True")
print("TASK5_STEP9_CONTRACT_INTEGRATION_BOUNDARY_OK")
print("=" * 70)
