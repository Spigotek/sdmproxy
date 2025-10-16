from fastapi import APIRouter
from app.auth_manager import auth_manager

router = APIRouter(prefix="/api/debug", tags=["debug"])


@router.get("/token")
def get_token_info():
    return {
        "access_key": auth_manager.token,
        "expires_at": auth_manager.expiry,
        "is_valid": bool(auth_manager.token)
    }


@router.post("/refresh")
def refresh_token():
    auth_manager.token = None
    token = auth_manager.get_token()
    return {
        "message": "New SDM token acquired",
        "access_key": token,
        "expires_at": auth_manager.expiry
    }
