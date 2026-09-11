import os
import json
import base64
import hashlib
import hmac
import secrets
import time
from dotenv import load_dotenv
load_dotenv()
AUTH_SECRET = os.getenv("AUTH_SECRET", "").strip()
if not AUTH_SECRET:
    raise RuntimeError("AUTH_SECRET is required.")
USERS_FILE = "database/users.json"
os.makedirs("database", exist_ok=True)
def _load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}
def _save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)
def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000,
    )
    return (
        base64.urlsafe_b64encode(salt).decode(),
        base64.urlsafe_b64encode(derived).decode(),
    )
def _verify_password(password, salt_b64, password_hash):
    try:
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(password_hash.encode())
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            200_000,
        )
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False
def create_user(username, password):
    username = username.strip()
    if not username or not password:
        raise ValueError("Username and password are required.")
    users = _load_users()
    key = username.lower()
    if key in users:
        raise ValueError("Username already exists.")
    salt, password_hash = _hash_password(password)
    user_id = "user-" + secrets.token_urlsafe(18)
    users[key] = {
        "user_id": user_id,
        "username": username,
        "salt": salt,
        "password_hash": password_hash,
        "created_at": int(time.time()),
    }
    _save_users(users)
    return {
        "user_id": user_id,
        "username": username,
    }
def authenticate_user(username, password):
    users = _load_users()
    user = users.get(username.strip().lower())
    if not user:
        return None
    if not _verify_password(
        password,
        user["salt"],
        user["password_hash"],
    ):
        return None
    return {
        "user_id": user["user_id"],
        "username": user["username"],
    }
def _sign_identity(user_id, issued_at):
    payload = {
        "user_id": user_id,
        "iat": issued_at,
    }
    raw_payload = json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")
    encoded_payload = base64.urlsafe_b64encode(
        raw_payload
    ).decode().rstrip("=")
    signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        encoded_payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(
        signature
    ).decode().rstrip("=")
    return f"{encoded_payload}.{encoded_signature}"
def create_token(user_id):
    return _sign_identity(
        user_id,
        int(time.time()),
    )
def verify_token(token):
    try:
        parts = token.split(".")
        if len(parts) != 2:
            raise ValueError("Invalid token.")
        encoded_payload, encoded_signature = parts
        expected_signature = hmac.new(
            AUTH_SECRET.encode("utf-8"),
            encoded_payload.encode("utf-8"),
            hashlib.sha256,
        ).digest()
        actual_signature = base64.urlsafe_b64decode(
            encoded_signature + "=="
        )
        if not hmac.compare_digest(
            actual_signature,
            expected_signature,
        ):
            raise ValueError("Invalid token.")
        raw_payload = base64.urlsafe_b64decode(
            encoded_payload + "=="
        )
        payload = json.loads(
            raw_payload.decode("utf-8")
        )
        user_id = payload.get("user_id")
        issued_at = payload.get("iat")
        if not user_id or not isinstance(issued_at, int):
            raise ValueError("Invalid token payload.")
        now = int(time.time())
        if issued_at > now + 60:
            raise ValueError("Invalid token time.")
        if now - issued_at > 30 * 24 * 60 * 60:
            raise ValueError("Token expired.")
        return user_id
    except Exception as e:
        raise ValueError("Invalid or expired identity token.") from e
