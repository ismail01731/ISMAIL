from backend.task_planner import TaskPlanner, TaskStep
def test_empty_capabilities():
    planner = TaskPlanner()
    assert planner.create_plan() == []
def test_valid_capabilities():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "programming", "reason": "Programming task."},
            {"capability": "medical", "reason": "Medical task."},
            {"capability": "research", "reason": "Current information."},
        ]
    )
    assert len(plan) == 3
    # Priority order: medical -> research -> programming
    assert plan[0] == TaskStep(
        capability="medical",
        action="assess",
        reason="Medical task.",
        order=1,
    )
    assert plan[1] == TaskStep(
        capability="research",
        action="research",
        reason="Current information.",
        order=2,
    )
    assert plan[2] == TaskStep(
        capability="programming",
        action="analyze_or_execute",
        reason="Programming task.",
        order=3,
    )
def test_invalid_entries_are_skipped():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            None,
            {"capability": "programming"},
            {},
            {"capability": ""},
            {"capability": "   "},
            {"capability": "research"},
        ]
    )
    assert len(plan) == 2
    assert {step.capability for step in plan} == {
        "programming",
        "research",
    }
    assert all(isinstance(step, TaskStep) for step in plan)
def test_capability_normalization():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "  Programming  "},
            {"capability": "RESEARCH"},
        ]
    )
    # research has higher priority than programming
    assert plan[0].capability == "research"
    assert plan[0].action == "research"
    assert plan[1].capability == "programming"
    assert plan[1].action == "analyze_or_execute"
def test_reason_fallback():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "programming"},
        ]
    )
    assert plan[0].reason == (
        "Use the programming capability for this task."
    )
def test_unknown_capability():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "unknown_capability"},
        ]
    )
    assert len(plan) == 1
    assert plan[0].capability == "unknown_capability"
    assert plan[0].action == "process"
def test_order_is_sequential():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "programming"},
            {"capability": "medical"},
            {"capability": "research"},
            {"capability": "vision"},
        ]
    )
    assert [step.order for step in plan] == [1, 2, 3, 4]
    # Priority order:
    # medical -> research -> vision -> programming
    assert [step.capability for step in plan] == [
        "medical",
        "research",
        "vision",
        "programming",
    ]
def test_priority_order():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "programming"},
            {"capability": "research"},
            {"capability": "knowledge"},
            {"capability": "medical"},
        ]
    )
    assert [step.capability for step in plan] == [
        "knowledge",
        "medical",
        "research",
        "programming",
    ]
def test_same_priority_preserves_input_order():
    planner = TaskPlanner()
    plan = planner.create_plan(
        capabilities=[
            {"capability": "unknown_a"},
            {"capability": "unknown_b"},
            {"capability": "unknown_c"},
        ]
    )
    assert [step.capability for step in plan] == [
        "unknown_a",
        "unknown_b",
        "unknown_c",
    ]
if __name__ == "__main__":
    test_empty_capabilities()
    test_valid_capabilities()
    test_invalid_entries_are_skipped()
    test_capability_normalization()
    test_reason_fallback()
    test_unknown_capability()
    test_order_is_sequential()
    test_priority_order()
    test_same_priority_preserves_input_order()
    print("TASK4_PLANNER_REGRESSION_OK")
