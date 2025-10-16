from fastapi import APIRouter, HTTPException
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

@router.get("/")
def list_workflows():
    """Získanie zoznamu workflow procesov"""
    response = sdm_client.get("workflow")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch workflows")
    return {"data": response.json()}

@router.get("/{workflow_id}")
def get_workflow(workflow_id: str):
    """Detail konkrétneho workflowu"""
    response = sdm_client.get(f"workflow/{workflow_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Workflow not found")
    return response.json()

@router.post("/")
def trigger_workflow(payload: dict):
    """Spustenie workflow procesu"""
    response = sdm_client.post("workflow", payload)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()
