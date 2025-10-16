from fastapi import APIRouter
import time

router = APIRouter(prefix="/api/metadata", tags=["metadata"])

@router.get("/")
def get_metadata():
    """
    Vracia manifest (LLM API manifest) všetkých endpointov s popismi.
    Používa sa na to, aby LLM vedelo, ktoré služby SDM Proxy poskytuje
    a ako ich má používať.
    """
    metadata = {
        "service": "SDM Proxy API",
        "version": "1.0.0",
        "description": "Middleware vrstva medzi LLM a Broadcom CA Service Desk Manager (SDM 17.4)",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "endpoints": [
            {
                "uri": "/api/incidents/",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "description": "CRUD operácie pre incidenty (Change Requests, objekt CR)"
            },
            {
                "uri": "/api/users/",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "description": "Získanie, vytvorenie a úprava používateľov (CNT objekty)"
            },
            {
                "uri": "/api/categories/",
                "methods": ["GET"],
                "description": "Zoznam kategórií v SDM"
            },
            {
                "uri": "/api/groups/",
                "methods": ["GET", "POST"],
                "description": "Správa a prehľad skupín (GRP objekty)"
            },
            {
                "uri": "/api/organizations/",
                "methods": ["GET", "POST"],
                "description": "Organizácie a zákaznícke entity (ORG objekty)"
            },
            {
                "uri": "/api/roles/",
                "methods": ["GET"],
                "description": "Zoznam rolí a priradených používateľov"
            },
            {
                "uri": "/api/ci/",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "description": "Konfiguračné položky (Configuration Items, CI objekty)"
            },
            {
                "uri": "/api/slas/",
                "methods": ["GET"],
                "description": "Zoznam SLA definícií a detailov"
            },
            {
                "uri": "/api/tickets/",
                "methods": ["GET", "POST", "PUT", "DELETE"],
                "description": "Zjednotený prístup ku všetkým typom tiketov (CR, REQ, CHG, PRB)"
            },
            {
                "uri": "/api/workflows/",
                "methods": ["GET", "POST"],
                "description": "Workflow procesy a spúšťanie workflowov"
            },
            {
                "uri": "/api/reports/",
                "methods": ["GET"],
                "description": "Prehľady, štatistiky a sumárne dáta (napr. podľa statusu, priority)"
            },
            {
                "uri": "/api/status/",
                "methods": ["GET"],
                "description": "Zoznam statusov a stavových prechodov v SDM"
            },
            {
                "uri": "/api/attachments/",
                "methods": ["GET", "POST"],
                "description": "Nahrávanie a sťahovanie príloh k tiketom"
            },
            {
                "uri": "/api/health/",
                "methods": ["GET"],
                "description": "Healthcheck služby – test pripojenia k SDM a stavu tokenu"
            },
            {
                "uri": "/api/debug/",
                "methods": ["GET"],
                "description": "Testovacie volania a interné diagnostické funkcie"
            },
            {
                "uri": "/api/metadata/",
                "methods": ["GET"],
                "description": "Tento manifest – popis všetkých dostupných proxy služieb pre LLM"
            }
        ]
    }
    return metadata
