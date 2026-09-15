from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
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
    intent: str = ""
    domains: list[dict[str, Any]] = field(default_factory=list)
    task_type: str = ""
    constraints: list[str] = field(default_factory=list)
    required_information: list[str] = field(
        default_factory=list
    )
    subtasks: list[str] = field(default_factory=list)
    freshness_required: bool = False
    risk_level: str = "low"
    required_tools: list[str] = field(default_factory=list)
    required_language: str = ""
    expected_output: str = ""
    confidence: str = "medium"
class TaskUnderstandingBuilder:
    """
    Builds structured task understanding from existing
    ISMAIL detection results.
    This layer does not perform intent, domain, capability,
    or task-plan detection itself.
    """
    def build(
        self,
        *,
        message: str,
        question_info: dict[str, Any],
    ) -> TaskUnderstanding:
        normalized_message = (
            message.strip()
            if isinstance(message, str)
            else ""
        )
        intent = str(
            question_info.get("intent", "")
        ).strip().lower()
        route = str(
            question_info.get("route", "")
        ).strip().lower()
        domains = question_info.get("domains", [])
        if not isinstance(domains, list):
            domains = []
        confidence = str(
            question_info.get("confidence", "medium")
        ).strip().lower()
        if confidence not in VALID_CONFIDENCE:
            confidence = "low"
        task_type = self._task_type_from_existing_route(
            intent=intent,
            route=route,
            message=normalized_message,
        )
        goal = self._goal_from_existing_context(
            message=normalized_message,
            intent=intent,
            route=route,
        )
        constraints = self._extract_constraints(
            question_info
        )
        required_information = (
            self._extract_required_information(
                question_info
            )
        )
        subtasks = self._build_subtasks(
            message=normalized_message,
            task_type=task_type,
            goal=goal,
        )
        freshness_required = self._extract_freshness_requirement(
            question_info
        )
        risk_level = self._extract_risk_level(
            question_info
        )
        return TaskUnderstanding(
            message=normalized_message,
            goal=goal,
            intent=intent,
            domains=domains,
            task_type=task_type,
            constraints=constraints,
            required_information=required_information,
            subtasks=subtasks,
            freshness_required=freshness_required,
            risk_level=risk_level,
            confidence=confidence,
        )
    @staticmethod
    def _build_subtasks(
        *,
        message: str,
        task_type: str,
        goal: str,
    ) -> list[str]:
        if not message:
            return []
        if task_type == "debugging":
            return [
                "identify_the_problem",
                "inspect_relevant_code_or_error",
                "determine_the_cause",
                "propose_a_fix",
                "verify_the_fix",
            ]
        if task_type == "code_generation":
            return [
                "understand_requirements",
                "design_the_solution",
                "generate_code",
                "check_for_errors",
            ]
        if task_type == "troubleshooting":
            return [
                "identify_the_problem",
                "collect_relevant_information",
                "determine_the_cause",
                "propose_a_solution",
                "verify_the_solution",
            ]
        if task_type == "calculation":
            return [
                "identify_values_and_units",
                "select_the_formula",
                "perform_the_calculation",
                "verify_the_result",
            ]
        if task_type == "information_retrieval":
            return [
                "identify_required_information",
                "select_an_appropriate_source",
                "retrieve_the_information",
                "verify_relevant_details",
            ]
        if goal:
            return [
                "understand_the_request",
                "determine_the_required_action",
            ]
        return []
    @staticmethod
    def _extract_freshness_requirement(
        question_info: dict[str, Any],
    ) -> bool:
        freshness = question_info.get(
            "research_freshness",
            {}
        )
        if not isinstance(freshness, dict):
            return False
        return bool(
            freshness.get("freshness_required", False)
        )
    @staticmethod
    def _extract_risk_level(
        question_info: dict[str, Any],
    ) -> str:
        risk_level = str(
            question_info.get("risk_level", "low")
        ).strip().lower()
        if risk_level in {"low", "medium", "high"}:
            return risk_level
        return "low"
    @staticmethod
    def _task_type_from_existing_route(
        *,
        intent: str,
        route: str,
        message: str = "",
    ) -> str:
        text = (
            message.strip().lower()
            if isinstance(message, str)
            else ""
        )

        if not text:
            return "unknown"

        programming_terms = (
            "python",
            "javascript",
            "java",
            "typescript",
            "c++",
            "cpp",
            "c#",
            "c sharp",
            "go",
            "golang",
            "rust",
            "php",
            "ruby",
            "kotlin",
            "swift",
            "sql",
            "bash",
            "html",
            "css",
            "programming",
            "program",
            "code",
            "coding",
            "function",
            "script",
            "class",
            "api",
            "algorithm",
            "website",
            "web site",
            "web development",
            "frontend",
            "backend",
            "app",
            "application",
            "software",
            "calculator",
            "sorting algorithm",
            "????????",
            "?????????",
            "????",
            "?????",
            "???",
            "?????????",
            "?????",
            "????????????",
        )

        debugging_terms = (
            "error",
            "bug",
            "debug",
            "exception",
            "traceback",
            "crash",
            "fix",
            "ঠিক করে দাও",
            "সমস্যা ঠিক",
        )

        troubleshooting_terms = (
            "wi-fi",
            "wifi",
            "internet",
            "network",
            "disconnect",
            "connection",
            "router",
            "connect হচ্ছে না",
            "বারবার disconnect",
        )

        if any(term in text for term in debugging_terms):
            if any(term in text for term in programming_terms):
                return "debugging"

        if any(term in text for term in programming_terms):
            return "code_generation"

        if any(term in text for term in troubleshooting_terms):
            return "troubleshooting"
        if intent == "conversation":
            return "unknown"

        mapping = {
            "programming": "code_generation",
            "calculation": "calculation",
            "live_information": "information_retrieval",
            "research": "information_retrieval",
            "knowledge": "information_retrieval",
        }

        if route in mapping:
            return mapping[route]

        if intent in mapping:
            return mapping[intent]

        return "unknown"
    @staticmethod
    def _goal_from_existing_context(
        *,
        message: str,
        intent: str,
        route: str,
    ) -> str:
        if not message:
            return ""
        if intent == "conversation":
            return ""

        text = message.strip().lower()

        if route == "calculation":
            return "Calculate the requested expression."

        if route in {
            "research",
            "live",
        } or intent == "live_information":
            return "Get the requested current information."

        debugging_terms = (
            "error",
            "bug",
            "debug",
            "exception",
            "traceback",
            "crash",
            "ঠিক করে দাও",
            "সমস্যা ঠিক",
        )

        programming_terms = (
            "python",
            "javascript",
            "java",
            "typescript",
            "c++",
            "cpp",
            "c#",
            "c sharp",
            "go",
            "golang",
            "rust",
            "php",
            "ruby",
            "kotlin",
            "swift",
            "sql",
            "bash",
            "html",
            "css",
            "programming",
            "program",
            "code",
            "coding",
            "function",
            "script",
            "class",
            "api",
            "algorithm",
            "website",
            "web site",
            "web development",
            "frontend",
            "backend",
            "app",
            "application",
            "software",
            "calculator",
            "sorting algorithm",
            "????????",
            "?????????",
            "????",
            "?????",
            "???",
            "?????????",
            "?????",
            "????????????",
        )

        troubleshooting_terms = (
            "wi-fi",
            "wifi",
            "internet",
            "network",
            "disconnect",
            "connection",
            "router",
            "connect হচ্ছে না",
            "বারবার disconnect",
        )

        if any(term in text for term in debugging_terms):
            if any(term in text for term in programming_terms):
                return "Troubleshoot and fix the reported programming error."

        if any(term in text for term in troubleshooting_terms):
            return "Troubleshoot the reported connectivity problem."

        if any(term in text for term in programming_terms):
            return "Create or provide the requested programming solution."

        if route == "programming":
            return "Complete the requested programming task."

        if route == "knowledge":
            return "Provide the requested information."

        return message
    @staticmethod
    def _extract_constraints(
        question_info: dict[str, Any],
    ) -> list[str]:

        message = question_info.get("normalized_question", "")
        text = (
            message.strip()
            if isinstance(message, str)
            else ""
        )
        lower = text.lower()

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
            constraints.append(
                "preserve_existing_function_names"
            )

        if (
            "20 lines" in lower
            or "20 লাইনের" in lower
        ):
            constraints.append("maximum_20_lines")

        return constraints

    @staticmethod
    def _extract_required_information(
        question_info: dict[str, Any],
    ) -> list[str]:

        message = question_info.get("normalized_question", "")
        text = (
            message.strip()
            if isinstance(message, str)
            else ""
        )
        lower = text.lower()

        if not text:
            return []

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

        return required




