from __future__ import annotations
from typing import Any, Dict
class FuturePromptBuilder:
    @staticmethod
    def build(
        question: str,
        forecast: Dict[str, Any],
    ) -> str:
        return f"""
You are the reasoning layer of a future-analysis system.
User question:
{question}
Quantitative forecast data:
{forecast}
Use the supplied forecast as evidence, not as certainty.
Your response should:
1. Explain the most likely future outcome.
2. Explain the main alternative scenarios.
3. Mention important uncertainty.
4. Identify assumptions.
5. Never claim that the future is guaranteed.
6. Clearly distinguish historical evidence from inference.
""".strip()
