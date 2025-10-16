from fastapi import APIRouter, Query, HTTPException
from app.sdm_client import sdm_client

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/")
def list_users(start: int = Query(1, ge=1), size: int = Query(25, ge=1)):
    """
    Zoznam používateľov
    """
    params = {"start": start, "size": size}
    resp = sdm_client.get("cnt", params)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/{user_id}")
def get_user_detail(user_id: str):
    """
    Detail používateľa
    """
    resp = sdm_client.get(f"cnt/{user_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.post("/")
def create_user(body: dict):
    """
    Vytvorenie používateľa
    """
    data = {"cnt": body}
    resp = sdm_client.post("cnt", data)
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.put("/{user_id}")
def update_user(user_id: str, body: dict):
    """
    Úprava používateľa
    """
    data = {"cnt": body}
    resp = sdm_client.put(f"cnt/{user_id}", data)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.delete("/{user_id}")
def delete_user(user_id: str):
    """
    Vymazanie používateľa
    """
    resp = sdm_client.delete(f"cnt/{user_id}")
    if resp.status_code not in (200, 204):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"message": f"User {user_id} deleted."}
