"""
ISMAIL AI - Computer State Model
Task 14F-F
Logical computer context with lifecycle metadata.
IMPORTANT:
This is a state/context model only.
It does NOT inspect or modify the real computer.
"""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
@dataclass
class ComputerState:
    """
    Logical state maintained by ISMAIL AI.
    """
    active_application: Optional[str] = None
    active_website: Optional[str] = None
    current_folder: Optional[str] = None
    active_file: Optional[str] = None
    known_files: List[str] = field(default_factory=list)
    known_folders: List[str] = field(default_factory=list)
    last_action: Optional[str] = None
    last_request: Optional[str] = None
    last_step: Optional[int] = None
    references: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    last_accessed_at: Optional[str] = None
    lifecycle_status: str = "active"
    execution_allowed: bool = False
    def to_dict(self) -> Dict[str, Any]:
        """
        Return the state as a serializable dictionary.
        """
        return {
            "active_application": self.active_application,
            "active_website": self.active_website,
            "current_folder": self.current_folder,
            "active_file": self.active_file,
            "known_files": list(self.known_files),
            "known_folders": list(self.known_folders),
            "last_action": self.last_action,
            "last_request": self.last_request,
            "last_step": self.last_step,
            "references": dict(self.references),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_accessed_at": self.last_accessed_at,
            "lifecycle_status": self.lifecycle_status,
            "execution_allowed": False,
        }
    @classmethod
    def from_dict(
        cls,
        data: Optional[Dict[str, Any]] = None,
    ) -> "ComputerState":
        """
        Build a ComputerState from a dictionary.
        Legacy states without lifecycle metadata remain compatible.
        Execution can never be enabled through this method.
        """
        source = data or {}
        lifecycle_status = str(
            source.get(
                "lifecycle_status",
                "active",
            )
            or "active"
        ).strip().lower()
        if lifecycle_status not in {
            "active",
            "stale",
            "expired",
        }:
            lifecycle_status = "active"
        return cls(
            active_application=source.get(
                "active_application"
            ),
            active_website=source.get(
                "active_website"
            ),
            current_folder=source.get(
                "current_folder"
            ),
            active_file=source.get(
                "active_file"
            ),
            known_files=list(
                source.get("known_files", [])
            ),
            known_folders=list(
                source.get("known_folders", [])
            ),
            last_action=source.get(
                "last_action"
            ),
            last_request=source.get(
                "last_request"
            ),
            last_step=source.get(
                "last_step"
            ),
            references=dict(
                source.get("references", {})
            ),
            created_at=source.get(
                "created_at"
            ),
            updated_at=source.get(
                "updated_at"
            ),
            last_accessed_at=source.get(
                "last_accessed_at"
            ),
            lifecycle_status=lifecycle_status,
            execution_allowed=False,
        )
    def reset(self) -> None:
        """
        Reset logical computer context.
        """
        self.active_application = None
        self.active_website = None
        self.current_folder = None
        self.active_file = None
        self.known_files.clear()
        self.known_folders.clear()
        self.last_action = None
        self.last_request = None
        self.last_step = None
        self.references.clear()
        self.created_at = None
        self.updated_at = None
        self.last_accessed_at = None
        self.lifecycle_status = "active"
        self.execution_allowed = False
