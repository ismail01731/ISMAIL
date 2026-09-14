from backend.capabilities.capability_registry import CapabilityRegistry
from backend.capabilities.capability_selector import CapabilitySelector
from backend.task_planner import TaskPlanner, TaskStep
registry = CapabilityRegistry()
selector = CapabilitySelector(registry)
planner = TaskPlanner()
selections = selector.select(
    intent="live_information",
    domains=[
        {"domain": "medical"},
    ],
)
assert len(selections) == 2
selected_names = {selection.capability for selection in selections}
assert selected_names == {"medical", "research"}
planner_input = [
    {
        "capability": selection.capability,
        "reason": selection.reason,
    }
    for selection in selections
]
plan = planner.create_plan(capabilities=planner_input)
assert len(plan) == 2
assert all(isinstance(step, TaskStep) for step in plan)
planned_names = {step.capability for step in plan}
assert planned_names == {"medical", "research"}
assert all(step.order >= 1 for step in plan)
assert [step.order for step in plan] == [1, 2]
assert plan[0].capability == "medical"
assert plan[0].action == "assess"
assert plan[1].capability == "research"
assert plan[1].action == "research"
print("SELECTOR_OUTPUT:", selections)
print("PLANNER_OUTPUT:", plan)
print("TASK4_STEP16_MULTI_CAPABILITY_BOUNDARY_OK")
