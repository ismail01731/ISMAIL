from __future__ import annotations
from dataclasses import dataclass, field
@dataclass
class CodeAnalysisResult:
    language: str
    valid: bool
    syntax_error: str | None = None
    imports: list[str] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    exceptions: list[str] = field(default_factory=list)
    async_functions: list[str] = field(default_factory=list)
    api_indicators: list[str] = field(default_factory=list)
    database_indicators: list[str] = field(default_factory=list)
