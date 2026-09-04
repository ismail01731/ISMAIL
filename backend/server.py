from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.ai_engine import AIEngine
from backend.web_research import WebResearch
from backend.knowledge_base import KnowledgeBase
app = FastAPI(
    title="ISMAIL AI",
    version="0.1.0",
    description="ISMAIL AI backend"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
ai_engine = AIEngine()
web_research = WebResearch()
knowledge_base = KnowledgeBase()
class ChatRequest(BaseModel):
    message: str
class ResearchRequest(BaseModel):
    question: str
    max_sources: int = 5
class KnowledgeSaveRequest(BaseModel):
    question: str
    answer: str
    topic: str = ""
    source: str = ""
    source_url: str = ""
    verified: bool = False
    confidence: str = "medium"
    expires_at: str | None = None
    knowledge_type: str = "permanent"
class KnowledgeLookupRequest(BaseModel):
    question: str
    knowledge_type: str | None = None
@app.get("/")
def root():
    return {
        "name": "ISMAIL AI",
        "status": "online",
        "version": "0.1.0"
    }
@app.get("/api/ai/status")
def ai_status():
    return {
        "name": "ISMAIL AI",
        "engine": ai_engine.status()
    }
@app.post("/api/question/understand")
def understand_question(request: ChatRequest):
    try:
        return {
            "name": "ISMAIL AI",
            "question": ai_engine.understand_question(
                request.message
            )
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
@app.post("/api/research")
def research(request: ResearchRequest):
    try:
        if request.max_sources < 2:
            raise ValueError(
                "max_sources must be at least 2."
            )
        if request.max_sources > 10:
            raise ValueError(
                "max_sources cannot be greater than 10."
            )
        question_info = ai_engine.understand_question(
            request.question
        )
        evidence = web_research.collect_evidence(
            request.question,
            max_sources=request.max_sources,
        )
        return {
            "name": "ISMAIL AI",
            "question": question_info,
            "research": evidence,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )
@app.post("/api/knowledge/save")
def save_knowledge(request: KnowledgeSaveRequest):
    try:
        knowledge_id = knowledge_base.save(
            question=request.question,
            answer=request.answer,
            topic=request.topic,
            source=request.source,
            source_url=request.source_url,
            verified=request.verified,
            confidence=request.confidence,
            expires_at=request.expires_at,
            knowledge_type=request.knowledge_type,
        )
        return {
            "name": "ISMAIL AI",
            "saved": True,
            "id": knowledge_id,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
@app.post("/api/knowledge/lookup")
def lookup_knowledge(request: KnowledgeLookupRequest):
    try:
        result = knowledge_base.get(
            question=request.question,
            knowledge_type=request.knowledge_type,
        )
        return {
            "name": "ISMAIL AI",
            "found": result is not None,
            "knowledge": result,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
@app.post("/api/chat")
def chat(request: ChatRequest):
    try:
        question = ai_engine.understand_question(
            request.message
        )
        response = ai_engine.generate(
            request.message
        )
        return {
            "name": "ISMAIL AI",
            "question": question,
            "response": response
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"AI generation error: {type(exc).__name__}: {exc}"
        )

