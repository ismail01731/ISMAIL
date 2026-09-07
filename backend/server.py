import base64
import hashlib
import hmac
import json
import os
from dotenv import load_dotenv

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "config",
        ".env"
    ),
    override=False
)

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from backend.ai_engine import AIEngine
from backend.input_security import InputSecurity
from backend.web_research import WebResearch
from backend.knowledge_base import KnowledgeBase
import time
import secrets


app = FastAPI(
    title="ISMAIL AI",
    version="0.1.0",
    description="ISMAIL AI backend"
)


FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

app.mount("/app", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


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
input_security = InputSecurity()
AUTH_SECRET = os.getenv("AUTH_SECRET", "").strip()
IDENTITY_TOKEN_MAX_AGE_SECONDS = 30 * 24 * 60 * 60
IDENTITY_TOKEN_CLOCK_SKEW_SECONDS = 60
if not AUTH_SECRET:
    raise RuntimeError("AUTH_SECRET is required for authentication.")




def _generate_identity() -> str:
    return "user-" + secrets.token_urlsafe(24)


def _hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = secrets.token_bytes(16)
    iterations = 310000

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt,
        iterations,
    )

    encoded_salt = base64.urlsafe_b64encode(
        salt
    ).decode("ascii").rstrip("=")

    encoded_hash = base64.urlsafe_b64encode(
        password_hash
    ).decode("ascii").rstrip("=")

    return f"pbkdf2_sha256${iterations}${encoded_salt}${encoded_hash}"


def _verify_password(
    password: str,
    stored_hash: str,
) -> bool:
    try:
        algorithm, iterations_text, encoded_salt, encoded_hash = (
            stored_hash.split("$", 3)
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations_text)

        salt = base64.urlsafe_b64decode(
            encoded_salt + "=" * (-len(encoded_salt) % 4)
        )

        expected_hash = base64.urlsafe_b64decode(
            encoded_hash + "=" * (-len(encoded_hash) % 4)
        )

        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(
            actual_hash,
            expected_hash,
        )

    except (ValueError, TypeError):
        return False




def _sign_identity(user_id: str, issued_at: int) -> str:
    payload = json.dumps(
        {
            "user_id": user_id,
            "iat": issued_at,
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
    signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode("ascii").rstrip("=")
    return f"{encoded_payload}.{encoded_signature}"

def _verify_identity(token: str) -> str:
    if not isinstance(token, str) or token.count(".") != 1:
        raise ValueError("Invalid identity token.")
    encoded_payload, encoded_signature = token.split(".", 1)
    try:
        payload_bytes = base64.urlsafe_b64decode(
            encoded_payload + "=" * (-len(encoded_payload) % 4)
        )
        provided_signature = base64.urlsafe_b64decode(
            encoded_signature + "=" * (-len(encoded_signature) % 4)
        )
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (ValueError, TypeError, json.JSONDecodeError):
        raise ValueError("Invalid identity token.")
    expected_signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        encoded_payload.encode("ascii"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(provided_signature, expected_signature):
        raise ValueError("Invalid identity token.")
    user_id = payload.get("user_id")
    issued_at = payload.get("iat")
    if not isinstance(user_id, str) or not user_id:
        raise ValueError("Invalid identity token.")
    if not isinstance(issued_at, int) or isinstance(issued_at, bool):
        raise ValueError("Invalid identity token.")
    now = int(time.time())
    if issued_at > now + IDENTITY_TOKEN_CLOCK_SKEW_SECONDS:
        raise ValueError("Identity token is not yet valid.")
    if now - issued_at > IDENTITY_TOKEN_MAX_AGE_SECONDS:
        raise ValueError("Identity token has expired.")
    return user_id

class ChatRateLimiter:
    """Simple in-memory per-IP rate limiter for the chat endpoint."""

    MAX_REQUESTS = 10
    WINDOW_SECONDS = 60

    def __init__(self):
        self._requests = {}

    def check(self, client_ip: str) -> bool:
        now = time.monotonic()
        timestamps = self._requests.get(client_ip, [])

        timestamps = [
            timestamp
            for timestamp in timestamps
            if now - timestamp < self.WINDOW_SECONDS
        ]

        if len(timestamps) >= self.MAX_REQUESTS:
            self._requests[client_ip] = timestamps
            return False

        timestamps.append(now)
        self._requests[client_ip] = timestamps
        return True


chat_rate_limiter = ChatRateLimiter()



class RegisterRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9._-]+$",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-z0-9._-]+$",
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )




@app.post("/api/auth/register")
def register_account(request: RegisterRequest):
    try:
        username = request.username.strip().lower()

        if len(username) < 3:
            raise HTTPException(
                status_code=400,
                detail="Username must contain at least 3 characters.",
            )

        user_id = _generate_identity()
        password_hash = _hash_password(request.password)

        created = knowledge_base.create_user_account(
            user_id,
            username,
            password_hash,
        )

        if not created:
            raise HTTPException(
                status_code=409,
                detail="Username is already registered.",
            )

        issued_at = int(time.time())
        token = _sign_identity(
            user_id,
            issued_at,
        )

        return {
            "name": "ISMAIL AI",
            "user_id": user_id,
            "username": username,
            "token": token,
            "expires_in": IDENTITY_TOKEN_MAX_AGE_SECONDS,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Registration error: {type(exc).__name__}: {exc}",
        )


@app.post("/api/auth/login")
def login_account(request: LoginRequest):
    try:
        username = request.username.strip().lower()

        account = knowledge_base.get_user_account(
            username
        )

        if account is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password.",
            )

        if not _verify_password(
            request.password,
            account["password_hash"],
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password.",
            )

        issued_at = int(time.time())

        token = _sign_identity(
            account["user_id"],
            issued_at,
        )

        return {
            "name": "ISMAIL AI",
            "user_id": account["user_id"],
            "username": account["username"],
            "token": token,
            "expires_in": IDENTITY_TOKEN_MAX_AGE_SECONDS,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Login error: {type(exc).__name__}: {exc}",
        )


