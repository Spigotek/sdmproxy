from fastapi import APIRouter, Query, HTTPException
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/groups", tags=["groups"])

@router.get("/")
def list_groups(limit: int = Query(25, ge=1), start: int = Query(1, ge=1)):
    """Získanie zoznamu skupín (grp objekty)"""
    logger.info("Fetching groups list from SDM...")
    response = sdm_client.get(f"grp?start={start}&size={limit}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch groups from SDM")
    return {"data": response.json()}

@router.get("/{group_id}")
def get_group(group_id: str):
    """Detail skupiny podľa ID"""
    response = sdm_client.get(f"grp/{group_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Group not found")
    return response.json()

@router.post("/")
def create_group(payload: dict):
    """Vytvorenie novej skupiny"""
    response = sdm_client.post("grp", payload)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
