from __future__ import annotations
from dataclasses import dataclass
from numbers import Number
from typing import Any
@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    reason: str
class ResultVerifier:
    """
    Verifies deterministic calculation and code-execution results.
    Research evidence verification remains handled by the existing
    Task 1-4 evidence pipeline.
    """
    def verify_calculation(self, result: Any) -> VerificationResult:
        if result is None:
            return VerificationResult(
                verified=False,
                reason="Calculation result is missing.",
            )
        if not getattr(result, "success", False):
            return VerificationResult(
                verified=False,
                reason=getattr(
                    result,
                    "reason",
                    "Calculation failed.",
                ),
            )
        value = getattr(result, "result", None)
        if isinstance(value, bool) or not isinstance(value, Number):
            return VerificationResult(
                verified=False,
                reason="Calculation result is not a valid numeric value.",
            )
        return VerificationResult(
            verified=True,
            reason="Calculation result passed deterministic verification.",
        )
    def verify_execution(self, result: Any) -> VerificationResult:
        if result is None:
            return VerificationResult(
                verified=False,
                reason="Execution result is missing.",
            )
        success = bool(getattr(result, "success", False))
        blocked = bool(getattr(result, "blocked", False))
        timed_out = bool(getattr(result, "timed_out", False))
        return_code = getattr(result, "return_code", None)
        if blocked:
            return VerificationResult(
                verified=False,
                reason="Execution was blocked by the safety policy.",
            )
        if timed_out:
            return VerificationResult(
                verified=False,
                reason="Execution timed out.",
            )
        if success and return_code != 0:
            return VerificationResult(
                verified=False,
                reason="Execution result is inconsistent: success with a non-zero exit code.",
            )
        if not success and return_code == 0:
            return VerificationResult(
                verified=False,
                reason="Execution result is inconsistent: failure with a zero exit code.",
            )
        if return_code is None:
            return VerificationResult(
                verified=False,
                reason="Execution result has no return code.",
            )
        return VerificationResult(
            verified=success and return_code == 0,
            reason=(
                "Code execution result passed consistency verification."
                if success
                else "Code execution did not complete successfully."
            ),
        )
