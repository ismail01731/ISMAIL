from dataclasses import dataclass
from backend.task4_answer_synthesis import (
    Task4AnswerSynthesisLayer,
)
@dataclass
class TestEvidence:
    title: str
    url: str
    source: str
    snippet: str
    content: str
    verification_status: str = "verified"
layer = Task4AnswerSynthesisLayer()
item1 = TestEvidence(
    title="Bangladesh Weather Today",
    url="https://weather.example.com/today",
    source="Weather Source",
    snippet="Current weather information.",
    content=(
        "Dhaka is expected to have partly cloudy weather today. "
        "Temperatures may remain around 30 degrees during the day."
    ),
)
item2 = TestEvidence(
    title="Bangladesh Weather Today",
    url="https://weather.example.com/today",
    source="Weather Source",
    snippet="Duplicate evidence.",
    content=(
        "Dhaka is expected to have partly cloudy weather today. "
        "Temperatures may remain around 30 degrees during the day."
    ),
)
item3 = TestEvidence(
    title="Bangladesh News Update",
    url="https://news.example.com/update",
    source="News Source",
    snippet="A current development.",
    content=(
        "A new development was reported in Bangladesh today. "
        "Officials provided additional information about the event."
    ),
)
original_count = 3
claims = [
    "Dhaka is expected to have partly cloudy weather today.",
    "Dhaka is expected to have partly cloudy weather today.",
    "A new development was reported in Bangladesh today.",
]
result = layer.synthesize(
    evidence=[item1, item2, item3],
    claims=claims,
)
assert len(result.evidence) == original_count
assert len(result.claims) == 2
assert len(result.answer_points) == 2
assert result.source_count == 2
assert result.claims[0] == (
    "Dhaka is expected to have partly cloudy weather today."
)
assert result.claims[1] == (
    "A new development was reported in Bangladesh today."
)
empty = layer.synthesize()
assert empty.evidence == []
assert empty.claims == []
assert empty.answer_points == []
assert empty.source_count == 0
print("EVIDENCE_INPUT:", original_count)
print("EVIDENCE_OUTPUT:", len(result.evidence))
print("CLAIM_INPUT:", len(claims))
print("CLAIM_OUTPUT:", len(result.claims))
print("ANSWER_POINTS:", len(result.answer_points))
print("SOURCE_COUNT:", result.source_count)
print("EMPTY_TEST: PASS")
print("TASK 4 UNIT TEST: PASS")
