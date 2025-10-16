from fastapi import APIRouter
from app.sdm_client import sdm_client
from app.utils.logger import logger
import time

router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("/full")
def full_health_check():
    """
    Preverí pripojenie k SDM API pre viaceré objekty.
    Vráti detailný stav jednotlivých entít.
    """
    start_time = time.time()
    entities = ["pri", "cr_stat", "cr_cat", "cr_type"]
    results = []

    for entity in entities:
        endpoint = f"{entity}?OP=GET_LIST&size=1"
        try:
            response = sdm_client.get(endpoint)
            if response.status_code == 200:
                results.append({"entity": entity, "status": "ok"})
            else:
                results.append({"entity": entity, "status": f"error {response.status_code}"})
        except Exception as e:
            logger.error(f"[HEALTH] {entity} check failed: {e}")
            results.append({"entity": entity, "status": f"exception: {str(e)}"})

    elapsed = round(time.time() - start_time, 2)
    return {
        "service": "sdmproxy",
        "base_url": sdm_client.base_url,
        "check_time_sec": elapsed,
        "entities": results
    }
