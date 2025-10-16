from fastapi import APIRouter, Body
from app.routers.priorities import _search_sdm_object

router = APIRouter(prefix="/api/urgencies", tags=["urgencies"])

@router.post("/search")
def search_urgencies(payload: dict = Body(default={"attrs": "id,common_name"})):
    return _search_sdm_object("urg", payload)
