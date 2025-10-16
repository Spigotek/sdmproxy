from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.post("/search")
async def search_categories(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,common_name")
        size = data.get("size", 50)

        logger.info(f"[CATEGORIES] Fetching list (attrs={attrs}, size={size})")
        result = sdm_client.call_sdm(f"cr_cat?OP=GET_LIST&attrs={attrs}&size={size}", method="GET")

        collection = result.get("collection_cr_cat", {})
        items = collection.get("cr_cat", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "cr_cat",
            "attrs": attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[CATEGORIES] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať kategórie z SDM: {str(e)}")
