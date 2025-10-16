from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/statuses", tags=["statuses"])

@router.post("/search")
async def search_statuses(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,common_name")
        size = data.get("size", 50)

        logger.info(f"[STATUSES] Fetching list (attrs={attrs}, size={size})")
        result = sdm_client.call_sdm(f"cr_stat?OP=GET_LIST&attrs={attrs}&size={size}", method="GET")

        collection = result.get("collection_cr_stat", {})
        items = collection.get("cr_stat", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "cr_stat",
            "attrs": attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[STATUSES] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať statusy z SDM: {str(e)}")
