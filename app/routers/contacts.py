from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/contacts", tags=["contacts"])

@router.post("/search")
async def search_contacts(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,userid,common_name,email_address")
        where = data.get("where", "")
        size = data.get("size", 50)

        query = f"cnt?OP=GET_LIST&attrs={attrs}&size={size}"
        if where:
            query += f"&WHERE={where}"

        logger.info(f"[CONTACTS] Fetching contacts via {query}")
        result = sdm_client.call_sdm(query, method="GET")

        collection = result.get("collection_cnt", {})
        items = collection.get("cnt", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "cnt",
            "attrs": attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[CONTACTS] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať kontakty z SDM: {str(e)}")
