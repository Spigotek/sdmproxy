from fastapi import APIRouter, HTTPException, Body, Query
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter()

# ---------------------------------------------------------------------
# GENERICKÝ ROUTER BUILDER
# ---------------------------------------------------------------------
def build_router(object_name: str, display_name: str):
    r = APIRouter(prefix=f"/api/{display_name}", tags=[display_name])

    # === [POST] /search ===
    @r.post("/search")
    def search_records(payload: dict = Body(default={})):
        """
        Načíta záznamy pre daný SDM objekt s plnými atribútmi.
        Voliteľné parametre:
          - where: filter, napr. "status.sym != 'Closed'"
          - size: limit výsledkov
        """
        try:
            where = payload.get("where")
            size = int(payload.get("size", 100))
            data = sdm_client.get_full_list(object_name, where=where, size=size)
            count = len(data) if isinstance(data, list) else 0
            logger.info(f"[{object_name.upper()}] Returned {count} records")
            return {"object": object_name, "count": count, "data": data}
        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error in search: {e}")
            raise HTTPException(status_code=500, detail=f"SDM {object_name} query failed: {e}")

    # === [POST] /count ===
    @r.post("/count")
    def count_records(payload: dict = Body(default={})):
        """
        Vráti len počet záznamov pre daný SDM objekt podľa filtra WHERE.
        Príklad:
        {
          "where": "status.sym != 'Closed'"
        }
        """
        try:
            where = payload.get("where")
            data = sdm_client.get_full_list(object_name, where=where, size=10000)
            count = len(data) if isinstance(data, list) else 0
            logger.info(f"[{object_name.upper()}] COUNT query → {count}")
            return {"object": object_name, "count": count, "where": where or "none"}
        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error in count: {e}")
            raise HTTPException(status_code=500, detail=f"SDM {object_name} count failed: {e}")

    # === [GET] /schema ===
    @r.get("/schema")
    def get_schema():
        """Vráti všetky dostupné atribúty pre objekt."""
        try:
            attrs = sdm_client.get_schema(object_name)
            return {"object": object_name, "attribute_count": len(attrs), "attributes": attrs}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load schema for {object_name}: {e}")

    return r


# ---------------------------------------------------------------------
# REGISTER ALL KNOWN SDM OBJECT ROUTERS
# ---------------------------------------------------------------------
object_map = {
    "incidents": "cr",
    "requests": "cr",
    "changes": "chg",
    "issues": "iss",
    "contacts": "cnt",
    "groups": "grp",
    "locations": "loc",
    "priorities": "pri",
    "urgencies": "urg",
    "impacts": "imp",
    "categories": "cr_cat",
    "statuses": "cr_stat",
    "request_types": "cr_type",
    "roles": "role",
    "assets": "asset",
    "cis": "ci",
}

routers = {}
for name, obj in object_map.items():
    routers[name] = build_router(obj, name)
    logger.info(f"🔗 Registered router /api/{name}")
