from __future__ import annotations
from typing import Any
from lxml import html
from lxml.etree import ParserError
from .analysis_types import CodeAnalysisResult
class HTMLCodeAnalyzer:
    """
    Task 6.2: HTML Code Understanding.
    Uses lxml to parse HTML structure without executing
    JavaScript or other embedded content.
    """
    API_INDICATORS = (
        "form",
        "fetch",
        "websocket",
        "iframe",
    )
    def analyze(
        self,
        source: Any,
        language: str = "HTML",
    ) -> CodeAnalysisResult:
        if not isinstance(source, str):
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error="Source code must be a string.",
            )
        try:
            document = html.fromstring(source)
        except (ParserError, ValueError, TypeError) as exc:
            return CodeAnalysisResult(
                language=language,
                valid=False,
                syntax_error=str(exc),
            )
        result = CodeAnalysisResult(
            language=language,
            valid=True,
        )
        result.imports = self._extract_resources(document)
        result.functions = self._extract_event_handlers(document)
        result.classes = self._extract_classes(document)
        result.variables = self._extract_ids(document)
        result.exceptions = []
        result.async_functions = []
        result.api_indicators = self._extract_api_indicators(
            source,
            document,
        )
        result.database_indicators = []
        return result
    @staticmethod
    def _extract_resources(document) -> list[str]:
        values = []
        for node in document.xpath("//script[@src]"):
            src = node.get("src")
            if src:
                values.append(src)
        for node in document.xpath("//link[@href]"):
            href = node.get("href")
            if href:
                values.append(href)
        return HTMLCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_event_handlers(document) -> list[str]:
        values = []
        for node in document.iter():
            for attribute in node.attrib:
                if attribute.lower().startswith("on"):
                    values.append(attribute.lower())
        return HTMLCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_classes(document) -> list[str]:
        values = []
        for node in document.iter():
            class_value = node.get("class")
            if not class_value:
                continue
            values.extend(
                item
                for item in class_value.split()
                if item
            )
        return HTMLCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_ids(document) -> list[str]:
        values = []
        for node in document.iter():
            value = node.get("id")
            if value:
                values.append(value)
        return HTMLCodeAnalyzer._unique(values)
    @staticmethod
    def _extract_api_indicators(
        source: str,
        document,
    ) -> list[str]:
        values = []
        if document.xpath("//form"):
            values.append("form")
        if document.xpath("//iframe"):
            values.append("iframe")
        lowered = source.lower()
        if "fetch(" in lowered:
            values.append("fetch")
        if "websocket" in lowered:
            values.append("websocket")
        return HTMLCodeAnalyzer._unique(values)
    @staticmethod
    def _unique(values: list[str]) -> list[str]:
        seen = set()
        result = []
        for value in values:
            if value in seen:
                continue
            seen.add(value)
            result.append(value)
        return result
html_code_analyzer = HTMLCodeAnalyzer()
