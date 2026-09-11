from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.auth.security import (
    create_user,
    authenticate_user,
    create_token,
    verify_token,
)
router = APIRouter()
security = HTTPBearer()
class AuthRequest(BaseModel):
    username: str
    password: str
@router.post("/register")
async def register(data: AuthRequest):
    try:
        user = create_user(
            data.username,
            data.password,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    token = create_token(user["user_id"])
    return {
        "name": "ISMAIL AI",
        "user_id": user["user_id"],
        "username": user["username"],
        "token": token,
        "expires_in": 30 * 24 * 60 * 60,
    }
@router.post("/login")
async def login(data: AuthRequest):
    user = authenticate_user(
        data.username,
        data.password,
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )
    token = create_token(user["user_id"])
    return {
        "name": "ISMAIL AI",
        "user_id": user["user_id"],
        "username": user["username"],
        "token": token,
        "expires_in": 30 * 24 * 60 * 60,
    }
@router.get("/me")
async def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        user_id = verify_token(
            credentials.credentials
        )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired identity token.",
        )
    return {
        "success": True,
        "user_id": user_id,
    }
