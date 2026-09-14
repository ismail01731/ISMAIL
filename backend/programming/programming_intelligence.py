from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from .code_analyzer import MultiLanguageCodeAnalyzer
from .code_debugger import CodeDebugger, DebugRequest
from .code_executor import CodeExecutor, ExecutionRequest
from .code_generator import CodeGenerationRequest, CodeGenerator
from .documentation_manager import DocumentationManager
from .project_analyzer import ProjectAnalyzer
from .test_runner import TestRunRequest, TestRunner
from backend.llm.router import LLMRouter
@dataclass
class ProgrammingRequest:
    action: str
    language: str = ""
    requirement: str = ""
    code: str = ""
    project_path: str = ""
    command: list[str] = field(default_factory=list)
    error_message: str = ""
    file_path: str = ""
    function_name: str = ""
    context: str = ""
    constraints: list[str] = field(default_factory=list)
    timeout_seconds: int = 10
@dataclass
class ProgrammingResult:
    success: bool
    action: str
    result: Any = None
    reason: str = ""
class ProgrammingIntelligence:
    """
    Task 5.9: Programming Intelligence Orchestrator.
    Provides one controlled entry point for:
    - code analysis
    - project analysis
    - code generation
    - debugging
    - safe execution
    - testing
    - documentation/version awareness
    This module coordinates existing Task 5.x components.
    It does not bypass their safety boundaries.
    """
    SUPPORTED_ACTIONS = {
        "analyze_code",
        "analyze_project",
        "generate_code",
        "debug_code",
        "execute",
        "run_tests",
        "check_version",
        "documentation",
    }
    def __init__(
        self,
        llm_router: LLMRouter | None = None,
        analyzer: MultiLanguageCodeAnalyzer | None = None,
        project_analyzer: ProjectAnalyzer | None = None,
        generator: CodeGenerator | None = None,
        debugger: CodeDebugger | None = None,
        executor: CodeExecutor | None = None,
        test_runner: TestRunner | None = None,
        documentation_manager: DocumentationManager | None = None,
    ) -> None:
        self.llm_router = llm_router
        self.analyzer = analyzer or MultiLanguageCodeAnalyzer()
        self.project_analyzer = (
            project_analyzer or ProjectAnalyzer()
        )
        self.generator = generator or CodeGenerator(
            llm_router=llm_router
        )
        self.debugger = debugger or CodeDebugger()
        self.executor = executor or CodeExecutor()
        self.test_runner = test_runner or TestRunner(
            executor=self.executor
        )
        self.documentation_manager = (
            documentation_manager
            or DocumentationManager()
        )
    def handle(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        action = request.action.strip().lower()
        if action not in self.SUPPORTED_ACTIONS:
            return ProgrammingResult(
                success=False,
                action=action,
                reason=f"Unsupported programming action: {action}",
            )
        if action == "analyze_code":
            return self._analyze_code(request)
        if action == "analyze_project":
            return self._analyze_project(request)
        if action == "generate_code":
            return self._generate_code(request)
        if action == "debug_code":
            return self._debug_code(request)
        if action == "execute":
            return self._execute(request)
        if action == "run_tests":
            return self._run_tests(request)
        if action == "check_version":
            return self._check_version(request)
        if action == "documentation":
            return self._documentation(request)
        return ProgrammingResult(
            success=False,
            action=action,
            reason="Programming action could not be handled.",
        )
    def _analyze_code(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        if request.language.strip().lower() not in {
            "python",
            "javascript",
            "typescript",
            "html",
            "css",
            "sql",
            "bash",
            "powershell",
            "pwsh",
            "ps1",
        }:
            return ProgrammingResult(
                success=False,
                action="analyze_code",
                reason=(
                    "Supported analysis languages: "
                    "Python, JavaScript, TypeScript, HTML, CSS, SQL, Bash, PowerShell."
                ),
            )
        result = self.analyzer.analyze(
            request.code,
            request.language,
        )
        return ProgrammingResult(
            success=result.valid,
            action="analyze_code",
            result=result,
            reason=(
                "Code analyzed successfully."
                if result.valid
                else "Code contains a syntax error."
            ),
        )
    def _analyze_project(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        if not request.project_path.strip():
            return ProgrammingResult(
                success=False,
                action="analyze_project",
                reason="Project path cannot be empty.",
            )
        result = self.project_analyzer.analyze(
            Path(request.project_path)
        )
        return ProgrammingResult(
            success=result.exists,
            action="analyze_project",
            result=result,
            reason=result.reason,
        )
    def _generate_code(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        result = self.generator.generate(
            CodeGenerationRequest(
                requirement=request.requirement,
                language=request.language,
                context=request.context,
                constraints=request.constraints,
                include_tests=True,
            )
        )
        return ProgrammingResult(
            success=result.success,
            action="generate_code",
            result=result,
            reason=result.reason,
        )
    def _debug_code(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        result = self.debugger.debug(
            DebugRequest(
                error_message=request.error_message,
                code=request.code,
                language=request.language,
                file_path=request.file_path,
                function_name=request.function_name,
            )
        )
        return ProgrammingResult(
            success=result.success,
            action="debug_code",
            result=result,
            reason=result.reason,
        )
    def _execute(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        if not request.command:
            return ProgrammingResult(
                success=False,
                action="execute",
                reason="Execution command cannot be empty.",
            )
        result = self.executor.execute(
            ExecutionRequest(
                command=request.command,
                timeout_seconds=request.timeout_seconds,
                working_directory=(
                    request.project_path or None
                ),
            )
        )
        return ProgrammingResult(
            success=result.success,
            action="execute",
            result=result,
            reason=result.reason,
        )
    def _run_tests(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        if not request.command:
            return ProgrammingResult(
                success=False,
                action="run_tests",
                reason="Test command cannot be empty.",
            )
        result = self.test_runner.run(
            TestRunRequest(
                command=request.command,
                timeout_seconds=request.timeout_seconds,
                working_directory=(
                    request.project_path or None
                ),
            )
        )
        return ProgrammingResult(
            success=result.passed,
            action="run_tests",
            result=result,
            reason=result.reason,
        )
    def _check_version(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        parts = request.context.split("|", 1)
        if len(parts) != 2:
            return ProgrammingResult(
                success=False,
                action="check_version",
                reason=(
                    "Version check context must be "
                    "'required_version|current_version'."
                ),
            )
        required_version, current_version = parts
        result = self.documentation_manager.check_version(
            request.language,
            required_version,
            current_version,
        )
        return ProgrammingResult(
            success=result.success,
            action="check_version",
            result=result,
            reason=result.reason,
        )
    def _documentation(
        self,
        request: ProgrammingRequest,
    ) -> ProgrammingResult:
        if "|" not in request.context:
            return ProgrammingResult(
                success=False,
                action="documentation",
                reason=(
                    "Documentation context must be "
                    "'technology|entry_name'."
                ),
            )
        technology, entry_name = (
            request.context.split("|", 1)
        )
        result = self.documentation_manager.get(
            technology,
            entry_name,
        )
        return ProgrammingResult(
            success=result.success,
            action="documentation",
            result=result,
            reason=result.reason,
        )
programming_intelligence = ProgrammingIntelligence()




