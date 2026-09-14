from __future__ import annotations
from dataclasses import dataclass, field
from .code_executor import (
    CodeExecutor,
    ExecutionRequest,
)
@dataclass
class TestRunRequest:
    command: list[str]
    timeout_seconds: int = 10
    working_directory: str | None = None
@dataclass
class TestRunResult:
    success: bool
    passed: bool
    return_code: int | None
    stdout: str
    stderr: str
    timed_out: bool
    blocked: bool
    failures: list[str] = field(default_factory=list)
    reason: str = ""
class TestRunner:
    """
    Task 5.7: Test Runner Foundation.
    Pipeline:
        test command
            -> safe executor
            -> test output
            -> pass/fail
            -> diagnostics
    This module does not execute commands directly.
    All execution is delegated to Task 5.6 CodeExecutor.
    """
    def __init__(
        self,
        executor: CodeExecutor | None = None,
    ) -> None:
        self.executor = executor or CodeExecutor()
    def run(
        self,
        request: TestRunRequest,
    ) -> TestRunResult:
        execution = self.executor.execute(
            ExecutionRequest(
                command=request.command,
                timeout_seconds=request.timeout_seconds,
                working_directory=request.working_directory,
            )
        )
        failures = self._extract_failures(
            execution.stdout,
            execution.stderr,
            execution.return_code,
        )
        passed = (
            execution.success
            and not execution.timed_out
            and not execution.blocked
        )
        if execution.blocked:
            reason = "Test command was blocked by the execution safety policy."
        elif execution.timed_out:
            reason = "Test execution timed out."
        elif passed:
            reason = "Tests completed successfully."
        else:
            reason = "Tests completed with failures."
        return TestRunResult(
            success=execution.success,
            passed=passed,
            return_code=execution.return_code,
            stdout=execution.stdout,
            stderr=execution.stderr,
            timed_out=execution.timed_out,
            blocked=execution.blocked,
            failures=failures,
            reason=reason,
        )
    @staticmethod
    def _extract_failures(
        stdout: str,
        stderr: str,
        return_code: int | None,
    ) -> list[str]:
        failures: list[str] = []
        combined = "\n".join(
            value
            for value in (stdout, stderr)
            if value
        )
        for line in combined.splitlines():
            normalized = line.strip()
            if not normalized:
                continue
            upper = normalized.upper()
            if (
                "FAILED" in upper
                or "FAIL:" in upper
                or "ERROR" in upper
                or "TRACEBACK" in upper
            ):
                failures.append(normalized)
        if return_code not in (None, 0) and not failures:
            failures.append(
                f"Test process exited with code {return_code}."
            )
        return failures
test_runner = TestRunner()
