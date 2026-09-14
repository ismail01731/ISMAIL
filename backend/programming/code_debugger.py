from __future__ import annotations
from dataclasses import dataclass, field
@dataclass
class DebugRequest:
    error_message: str
    code: str = ""
    language: str = ""
    file_path: str = ""
    function_name: str = ""
@dataclass
class DebugResult:
    success: bool
    error_type: str
    location: str
    likely_causes: list[str] = field(default_factory=list)
    targeted_fix: str = ""
    verification_steps: list[str] = field(default_factory=list)
    reason: str = ""
class CodeDebugger:
    """
    Task 5.5: Code Debugger Foundation.
    Pipeline:
        error
          -> error type
          -> location
          -> likely cause
          -> targeted fix
          -> verification
    This foundation is analysis-only.
    It does not execute code or modify project files.
    """
    ERROR_PATTERNS = {
        "SyntaxError": (
            "syntaxerror",
            "invalid syntax",
            "unexpected token",
            "expected ':'",
        ),
        "NameError": (
            "nameerror",
            "is not defined",
            "not defined",
        ),
        "TypeError": (
            "typeerror",
            "unsupported operand type",
            "takes ",
            "argument",
        ),
        "ValueError": (
            "valueerror",
            "invalid value",
            "could not convert",
        ),
        "KeyError": (
            "keyerror",
        ),
        "IndexError": (
            "indexerror",
            "index out of range",
        ),
        "AttributeError": (
            "attributeerror",
            "has no attribute",
        ),
        "ImportError": (
            "importerror",
            "cannot import",
        ),
        "ModuleNotFoundError": (
            "modulenotfounderror",
            "no module named",
        ),
        "FileNotFoundError": (
            "filenotfounderror",
            "no such file or directory",
        ),
        "PermissionError": (
            "permissionerror",
            "permission denied",
        ),
        "ConnectionError": (
            "connectionerror",
            "connection refused",
            "failed to establish",
        ),
        "TimeoutError": (
            "timeouterror",
            "timed out",
            "timeout",
        ),
    }
    def debug(
        self,
        request: DebugRequest,
    ) -> DebugResult:
        error_message = request.error_message.strip()
        if not error_message:
            return DebugResult(
                success=False,
                error_type="UnknownError",
                location=self._location(request),
                reason="Error message cannot be empty.",
            )
        error_type = self._detect_error_type(error_message)
        location = self._location(request)
        causes = self._likely_causes(
            error_type,
            request,
        )
        targeted_fix = self._targeted_fix(
            error_type,
            request,
        )
        verification_steps = self._verification_steps(
            error_type,
            request,
        )
        return DebugResult(
            success=True,
            error_type=error_type,
            location=location,
            likely_causes=causes,
            targeted_fix=targeted_fix,
            verification_steps=verification_steps,
            reason="Debug analysis prepared successfully.",
        )
    def _detect_error_type(
        self,
        error_message: str,
    ) -> str:
        normalized = error_message.lower()
        for error_type, patterns in self.ERROR_PATTERNS.items():
            for pattern in patterns:
                if pattern in normalized:
                    return error_type
        return "UnknownError"
    @staticmethod
    def _location(
        request: DebugRequest,
    ) -> str:
        parts = []
        if request.file_path.strip():
            parts.append(request.file_path.strip())
        if request.function_name.strip():
            parts.append(
                f"function={request.function_name.strip()}"
            )
        if parts:
            return " | ".join(parts)
        return "Location not specified."
    def _likely_causes(
        self,
        error_type: str,
        request: DebugRequest,
    ) -> list[str]:
        causes = {
            "SyntaxError": [
                "Invalid syntax or malformed code.",
                "Missing punctuation, delimiter, or language keyword.",
            ],
            "NameError": [
                "A variable, function, or class name is undefined.",
                "The name may be misspelled or outside its scope.",
            ],
            "TypeError": [
                "An operation received an incompatible type.",
                "A function may have received an unexpected argument type.",
            ],
            "ValueError": [
                "A value has the correct general type but an invalid value.",
                "Input conversion or validation may have failed.",
            ],
            "KeyError": [
                "A requested dictionary key is missing.",
                "The key name may be incorrect or unavailable.",
            ],
            "IndexError": [
                "A sequence index is outside the available range.",
                "The collection may contain fewer elements than expected.",
            ],
            "AttributeError": [
                "The object does not provide the requested attribute.",
                "The object may have the wrong type or an incorrect attribute name.",
            ],
            "ImportError": [
                "The requested module or symbol cannot be imported.",
                "The import path or installed package may be incorrect.",
            ],
            "ModuleNotFoundError": [
                "The required module is not available.",
                "The package may not be installed or the import name may be wrong.",
            ],
            "FileNotFoundError": [
                "The requested file or directory does not exist at the specified path.",
                "The path may be incorrect or relative to an unexpected working directory.",
            ],
            "PermissionError": [
                "The process does not have sufficient permission.",
                "The target resource may be locked or protected.",
            ],
            "ConnectionError": [
                "The target service may be unavailable.",
                "Host, port, network, or connection configuration may be incorrect.",
            ],
            "TimeoutError": [
                "The operation exceeded its allowed time.",
                "The remote service or local operation may be slow or unavailable.",
            ],
        }
        result = list(
            causes.get(
                error_type,
                [
                    "The error type could not be determined from the supplied message.",
                    "More context such as traceback and surrounding code is required.",
                ],
            )
        )
        if request.code.strip():
            result.append(
                "Inspect the relevant code path around the reported failure."
            )
        return result
    def _targeted_fix(
        self,
        error_type: str,
        request: DebugRequest,
    ) -> str:
        fixes = {
            "SyntaxError": "Correct the reported syntax and re-parse the code.",
            "NameError": "Check the name, definition order, spelling, and scope.",
            "TypeError": "Check the operand types and function arguments.",
            "ValueError": "Validate or convert the supplied value before use.",
            "KeyError": "Verify the key exists before accessing it.",
            "IndexError": "Check the collection length and index bounds.",
            "AttributeError": "Verify the object's type and the attribute name.",
            "ImportError": "Verify the import path and exported symbol.",
            "ModuleNotFoundError": "Verify the module name and environment dependency.",
            "FileNotFoundError": "Verify the path and working directory.",
            "PermissionError": "Verify access permissions before retrying.",
            "ConnectionError": "Verify service availability and connection settings.",
            "TimeoutError": "Check service responsiveness and timeout configuration.",
        }
        return fixes.get(
            error_type,
            "Inspect the traceback and surrounding code before applying a targeted fix.",
        )
    def _verification_steps(
        self,
        error_type: str,
        request: DebugRequest,
    ) -> list[str]:
        steps = [
            "Apply only the targeted change.",
            "Re-check the affected code.",
        ]
        if request.language.strip():
            steps.append(
                f"Validate the code using the {request.language.strip()} toolchain."
            )
        steps.append(
            "Run the relevant test or reproduction case."
        )
        steps.append(
            "Confirm that the original error no longer occurs."
        )
        return steps
code_debugger = CodeDebugger()
