from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/priorities", tags=["priorities"])

@router.post("/search")
async def search_priorities(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,common_name")
        size = data.get("size", 50)

        logger.info(f"[PRIORITIES] Fetching list (attrs={attrs}, size={size})")
        result = sdm_client.call_sdm(f"pri?OP=GET_LIST&attrs={attrs}&size={size}", method="GET")

        collection = result.get("collection_pri", {})
        items = collection.get("pri", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "pri",
            "attrs": attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[PRIORITIES] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať priority z SDM: {str(e)}")
