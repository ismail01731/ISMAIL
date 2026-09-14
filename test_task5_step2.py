from dataclasses import fields
from backend.ai_engine import AIEngine
engine = AIEngine()
info = engine.understand_question(
    "Python-এ দুইটা সংখ্যার যোগ করার function লিখে দাও."
)
print("=" * 70)
print("TASK 5 - STEP 2")
print("TASK UNDERSTANDING CONTRACT BASELINE")
print("=" * 70)
print()
print("CURRENT_KEYS:")
for key in sorted(info.keys()):
    print(" -", key)
# Existing understanding contract must remain intact.
required_existing_keys = {
    "intent",
    "route",
    "domains",
    "capabilities",
    "task_plan",
}
for key in required_existing_keys:
    assert key in info, f"Missing existing key: {key}"
assert isinstance(info["domains"], list)
assert isinstance(info["capabilities"], list)
assert isinstance(info["task_plan"], list)
# Candidate Task 5 contract.
candidate_fields = [
    "goal",
    "task_type",
    "required_information",
    "constraints",
    "freshness_required",
    "risk_level",
    "required_tools",
    "required_language",
    "multi_capability",
]
print()
print("CANDIDATE_TASK_FIELDS:")
for field_name in candidate_fields:
    print(" -", field_name)
print()
print("EXISTING_CONTRACT_OK: True")
print("CANDIDATE_FIELDS_DEFINED: True")
print("TASK5_STEP2_TASK_UNDERSTANDING_CONTRACT_OK")
print("=" * 70)
