from backend.capabilities.capability_registry import CapabilityRegistry
from backend.capabilities.capability_selector import CapabilitySelector
from backend.task_planner import TaskPlanner
registry = CapabilityRegistry()
selector = CapabilitySelector(registry)
planner = TaskPlanner()
selections = selector.select(
    intent="programming",
    route="research",
    domains=[],
)
selected_names = {selection.capability for selection in selections}
assert selected_names == {"programming", "research"}
planner_input = [
    {
        "capability": selection.capability,
        "reason": selection.reason,
    }
    for selection in selections
]
for item in planner_input:
    if item["capability"] == "programming":
        item["depends_on"] = ["research"]
plan = planner.create_plan(capabilities=planner_input)
assert [step.capability for step in plan] == [
    "research",
    "programming",
]
assert plan[0].order == 1
assert plan[1].order == 2
assert plan[0].action == "research"
assert plan[1].action == "analyze_or_execute"
print("SELECTOR_OUTPUT:", selections)
print("PLANNER_INPUT:", planner_input)
print("PLANNER_OUTPUT:", plan)
print("TASK4_STEP17_DEPENDENCY_BOUNDARY_OK")
