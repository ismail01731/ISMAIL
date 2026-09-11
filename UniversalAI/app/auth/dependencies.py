from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.security import verify_token
security = HTTPBearer()
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        user_id = verify_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired identity token.",
        )
    return user_id
