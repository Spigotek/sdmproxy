from fastapi import APIRouter, Query, HTTPException
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/organizations", tags=["organizations"])

@router.get("/")
def list_organizations(limit: int = Query(25, ge=1), start: int = Query(1, ge=1)):
    """Získanie zoznamu organizácií (org objekty)"""
    response = sdm_client.get(f"org?start={start}&size={limit}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch organizations")
    return {"data": response.json()}

@router.get("/{org_id}")
def get_organization(org_id: str):
    """Detail organizácie"""
    response = sdm_client.get(f"org/{org_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Organization not found")
    return response.json()

@router.post("/")
def create_organization(payload: dict):
    """Vytvorenie novej organizácie"""
    response = sdm_client.post("org", payload)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
