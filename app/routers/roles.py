from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/roles", tags=["roles"])

@router.post("/search")
async def search_roles(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,common_name,description")
        size = data.get("size", 50)

        logger.info(f"[ROLES] Fetching list (attrs={attrs}, size={size})")
        result = sdm_client.call_sdm(f"role?OP=GET_LIST&attrs={attrs}&size={size}", method="GET")

        collection = result.get("collection_role", {})
        items = collection.get("role", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "role",
            "attrs": attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[ROLES] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať roly z SDM: {str(e)}")
