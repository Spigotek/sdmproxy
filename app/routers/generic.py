from fastapi import APIRouter, HTTPException, Body
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/generic", tags=["generic"])


@router.post("/query")
def generic_query(payload: dict = Body(...)):
    try:
        obj = payload.get("object")
        if not obj:
            raise HTTPException(status_code=400, detail="Missing 'object' parameter in request body")
        where = payload.get("where", "")
        attrs = payload.get("attrs", "*")
        limit = payload.get("limit", 100)

        path = f"{obj}?OP=GET_LIST&attrs={attrs}&where={where}&size={limit}"
        data = sdm_client.get(path)
        return {"object": obj, "count": len(data.get(f"collection_{obj}", {}).get(obj, [])), "data": data}

    except Exception as e:
        logger.error(f"[GENERIC][QUERY] {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")


@router.post("/create")
def generic_create(payload: dict = Body(...)):
    try:
        obj = payload.get("object")
        values = payload.get("values", {})
        if not obj or not values:
            raise HTTPException(status_code=400, detail="Missing object or values")
        result = sdm_client.post(obj, data=values)
        return {"object": obj, "result": result}
    except Exception as e:
        logger.error(f"[GENERIC][CREATE] {e}")
        raise HTTPException(status_code=500, detail=f"Create failed: {e}")


@router.put("/update")
def generic_update(payload: dict = Body(...)):
    try:
        obj = payload.get("object")
        obj_id = payload.get("id")
        values = payload.get("values", {})
        if not obj or not obj_id:
            raise HTTPException(status_code=400, detail="Missing object or id")
        path = f"{obj}/{obj_id}"
        result = sdm_client.put(path, data=values)
        return {"object": obj, "id": obj_id, "result": result}
    except Exception as e:
        logger.error(f"[GENERIC][UPDATE] {e}")
        raise HTTPException(status_code=500, detail=f"Update failed: {e}")


@router.delete("/delete")
def generic_delete(payload: dict = Body(...)):
    try:
        obj = payload.get("object")
        obj_id = payload.get("id")
        if not obj or not obj_id:
            raise HTTPException(status_code=400, detail="Missing object or id")
        path = f"{obj}/{obj_id}"
        sdm_client.delete(path)
        return {"object": obj, "id": obj_id, "status": "deleted"}
    except Exception as e:
        logger.error(f"[GENERIC][DELETE] {e}")
        raise HTTPException(status_code=500, detail=f"Delete failed: {e}")
