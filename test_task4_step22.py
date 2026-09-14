from backend.ai_engine import AIEngine
from backend.task_planner import TaskStep
engine = AIEngine()
result = engine.understand_question(
    "Write a Python program and use current information if needed."
)
assert isinstance(result, dict)
assert "intent" in result
assert "route" in result
assert "domains" in result
assert "capabilities" in result
assert isinstance(result["domains"], list)
assert isinstance(result["capabilities"], list)
for capability in result["capabilities"]:
    assert isinstance(capability, dict)
    assert isinstance(capability.get("capability"), str)
    assert isinstance(capability.get("reason"), str)
    assert isinstance(capability.get("confidence"), str)
print("INTENT:", result.get("intent"))
print("ROUTE:", result.get("route"))
print("DOMAINS:", result["domains"])
print("CAPABILITIES:", result["capabilities"])
print("TASK4_STEP22_AIENGINE_BOUNDARY_BASELINE_OK")
