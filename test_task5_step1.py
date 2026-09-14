from backend.ai_engine import AIEngine
engine = AIEngine()
test_cases = [
    "Python-এ এই error কেন হচ্ছে?",
    "আমার ফোনে Wi-Fi বারবার disconnect হচ্ছে, কী করব?",
    "আজকের বাংলাদেশের weather কেমন?",
    "এই electrical calculation করে একটা Python calculator বানিয়ে দাও.",
    "Python-এ দুইটা সংখ্যার যোগ করার function লিখে দাও.",
]
print("=" * 70)
print("TASK 5 - STEP 1")
print("CURRENT TASK UNDERSTANDING BASELINE")
print("=" * 70)
for index, message in enumerate(test_cases, start=1):
    print()
    print(f"CASE {index}")
    print("QUESTION:", message)
    info = engine.understand_question(message)
    print("INTENT:", info.get("intent"))
    print("ROUTE:", info.get("route"))
    print("DOMAINS:", info.get("domains"))
    print("CAPABILITIES:", info.get("capabilities"))
    print("TASK_PLAN:", info.get("task_plan"))
    assert isinstance(info, dict)
    assert "intent" in info
    assert "route" in info
    assert "domains" in info
    assert "capabilities" in info
    assert "task_plan" in info
print()
print("=" * 70)
print("TASK5_STEP1_CURRENT_UNDERSTANDING_BASELINE_OK")
print("=" * 70)
