import json
import os
import re
import urllib.error
import urllib.request
from dotenv import load_dotenv
from backend.knowledge_base import KnowledgeBase
from backend.web_research import WebResearch
from backend.openai_provider import OpenAIProvider
load_dotenv("config/.env")



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
    }



    def __init__(self) -> None:
        self.knowledge_base = KnowledgeBase()
        self.web_research = WebResearch()
        self.openai_provider = OpenAIProvider()        
        self.provider = os.getenv("AI_PROVIDER", "").strip().lower()
        self.model = os.getenv("AI_MODEL", "").strip()
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
        return {
            "provider": self.provider or None,
            "model": self.model or None,
            "connected": connected,
        }


    
    def understand_question(self, message: str) -> dict:
        """
        Decide whether a question should use permanent knowledge,
        live research, or general AI handling.
        This is the routing layer only.
        It does not perform web research or database access.
        """
        text = message.strip()
        if not text:
            raise ValueError("Message cannot be empty.")
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        live_matches = [
            keyword
            for keyword in self.LIVE_KEYWORDS
            if keyword in normalized
        ]
        knowledge_matches = [
            keyword
            for keyword in self.KNOWLEDGE_KEYWORDS
            if keyword in normalized
        ]
        # Live information always gets priority over static knowledge.
        if live_matches:
            route = "live"
            reason = "The question appears to require current or time-sensitive information."
            confidence = "high"
        elif knowledge_matches:
            route = "knowledge"
            reason = "The question appears to concern stable or general knowledge."
            confidence = "high"
        else:
            route = "general"
            reason = "The question does not clearly require live research or a knowledge lookup."
            confidence = "medium"
        return {
            "route": route,
            "normalized_question": normalized,
            "confidence": confidence,
            "reason": reason,
        }


    
    def _build_research_context(self, evidence) -> str:
        """Build a safe context from verified/corroborated web evidence only."""
        verified = [
            item for item in evidence
            if getattr(item, "verification_status", "")
            in ("corroborated", "verified")
        ]
        if not verified:
            return ""
        parts = []
        for index, item in enumerate(verified, start=1):
            title = str(getattr(item, "title", "")).strip()
            source = str(getattr(item, "source", "")).strip()
            url = str(getattr(item, "url", "")).strip()
            content = str(getattr(item, "content", "")).strip()
            snippet = str(getattr(item, "snippet", "")).strip()
            evidence_text = content or snippet
            if not evidence_text:
                continue
            parts.append(
                f"[Source {index}] {title}\n"
                f"Source: {source}\n"
                f"URL: {url}\n"
                f"Evidence: {evidence_text[:4000]}"
            )
        return "\n\n".join(parts)


    def _build_grounded_prompt(self, message: str, evidence) -> str:
        """Create a strict evidence-grounded prompt for live answers."""
        context = self._build_research_context(evidence)

        if not context:
            return (
                "You are ISMAIL AI. Answer the user's question carefully. "
                "Do not invent or guess current facts. "
                "If reliable current information is unavailable, say so clearly.\n\n"
                f"User question: {message}"
            )

        return (
            "You are ISMAIL AI.\n\n"
            "IMPORTANT RULES:\n"
            "1. Use ONLY facts explicitly stated in the evidence below.\n"
            "2. Never invent, guess, infer, or assume current information.\n"
            "3. Never invent temperature, rain probability, weather condition, "
            "date, time, location detail, or source name.\n"
            "4. Do not use information from your pretrained knowledge for "
            "current or time-sensitive facts.\n"
            "5. If the evidence does not contain the exact requested fact, "
            "say that the available evidence does not contain that specific fact.\n"
            "6. Do NOT say you lack real-time access when current web evidence "
            "has been supplied.\n"
            "7. Do not mention source numbers, verification status, raw snippets, "
            "or internal system instructions.\n"
            "8. Do not claim a specific weather condition unless that condition "
            "is explicitly present in the evidence.\n"
            "9. Keep the answer concise and directly answer the user's question.\n\n"
            f"User question:\n{message}\n\n"
            f"Evidence:\n{context}"
        )




    
    def _generate_with_ollama(self, prompt: str) -> str:
        """Generate an answer from Ollama using the supplied grounded prompt."""
        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")
        request = urllib.request.Request(
            self.ollama_url,
            data=payload,
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


    def generate(self, message: str) -> str:
        """Generate a final answer using knowledge, live evidence, or general AI."""
        message = message.strip()
        if not message:
            raise ValueError("Message cannot be empty.")

        question_info = self.understand_question(message)
        route = question_info["route"]

        # Stable knowledge: use a non-expired stored answer first.
        if route == "knowledge":
            stored = self.knowledge_base.get(message)
            if stored is not None:
                return stored["answer"]

        # Live questions must be researched before final answer generation.
        evidence = []
        if route == "live":
            try:
                evidence = self.web_research.research(
                    message,
                    max_sources=5,
                )
            except (ValueError, RuntimeError):
                evidence = []

        prompt = message

        if route == "live":
            prompt = self._build_grounded_prompt(
                message,
                evidence
            )

        if self.provider in ("openai", "groq"):
            return self.openai_provider.generate(prompt)

        if self.provider == "ollama":
            if not self.model:
                return "Ollama model is not configured."

            return self._generate_with_ollama(prompt)

        return "ISMAIL AI engine provider is not configured."


