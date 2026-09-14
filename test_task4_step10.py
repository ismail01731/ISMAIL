from backend.task_planner import TaskPlanner
planner = TaskPlanner()
plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "First programming request.",
        },
        {
            "capability": "mathematics",
            "reason": "Perform calculation.",
        },
        {
            "capability": "programming",
            "reason": "Second programming request.",
        },
    ]
)
print("PLAN:", [
    (step.capability, step.reason, step.order)
    for step in plan
])
# Duplicate capability is collapsed.
assert len(plan) == 2
# Current planner priority puts programming (50)
# before unknown capability mathematics (100).
assert [step.capability for step in plan] == [
    "programming",
    "mathematics",
]
# First occurrence of duplicate programming is preserved.
assert plan[0].reason == "First programming request."
assert plan[1].reason == "Perform calculation."
assert [step.order for step in plan] == [1, 2]
print("TASK4_STEP10_DUPLICATE_CAPABILITY_OK")
