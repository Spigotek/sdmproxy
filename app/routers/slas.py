from fastapi import APIRouter, HTTPException, Query
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/slas", tags=["SLA"])

@router.get("/")
def list_slas(limit: int = Query(25, ge=1), start: int = Query(1, ge=1)):
    """Získanie zoznamu SLA (Service Level Agreements)"""
    logger.info("Fetching SLA definitions from SDM...")
    response = sdm_client.get(f"sla?start={start}&size={limit}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch SLA list")
    return {"data": response.json()}

@router.get("/{sla_id}")
def get_sla(sla_id: str):
    """Získanie detailu SLA podľa ID"""
    response = sdm_client.get(f"sla/{sla_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="SLA not found")
    return response.json()
