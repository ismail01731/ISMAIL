import json
import os
import re
import urllib.error
import urllib.request
from dotenv import load_dotenv
from backend.knowledge_base import KnowledgeBase
from backend.web_research import WebResearch
from backend.openai_provider import OpenAIProvider
from backend.browser_actions import detect_browser_action
from backend.intent_detector import IntentDetector
from backend.domain_detector import DomainDetector
from backend.live_intelligence.router import LiveIntelligenceRouter
load_dotenv("config/.env")
from typing import List
from backend.web_research import WebResearch, WebEvidence
from backend.creator_identity import get_identity_answer
from backend.llm.config import load_llm_config
from backend.llm.router import LLMRouter
from backend.medical.medical_response import MedicalResponse
from backend.vision.vision_ai import VisionAI
from backend.vision.vision_provider import OllamaVisionProvider
from backend.programming.calculator import SafeCalculator
from backend.programming.programming_intelligence import(
    ProgrammingIntelligence,
    ProgrammingRequest,
    ProgrammingResult,
)
from backend.capabilities.capability_registry import CapabilityRegistry
from backend.capabilities.capability_selector import CapabilitySelector
from backend.task_planner import TaskPlanner
from backend.capability_orchestrator import (
    CapabilityOrchestrator,
    CapabilityExecutionContext,
)
from backend.domain_knowledge_router import DomainKnowledgeRouter
from backend.programming.language_selector import LanguageSelector
from backend.research_freshness_router import ResearchFreshnessRouter
from backend.result_verifier import ResultVerifier
from backend.task_understanding import TaskUnderstandingBuilder
from backend.emotion.emotion_engine import emotion_engine
from backend.emotion.mood_state import mood_state_engine
from backend.emotion.emotion_models import EmotionalContext
from backend.emotion.companion_strategy import companion_strategy
from backend.emotion.companion_personality import companion_personality
from backend.emotion.mood_detector import mood_detector
from backend.emotion.conversation_context_builder import (
    conversation_context_builder,
)


