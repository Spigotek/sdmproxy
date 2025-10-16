from fastapi import APIRouter, Query, HTTPException
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/ci", tags=["configuration items"])

@router.get("/")
def list_ci(limit: int = Query(25, ge=1), start: int = Query(1, ge=1)):
    """Získanie zoznamu konfiguračných položiek (CI objekty, typ ci)"""
    response = sdm_client.get(f"ci?start={start}&size={limit}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch CIs")
    return {"data": response.json()}

@router.get("/{ci_id}")
def get_ci(ci_id: str):
    """Detail CI objektu"""
    response = sdm_client.get(f"ci/{ci_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="CI not found")
    return response.json()

@router.post("/")
def create_ci(payload: dict):
    """Vytvorenie novej CI"""
    response = sdm_client.post("ci", payload)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.put("/{ci_id}")
def update_ci(ci_id: str, payload: dict):
    """Aktualizácia CI"""
    response = sdm_client.put(f"ci/{ci_id}", payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.delete("/{ci_id}")
def delete_ci(ci_id: str):
    """Odstránenie CI"""
    response = sdm_client.delete(f"ci/{ci_id}")
    if response.status_code not in (200, 204):
        raise HTTPException(status_code=response.status_code, detail="Failed to delete CI")
    return {"message": "CI deleted successfully"}
