from __future__ import annotations
from typing import Any, Dict, List, Optional
class IntelligenceContext:
    """
    Common context passed between the existing AI and
    future-prediction modules.
    """
    def __init__(
        self,
        question: str,
        values: Optional[List[float]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        live_data: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.question = question
        self.values = values or []
        self.evidence = evidence or []
        self.live_data = live_data or []
        self.metadata = metadata or {}
    def to_dict(self) -> Dict[str, Any]:
        return {
            "question": self.question,
            "values": self.values,
            "evidence": self.evidence,
            "live_data": self.live_data,
            "metadata": self.metadata,
        }
