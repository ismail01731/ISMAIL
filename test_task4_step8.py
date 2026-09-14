from dataclasses import is_dataclass
from backend.task_planner import TaskPlanner, TaskStep
planner = TaskPlanner()
plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Build the calculator.",
            "depends_on": ["mathematics"],
        },
        {
            "capability": "mathematics",
            "reason": "Perform the calculation.",
        },
    ]
)
assert isinstance(plan, list)
assert len(plan) == 2
for step in plan:
    assert isinstance(step, TaskStep)
    assert is_dataclass(step)
    assert isinstance(step.capability, str)
    assert step.capability.strip()
    assert isinstance(step.action, str)
    assert step.action.strip()
    assert isinstance(step.reason, str)
    assert step.reason.strip()
    assert isinstance(step.order, int)
    assert step.order >= 1
assert [step.order for step in plan] == [1, 2]
assert plan[0].capability == "mathematics"
assert plan[0].action == "process"
assert plan[1].capability == "programming"
assert plan[1].action == "analyze_or_execute"
print("TASK4_STEP8_OUTPUT_CONTRACT_OK")
