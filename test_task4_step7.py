from backend.task_planner import TaskPlanner
planner = TaskPlanner()
plan = planner.create_plan(
    capabilities=[
        {
            "capability": "programming",
            "reason": "Build a Python calculator for the calculation.",
            "depends_on": ["mathematics"],
        },
        {
            "capability": "verification",
            "reason": "Verify the final calculation and program result.",
            "depends_on": ["programming"],
        },
        {
            "capability": "mathematics",
            "reason": "Perform the required mathematical calculation.",
        },
        {
            "capability": "electronics",
            "reason": "Analyze the electrical/electronics part of the task.",
            "depends_on": ["mathematics"],
        },
    ]
)
actual = [step.capability for step in plan]
print("PLAN:", [
    (step.capability, step.order)
    for step in plan
])
assert set(actual) == {
    "mathematics",
    "electronics",
    "programming",
    "verification",
}
position = {
    capability: index
    for index, capability in enumerate(actual)
}
assert position["mathematics"] < position["programming"]
assert position["mathematics"] < position["electronics"]
assert position["programming"] < position["verification"]
assert [step.order for step in plan] == [1, 2, 3, 4]
print("TASK4_STEP7_COMPLEX_PLAN_OK")
