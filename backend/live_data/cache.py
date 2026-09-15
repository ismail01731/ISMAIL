import json
from pathlib import Path
from typing import Any
class LiveDataCache:
    def __init__(
        self,
        directory: str = "live_data/cache",
    ):
        self.directory = Path(
            directory
        )
        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )
    def _path(
        self,
        topic: str,
    ) -> Path:
        safe_name = "".join(
            char if char.isalnum()
            else "_"
            for char in topic
        )
        return (
            self.directory
            / f"{safe_name}.json"
        )
    def save(
        self,
        topic: str,
        data: list[dict[str, Any]],
    ):
        self._path(topic).write_text(
            json.dumps(
                data,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
    def load(
        self,
        topic: str,
    ) -> list[dict[str, Any]]:
        path = self._path(topic)
        if not path.exists():
            return []
        try:
            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return []