@app.post("/api/session")
def create_session():
    user_id = _generate_identity()
    issued_at = int(time.time())
    token = _sign_identity(user_id, issued_at)
    return {
        "user_id": user_id,
        "token": token,
        "expires_in": IDENTITY_TOKEN_MAX_AGE_SECONDS,
    }





class ChatRequest(BaseModel):
    message: str = Field(..., max_length=12000)
    user_id: str = Field("", max_length=200, pattern=r"^[A-Za-z0-9._:-]*$")


class ChatHistoryMessage(BaseModel):
    chat_id: str = Field(..., min_length=1, max_length=200)
    role: str = Field(..., pattern=r"^(user|assistant)$")
    message: str = Field(..., min_length=1, max_length=12000)


class ChatHistoryClearRequest(BaseModel):
    pass


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



@app.get("/api/chat/history")
def get_chat_history(
    chat_id: str,
    http_request: Request
):
    try:
        authorization = http_request.headers.get("Authorization", "").strip()

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        identity_token = authorization[7:].strip()

        if not identity_token:
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        try:
            authenticated_user_id = _verify_identity(identity_token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired identity token.",
            )

        return {
            "name": "ISMAIL AI",
            "user_id": authenticated_user_id,
            "history": knowledge_base.get_chat_history(
                authenticated_user_id,
                chat_id,
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chat history error: {type(exc).__name__}: {exc}"
        )


@app.post("/api/chat/history")
def save_chat_history(
    request: ChatHistoryMessage,
    http_request: Request,
):
    try:
        authorization = http_request.headers.get("Authorization", "").strip()

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        identity_token = authorization[7:].strip()

        if not identity_token:
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        try:
            authenticated_user_id = _verify_identity(identity_token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired identity token.",
            )

        saved = knowledge_base.save_chat_message(
            authenticated_user_id,
            request.chat_id,
            request.role,
            request.message,
        )

        if not saved:
            raise HTTPException(
                status_code=400,
                detail="Unable to save chat message.",
            )

        return {
            "name": "ISMAIL AI",
            "saved": True,
            "user_id": authenticated_user_id,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chat history error: {type(exc).__name__}: {exc}"
        )


@app.delete("/api/chat/history")
def clear_chat_history(http_request: Request):
    try:
        authorization = http_request.headers.get("Authorization", "").strip()

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        identity_token = authorization[7:].strip()

        if not identity_token:
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        try:
            authenticated_user_id = _verify_identity(identity_token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired identity token.",
            )

        cleared = knowledge_base.clear_chat_history(
            authenticated_user_id
        )

        if not cleared:
            raise HTTPException(
                status_code=400,
                detail="Unable to clear chat history.",
            )

        return {
            "name": "ISMAIL AI",
            "cleared": True,
            "user_id": authenticated_user_id,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Chat history error: {type(exc).__name__}: {exc}"
        )




    

    
@app.post("/api/chat")
def chat(request: ChatRequest, http_request: Request):
    try:
        authorization = http_request.headers.get("Authorization", "").strip()

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        identity_token = authorization[7:].strip()

        if not identity_token:
            raise HTTPException(
                status_code=401,
                detail="Authentication required.",
            )

        try:
            authenticated_user_id = _verify_identity(identity_token)
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired identity token.",
            )

        client_ip = (
            http_request.client.host
            if http_request.client
            else "unknown"
        )

        if not chat_rate_limiter.check(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        security = input_security.scan(request.message)

        if not security.allowed:
            raise HTTPException(
                status_code=400,
                detail=security.reason,
            )


        question = ai_engine.understand_question(
            request.message
        )


        response = ai_engine.generate(
            request.message,
            authenticated_user_id
        )

        action = None

        try:
            parsed_response = json.loads(response)

            if isinstance(parsed_response, dict):
                if parsed_response.get("action") != "none":
                    action = parsed_response

        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "name": "ISMAIL AI",
            "question": question,
            "response": response if action is None else "",
            "action": action
        }

    except HTTPException:
        raise

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )















