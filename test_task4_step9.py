from backend.task_planner import TaskPlanner
planner = TaskPlanner()
plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Build the program.",
            "depends_on": [
                " mathematics ",
                "mathematics",
                "",
                "   ",
                123,
                None,
                "MATHEMATICS",
            ],
        },
        {
            "capability": "mathematics",
            "reason": "Perform the calculation.",
            "depends_on": "not-a-list",
        },
    ]
)
actual = [step.capability for step in plan]
print("PLAN:", [
    (step.capability, step.order)
    for step in plan
])
assert actual == ["mathematics", "programming"]
assert plan[0].order == 1
assert plan[1].order == 2
assert plan[0].capability == "mathematics"
assert plan[1].capability == "programming"
print("TASK4_STEP9_MALFORMED_DEPENDENCY_OK")
