from backend.ai_engine import AIEngine
engine = AIEngine()
research = engine.web_research
assert hasattr(research, "research")
assert callable(research.research)
print("RESEARCH_METHOD:", research.research.__name__)
result = research.research(
    "What is Python?",
    max_sources=1,
)
assert isinstance(result, list)
print("RESULT_TYPE:", type(result).__name__)
print("RESULT_COUNT:", len(result))
if result:
    first = result[0]
    print("FIRST_RESULT_TYPE:", type(first).__name__)
    required_fields = [
        "title",
        "url",
        "source",
        "snippet",
        "content",
        "reliability_score",
        "reliability_level",
        "verification_status",
    ]
    for field in required_fields:
        assert hasattr(first, field), f"Missing field: {field}"
    print("RESEARCH_FIELDS_OK:", required_fields)
print("TASK4_STEP44_RESEARCH_EXECUTION_BOUNDARY_OK")