class AIEngine:
    """Core AI engine and unified question-understanding layer for ISMAIL AI."""
    KNOWLEDGE_KEYWORDS = {
        "what is",
        "what are",
        "who is",
        "who was",
        "explain",
        "define",
        "meaning of",
        "how does",
        "how do",
        "why does",
        "why do",
        "python",
        "programming",
        "physics",
        "mathematics",
        "math",
        "science",
        "history",
        "grammar",
        "algorithm",
        "database",
        "computer",
        "coding",
    }
    LIVE_KEYWORDS = {
        "today",
        "tonight",
        "now",
        "currently",
        "current",
        "latest",
        "recent",
        "recently",
        "this week",
        "this month",
        "breaking",
        "news",
        "weather",
        "temperature",
        "forecast",
        "price",
        "prices",
        "stock",
        "score",
        "scores",
        "match",
        "matches",
        "population",
        "fire",
        "earthquake",
        "outage",
        "version",
        "release",
        "available",
        "availability",
        "status",

        "event",
        "events",
        "incident",
        "ঘটনা",
        "ঘটনাগুলো",
        "ঘটনাসমূহ",
        "গুরুত্বপূর্ণ ঘটনা",
        "বর্তমান ঘটনা",
        "সাম্প্রতিক ঘটনা",
        "কী ঘটছে",
        "কি ঘটছে",
        "কী হচ্ছে",
        "কি হচ্ছে",
        "আজ কী ঘটেছে",
        "আজ কি ঘটেছে",
        "আজ কী ঘটছে",
        "আজ কি ঘটছে",
        "এখন কী ঘটছে",
        "এখন কি ঘটছে",
        "বর্তমানে কী ঘটছে",
        "বর্তমানে কি ঘটছে",
        "আন্তর্জাতিক ঘটনা",
        "গুরুত্বপূর্ণ আন্তর্জাতিক ঘটনা",
        "incidents",
        "happening",
        "happenings",
        "what's happening",
        "what is happening",
        "ঘটনা",
        "ঘটনাগুলো",
        "ঘটনাসমূহ",
        "কী ঘটছে",
        "কি ঘটছে",
        "কী হচ্ছে",
        "কি হচ্ছে",
        "গুরুত্বপূর্ণ ঘটনা",
        "বর্তমান ঘটনা",
        "সাম্প্রতিক ঘটনা",
        "আন্তর্জাতিক ঘটনা",

        "আজ",
        "এখন",
        "বর্তমানে",
        "সর্বশেষ",
        "সাম্প্রতিকতম",
        "খবর",
        "সংবাদ",
        "আবহাওয়া",
        "আবহাওয়া",
        "তাপমাত্রা",
        "পূর্বাভাস",
        "দাম",
        "মূল্য",
        "বিটকয়েন",
        "বিটকয়েন",
        "আগামীকাল",
        "কাল",
    }



    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()
        self.web_research = WebResearch()
        self.intent_detector = IntentDetector()
        self.domain_detector = DomainDetector()
        self.llm_config = load_llm_config()
        self.llm_router = LLMRouter.create(self.llm_config)
        self.openai_provider = OpenAIProvider(self.llm_config)
        self.provider = self.llm_config.provider
        self.model = self.llm_config.model
        self.ollama_url = self.llm_config.ollama_url
        self.medical_response = MedicalResponse()
        self.calculator = SafeCalculator()
        self.result_verifier = ResultVerifier()
        self.programming_intelligence = ProgrammingIntelligence(
            llm_router=self.llm_router
        )


        self.vision_ai = VisionAI()
        self.vision_provider = OllamaVisionProvider(
            model=os.getenv("VISION_MODEL", "qwen2.5vl:7b"),
            ollama_url=self.ollama_url.replace("/api/generate", ""),
        )

        self.capability_registry = CapabilityRegistry()
        self.capability_selector = CapabilitySelector(self.capability_registry)
        self.task_planner = TaskPlanner()
        self.capability_orchestrator = CapabilityOrchestrator()
        self.domain_knowledge_router = DomainKnowledgeRouter()
        self.language_selector = LanguageSelector()
        self.research_freshness_router = ResearchFreshnessRouter()
        self.task_understanding_builder = TaskUnderstandingBuilder()




    def status(self) -> dict:
        connected = False

        if self.provider == "ollama":
            try:
                request = urllib.request.Request(
                    self.ollama_url,
                    method="GET",
                )
                with urllib.request.urlopen(request, timeout=3):
                    connected = True
            except Exception:
                connected = False

        elif self.provider in ("openai", "openrouter", "groq"):
            connected = self.openai_provider.status().get(
                "configured",
                False
            )

        return {
            "provider": self.provider or None,
            "model": self.model or None,
            "connected": connected,
        }


    
    def understand_question(self, message: str) -> dict:
        """
        Understand and classify a user message.
        The actual intent detection is handled by the modular
        IntentDetector system.
        """
        question_info = self.intent_detector.detect(message)
        domain_matches = self.domain_detector.detect(message)
        emotion_result = emotion_engine.detect(message)
        emotional_context = EmotionalContext(
            emotion=emotion_result.emotion,
            confidence=emotion_result.confidence,
            signals=emotion_result.signals,
            companion_instruction=companion_strategy.build_instruction(
                emotion_result.emotion
            ),
        )
        question_info["emotional_context"] = {
            "emotion": emotional_context.emotion,
            "confidence": emotional_context.confidence,
            "signals": emotional_context.signals,
            "companion_instruction": (
                emotional_context.companion_instruction
            ),
        }
        question_info["domains"] = [
            {
                "domain": match.domain,
                "confidence": match.confidence,
                "matches": match.matches,
            }
            for match in domain_matches
        ]
        # Step 7: determine available stable knowledge routes first.
        knowledge_routes = self.domain_knowledge_router.route(
            domains=question_info["domains"]
        )
        question_info["knowledge_routes"] = [
            {
                "domain": route.domain,
                "source": route.source,
                "reason": route.reason,
                "confidence": route.confidence,
            }
            for route in knowledge_routes
        ]
        has_knowledge_source = any(
            route.source == "knowledge"
            for route in knowledge_routes
        )
        # Step 7: a knowledge route can come either from the
        # domain router or directly from the intent route.
        knowledge_route_selected = (
            question_info.get("route") == "knowledge"
            or has_knowledge_source
        )
        # Check whether the existing Knowledge Base actually
        # contains a valid, non-expired answer.
        stored_knowledge = None
        if knowledge_route_selected:
            try:
                stored_knowledge = self.knowledge_base.get(message)
            except Exception:
                stored_knowledge = None
        knowledge_sufficient = stored_knowledge is not None
        question_info["knowledge_sufficiency"] = {
            "available": knowledge_route_selected,
            "sufficient": knowledge_sufficient,
            "found": knowledge_sufficient,
            "reason": (
                "A valid stored knowledge answer was found."
                if knowledge_sufficient
                else "No valid stored knowledge answer was found."
            ),
        }
        research_freshness_decision = self.research_freshness_router.decide(
            message=message,
            intent=question_info.get("intent"),
            route=question_info.get("route"),
            domains=question_info.get("domains"),
        )
        question_info["research_freshness"] = {
            "needs_research": research_freshness_decision.needs_research,
            "freshness_required": (
                research_freshness_decision.freshness_required
            ),
            "reason": research_freshness_decision.reason,
            "confidence": research_freshness_decision.confidence,
        }
        # Step 7 source decision:
        # fresh/current/explicit research -> research
        # stable knowledge route -> knowledge
        # otherwise -> general
        if research_freshness_decision.needs_research:
            source_decision = "research"
            source_reason = research_freshness_decision.reason
            source_confidence = research_freshness_decision.confidence
        elif knowledge_sufficient:
            source_decision = "knowledge"
            source_reason = (
                "A valid existing knowledge answer is available."
            )
            source_confidence = "high"
        elif knowledge_route_selected:
            source_decision = "general"
            source_reason = (
                "A knowledge route exists, but no valid stored answer "
                "was found, so the request falls back to general AI."
            )
            source_confidence = "medium"
        else:
            source_decision = "general"
            source_reason = (
                "No specialized knowledge or fresh research route "
                "was selected."
            )
            source_confidence = "medium"
        question_info["source_decision"] = {
            "source": source_decision,
            "reason": source_reason,
            "confidence": source_confidence,
        }
        medical_assessment = self.medical_response.assess(message)
        if medical_assessment.is_medical:
            question_info["risk_level"] = (
                "high"
                if medical_assessment.urgency == "emergency"
                else "medium"
            )
        else:
            question_info["risk_level"] = "low"
        task_understanding = self.task_understanding_builder.build(
            message=message,
            question_info=question_info,
        )
        question_info["task_understanding"] = {
            "message": task_understanding.message,
            "goal": task_understanding.goal,
            "intent": task_understanding.intent,
            "domains": task_understanding.domains,
            "task_type": task_understanding.task_type,
            "constraints": task_understanding.constraints,
            "required_information": (
                task_understanding.required_information
            ),
            "subtasks": task_understanding.subtasks,
            "freshness_required": task_understanding.freshness_required,
            "risk_level": task_understanding.risk_level,
            "confidence": task_understanding.confidence,
        }
        capability_selections = self.capability_selector.select(
            intent=question_info.get("intent"),
            route=question_info.get("route"),
            domains=question_info.get("domains"),
            task_type=question_info.get(
                "task_understanding", {}
            ).get("task_type"),
            source_decision=question_info.get("source_decision"),
        )
        question_info["capabilities"] = [
            {
                "capability": selection.capability,
                "reason": selection.reason,
                "confidence": selection.confidence,
            }
            for selection in capability_selections
        ]
        if any(
            isinstance(item, dict)
            and item.get("capability") == "programming"
            for item in question_info["capabilities"]
        ):
            language_domain = None
            if "android" in programming_text or "android app" in programming_text:
                language_domain = "android"
            elif "backend" in programming_text or "back-end" in programming_text:
                language_domain = "backend"
            elif "frontend" in programming_text or "front-end" in programming_text:
                language_domain = "frontend"
            elif "website" in programming_text or "web application" in programming_text or "web app" in programming_text:
                language_domain = "web"

            language_selection = self.language_selector.select(
                requirement=message,
                domain=language_domain or (
                    question_info["domains"][0].get("domain")
                    if question_info.get("domains")
                    and isinstance(question_info["domains"][0], dict)
                    else None
                ),
            )
            if language_selection is not None:
                question_info["programming_language"] = {
                    "language": language_selection.language,
                    "reason": language_selection.reason,
                    "confidence": language_selection.confidence,
                }
        question_info["task_plan"] = self.task_planner.create_plan(
            capabilities=question_info["capabilities"]
        )
        return question_info

    def _format_structured_live_evidence(
        self,
        evidence: List[WebEvidence],
    ) -> str:
        """Format structured live evidence deterministically."""

        sections = []

        weather_items = []
        bitcoin_items = []
        news_items = []

        for item in evidence:
            title = str(
                getattr(item, "title", "") or ""
            ).strip()

            source = str(
                getattr(item, "source", "") or ""
            ).strip()



            content = str(
                getattr(item, "content", "") or ""
            ).strip()

            snippet = str(
                getattr(item, "snippet", "") or ""
            ).strip()

            if not content:
                content = snippet



            

            title_lower = title.lower()

            if "weather" in title_lower:
                weather_items.append(
                    {
                        "title": title,
                        "source": source,
                        "content": content,
                    }
                )
                continue

            if (
                "bitcoin" in title_lower
                or "btc" in title_lower
                or "coingecko" in source.lower()
                or "coinbase" in source.lower()
            ):
                bitcoin_items.append(
                    {
                        "title": title,
                        "source": source,
                        "content": content,
                    }
                )
                continue

            if (
                getattr(item, "verification_status", "")
                in ("verified", "corroborated")
            ):
                if title:
                    news_items.append(
                        {
                            "title": title,
                            "source": source,
                        }
                    )

        # ---------------------------------------------------------
        # WEATHER
        # ---------------------------------------------------------

        for item in weather_items:
            content = item["content"]

            allowed_fields = {
                "Location",
                "Observation time",
                "Forecast date",
                "Temperature",
                "Feels like",
                "Relative humidity",
                "Precipitation",
                "Rain",
                "Showers",
                "Snowfall",
                "Wind speed",
                "Weather condition",
                "Minimum",
                "Maximum",
                "Precipitation probability",
            }

            field_values = {}

            for raw_line in content.splitlines():
                line = raw_line.strip()

                if not line or ":" not in line:
                    continue

                field, value = line.split(":", 1)

                field = field.strip()
                value = value.strip()

                if field not in allowed_fields:
                    continue

                if not value:
                    continue

                field_values[field] = value

            if not field_values:
                continue

            weather_lines = [
                f"- {field}: {field_values[field]}"
                for field in (
                    "Location",
                    "Observation time",
                    "Forecast date",
                    "Temperature",
                    "Feels like",
                    "Relative humidity",
                    "Precipitation",
                    "Rain",
                    "Showers",
                    "Snowfall",
                    "Wind speed",
                    "Weather condition",
                    "Minimum",
                    "Maximum",
                    "Precipitation probability",
                )
                if field in field_values
            ]

            if weather_lines:
                sections.append(
                    f"{item['title']}\n"
                    f"Source: {item['source']}\n"
                    + "\n".join(weather_lines)
                )

        # ---------------------------------------------------------
        # BITCOIN
        # ---------------------------------------------------------

        for item in bitcoin_items:
            content = item["content"]

            bitcoin_lines = []

            for raw_line in content.splitlines():
                line = raw_line.strip()

                if not line or ":" not in line:
                    continue

                field, value = line.split(":", 1)

                field = field.strip()
                value = value.strip()

                if field in (
                    "Current price",
                    "24-hour change",
                ):
                    if value:
                        bitcoin_lines.append(
                            f"- {field}: {value}"
                        )

            if bitcoin_lines:
                sections.append(
                    f"{item['title']}\n"
                    f"Source: {item['source']}\n"
                    + "\n".join(bitcoin_lines)
                )

        # ---------------------------------------------------------
        # NEWS
        # ---------------------------------------------------------

        if news_items:
            news_lines = [
                f"- {item['title']} ({item['source']})"
                for item in news_items
            ]

            sections.append(
                "LATEST VERIFIED NEWS\n"
                "====================\n"
                + "\n".join(news_lines)
            )

        if not sections:
            return ""

        return (
            "VERIFIED LIVE DATA\n"
            "==================\n\n"
            + "\n\n".join(sections)
        )






    


    def _build_grounded_prompt(
        self,
        question: str,
        evidence: List[WebEvidence],
    ) -> str:
        """Build a strict prompt for answers grounded only in live evidence."""

        verified = [
            item
            for item in evidence
            if getattr(item, "verification_status", "")
            in ("corroborated", "verified")
        ]

        if not verified:
            return (
                "You are ISMAIL AI.\n"
                "The user asked a current factual question, but no reliable "
                "verified evidence is available.\n\n"
                "STRICT RULES:\n"
                "- Do not answer the current factual question from memory.\n"
                "- Do not guess.\n"
                "- Do not invent facts, numbers, dates, prices, temperatures, "
                "weather conditions, scores, headlines, or availability.\n"
                "- Clearly say that reliable current information could not be "
                "verified.\n\n"
                f"USER QUESTION:\n{question}\n"
            )

        evidence_lines = []

        for index, item in enumerate(verified, start=1):
            title = str(getattr(item, "title", "") or "").strip()
            source = str(getattr(item, "source", "") or "").strip()
            url = str(getattr(item, "url", "") or "").strip()
            snippet = str(getattr(item, "snippet", "") or "").strip()
            content = str(getattr(item, "content", "") or "").strip()

            evidence_lines.append(
                f"[EVIDENCE {index}]\n"
                f"TITLE: {title}\n"
                f"SOURCE: {source}\n"
                f"URL: {url}\n"
                f"SNIPPET: {snippet}\n"
                f"CONTENT: {content}\n"
            )

        evidence_text = "\n".join(evidence_lines)

        return (
            "You are ISMAIL AI, a careful factual assistant.\n"
            "Answer the user's current question using ONLY the verified "
            "evidence supplied below.\n\n"

            "For broad current-event questions, begin with a concise summary and "
            "then give 2-5 bullet points of distinct reported developments when "
            "the evidence supports them. Do not imply that the list is exhaustive.\n\n"

            "==================== ABSOLUTE GROUNDING RULES ====================\n"

            "1. Use ONLY facts explicitly present in the supplied evidence.\n"

            "2. NEVER use pretrained knowledge, memory, assumptions, guesses, "
            "common sense, or outside information to fill gaps.\n"

            "3. NEVER invent a missing value.\n"

            "4. NEVER estimate a value when the evidence does not explicitly "
            "provide it.\n"

            "5. NEVER change, round, convert, reinterpret, or substitute a "
            "numerical value unless the user explicitly asks for conversion.\n"

            "6. Preserve the meaning of every evidence field exactly.\n"

            "7. Do NOT rename one evidence field into another field.\n"

            "8. For current news, events, incidents, or 'what is happening now' "
            "questions, do NOT generalize from one article to the whole world, country, "
            "or population.\n"
            "9. Report only the specific events or developments explicitly supported "
            "by the evidence.\n"
            "10. If multiple evidence items describe the same event, combine them "
            "into one concise point instead of repeating the same event.\n"
            "11. If the evidence covers only one or a few events, explicitly say that "
            "these are among the notable reported developments rather than claiming "
            "they represent everything happening.\n"
            "12. NEVER invent attendance numbers, leaders, countries, reactions, "
            "casualties, causes, locations, or other details that are not explicitly "
            "present in the evidence.\n"
            "13. For a broad current-event question, identify distinct real-world "
            "events supported by the evidence. If multiple evidence items refer to "
            "the same event, mention that event only once. If only one distinct event "
            "is supported, provide only that event rather than inventing additional "
            "events.\n"
            "14. Do NOT use phrases such as 'প্রথম প্রমাণ', 'দ্বিতীয় প্রমাণ', "
            "'প্রথম evidence', or 'দ্বিতীয় evidence' in the final answer.\n"
            "15. Use natural conversational language. Do not describe the evidence "
            "itself; describe the reported events.\n"
            "16. Do NOT create a bullet point merely because multiple sources "
            "reported the same event. Sources are supporting evidence, not events.\n"
            "17. Do NOT mention 'media sources', 'evidence', 'sources', or "

            "18. Multiple evidence items may describe the same real-world event. "
            "Treat repeated coverage of the same event as ONE event with multiple "
            "supporting sources, not as separate events.\n"
            "19. Never infer a new event merely from a source name, URL, or article "
            "title fragment. An event must be explicitly supported by the evidence "
            "text.\n"
            "20. If the available evidence is narrowly focused on one event, say so "
            "clearly. Do not pretend that it represents all events happening "
            "worldwide.\n"

            "21. SOURCE, URL, TITLE, and publisher names are metadata. "
            "Never treat a source name, URL, or publisher name as factual evidence.\n"
            "22. A headline alone does not prove every detail implied by the headline. "
            "Only state details that are explicitly supported by the supplied evidence text.\n"
            "23. When several evidence items describe the same named event, location, "
            "date, anniversary, ceremony, incident, or development, merge them into "
            "ONE event. The number of sources must never become the number of events.\n"
            "24. Do not create a separate event merely because another source has a "
            "different headline describing the same underlying event.\n"
            "25. Do not say 'বিশ্বব্যাপী', 'বিভিন্ন দেশ থেকে', 'সারা বিশ্বে', "
            "'অনেক মানুষ', 'বিভিন্ন স্থানে', or similar broad claims unless those "
            "claims are explicitly supported by the evidence text.\n"
            "26. For broad current-event questions, if all verified evidence concerns "
            "one underlying event, report only that one event and clearly state that "
            "the currently retrieved evidence is focused on that event.\n"


            "'evidence items' in the answer unless the user explicitly asks about "
            "sources or verification.\n"


            "   Examples:\n"
            "   - 'Feels like' must remain 'Feels like'.\n"
            "   - 'Wind speed' must remain 'Wind speed'.\n"
            "   - 'Showers' must remain 'Showers'.\n"
            "   - 'Rain' must remain 'Rain'.\n"
            "   - 'Precipitation' must remain 'Precipitation'.\n"
            "   - 'Relative humidity' must remain 'Relative humidity'.\n"

            "8. Never translate a technical weather condition into a different "
            "weather condition.\n"
            "   For example, if the evidence says 'Overcast', do NOT call it "
            "'Clear', 'Sunny', or 'মেঘমুক্ত'.\n"

            "9. If the evidence says 'Thunderstorm with slight hail', preserve "
            "that exact meaning. Do NOT simplify it to merely 'Rain' or "
            "'Light rain'.\n"

            "10. Weather condition names are factual data, not suggestions "
            "for creative translation.\n"

            "11. For weather data, preserve the original field/value pairing.\n"
            "    Do not move a value from one field to another.\n"

            "12. If a value is present in the evidence, copy that value "
            "faithfully.\n"

            "13. If a value is NOT present in the evidence, do not create it.\n"

            "14. If the evidence contains several separate live questions, "
            "answer each question separately.\n"

            "15. Match each answer to the correct evidence item.\n"

            "16. Do not combine today's weather with tomorrow's weather.\n"

            "17. Do not combine current Bitcoin price with historical price.\n"

            "18. Do not combine one news article's facts with another article.\n"

            "19. For news questions, the TITLE and SOURCE of each evidence item "
            "are authoritative.\n"

            "20. When presenting a news headline, preserve the evidence TITLE "
            "exactly whenever practical.\n"

            "21. Do not invent a headline that is not present in evidence.\n"

            "22. When several verified news items are available, present "
            "several relevant headlines instead of pretending that only one "
            "news item exists.\n"

            "23. Do not claim that a news item is 'the most important' unless "
            "the evidence explicitly establishes that.\n"

            "24. Do not add opinions such as 'probably', 'likely', or "
            "'it seems' to factual live data unless the evidence itself says so.\n"

            "25. Do not fabricate explanations for weather, Bitcoin, or news "
            "unless the explanation is explicitly supported by evidence.\n"

            "26. If evidence conflicts, do not silently choose a value. "
            "Clearly mention the conflict and identify the differing sources.\n"

            "27. If the evidence is insufficient for one part of the question, "
            "say that the available evidence does not verify that specific part.\n"

            "28. The user's language should determine the answer language. "
            "If the user writes Bangla, answer naturally in Bangla while "
            "preserving important technical field names in English when that "
            "prevents meaning from changing.\n"

            "29. Keep factual precision more important than stylistic fluency.\n"

            "30. NEVER sacrifice factual accuracy to make the answer sound "
            "more natural.\n"
            "31. For structured live data, prefer the original English field "
            "names and values from the evidence rather than translating or "
            "paraphrasing technical terms.\n"

            "32. For weather condition, copy the exact condition text from "
            "the evidence. Do not translate it into a different phrase.\n"

            "33. For example, 'Overcast' must be written as 'Overcast' and "
            "must not become 'ঘন মেঘ', 'মেঘলা', 'মেঘাচ্ছন্ন', or another "
            "interpretation.\n"

            "34. For example, 'Thunderstorm with slight hail' must be "
            "written exactly as 'Thunderstorm with slight hail'. Do not "
            "replace it with 'Rain', 'Light rain', 'বৃষ্টি', 'বৃষ্টির সাথে "
            "মেঘ', or any other interpretation.\n"

            "35. For numerical weather fields, preserve the exact value and "
            "the exact field association from the evidence.\n"

            "36. Do not add a conclusion such as 'বৃষ্টি নেই' unless the "
            "evidence explicitly supports that conclusion and the conclusion "
            "is directly derived from the relevant field.\n"

            "37. Do not use phrases such as 'ঠান্ডা হবে না', 'বেশ গরম হবে', "
            "'বিকুল আকাশ', or similar descriptive interpretations unless "
            "those exact facts are present in the evidence.\n"

            "38. For news headlines, copy the TITLE from the evidence exactly. "
            "Do not paraphrase, summarize, translate, shorten, or rewrite "
            "the headline when presenting it as a headline.\n"

            "39. When multiple verified news evidence items are available, "
            "include multiple relevant titles rather than selecting only one "
            "unless the user explicitly asks for one.\n"

            "==================== WEATHER OUTPUT RULE ====================\n"

            "For weather questions, use a clear field-based format when "
            "multiple measurements are available.\n"

            "Use the following conceptual mapping only:\n"
            "- Temperature → Temperature\n"
            "- Feels like → Feels like\n"
            "- Relative humidity → Relative humidity\n"
            "- Precipitation → Precipitation\n"
            "- Rain → Rain\n"
            "- Showers → Showers\n"
            "- Snowfall → Snowfall\n"
            "- Wind speed → Wind speed\n"
            "- Weather condition → Weather condition\n"
            "- Minimum → Minimum temperature\n"
            "- Maximum → Maximum temperature\n"
            "- Precipitation probability → Precipitation probability\n"

            "Do not invent additional weather fields.\n"

            "==================== BITCOIN OUTPUT RULE ====================\n"

            "For Bitcoin questions, use only the supplied current price and "
            "24-hour change when those values exist.\n"

            "Do not invent market direction, trading advice, historical prices, "
            "market cap, volume, or future predictions.\n"

            "==================== NEWS OUTPUT RULE ====================\n"

            "For news questions:\n"
            "- Use only supplied verified news evidence.\n"
            "- Prefer multiple relevant verified headlines when available.\n"
            "- Keep each headline attached to its own source.\n"
            "- Do not merge facts from different articles.\n"
            "- Do not invent a ranking unless evidence provides one.\n"
            "- Do not call something 'breaking' unless the evidence supports it.\n"

            "==================== EVIDENCE ====================\n"
            f"{evidence_text}\n"
            "==================== END EVIDENCE ====================\n\n"

            "CURRENT USER QUESTION:\n"
            f"{question}\n\n"

            "FINAL INSTRUCTION:\n"
            "Answer the user now.\n\n"

            "STRICT SOURCE-BOUND MODE:\n"
            "Every factual statement in your answer MUST be directly supported "
            "by the supplied evidence text.\n"
            "If a fact is not explicitly present in the evidence, DO NOT say it.\n"
            "Do not infer, assume, explain, interpret, or complete missing details.\n"
            "Do not use your general knowledge to fill gaps.\n\n"

            "IMPORTANT FOR BROAD CURRENT-EVENT QUESTIONS:\n"
            "If the evidence only supports one event or one topic, report ONLY "
            "that supported event or topic.\n"
            "Do not turn five sources about the same event into five different events.\n"
            "Do not add people, countries, locations, organizations, attendance, "
            "opinions, causes, consequences, casualties, ceremonies, or reactions "
            "unless explicitly stated in the evidence.\n\n"

            "IMPORTANT FOR HEADLINE-ONLY EVIDENCE:\n"
            "If the supplied evidence mainly contains headlines and does not contain "
            "supporting factual details, DO NOT invent details from the headlines.\n"
            "In that situation, present the exact supported headline(s) and source "
            "rather than explaining facts that are not explicitly available.\n\n"

            "NEVER COMPLETE A SENTENCE WITH AN UNSUPPORTED FACT.\n"
            "NEVER GUESS WHAT HAPPENED.\n"
            "NEVER ADD DETAILS JUST TO MAKE THE ANSWER LONGER.\n\n"

            "Prefer a short answer over an unsupported answer.\n"
        )

    def _clean_live_response(
        self,
        response: str,
        evidence: list,
    ) -> str:
        """Keep live answers concise and remove obvious unsupported output."""

        response = str(response).strip()

        if not response:
            return "দুঃখিত, নির্ভরযোগ্য তথ্য থেকে উত্তর তৈরি করা যায়নি।"

        # Remove incomplete trailing sentence/bullet.
        lines = response.splitlines()

        cleaned = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            cleaned.append(line)

        if not cleaned:
            return "দুঃখিত, নির্ভরযোগ্য তথ্য থেকে উত্তর তৈরি করা যায়নি।"

        # Keep the answer short for small local models.
        cleaned = cleaned[:6]

        return "\n".join(cleaned).strip()




    def _format_verified_live_answer(
        self,
        question: str,
        evidence: list,
    ) -> str:
        """Build a safe live answer from verified evidence."""

        verified = [
            item
            for item in evidence
            if getattr(item, "verification_status", "")
            in (
                "verified",
                "corroborated",
                "high_confidence_source",
            )
        ]

        if not verified:
            return "দুঃখিত, নির্ভরযোগ্য তথ্য যাচাই করা যায়নি।"

        # ---------------------------------------------------------
        # Normalize headline for safe same-event comparison.
        # ---------------------------------------------------------
        def normalize_title(title: str) -> set:
            text = (title or "").lower()

            # Normalize explicit date/event identifiers.
            text = re.sub(
                r"\b(sept|sep|september)\s+(\d{1,2})\b",
                r"9-\2",
                text,
            )

            text = re.sub(
                r"(\d+)\s*/\s*(\d+)",
                r"\1-\2",
                text,
            )

            # Keep normalized event identifiers intact.
            text = text.replace("9-11", "event911")

            text = re.sub(
                r"[^a-z0-9\u0980-\u09ff-]+",
                " ",
                text,
            )

            stop_words = {
                "the", "a", "an", "and", "or", "of",
                "to", "in", "on", "for", "with", "at",
                "is", "are", "was", "were",
                "this", "that", "its", "about",
                "live", "watch", "news", "today",
                "latest", "updates", "gather",
                "remember", "remembering",

                "years", "year", "later",
                "ceremony", "site", "marks",
                "gather", "divided", "legacy",
                "those", "lost",

                "আজ", "আজকের", "এখন", "বর্তমানে",
                "সর্বশেষ", "খবর", "সংবাদ", "গুরুত্বপূর্ণ",
                "ঘটনা", "ঘটনাগুলো", "ঘটনাসমূহ",
            }

            return {
                word
                for word in text.split()
                if len(word) > 1
                and word not in stop_words
            }

        # ---------------------------------------------------------
        # Group only when headlines have strong word overlap.
        # This avoids treating unrelated events as one event.
        # ---------------------------------------------------------
        groups = []

        for item in verified[:5]:
            title = str(
                getattr(item, "title", "") or ""
            ).strip()

            if not title:
                continue



            words = normalize_title(title)

            # Detect strong canonical event identifiers.
            event_markers = set()

            if re.search(
                r"\b9\s*[-/]\s*11\b"
                r"|\bsept(?:ember)?\s+11\b"
                r"|\b11\s+september\b",
                title,
                re.IGNORECASE,
            ):
                event_markers.add("event_9_11")

            matched_group = None

            for group in groups:
                # Strong event marker match.
                if event_markers & group["event_markers"]:
                    matched_group = group
                    break

                common = words & group["words"]

                distinctive_common = {
                    word
                    for word in common
                    if len(word) >= 4
                    and word not in {
                        "live",
                        "watch",
                        "news",
                        "today",
                        "latest",
                        "event",
                        "events",
                        "remember",
                        "remembering",
                    }
                }

                if len(distinctive_common) >= 2:
                    matched_group = group
                    break



            

            if matched_group is not None:
                matched_group["items"].append(item)
                matched_group["words"].update(words)
                matched_group["event_markers"].update(event_markers)
            else:
                groups.append(
                    {
                        "items": [item],
                        "words": set(words),
                        "event_markers": set(event_markers),
                    }
                )

        if not groups:
            return "দুঃখিত, নির্ভরযোগ্য তথ্য থেকে উত্তর তৈরি করা যায়নি।"

        lines = [
            "সর্বশেষ যাচাই করা তথ্য অনুযায়ী:"
        ]

        # ---------------------------------------------------------
        # Format each distinct event/topic once.
        # ---------------------------------------------------------
        for group in groups:
            items = group["items"]

            first = items[0]

            title = str(
                getattr(first, "title", "") or ""
            ).strip()

            if not title:
                continue

            sources = []

            for item in items:
                source = str(
                    getattr(item, "source", "") or ""
                ).strip()

                if source and source not in sources:
                    sources.append(source)

            event_markers = group.get(
                "event_markers",
                set(),
            )



        # -----------------------------------------
        # Safe Bengali formatting for known events.
        # -----------------------------------------

        if "event_9_11" in event_markers:
            event_text = (
                "9/11-এর ২৫তম বার্ষিকী নিয়ে "
                "স্মরণ ও সাম্প্রতিক প্রতিবেদন"
            )
        else:
            # Unknown event:
            # Do not invent a Bengali summary.
            event_text = title

        source = str(
            getattr(item, "source", "") or ""
        ).strip()

        if source and source not in sources:
            sources.append(source)

        if len(sources) > 1:
            source_text = ", ".join(sources)
            lines.append(
                f"• {event_text} — {source_text}"
            )
        elif sources:
            lines.append(
                f"• {event_text} — {sources[0]}"
            )
        else:
            lines.append(
                f"• {event_text}"
            )

            if len(lines) == 1:
                return "দুঃখিত, নির্ভরযোগ্য তথ্য থেকে উত্তর তৈরি করা যায়নি।"

        return "\n".join(lines)








    
    def _generate_with_ollama(self, prompt: str) -> str:
        """Generate an answer from Ollama using the supplied grounded prompt."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "num_predict": 400,
                "temperature": 0.05,
                "top_p": 0.8,
                "repeat_penalty": 1.15,
            },
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            self.ollama_url,
            data=data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Unable to connect to Ollama. Make sure Ollama is running."
            ) from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Ollama returned an invalid response."
            ) from exc
        response_text = str(result.get("response", "")).strip()
        if not response_text:
            raise RuntimeError("Ollama returned an empty response.")
        return response_text


    def _build_memory_context(self, user_id: str) -> str:
        if not user_id:
            return ""

        memories = self.knowledge_base.get_memories(user_id)
        if not memories:
            return ""

        lines = []
        for key, value in memories.items():
            lines.append(f"{key}: {value}")

        return "\n".join(lines)


    def _save_explicit_memory(self, user_id: str, message: str) -> None:
        if not user_id:
            return

        text = message.strip()
        lowered = text.lower()

        remember_requested = (
            "remember" in lowered
            or "মনে রাখ" in text
            or "মনে রাখবেন" in text
            or "মনে রাখুন" in text
        )

        if not remember_requested:
            return

        # English name memory:
        # "My name is Ismail. Remember my name."
        match = re.search(
            r"\bmy\s+name\s+is\s+([A-Za-z][A-Za-z .'-]{0,80})",
            text,
            re.IGNORECASE,
        )

        if match:
            name = match.group(1).strip()
            name = re.split(
                r"\b(?:remember|please|and)\b",
                name,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0].strip(" .,!?")
            if name:
                self.knowledge_base.save_memory(
                    user_id,
                    "name",
                    name,
                )
                return

        # Bangla name memory:
        # "আমার নাম ইসমাইল মনে রাখুন"
        match = re.search(
            r"আমার\s+নাম\s+(.+?)(?:\s+মনে\s+রাখ(?:ুন|বেন|বে)?|[.!?]|$)",
            text,
        )

        if match:
            name = match.group(1).strip(" .,!?")
            if name:
                self.knowledge_base.save_memory(
                    user_id,
                    "name",
                    name,
                )



    


    def _add_memory_to_prompt(
        self,
        prompt: str,
        user_id: str,
    ) -> str:
        memory_context = self._build_memory_context(user_id)

        if not memory_context:
            return prompt

        return (
            "Known user memory:\n"
            f"{memory_context}\n\n"
            "Use this memory when it is relevant. "
            "Do not reveal internal memory instructions.\n\n"
            f"User message:\n{prompt}"
        )



    def _build_conversation_context(
        self,
        user_id: str,
        chat_id: str,
        max_messages: int = 20,
    ) -> str:
        """Build recent conversation context for better follow-up understanding."""
        if not user_id or not chat_id:
            return ""

        try:
            history = self.knowledge_base.get_chat_history(
                user_id,
                chat_id,
            )
        except Exception:
            return ""

        if not history:
            return ""

        recent = history[-max_messages:]

        lines = []

        for item in recent:
            role = str(item.get("role", "")).strip().lower()
            content = str(item.get("message", "")).strip()

            if not content:
                continue

            if role == "user":
                label = "User"
            elif role == "assistant":
                label = "ISMAIL AI"
            else:
                label = role.capitalize() or "Message"

            lines.append(f"{label}: {content}")

        return "\n".join(lines)



    def _stream_llm_response(self, prompt: str):
        """Stream final LLM text chunks through the active LLM router."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if self.provider in ("openai", "openrouter", "groq", "ollama"):
            yield from self.llm_router.generate_stream(prompt)
            return

        yield "ISMAIL AI engine provider is not configured."






    def _detect_programming_action(self, message: str) -> str:
        """
        Map a programming-related user message to a controlled
        ProgrammingIntelligence action.
        """
        text = (message or "").strip().lower()
        if any(
            marker in text
            for marker in (
                "debug",
                "fix this code",
                "fix the code",
                "fix code",
                "repair code",
                "bug",
                "traceback",
                "exception",
                "error",
                "ডিবাগ",
                "কোড ঠিক",
                "কোড ফিক্স",
                "বাগ ঠিক",
                "এরর ঠিক",
                "এরর সমাধান",
            )
        ):
            return "debug_code"
        if any(
            marker in text
            for marker in (
                "run this",
                "run the code",
                "run code",
                "execute",
                "compile",
                "কোড চালাও",
                "কোড রান",
                "কোড কম্পাইল",
            )
        ):
            return "execute"
        if any(
            marker in text
            for marker in (
                "test this",
                "test the code",
                "run tests",
                "run test",
                "unit test",
                "কোড টেস্ট",
                "কোড পরীক্ষা",
                "টেস্ট চালাও",
            )
        ):
            return "run_tests"
        if any(marker in text for marker in (
            "analyze this project",
            "analyze the project",
            "analyze project",
            "review this project",
            "inspect this project",
            "analyze this code",
            "analyze the code",
            "review this code",
            "inspect this code",
            "analyze this python code",
            "analyze this python project",
            "analyze python code",
            "কোড বিশ্লেষণ",
            "কোড অ্যানালাইস",
            "প্রজেক্ট বিশ্লেষণ",
            "প্রজেক্ট অ্যানালাইস",
            "code analyze",
            "code analyse",
        )):
            if "project" in text or "প্রজেক্ট" in text:
                return "analyze_project"
            return "analyze_code"
        

        if any(
            marker in text
            for marker in (
                "documentation",
                "documentation for",
                "api docs",
                "api documentation",
                "ডকুমেন্টেশন",
                "ডকুমেন্টেশন তৈরি",
                "এপিআই ডকুমেন্টেশন",
            )
        ):
            return "documentation"
        if any(
            marker in text
            for marker in (
                "version",
                "compatible",
                "compatibility",
                "ভার্সন",
                "কম্প্যাটিবল",
                "সামঞ্জস্যপূর্ণ",
            )
        ):
            return "check_version"
        return "generate_code"
    @staticmethod
    def _extract_calculation_expression(message: str) -> str:
        text = (message or "").strip()
        if not text:
            return ""
        # A pure arithmetic expression can be sent directly.
        import re
        if re.fullmatch(r"[0-9+\-*/%().\s]+", text):
            return text
        # Extract arithmetic from common calculation phrases.
        patterns = (
            r"^(?:calculate|calculation|calculator|compute)\s+(.+)$",
            r"^what\s+is\s+(.+)$",
            r"^how\s+much\s+is\s+(.+)$",
        )
        for pattern in patterns:
            match = re.match(pattern, text, flags=re.IGNORECASE)
            if match:
                expression = match.group(1).strip()
                if re.fullmatch(
                    r"[0-9+\-*/%().\s]+",
                    expression,
                ):
                    return expression
        return text
    def generate(
        self,
        message: str,
        user_id: str = "",
        file_context: str = "",
        chat_id: str = "",
        image_bytes: bytes | None = None,
        image_type: str = "",
    ) -> str:

        
        """Generate a final answer using knowledge, live evidence, or general AI."""
        message = message.strip()

        if image_bytes is not None:
            prompt = self.vision_ai.prepare_for_analysis(
                image_bytes,
                image_type,
                message,
            )
            return self.vision_provider.analyze(
                image_bytes,
                prompt,
            )


        if not message:
            raise ValueError("Message cannot be empty.")

        # ================================
        # MEDICAL SAFETY ROUTER
        # ================================

        medical_assessment = self.medical_response.assess(message)

        if medical_assessment.is_medical:
            if medical_assessment.urgency == "emergency":
                return medical_assessment.response


        # =========================================================
        # LIVE INTELLIGENCE: TIME / DATE
        # =========================================================

        live_result = LiveIntelligenceRouter.handle(message)

        if live_result is not None:
            if live_result["type"] == "time":
                return (
                    f"এখন সময় {live_result['time_12']}। "
                    f"সময় অঞ্চল: {live_result['timezone']}।"
                )

            if live_result["type"] == "date":
                return (
                    f"আজ {live_result['date']}। "
                    f"বার: {live_result['day']}।"
                )

        identity_answer = get_identity_answer(message)

        if identity_answer is not None:
            return identity_answer

        emotion_result = emotion_engine.detect(message)

        companion_instruction = companion_strategy.build_instruction(
            emotion_result.emotion
        )
        personality = companion_personality.get_default()
        personality_instruction = (
            f"Personality traits: {', '.join(personality.traits)}. "
            f"Communication style: {personality.communication_style} "
            f"Safety boundaries: {' '.join(personality.safety_boundaries)}"
        )

        user_id = str(user_id).strip()
        chat_id = str(chat_id).strip()

        conversation_context = self._build_conversation_context(
            user_id,
            chat_id,
        )

        mood_state = mood_state_engine.detect(
            message,
            context=conversation_context,
        )

        mood_result = mood_detector.detect(emotion_result)

        conversation_emotion_context = (
            conversation_context_builder.build(
                emotional_context=EmotionalContext(
                    emotion=emotion_result.emotion,
                    confidence=emotion_result.confidence,
                    signals=emotion_result.signals,
                    companion_instruction=companion_instruction,
                ),
                mood_result=mood_result,
                conversation_context=conversation_context,
            )
        )

        self._save_explicit_memory(
            user_id,
            message,
        )


        browser_action = detect_browser_action(message)

        if browser_action["action"] != "none":
            return json.dumps(browser_action)

        question_info = self.understand_question(message)
        question_info["conversation_emotion_context"] = {
            "emotion": conversation_emotion_context.emotion,
            "mood": conversation_emotion_context.mood,
            "confidence": conversation_emotion_context.confidence,
            "signals": conversation_emotion_context.signals,
            "companion_instruction": (
                conversation_emotion_context.companion_instruction
            ),
            "conversation_context": (
                conversation_emotion_context.conversation_context
            ),
        }

        task_understanding = question_info.get(
            "task_understanding",
            {}
        )

        research_freshness = question_info.get(
            "research_freshness",
            {}
        )

        needs_research = bool(
            research_freshness.get("needs_research")
        )
        # Personal emotional messages should not trigger web research.
        emotional_intents = {
            "sad",
            "lonely",
            "happy",
            "angry",
            "stressed",
            "excited",
            "fun",
            "romantic",
            "confused",
        }
        if emotion_result.emotion in emotional_intents:
            needs_research = False


        route = question_info["route"]
        task_plan = question_info.get("task_plan", [])
        capability_context = CapabilityExecutionContext(
            message=message,
            intent=question_info.get("intent", ""),
            domains=question_info.get("domains", []),
            source_decision=question_info.get("source_decision"),
            programming_language=question_info.get(
                "programming_language"
            ),
            file_context=file_context,
            conversation_context=conversation_emotion_context.conversation_context,
        )
        # ================================
        # DETERMINISTIC CALCULATION ROUTER
        # ================================
        if route == "calculation":
            calculation_expression = self._extract_calculation_expression(
                message
            )
            calculation_result = self.calculator.calculate(
                calculation_expression
            )
            if not calculation_result.success:
                return calculation_result.reason

            calculation_verification = self.result_verifier.verify_calculation(
                calculation_result
            )

            if not calculation_verification.verified:
                return calculation_verification.reason

            return str(calculation_result.result)

        # ================================
        # ROUTINE MEDICAL LLM ROUTING
        # ================================

        medical_assessment = self.medical_response.assess(message)

        if medical_assessment.is_medical:
            if medical_assessment.urgency == "emergency":
                return medical_assessment.response

            return self.medical_response.get_response(message)

            medical_prompt = self.medical_response.build_llm_prompt(message)
            return self.llm_router.generate(medical_prompt)

        # ================================
        # PROGRAMMING INTELLIGENCE ROUTER
        # ================================
        if route == "programming":
            programming_action = self._detect_programming_action(message)


            programming_text = (message or "").strip().lower()

            language_selection = self.language_selector.select(
                requirement=message,
                domain=(
                    question_info["domains"][0].get("domain")
                    if question_info.get("domains")
                    and isinstance(question_info["domains"][0], dict)
                    else None
                ),
            )

            language = (
                language_selection.language
                if language_selection is not None
                else ""
            )

            if not language and file_context:
                code_lower = file_context.lower()
                if "def " in code_lower or "import " in code_lower:
                    language = "python"
                elif "function " in code_lower or "const " in code_lower:
                    language = "javascript"


            programming_code = file_context

            if not programming_code:
                programming_code = message

            command = []

            if programming_action in ("execute", "run_tests"):
                if "pytest" in programming_text:
                    command = ["python", "-m", "pytest"]

                elif "npm test" in programming_text:
                    command = ["npm", "test"]

                elif programming_action == "execute" and language.lower() == "python":
                    execution_code = programming_code

                    prefixes = (
                        "run this python code:",
                        "run the python code:",
                        "execute this python code:",
                        "execute the python code:",
                        "python code:",
                        "run python:",
                        "execute python:",
                    )

                    for prefix in prefixes:
                        if execution_code.lower().startswith(prefix):
                            execution_code = execution_code[len(prefix):].strip()
                            break

                    command = ["python", "-c", execution_code]

                elif programming_action == "execute" and language.lower() in (
                    "javascript",
                    "node.js",
                ):
                    execution_code = programming_code

                    prefixes = (
                        "run this javascript code:",
                        "run the javascript code:",
                        "execute this javascript code:",
                        "execute the javascript code:",
                        "javascript code:",
                        "run javascript:",
                        "execute javascript:",
                    )

                    for prefix in prefixes:
                        if execution_code.lower().startswith(prefix):
                            execution_code = execution_code[len(prefix):].strip()
                            break

                    command = ["node", "-e", execution_code]
            error_message = ""
            if programming_action == "debug_code":
                error_message = message
            

            if "analyze this python code:" in programming_code.lower():
                programming_code = programming_code.split(":", 1)[1].strip()
            programming_context = conversation_context

            if programming_action == "documentation":
                documentation_match = re.search(
                    r"(?i)\b(python|javascript|typescript|code|function|class|api|programming)\b.*?\b(documentation|api docs|api documentation)\b(?:\s+for\s+|\s*:\s*)?(.*)$",
                    message.strip(),
                )

                if documentation_match:
                    technology = documentation_match.group(1).strip()
                    entry_name = documentation_match.group(3).strip()
                    if entry_name:
                        programming_context = f"{technology}|{entry_name}"
                    else:
                        programming_context = f"{technology}|documentation"

            elif programming_action == "check_version":
                version_match = re.search(
                    r"(?i)\b(?:required|requires?)\s*(?:version)?\s*[=:]?\s*v?([0-9]+(?:\.[0-9]+)*)\s*.*?\b(?:current|installed)\s*(?:version)?\s*[=:]?\s*v?([0-9]+(?:\.[0-9]+)*)",
                    message.strip(),
                )

                if not version_match:
                    version_match = re.search(
                        r"(?i)\bv?([0-9]+(?:\.[0-9]+)*)\b\s+(?:is\s+)?(?:compatible|compatibility)\s+(?:with\s+)?\bv?([0-9]+(?:\.[0-9]+)*)\b",
                        message.strip(),
                    )

                if not version_match:
                    version_match = re.search(
                        r"(?i)\bv?([0-9]+(?:\.[0-9]+)*)\b.*?\b(?:compatible\s+with|compatibility\s+with|compatible|compatibility)\b.*?\bv?([0-9]+(?:\.[0-9]+)*)\b",
                        message.strip(),
                    )

                if version_match:
                    programming_context = (
                        f"{version_match.group(1)}|{version_match.group(2)}"
                    )

            programming_request = ProgrammingRequest(
                action=programming_action,
                language=language,
                requirement=message,
                
                code=programming_code,
                project_path="",
                command=command,
                error_message=error_message,
                context=programming_context,
                timeout_seconds=10,
            )
            programming_result = self.programming_intelligence.handle(
                programming_request
            )

            if programming_action == "execute":
                execution_verification = self.result_verifier.verify_execution(
                    programming_result.result
                )

                if not execution_verification.verified:
                    programming_result = ProgrammingResult(
                        success=False,
                        action=programming_result.action,
                        result=programming_result.result,
                        reason=execution_verification.reason,
                    )

            return json.dumps(
                {
                    "type": "programming",
                    "action": programming_result.action,
                    "success": programming_result.success,
                    "result": programming_result.result,
                    "reason": programming_result.reason,
                },
                ensure_ascii=False,
                default=str,
            )
        # Stable knowledge: use a non-expired stored answer first.

        knowledge_routes = question_info.get("knowledge_routes", [])

        has_knowledge_route = any(
            isinstance(item, dict)
            and item.get("source") == "knowledge"
            for item in knowledge_routes
        )


        if (route == "knowledge" or has_knowledge_route) and not file_context:
            stored = self.knowledge_base.get(message)
            if stored is not None:
                return stored["answer"]
            

        # Live questions must be researched before final answer generation.
        evidence = []

        # Safety net: even if intent detection misses a Bengali/mixed-language
        # live query, obvious current-data requests must still reach research.
        
        message_lower = message.lower()

        obvious_live = any(
            marker in message_lower
            for marker in self.LIVE_KEYWORDS
        )
        if emotion_result.emotion in emotional_intents:
            obvious_live = False
        

        if (needs_research or obvious_live) and not file_context:
            try:
                evidence = self.web_research.research(
                    message,
                    max_sources=5,
                )

                prompt = self._build_grounded_prompt(
                    message,
                    evidence
                )
                
            except Exception as exc:
                evidence = []


        structured_live = self._format_structured_live_evidence(
            evidence
        )

        



        prompt = (
            "You are ISMAIL AI. Your name is ISMAIL AI. "
            "When the user asks your name, identity, or who you are, "
            "answer that you are ISMAIL AI. "
            "Do not identify yourself as ChatGPT, OpenAI, or another AI name. "
            "The user's name is separate from your own identity.\n\n"

            "You are a careful, truthful, and conversational AI. "
            "Answer the user's actual question directly.\n\n"

            "ACCURACY RULES:\n"
            "1. Never invent facts, numbers, statistics, benchmarks, "
            "prices, dates, names, sources, or technical claims.\n"
            "2. Do not present an uncertain claim as a confirmed fact.\n"
            "3. If you are not sure about a fact, say that you are not sure "
            "instead of guessing.\n"
            "4. Never create fake citations, sources, studies, links, or "
            "references.\n"
            "5. Do not exaggerate performance or capabilities using unsupported "
            "numbers such as '10x faster', '1000+ requests/sec', or similar "
            "claims unless reliable evidence is provided.\n"
            "6. For current or time-sensitive information, use supplied live "
            "evidence when available. Do not invent current information.\n"
            "7. If reliable evidence is unavailable for a current fact, clearly "
            "say that the information could not be verified.\n"
            "8. When giving an estimate or approximation, clearly label it as "
            "an estimate rather than a fact.\n"
            "9. Prefer a short accurate answer over a long answer containing "
            "unsupported claims.\n\n"
            "10. Do not claim that ISMAIL AI, the backend, server, hardware, "
            "or infrastructure can handle a specific number of requests, users, "
            "speed, latency, or workload unless that exact capability has been "
            "measured or is explicitly provided as reliable evidence.\n"

            "11. When recommending books, libraries, frameworks, products, "
            "services, or other resources, do not invent or guess names. "
            "If you are unsure whether a resource exists, say that you are unsure "
            "instead of presenting it as a recommendation.\n"

            "CONVERSATION RULES:\n"
            "Understand the current user message together with the recent "
            "conversation. "
            "If the user says 'এটা', 'এটার', 'ওটা', 'সেটা', 'আগেরটা', "
            "'this', 'that', 'it', or similar expressions, resolve the "
            "reference using the most relevant previous message. "
            "Do not ask the user to repeat information that is already clear "
            "from the conversation. "
            "If the user continues an existing topic, answer within that topic "
            "instead of starting a new generic explanation.\n\n"
        )

        if file_context:
            prompt += (
                "The user uploaded a document. "
                "Use the document as the primary source for answering the user's request.\n"
                "Do not invent facts that are not present in the document.\n"
                "If the document does not contain the requested information, "
                "say so clearly.\n\n"
                "DOCUMENT CONTENT:\n"
                f"{file_context}\n\n"
            )

        if conversation_context:
            prompt += (
                "\n\nRECENT CONVERSATION:\n"
                f"{conversation_context}\n\n"
                "Use the recent conversation to understand "
                "what the user means. Resolve references such as "
                "'it', 'that', 'this', 'he', 'she', 'they', "
                "'আগেরটা', 'ওটা', 'এটা', 'সে', and similar "
                "follow-up references from the conversation.\n"
            )

        prompt += (
            "\nEMOTIONAL CONTEXT:\n"
            f"Detected emotion: {emotion_result.emotion}\n"
            f"Confidence: {emotion_result.confidence}\n"
            f"Signals: {', '.join(emotion_result.signals)}\n"
              f"Detected intent: {mood_state.intent}\n"
              f"Intent confidence: {mood_state.intent_confidence}\n"
            "Use this emotional context to make the response "
            "appropriate, warm, and natural. Do not mention the "
            "emotion detection system unless the user asks.\n"
              f"Companion strategy: {companion_instruction}\n"
            f"Companion personality: {personality_instruction}\n"
        )
        prompt += (
            "\nCURRENT USER MESSAGE:\n"
            f"{message}"
        )

        if (needs_research or obvious_live) and not file_context:
            # ---------------------------------------------------------
            # Task 4 Answer Synthesis Layer.
            # Reuse the synthesis result prepared by WebResearch.
            # Answer points are synthesis hints only; factual claims
            # must still be supported by the grounded evidence.
            # ---------------------------------------------------------
            task4_result = getattr(
                self.web_research,
                "last_task4_result",
                None,
            )

            prompt = self._build_grounded_prompt(
                message,
                evidence
            )

            if task4_result is not None:
                answer_points = getattr(
                    task4_result,
                    "answer_points",
                    [],
                )

                if answer_points:
                    prompt += (
                        "\n\nTASK 4 ANSWER SYNTHESIS GUIDANCE:\n"
                        "Use these supported answer points to organize "
                        "the response.\n"
                        "Do not add facts that are not supported by the "
                        "grounded evidence above.\n"
                    )

                    for point in answer_points:
                        prompt += f"- {point}\n"

            if conversation_context:
                prompt += (
                    "\n\nRECENT CONVERSATION:\n"
                    f"{conversation_context}\n\n"
                    "Use this conversation only to understand "
                    "the user's current question and references. "
                    "Current factual claims must still come from "
                    "the supplied evidence.\n"
                )

        # Add saved user memory after the final base prompt is built.
        prompt = self._add_memory_to_prompt(
            prompt,
            user_id,
        )

        if self.provider in ("openai", "openrouter", "groq"):
            return self.llm_router.generate(prompt)

        

        if self.provider == "ollama":
            if not self.model:
                return "Ollama model is not configured."

            if needs_research and evidence:
                if structured_live:
                    return structured_live

                return self._format_verified_live_answer(
                    message,
                    evidence,
                )

            if emotion_result.emotion in emotional_intents:
                return companion_strategy.get_fallback(
                    emotion_result.emotion
                )

            return self.llm_router.generate(prompt)

        return "ISMAIL AI engine provider is not configured."
