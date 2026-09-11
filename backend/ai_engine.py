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
load_dotenv("config/.env")
from typing import List
from backend.web_research import WebResearch, WebEvidence
from backend.creator_identity import get_identity_answer



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
        self.openai_provider = OpenAIProvider()
        self.intent_detector = IntentDetector()        
        self.provider = os.getenv("AI_PROVIDER", "").strip().lower()
        self.model = os.getenv("AI_MODEL", "").strip() or self.openai_provider.model
        self.ollama_url = os.getenv(
            "OLLAMA_URL",
            "http://127.0.0.1:11434/api/generate"
        ).strip()



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
        return self.intent_detector.detect(message)


    




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
            "Answer the user now.\n"
            "Use ONLY the supplied verified evidence.\n"
            "Preserve factual values and field meanings exactly.\n"
            "Do not add unsupported facts.\n"
        )




    
    def _generate_with_ollama(self, prompt: str) -> str:
        """Generate an answer from Ollama using the supplied grounded prompt."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": 4096,
                "num_predict": 700,
                "temperature": 0.1,
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




    def generate(
        self,
        message: str,
        user_id: str = "",
        file_context: str = "",
        chat_id: str = "",
    ) -> str:

        
        """Generate a final answer using knowledge, live evidence, or general AI."""
        message = message.strip()
        if not message:
            raise ValueError("Message cannot be empty.")

        user_id = str(user_id).strip()

        

        chat_id = str(chat_id).strip()

        conversation_context = self._build_conversation_context(
            user_id,
            chat_id,
        )

        self._save_explicit_memory(
            user_id,
            message,
        )


        browser_action = detect_browser_action(message)

        if browser_action["action"] != "none":
            return json.dumps(browser_action)

        question_info = self.understand_question(message)
        route = question_info["route"]

        # Stable knowledge: use a non-expired stored answer first.
        if route == "knowledge" and not file_context:
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
        

        if (route == "live" or obvious_live) and not file_context:
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

        if (
            structured_live
            and (
                "weather" in message_lower
                or "আবহাওয়া" in message_lower
                or "আবহাওয়া" in message_lower
                or "temperature" in message_lower
                or "তাপমাত্রা" in message_lower
                or "forecast" in message_lower
                or "পূর্বাভাস" in message_lower
                or "bitcoin" in message_lower
                or "btc" in message_lower
                or "বিটকয়েন" in message_lower
                or "বিটকয়েন" in message_lower
                or "news" in message_lower
                or "latest" in message_lower
                or "breaking" in message_lower
                or "খবর" in message_lower
                or "সংবাদ" in message_lower
                or "সর্বশেষ" in message_lower
                or "আজকের" in message_lower
            )
        ):
            return structured_live



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
            "\nCURRENT USER MESSAGE:\n"
            f"{message}"
        )

        if (route == "live" or obvious_live) and not file_context:
            prompt = self._build_grounded_prompt(
                message,
                evidence
            )

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
            return self.openai_provider.generate(prompt)

        

        if self.provider == "ollama":
            if not self.model:
                return "Ollama model is not configured."

            return self._generate_with_ollama(prompt)

        return "ISMAIL AI engine provider is not configured."

