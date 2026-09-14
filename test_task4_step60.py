from backend.ai_engine import AIEngine
from backend.capability_orchestrator import CapabilityOrchestrator
from backend.task_planner import TaskPlanner
engine = AIEngine()
assert hasattr(engine, "task_planner")
assert isinstance(engine.task_planner, TaskPlanner)
orchestrator = CapabilityOrchestrator()
assert isinstance(
    orchestrator,
    CapabilityOrchestrator,
)
question_info = engine.understand_question(
    "Write a Python program to calculate factorial."
)
assert "capabilities" in question_info
assert "task_plan" in question_info
task_plan = question_info["task_plan"]
assert isinstance(task_plan, list)
assert len(task_plan) >= 1
print(
    "TASK_PLANNER_TYPE:",
    type(engine.task_planner).__name__,
)
print(
    "ORCHESTRATOR_TYPE:",
    type(orchestrator).__name__,
)
print(
    "CAPABILITIES:",
    question_info["capabilities"],
)
print(
    "TASK_PLAN:",
    [
        (step.capability, step.action, step.order)
        for step in task_plan
    ],
)
print("TASK4_STEP60_PRODUCTION_INTEGRATION_BOUNDARY_OK")
