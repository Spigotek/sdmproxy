from fastapi import APIRouter, Query, HTTPException
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/tickets", tags=["tickets"])

@router.get("/")
def list_tickets(limit: int = Query(25, ge=1), start: int = Query(1, ge=1), type: str = Query("cr")):
    """
    Získanie zoznamu tiketov (CR, REQ, PRB, CHG)
    Parametre:
      - type: "cr" | "req" | "prb" | "chg"
    """
    logger.info(f"Fetching {type.upper()} list from SDM...")
    response = sdm_client.get(f"{type}?start={start}&size={limit}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch tickets")
    return {"data": response.json()}

@router.get("/{ticket_type}/{ticket_id}")
def get_ticket(ticket_type: str, ticket_id: str):
    """Získanie detailu tiketu podľa ID"""
    response = sdm_client.get(f"{ticket_type}/{ticket_id}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Ticket not found")
    return response.json()

@router.post("/{ticket_type}")
def create_ticket(ticket_type: str, payload: dict):
    """Vytvorenie nového tiketu"""
    response = sdm_client.post(ticket_type, payload)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.put("/{ticket_type}/{ticket_id}")
def update_ticket(ticket_type: str, ticket_id: str, payload: dict):
    """Aktualizácia tiketu"""
    response = sdm_client.put(f"{ticket_type}/{ticket_id}", payload)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

@router.delete("/{ticket_type}/{ticket_id}")
def delete_ticket(ticket_type: str, ticket_id: str):
    """Vymazanie tiketu"""
    response = sdm_client.delete(f"{ticket_type}/{ticket_id}")
    if response.status_code not in (200, 204):
        raise HTTPException(status_code=response.status_code, detail="Failed to delete ticket")
    return {"message": f"{ticket_type.upper()} ticket {ticket_id} deleted successfully"}
