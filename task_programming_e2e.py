from backend.ai_engine import AIEngine
import json
engine = AIEngine()
tests = [
    ("Generate", "Write Python code to add two numbers"),
    ("Analyze", "analyze this python code: def add(a, b): return a + b"),
    ("Debug", "Fix this Python error: SyntaxError: invalid syntax"),
    ("Execute", "run this python code"),
    ("Test", "test this python code"),
    ("Documentation", "Python documentation for functions"),
    ("Version", "Python version compatibility check"),
]
print()
print("AI ENGINE:", type(engine).__name__)
print("PROGRAMMING INTELLIGENCE:", type(engine.programming_intelligence).__name__)
print()
for name, message in tests:
    print("=" * 70)
    print("TEST:", name)
    print("INPUT:", message)
    try:
        result = engine.generate(message)
        print("RAW TYPE:", type(result).__name__)
        if isinstance(result, str):
            try:
                data = json.loads(result)
                print("TYPE:", data.get("type"))
                print("ACTION:", data.get("action"))
                print("SUCCESS:", data.get("success"))
                print("REASON:", data.get("reason"))
                print("RESULT TYPE:", type(data.get("result")).__name__)
            except Exception:
                print("RESPONSE:", result[:1000])
        else:
            print("RESPONSE:", str(result)[:1000])
    except Exception as exc:
        print("ERROR:", type(exc).__name__, str(exc))
print()
print("=" * 70)
print("===== FULL E2E TEST FINISHED =====")
