from fastapi import APIRouter, HTTPException
from app.sdm_client import sdm_client

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("/")
def list_statuses():
    """
    Zoznam všetkých stavov (status)
    """
    resp = sdm_client.get("status")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/{status_id}")
def get_status_detail(status_id: str):
    """
    Detail statusu
    """
    resp = sdm_client.get(f"status/{status_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
