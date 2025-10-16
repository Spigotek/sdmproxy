from fastapi import APIRouter, Body
from app.routers.priorities import _search_sdm_object

router = APIRouter(prefix="/api/request_types", tags=["request_types"])

@router.post("/search")
def search_request_types(payload: dict = Body(default={"attrs": "id,common_name"})):
    # správny objekt v SDM: crtype
    return _search_sdm_object("crtype", payload)
