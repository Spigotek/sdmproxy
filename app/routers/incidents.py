from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

@router.post("/search")
async def search_incidents(request: Request):
    try:
        data = await request.json()
        attrs = data.get("attrs", "id,ref_num,summary,status,priority,assignee")
        where = data.get("where", "")
        size = data.get("size", 50)

        alias_map = {
            "status": "status.sym",
            "priority": "priority.sym",
            "assignee": "assignee.userid",
            "requester": "requestor.userid",
            "category": "category.sym",
            "type": "type.sym",
        }
        translated_attrs = ",".join(alias_map.get(a.strip(), a.strip()) for a in attrs.split(","))

        query = f"cr?OP=GET_LIST&attrs={translated_attrs}&size={size}"
        if where:
            query += f"&WHERE={where}"

        logger.info(f"[INCIDENTS] Fetching incidents via {query}")
        result = sdm_client.call_sdm(query, method="GET")

        collection = result.get("collection_cr", {})
        items = collection.get("cr", [])
        if isinstance(items, dict):
            items = [items]

        return {
            "object": "cr",
            "attrs": translated_attrs,
            "count": len(items),
            "items": items
        }

    except Exception as e:
        logger.error(f"[INCIDENTS] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať incidenty z SDM: {str(e)}")
