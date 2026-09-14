from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class TaskStep:
    capability: str
    action: str
    reason: str
    order: int
class TaskPlanner:
    """
    Creates an ordered execution plan from detected capabilities.
    The planner only creates plans.
    It does not execute capabilities.
    Ordering is determined by:
    1. Explicit dependencies
    2. Capability priority
    3. Original input order
    """
    _CAPABILITY_PRIORITY = {
        "knowledge": 10,
        "medical": 20,
        "research": 30,
        "vision": 40,
        "programming": 50,
    }
    def create_plan(
        self,
        *,
        capabilities: list[dict] | None = None,
    ) -> list[TaskStep]:
        normalized: list[dict] = []
        for capability_info in capabilities or []:
            if not isinstance(capability_info, dict):
                continue
            capability = capability_info.get("capability")
            if not isinstance(capability, str) or not capability.strip():
                continue
            capability = capability.strip().lower()
            reason = capability_info.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                reason = f"Use the {capability} capability for this task."
            depends_on = capability_info.get("depends_on", [])
            if not isinstance(depends_on, list):
                depends_on = []
            normalized_dependencies: list[str] = []
            for dependency in depends_on:
                if not isinstance(dependency, str):
                    continue
                dependency = dependency.strip().lower()
                if dependency and dependency != capability:
                    if dependency not in normalized_dependencies:
                        normalized_dependencies.append(dependency)
            normalized.append(
                {
                    "capability": capability,
                    "reason": reason,
                    "depends_on": normalized_dependencies,
                    "input_order": len(normalized),
                }
            )
        ordered = self._resolve_dependencies(normalized)
        plan: list[TaskStep] = []
        for item in ordered:
            capability = item["capability"]
            plan.append(
                TaskStep(
                    capability=capability,
                    action=self._default_action(capability),
                    reason=item["reason"],
                    order=len(plan) + 1,
                )
            )
        return plan
    def _resolve_dependencies(self, items: list[dict]) -> list[dict]:
        if not items:
            return []
        by_capability: dict[str, dict] = {}
        for item in items:
            by_capability.setdefault(item["capability"], item)
        result: list[dict] = []
        visiting: set[str] = set()
        visited: set[str] = set()
        def visit(capability: str) -> None:
            if capability in visited:
                return
            if capability in visiting:
                raise ValueError(
                    f"Circular task dependency detected: {capability}"
                )
            item = by_capability.get(capability)
            if item is None:
                return
            visiting.add(capability)
            dependencies = sorted(
                item["depends_on"],
                key=lambda dependency: (
                    self._priority(dependency),
                    by_capability.get(
                        dependency,
                        {"input_order": float("inf")},
                    )["input_order"],
                ),
            )
            for dependency in dependencies:
                visit(dependency)
            visiting.remove(capability)
            visited.add(capability)
            result.append(item)
        capabilities = sorted(
            by_capability,
            key=lambda capability: (
                self._priority(capability),
                by_capability[capability]["input_order"],
            ),
        )
        for capability in capabilities:
            visit(capability)
        return result
    @classmethod
    def _priority(cls, capability: str) -> int:
        return cls._CAPABILITY_PRIORITY.get(capability, 100)
    @staticmethod
    def _default_action(capability: str) -> str:
        actions = {
            "programming": "analyze_or_execute",
            "medical": "assess",
            "research": "research",
            "knowledge": "lookup",
            "vision": "assess",
        }
        return actions.get(capability, "process")
