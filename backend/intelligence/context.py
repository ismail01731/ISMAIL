from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
@dataclass
class IntelligenceContext:
    question: str
    values: List[float] = field(
        default_factory=list
    )
    evidence: List[Any] = field(
        default_factory=list
    )
    live_data: List[Any] = field(
        default_factory=list
    )
    metadata: Dict[str, Any] = field(
        default_factory=dict
    )
    def to_dict(
        self,
    ) -> Dict[str, Any]:
        return {
            "question":
                self.question,
            "values":
                self.values,
            "evidence":
                self.evidence,
            "live_data":
                self.live_data,
            "metadata":
                self.metadata,
        }
