from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter(prefix="/api/objects", tags=["objects"])

# 📘 Statický register REST objektov pre SDM 17.4 (z Broadcom TechDocs)
SDM_OBJECTS = {
    "cr": "Incident (Request/Change/Issue)",
    "chg": "Change Order",
    "iss": "Issue",
    "cnt": "Contact / User",
    "grp": "Group",
    "loc": "Location",
    "urg": "Urgency",
    "imp": "Impact",
    "pri": "Priority",
    "cr_cat": "Category (Request Area)",
    "cr_stat": "Status (Request Status)",
    "cr_type": "Request Type",
    "wf": "Workflow Definition",
    "act_log": "Activity Log",
    "attmnt": "Attachment",
    "sla": "Service Level Agreement",
    "slalist": "SLA List",
    "role": "Role",
    "tenancy": "Tenant",
    "issue_code": "Issue Code",
    "iss_cat": "Issue Category",
    "chg_cat": "Change Category",
    "chg_stat": "Change Status",
    "chg_type": "Change Type",
    "prob_cat": "Problem Category",
    "prob_stat": "Problem Status",
    "prob_type": "Problem Type",
    "ci": "Configuration Item",
    "asset": "Asset",
    "lrel_cnt_cr": "Link Contact ↔ Incident",
    "lrel_cr_act_log": "Link Incident ↔ Activity Log",
    "lrel_cr_urg": "Link Incident ↔ Urgency",
    "lrel_cr_pri": "Link Incident ↔ Priority",
    "lrel_cr_imp": "Link Incident ↔ Impact"
}

@router.get("/list")
def list_sdm_objects():
    """
    Vracia statický zoznam známych REST objektov SDM 17.4.
    LLM môže použiť tieto názvy pre volania na sdmproxy.
    """
    logger.info(f"[OBJECTS] Returning static SDM object register ({len(SDM_OBJECTS)} items)")
    return {
        "source": "static_register",
        "count": len(SDM_OBJECTS),
        "objects": [{"object": k, "description": v} for k, v in SDM_OBJECTS.items()]
    }
