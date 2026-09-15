import sys
from pathlib import Path
import json
BACKEND_ROOT = Path(__file__).resolve().parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
from intelligence.adapter import ExistingAIAdapter
from intelligence.orchestrator import FutureIntelligence
from pipeline.automatic import AutomaticFuturePipeline
def fake_ai(prompt):
    return "Existing AI received automatic historical and live forecast context."
adapter = ExistingAIAdapter(
    fake_ai,
    "test_ai"
)
system = FutureIntelligence(
    adapter
)
pipeline = AutomaticFuturePipeline(
    intelligence=system
)
result = pipeline.analyze(
    question="আগামী 30 দিনে এই trend কোন দিকে যেতে পারে?",
    topic="task20_test_topic",
    horizon_days=30,
    live_provider="manual",
    live_value=160,
)
print(json.dumps({
    "ai_analysis": result.get("ai_analysis"),
    "integration": result.get("integration"),
    "pipeline": result.get("pipeline"),
    "natural_answer": result.get("natural_answer"),
    "forecast_status": result.get("forecast", {}).get("status"),
}, ensure_ascii=False, indent=2, default=str))
