from fastapi import APIRouter, HTTPException, Query
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/incidents/by_priority")
def incidents_by_priority():
    """Prehľad počtu incidentov podľa priority"""
    query = "cr?select=priority,count(*) group by priority"
    response = sdm_client.get(query)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate report")
    return {"report": response.json()}

@router.get("/incidents/by_status")
def incidents_by_status():
    """Prehľad počtu incidentov podľa statusu"""
    query = "cr?select=status,count(*) group by status"
    response = sdm_client.get(query)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to generate report")
    return {"report": response.json()}

@router.get("/tickets/summary")
def tickets_summary():
    """Základné štatistiky pre všetky typy tiketov"""
    summary = {}
    for ttype in ["cr", "chg", "prb", "req"]:
        resp = sdm_client.get(f"{ttype}?select=status")
        if resp.status_code == 200:
            summary[ttype] = len(resp.json().get("collection_" + ttype, []))
    return {"summary": summary}
