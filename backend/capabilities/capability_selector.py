from __future__ import annotations

from dataclasses import dataclass

from backend.capabilities.capability_registry import CapabilityRegistry


@dataclass(frozen=True)
class CapabilitySelection:
    capability: str
    reason: str
    confidence: str = "medium"


class CapabilitySelector:
    def __init__(self, registry: CapabilityRegistry) -> None:
        self.registry = registry

    def select(
        self,
        *,
        intent: str | None = None,
        route: str | None = None,
        domains: list[dict] | None = None,
        task_type: str | None = None,
    ) -> list[CapabilitySelection]:
        selections: list[CapabilitySelection] = []

        if task_type in {
            "code_generation",
            "debugging",
        }:
            if self.registry.has("programming"):
                selections.append(
                    CapabilitySelection(
                        capability="programming",
                        reason="The task requires programming capability.",
                        confidence="high",
                    )
                )

        if task_type == "troubleshooting":
            if self.registry.has("knowledge"):
                selections.append(
                    CapabilitySelection(
                        capability="knowledge",
                        reason="The task requires troubleshooting knowledge.",
                        confidence="medium",
                    )
                )

        
        
        if intent == "programming" or route == "programming":
            if self.registry.has("programming"):
                selections.append(
                    CapabilitySelection(
                        capability="programming",
                        reason="The request is classified as a programming task.",
                        confidence="high",
                    )
                )


        medical_domains = {
            "medical",
            "health",
        }

        if any(
            isinstance(domain, dict)
            and domain.get("domain") in medical_domains
            for domain in (domains or [])
        ):
            if self.registry.has("medical"):
                selections.append(
                    CapabilitySelection(
                        capability="medical",
                        reason="The request matches a medical or health domain.",
                        confidence="high",
                    )
                )


        if any(
            isinstance(domain, dict)
            and domain.get("domain") == "electronics"
            for domain in (domains or [])
        ):
            if self.registry.has("knowledge"):
                selections.append(
                    CapabilitySelection(
                        capability="knowledge",
                        reason="The request matches an electronics domain and requires domain knowledge.",
                        confidence="medium",
                    )
                )

        if intent == "live_information" or route == "research":
            if self.registry.has("research"):
                selections.append(
                    CapabilitySelection(
                        capability="research",
                        reason="The request requires current or externally researched information.",
                        confidence="high",
                    )
                )

        if any(
            isinstance(domain, dict)
            and domain.get("domain") in {"vision", "image", "visual"}
            for domain in (domains or [])
        ):
            if self.registry.has("vision"):
                selections.append(
                    CapabilitySelection(
                        capability="vision",
                        reason="The request requires visual or image understanding.",
                        confidence="high",
                    )
                )

        knowledge_domains = {
            "education",
            "mathematics",
            "science",
        }

        if any(
            isinstance(domain, dict)
            and domain.get("domain") in knowledge_domains
            for domain in (domains or [])
        ):
            if self.registry.has("knowledge"):
                selections.append(
                    CapabilitySelection(
                        capability="knowledge",
                        reason="The request requires domain-specific knowledge.",
                        confidence="medium",
                    )
                )


        unique_selections: list[CapabilitySelection] = []
        seen_capabilities: set[str] = set()

        for selection in selections:
            if selection.capability in seen_capabilities:
                continue

            seen_capabilities.add(selection.capability)
            unique_selections.append(selection)

        return unique_selections
       
