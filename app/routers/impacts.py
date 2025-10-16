from fastapi import APIRouter, Body
from app.routers.priorities import _search_sdm_object

router = APIRouter(prefix="/api/impacts", tags=["impacts"])

@router.post("/search")
def search_impacts(payload: dict = Body(default={"attrs": "id,common_name"})):
    return _search_sdm_object("imp", payload)
