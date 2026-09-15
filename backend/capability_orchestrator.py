from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any, Callable
from backend.task_planner import TaskStep
@dataclass(frozen=True)
class CapabilityExecutionContext:
    message: str = ""
    intent: str = ""
    domains: list[dict[str, Any]] | None = None
    source_decision: dict[str, Any] | None = None
    programming_language: dict[str, Any] | None = None
    file_context: str = ""
    conversation_context: Any = None
    previous_results: list["CapabilityExecutionResult"] | None = None
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
    Execution results are automatically passed forward through
    CapabilityExecutionContext so later capabilities can use
    earlier capability results.
    """
    def execute(
        self,
        plan: list[TaskStep],
        executor: Callable[..., CapabilityExecutionResult],
        context: CapabilityExecutionContext | None = None,
    ) -> list[CapabilityExecutionResult]:
        results: list[CapabilityExecutionResult] = []
        for step in plan:
            if not isinstance(step, TaskStep):
                continue
            if context is None:
                result = executor(step)
            else:
                execution_context = replace(
                    context,
                    previous_results=list(results),
                )
                result = executor(step, execution_context)
            if not isinstance(result, CapabilityExecutionResult):
                raise TypeError(
                    "Capability executor must return "
                    "CapabilityExecutionResult."
                )
            results.append(result)
        return results
