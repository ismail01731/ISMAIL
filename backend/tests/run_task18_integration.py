import sys
from pathlib import Path
# Ensure backend root is importable when this file
# is executed directly from the tests directory.
BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
from intelligence.orchestrator import FutureIntelligence
from intelligence.adapter import ExistingAIAdapter
import json
def ai(prompt):
    return "Existing AI received forecast context."
adapter = ExistingAIAdapter(
    ai,
    "test_ai"
)
system = FutureIntelligence(
    adapter
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
output = {
    "selected_model":
        result["forecast"].get(
            "selected_model"
        ),
    "confidence_percent":
        result["forecast"].get(
            "confidence_percent"
        ),
    "data_quality":
        result["forecast"].get(
            "data_quality"
        ),
    "uncertainty":
        result["forecast"].get(
            "uncertainty"
        ),
    "ai_status":
        result["ai_analysis"].get(
            "status"
        ),
    "ai_response":
        result["ai_analysis"].get(
            "response"
        ),
    "integration":
        result["integration"],
}
print(
    json.dumps(
        output,
        ensure_ascii=False,
        indent=2,
        default=str,
    )
)
