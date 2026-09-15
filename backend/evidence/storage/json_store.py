import json
from pathlib import Path
from ..models import Evidence
class EvidenceStorage:
    def __init__(self, path: str = "data/evidence.json"):
        self.path = Path(path)
        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    def save(
        self,
        evidence: list[Evidence],
    ):
        data = [
            item.to_dict()
            for item in evidence
        ]
        self.path.write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    def load(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )
