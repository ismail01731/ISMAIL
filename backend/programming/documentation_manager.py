from __future__ import annotations
from dataclasses import dataclass, field
@dataclass
class DocumentationEntry:
    name: str
    technology: str
    version: str = ""
    documentation_url: str = ""
    notes: list[str] = field(default_factory=list)
@dataclass
class DocumentationResult:
    success: bool
    technology: str
    version: str
    documentation_url: str
    notes: list[str] = field(default_factory=list)
    compatible: bool | None = None
    reason: str = ""
class DocumentationManager:
    """
    Task 5.8: Documentation + Version Awareness Foundation.
    Responsibilities:
    - store documentation references
    - track technology/library versions
    - provide version-aware context
    - perform basic compatibility checks
    This foundation does not automatically access the internet.
    Future web/API documentation retrieval can be connected later.
    """
    def __init__(self) -> None:
        self._entries: dict[str, DocumentationEntry] = {}
    def register(
        self,
        entry: DocumentationEntry,
    ) -> DocumentationResult:
        technology = entry.technology.strip()
        name = entry.name.strip()
        if not technology:
            return DocumentationResult(
                success=False,
                technology="",
                version=entry.version,
                documentation_url=entry.documentation_url,
                reason="Technology name cannot be empty.",
            )
        if not name:
            return DocumentationResult(
                success=False,
                technology=technology,
                version=entry.version,
                documentation_url=entry.documentation_url,
                reason="Documentation entry name cannot be empty.",
            )
        key = self._key(technology, name)
        self._entries[key] = entry
        return DocumentationResult(
            success=True,
            technology=technology,
            version=entry.version,
            documentation_url=entry.documentation_url,
            notes=list(entry.notes),
            reason="Documentation entry registered successfully.",
        )
    def get(
        self,
        technology: str,
        name: str,
    ) -> DocumentationResult:
        key = self._key(
            technology,
            name,
        )
        entry = self._entries.get(key)
        if entry is None:
            return DocumentationResult(
                success=False,
                technology=technology,
                version="",
                documentation_url="",
                reason="Documentation entry not found.",
            )
        return DocumentationResult(
            success=True,
            technology=entry.technology,
            version=entry.version,
            documentation_url=entry.documentation_url,
            notes=list(entry.notes),
            reason="Documentation entry retrieved successfully.",
        )
    def check_version(
        self,
        technology: str,
        required_version: str,
        current_version: str,
    ) -> DocumentationResult:
        technology = technology.strip()
        required_version = required_version.strip()
        current_version = current_version.strip()
        if not technology:
            return DocumentationResult(
                success=False,
                technology="",
                version=current_version,
                documentation_url="",
                reason="Technology name cannot be empty.",
            )
        if not required_version or not current_version:
            return DocumentationResult(
                success=False,
                technology=technology,
                version=current_version,
                documentation_url="",
                reason="Both required and current versions are required.",
            )
        compatible = self._versions_match(
            required_version,
            current_version,
        )
        return DocumentationResult(
            success=True,
            technology=technology,
            version=current_version,
            documentation_url="",
            compatible=compatible,
            reason=(
                "Version requirement is satisfied."
                if compatible
                else "Version requirement is not satisfied."
            ),
        )
    def list_entries(self) -> list[DocumentationEntry]:
        return list(self._entries.values())
    @staticmethod
    def _key(
        technology: str,
        name: str,
    ) -> str:
        return (
            f"{technology.strip().lower()}:"
            f"{name.strip().lower()}"
        )
    @staticmethod
    def _versions_match(
        required_version: str,
        current_version: str,
    ) -> bool:
        required = required_version.lstrip("v=").strip()
        current = current_version.lstrip("v=").strip()
        if required in {"*", "latest"}:
            return True
        if required == current:
            return True
        # Basic major-version compatibility.
        required_major = required.split(".", 1)[0]
        current_major = current.split(".", 1)[0]
        return required_major == current_major
documentation_manager = DocumentationManager()
