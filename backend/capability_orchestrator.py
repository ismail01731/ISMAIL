from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from backend.task_planner import TaskStep
@dataclass(frozen=True)
class CapabilityExecutionResult:
    capability: str
    action: str
    success: bool
    result: Any = None
    reason: str = ""
    order: int = 0
class CapabilityOrchestrator:
    """
    Executes an ordered TaskPlanner plan.
    The orchestrator coordinates execution only.
    Individual capability implementations remain responsible
    for their own domain-specific behavior.
    """
    def execute(
        self,
        plan: list[TaskStep],
        executor: Callable[[TaskStep], CapabilityExecutionResult],
    ) -> list[CapabilityExecutionResult]:
        results: list[CapabilityExecutionResult] = []
        for step in plan:
            if not isinstance(step, TaskStep):
                continue
            result = executor(step)
            if not isinstance(result, CapabilityExecutionResult):
                raise TypeError(
                    "Capability executor must return "
                    "CapabilityExecutionResult."
                )
            results.append(result)
        return results
