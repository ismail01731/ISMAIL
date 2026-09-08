from backend.ai_engine import AIEngine
ai = AIEngine()
tests = [
    "পাইথন কি?",
    "ঢাকায় এখন আবহাওয়া কেমন?",
    "হ্যালো, কেমন আছো?",
]
for message in tests:
    result = ai.understand_question(message)
    print("\nMESSAGE:", message)
    print("RESULT:", result)


from backend.ai_engine import AIEngine

ai = AIEngine()

tests = [
    "Python কি?",
    "Python শেখাও",
    "YouTube খুলে দাও",
    "আজকের আবহাওয়া কেমন?",
    "আজকের খবর দেখাও",
    "একটা Python code লিখে দাও",
    "Hello",
]


"একটা Python code লিখে দাও",
"YouTube খুলে দাও",

for message in tests:
    result = ai.understand_question(message)

    print("\nMESSAGE:", message)

    print(
        "INTENT:",
        result["intent"],
    )
    print(
        "ROUTE:",
        result["route"],
    )
    print("INPUT TYPE:", result["input_type"])
    print(
        "CONFIDENCE:",
        result["confidence"],
    )
    print(
        "MATCHES:",
        result["matches"],
    )