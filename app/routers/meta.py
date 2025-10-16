from fastapi import APIRouter

router = APIRouter(prefix="/api/meta", tags=["meta"])

@router.get("/")
def get_metadata():
    """
    Poskytuje LLM prehľad o všetkých proxy endpointoch a ich účele.
    """
    return {
        "proxy_version": "1.0.0",
        "description": "SDM Proxy API pre Broadcom Service Desk Manager 17.4",
        "entities": {
            "incidents": {"object": "cr", "operations": ["search", "get", "create", "update", "delete"]},
            "priorities": {"object": "pri", "operations": ["search", "get"]},
            "categories": {"object": "cr_cat", "operations": ["search", "get"]},
            "statuses": {"object": "cr_stat", "operations": ["search", "get"]},
            "request_types": {"object": "cr_type", "operations": ["search", "get"]},
            "urgencies": {"object": "urg", "operations": ["search", "get"]},
            "impacts": {"object": "imp", "operations": ["search", "get"]},
            "contacts": {"object": "cnt", "operations": ["search", "get"]},
        }
    }
