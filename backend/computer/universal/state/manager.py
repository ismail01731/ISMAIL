"""
ISMAIL AI - Computer State Manager
Task 14F-F
Lifecycle-aware logical state manager.
IMPORTANT:
Real computer execution remains disabled.
"""
from typing import Dict, Optional
from backend.computer.universal.state.model import (
    ComputerState,
)
from backend.computer.universal.state.persistence import (
    ComputerStatePersistence,
)
from backend.computer.universal.lifecycle import (
    LIFECYCLE_EXPIRED,
    get_lifecycle_status,
    utc_now_iso,
)
class ComputerStateManager:
    """
    Manage logical computer states by session/user key.
    """
    def __init__(
        self,
        persistence=None,
    ):
        self._states: Dict[str, ComputerState] = {}
        self._persistence = (
            persistence
            if persistence is not None
            else ComputerStatePersistence()
        )
    @staticmethod
    def _normalize_key(
        key: Optional[str],
    ) -> str:
        value = str(key or "").strip()
        if not value:
            return "default"
        return value
    @staticmethod
    def _initialize_lifecycle(
        state: ComputerState,
        now: Optional[str] = None,
    ) -> ComputerState:
        timestamp = now or utc_now_iso()
        if not state.created_at:
            state.created_at = timestamp
        if not state.updated_at:
            state.updated_at = timestamp
        if not state.last_accessed_at:
            state.last_accessed_at = timestamp
        state.lifecycle_status = get_lifecycle_status(
            state.updated_at,
        )
        state.execution_allowed = False
        return state
    def get_state(
        self,
        session_key: Optional[str] = None,
    ) -> ComputerState:
        """
        Get an existing state, loading it from persistent
        storage when necessary.
        Expired context remains readable but is marked expired.
        It is never treated as executable state.
        """
        key = self._normalize_key(session_key)
        if key not in self._states:
            state = self._persistence.load_state(key)
            state = self._initialize_lifecycle(state)
            self._states[key] = state
        state = self._states[key]
        state.lifecycle_status = get_lifecycle_status(
            state.updated_at,
        )
        state.last_accessed_at = utc_now_iso()
        state.execution_allowed = False
        return state
    def has_state(
        self,
        session_key: Optional[str] = None,
    ) -> bool:
        key = self._normalize_key(session_key)
        return key in self._states
    def update_state(
        self,
        session_key: Optional[str] = None,
        **updates,
    ) -> ComputerState:
        """
        Update known logical state fields.
        Lifecycle metadata is maintained automatically.
        """
        key = self._normalize_key(session_key)
        state = self.get_state(key)
        allowed_fields = {
            "active_application",
            "active_website",
            "current_folder",
            "active_file",
            "known_files",
            "known_folders",
            "last_action",
            "last_request",
            "last_step",
            "references",
        }
        for field_name, value in updates.items():
            if field_name not in allowed_fields:
                continue
            setattr(
                state,
                field_name,
                value,
            )
        now = utc_now_iso()
        if not state.created_at:
            state.created_at = now
        state.updated_at = now
        state.last_accessed_at = now
        state.lifecycle_status = get_lifecycle_status(
            state.updated_at,
        )
        state.execution_allowed = False
        self._persistence.save_state(
            key,
            state,
        )
        return state
    def reset_state(
        self,
        session_key: Optional[str] = None,
    ) -> ComputerState:
        """
        Reset one logical computer state.
        """
        key = self._normalize_key(session_key)
        state = self.get_state(key)
        state.reset()
        now = utc_now_iso()
        state.created_at = now
        state.updated_at = now
        state.last_accessed_at = now
        state.lifecycle_status = "active"
        state.execution_allowed = False
        self._persistence.save_state(
            key,
            state,
        )
        return state
    def remove_state(
        self,
        session_key: Optional[str] = None,
    ) -> bool:
        """
        Remove one session state completely.
        """
        key = self._normalize_key(session_key)
        existed_in_memory = (
            key in self._states
        )
        existed_persisted = (
            self._persistence.has_state(key)
        )
        if not existed_in_memory and not existed_persisted:
            return False
        self._states.pop(
            key,
            None,
        )
        self._persistence.delete_state(
            key,
        )
        return True
    def cleanup_expired(
        self,
    ) -> int:
        """
        Remove only expired logical states.
        Returns the number of removed sessions.
        """
        states = self._persistence.load_all()
        removed = 0
        for key, state in states.items():
            status = get_lifecycle_status(
                state.updated_at,
            )
            if status != LIFECYCLE_EXPIRED:
                continue
            self._states.pop(
                key,
                None,
            )
            self._persistence.delete_state(
                key,
            )
            removed += 1
        return removed
    def is_expired(
        self,
        session_key: Optional[str] = None,
    ) -> bool:
        state = self.get_state(session_key)
        return (
            state.lifecycle_status
            == LIFECYCLE_EXPIRED
        )
    def clear_all(self) -> None:
        """
        Remove all logical computer states.
        """
        self._states.clear()
        self._persistence.clear_all()
    def state_count(self) -> int:
        return self._persistence.state_count()
    def get_state_dict(
        self,
        session_key: Optional[str] = None,
    ):
        state = self.get_state(session_key)
        return state.to_dict()
_default_manager = ComputerStateManager()
def get_computer_state_manager() -> ComputerStateManager:
    return _default_manager
def get_computer_state(
    session_key: Optional[str] = None,
) -> ComputerState:
    return _default_manager.get_state(session_key)
def update_computer_state(
    session_key: Optional[str] = None,
    **updates,
) -> ComputerState:
    return _default_manager.update_state(
        session_key,
        **updates,
    )
def reset_computer_state(
    session_key: Optional[str] = None,
) -> ComputerState:
    return _default_manager.reset_state(
        session_key,
    )
