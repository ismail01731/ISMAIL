from __future__ import annotations
import json
from typing import Any, Dict
class FuturePromptBuilder:
    def build(
        self,
        question: str,
        forecast: Dict[str, Any],
    ) -> str:
        forecast_json = json.dumps(
            forecast,
            ensure_ascii=False,
            indent=2,
            default=str,
        )
        return f"""
You are the reasoning layer of an existing AI system.
Do NOT claim certainty.
Do NOT invent facts.
Do NOT treat a forecast as guaranteed.
Use the forecast as one source of evidence.
User question:
{question}
Forecast system output:
{forecast_json}
Your task:
1. Explain the most likely future direction.
2. Explain the selected model and why it was selected.
3. Discuss downside, base and upside scenarios.
4. Explain the scenario probabilities.
5. Explain confidence and uncertainty.
6. Mention important data-quality limitations.
7. Explain what evidence could change the prediction.
8. If the forecast is weak, say so clearly.
9. Give a concise final answer first.
10. Do not manufacture external evidence.
Use natural language appropriate to the user's question.
""".strip()
