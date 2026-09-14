from __future__ import annotations
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
@dataclass
class ExecutionRequest:
    command: list[str]
    timeout_seconds: int = 10
    working_directory: str | None = None
@dataclass
class ExecutionResult:
    success: bool
    return_code: int | None
    stdout: str
    stderr: str
    timed_out: bool
    blocked: bool
    reason: str = ""
class CodeExecutor:
    """
    Task 5.6: Safe Code Execution Foundation.
    Safety boundaries:
    - executes through subprocess rather than the current Python process
    - applies a timeout
    - captures stdout/stderr
    - rejects empty commands
    - rejects obviously dangerous Windows shell commands
    - does not invoke a shell
    - does not install packages
    - does not delete files
    - does not modify project files automatically
    This is a foundation, not a complete OS-level sandbox.
    A stronger sandbox/container boundary can be added later.
    """
    DEFAULT_TIMEOUT = 10
    MAX_TIMEOUT = 60
    BLOCKED_COMMANDS = {
        "del",
        "erase",
        "rd",
        "rmdir",
        "format",
        "diskpart",
        "shutdown",
        "restart-computer",
        "stop-computer",
        "remove-item",
    }
    BLOCKED_FLAGS = {
        "-enc",
        "-encodedcommand",
        "/c",
    }
    def execute(
        self,
        request: ExecutionRequest,
    ) -> ExecutionResult:
        command = [
            str(part).strip()
            for part in request.command
            if str(part).strip()
        ]
        if not command:
            return ExecutionResult(
                success=False,
                return_code=None,
                stdout="",
                stderr="",
                timed_out=False,
                blocked=True,
                reason="Execution command cannot be empty.",
            )
        if self._is_blocked(command):
            return ExecutionResult(
                success=False,
                return_code=None,
                stdout="",
                stderr="",
                timed_out=False,
                blocked=True,
                reason="Command blocked by execution safety policy.",
            )
        timeout = self._normalize_timeout(
            request.timeout_seconds
        )
        working_directory = self._prepare_working_directory(
            request.working_directory
        )
        try:
            completed = subprocess.run(
                command,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=False,
                check=False,
                env=self._safe_environment(),
            )
            return ExecutionResult(
                success=completed.returncode == 0,
                return_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                timed_out=False,
                blocked=False,
                reason=(
                    "Command executed successfully."
                    if completed.returncode == 0
                    else "Command completed with a non-zero exit code."
                ),
            )
        except subprocess.TimeoutExpired as exc:
            stdout = self._decode_output(exc.stdout)
            stderr = self._decode_output(exc.stderr)
            return ExecutionResult(
                success=False,
                return_code=None,
                stdout=stdout,
                stderr=stderr,
                timed_out=True,
                blocked=False,
                reason="Execution timed out.",
            )
        except (FileNotFoundError, OSError) as exc:
            return ExecutionResult(
                success=False,
                return_code=None,
                stdout="",
                stderr="",
                timed_out=False,
                blocked=False,
                reason=f"Execution failed to start: {exc}",
            )
    def _is_blocked(
        self,
        command: list[str],
    ) -> bool:
        for part in command:
            raw = str(part).strip().lower()
            normalized = Path(raw).name.lower()
            if raw in self.BLOCKED_FLAGS:
                return True
            if normalized in self.BLOCKED_COMMANDS:
                return True
        return False
    def _normalize_timeout(
        self,
        timeout_seconds: int,
    ) -> int:
        try:
            timeout = int(timeout_seconds)
        except (TypeError, ValueError):
            timeout = self.DEFAULT_TIMEOUT
        if timeout <= 0:
            timeout = self.DEFAULT_TIMEOUT
        return min(
            timeout,
            self.MAX_TIMEOUT,
        )
    def _prepare_working_directory(
        self,
        requested_directory: str | None,
    ) -> str:
        if requested_directory:
            path = Path(requested_directory).resolve()
            if path.exists() and path.is_dir():
                return str(path)
        return tempfile.gettempdir()
    @staticmethod
    def _safe_environment() -> dict[str, str]:
        allowed = {
            "PATH",
            "SystemRoot",
            "WINDIR",
            "TEMP",
            "TMP",
            "PYTHONIOENCODING",
        }
        return {
            key: value
            for key, value in os.environ.items()
            if key in allowed
        }
    @staticmethod
    def _decode_output(
        value,
    ) -> str:
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode(
                "utf-8",
                errors="replace",
            )
        return str(value)
code_executor = CodeExecutor()
