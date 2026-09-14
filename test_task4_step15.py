from backend.capabilities.capability_registry import CapabilityRegistry
from backend.capabilities.capability_selector import CapabilitySelector
from backend.task_planner import TaskPlanner, TaskStep
registry = CapabilityRegistry()
selector = CapabilitySelector(registry)
planner = TaskPlanner()
selections = selector.select(
    intent="programming",
    domains=[],
)
assert selections
assert selections[0].capability == "programming"
assert isinstance(selections[0].reason, str)
assert isinstance(selections[0].confidence, str)
planner_input = [
    {
        "capability": selection.capability,
        "reason": selection.reason,
    }
    for selection in selections
]
plan = planner.create_plan(capabilities=planner_input)
assert isinstance(plan, list)
assert len(plan) == 1
assert isinstance(plan[0], TaskStep)
assert plan[0].capability == "programming"
assert plan[0].action == "analyze_or_execute"
assert plan[0].reason == selections[0].reason
assert plan[0].order == 1
print("SELECTOR_OUTPUT:", selections)
print("PLANNER_OUTPUT:", plan)
print("TASK4_STEP15_SELECTOR_PLANNER_BOUNDARY_OK")
