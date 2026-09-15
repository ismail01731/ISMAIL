import sys
from pathlib import Path
# Make backend root importable when running this file directly.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
import json
from intelligence.adapter import ExistingAIAdapter
from intelligence.answer import FutureAnswerBuilder
from intelligence.orchestrator import FutureIntelligence
def fake_ai(prompt):
    return (
        "বর্তমান forecast অনুযায়ী trend upward হওয়ার "
        "সম্ভাবনা বেশি।"
    )
def test_answer_builder():
    builder = FutureAnswerBuilder()
    forecast = {
        "horizon": 30,
        "trend": {
            "direction": "upward"
        },
        "selected_model": "naive_v1",
        "expected_value": 160,
        "latest_value": 154,
        "confidence_calibration": {
            "level": "moderate"
        },
        "uncertainty": {
            "level": "moderate"
        },
        "data_quality": {
            "level": "good"
        },
        "scenarios": [
            {
                "name": "upside",
                "probability": 0.60
            },
            {
                "name": "base",
                "probability": 0.30
            },
            {
                "name": "downside",
                "probability": 0.10
            }
        ]
    }
    answer = builder.build(
        "আগামী 30 দিনে trend কোন দিকে যেতে পারে?",
        forecast,
        {
            "status": "success",
            "response": "AI reasoning"
        }
    )
    assert answer["direction"] == "upward"
    assert answer["confidence"] == "moderate"
    assert answer["uncertainty"] == "moderate"
    assert answer["guarantee"] is False
    assert "summary" in answer
    assert "warning" in answer
    assert answer["probabilities"]["upside"] == 60.0
def test_full_natural_answer_pipeline():
    system = FutureIntelligence(
        ExistingAIAdapter(
            fake_ai,
            "test_ai"
        )
    )
    result = system.analyze(
        "আগামী 30 দিনে trend কোন দিকে যেতে পারে?",
        [
            100,
            105,
            108,
            115,
            120,
            125,
            132,
            138,
            142,
            145,
            150,
            154,
        ],
        horizon_days=30,
    )
    answer = result["natural_answer"]
    assert "summary" in answer
    assert "direction" in answer
    assert "probabilities" in answer
    assert "confidence" in answer
    assert "uncertainty" in answer
    assert "warning" in answer
    assert result["ai_analysis"]["status"] == "success"
    assert result["integration"]["ai_connected"] is True
    assert result["integration"]["existing_ai_preserved"] is True
    assert result["integration"]["new_ai_created"] is False
def test_insufficient_data():
    system = FutureIntelligence()
    result = system.analyze(
        "future?",
        [100, 105],
        horizon_days=30,
    )
    answer = result["natural_answer"]
    assert answer["direction"] == "unknown"
    assert answer["confidence"] == "very_low"
    assert answer["uncertainty"] == "very_high"
    assert answer["guarantee"] is False
if __name__ == "__main__":
    test_answer_builder()
    test_full_natural_answer_pipeline()
    test_insufficient_data()
    print(
        json.dumps(
            {
                "status": "PASS",
                "task": 19,
                "message": (
                    "Natural language future answer "
                    "pipeline is working."
                )
            },
            ensure_ascii=False,
            indent=2
        )
    )
