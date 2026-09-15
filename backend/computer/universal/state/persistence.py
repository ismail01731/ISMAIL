from pathlib import Path
from typing import Dict, Optional
from backend.computer.universal.state.model import (
    ComputerState,
)
class ComputerStatePersistence:
    """
    ISMAIL AI - Persistent Computer State Repository
    Task 14F-A
    This module persists logical/planned computer state only.
    IMPORTANT:
    - Does NOT inspect the real computer.
    - Does NOT execute computer actions.
    - Does NOT grant execution permission.
    - execution_allowed is ALWAYS False.
    """
    def __init__(
        self,
        storage_path: Optional[str] = None,
    ):
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = (
                Path("data")
                / "computer_state"
                / "states.json"
            )
    @staticmethod
    def _normalize_key(
        key: Optional[str],
    ) -> str:
        value = str(key or "").strip()
        if not value:
            return "default"
        return value
    def _ensure_storage_directory(self) -> None:
        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
    def _read_storage(self) -> Dict:
        if not self.storage_path.exists():
            return {}
        try:
            import json
            raw = self.storage_path.read_text(
                encoding="utf-8",
            )
            if not raw.strip():
                return {}
            data = json.loads(raw)
            if not isinstance(data, dict):
                return {}
            return data
        except (
            OSError,
            ValueError,
            TypeError,
        ):
            return {}
    def _write_storage(
        self,
        data: Dict,
    ) -> None:
        import json
        self._ensure_storage_directory()
        temporary_path = self.storage_path.with_suffix(
            self.storage_path.suffix + ".tmp"
        )
        payload = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )
        temporary_path.write_text(
            payload,
            encoding="utf-8",
        )
        temporary_path.replace(
            self.storage_path,
        )
    def has_state(
        self,
        session_key: Optional[str] = None,
    ) -> bool:
        key = self._normalize_key(session_key)
        data = self._read_storage()
        return key in data
    def load_state(
        self,
        session_key: Optional[str] = None,
    ) -> ComputerState:
        key = self._normalize_key(session_key)
        data = self._read_storage()
        raw_state = data.get(key)
        if not isinstance(raw_state, dict):
            return ComputerState()
        try:
            state = ComputerState.from_dict(
                raw_state,
            )
        except (
            TypeError,
            ValueError,
            KeyError,
        ):
            state = ComputerState()
        state.execution_allowed = False
        return state
    def save_state(
        self,
        session_key: Optional[str],
        state: ComputerState,
    ) -> ComputerState:
        key = self._normalize_key(session_key)
        if state is None:
            state = ComputerState()
        state.execution_allowed = False
        data = self._read_storage()
        data[key] = state.to_dict()
        data[key]["execution_allowed"] = False
        self._write_storage(data)
        return state
    def delete_state(
        self,
        session_key: Optional[str] = None,
    ) -> bool:
        key = self._normalize_key(session_key)
        data = self._read_storage()
        if key not in data:
            return False
        del data[key]
        self._write_storage(data)
        return True
    def reset_state(
        self,
        session_key: Optional[str] = None,
    ) -> ComputerState:
        key = self._normalize_key(session_key)
        state = ComputerState()
        self.save_state(
            key,
            state,
        )
        return state
    def clear_all(self) -> None:
        self._write_storage({})
    def state_count(self) -> int:
        return len(self._read_storage())
    def load_all(self) -> Dict[str, ComputerState]:
        data = self._read_storage()
        states = {}
        for key, raw_state in data.items():
            if not isinstance(raw_state, dict):
                continue
            try:
                state = ComputerState.from_dict(
                    raw_state,
                )
            except (
                TypeError,
                ValueError,
                KeyError,
            ):
                continue
            state.execution_allowed = False
            states[str(key)] = state
        return states
__all__ = [
    "ComputerStatePersistence",
]
