from fastapi import APIRouter, HTTPException, Query
from app.sdm_client import sdm_client
from app.utils.logger import logger

router = APIRouter(prefix="/api/contacts", tags=["contacts", "roles"])


@router.post("/set_role")
async def set_contact_role(data: dict):
    """
    Automaticky priradí rolu kontaktu podľa mena a názvu roly.
    Príklad:
    {
      "contact": "vueuser",
      "role": "Administrator"
    }
    """
    contact_name = data.get("contact")
    role_name = data.get("role")

    if not contact_name or not role_name:
        raise HTTPException(status_code=400, detail="Missing 'contact' or 'role' in request body")

    logger.info(f"[CONTACT_ROLE] Assigning role '{role_name}' to contact '{contact_name}'...")

    # 1️⃣ Nájsť kontakt podľa userID alebo mena
    try:
        cnts = sdm_client.get_list(
            "cnt",
            attrs="id,userid,first_name,last_name,common_name",
            where=f"userid='{contact_name}'"
        )
        if not cnts["items"]:
            raise HTTPException(status_code=404, detail=f"Contact '{contact_name}' not found in SDM")
        contact = cnts["items"][0]
        contact_id = contact.get("@id") or contact.get("id")
    except Exception as e:
        logger.error(f"[CONTACT_ROLE] Error fetching contact: {e}")
        raise HTTPException(status_code=500, detail=f"Cannot find contact '{contact_name}'")

    # 2️⃣ Nájsť rolu podľa názvu
    try:
        roles = sdm_client.get_list(
            "role",
            attrs="id,common_name",
            where=f"common_name='{role_name}'"
        )
        if not roles["items"]:
            raise HTTPException(status_code=404, detail=f"Role '{role_name}' not found in SDM")
        role = roles["items"][0]
        role_id = role.get("@id") or role.get("id")
    except Exception as e:
        logger.error(f"[CONTACT_ROLE] Error fetching role: {e}")
        raise HTTPException(status_code=500, detail=f"Cannot find role '{role_name}'")

    # 3️⃣ Over existujúce priradenie
    try:
        existing = sdm_client.get_list(
            "lrel_cnt_role",
            attrs="id,role,cnt",
            where=f"cnt.id={contact_id} and role.id={role_id}"
        )
        if existing["items"]:
            logger.info(f"[CONTACT_ROLE] Contact already has role '{role_name}'.")
            return {
                "contact": contact_name,
                "role": role_name,
                "action": "already_assigned",
                "contact_id": contact_id,
                "role_id": role_id
            }
    except Exception as e:
        logger.warning(f"[CONTACT_ROLE] Verification failed: {e}")

    # 4️⃣ Pridanie väzby
    try:
        payload = {"lrel_cnt_role": {"cnt": {"id": contact_id}, "role": {"id": role_id}}}
        result = sdm_client.create_object("lrel_cnt_role", payload["lrel_cnt_role"])
        logger.info(f"[CONTACT_ROLE] Role '{role_name}' assigned to '{contact_name}'.")
        return {
            "contact": contact_name,
            "role": role_name,
            "action": "assigned",
            "contact_id": contact_id,
            "role_id": role_id,
            "sdm_result": result
        }
    except Exception as e:
        logger.error(f"[CONTACT_ROLE] Failed to assign role: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to assign role '{role_name}' to '{contact_name}'")


@router.get("/get_roles")
async def get_contact_roles(userid: str = Query(..., description="UserID používateľa, napr. vueuser")):
    """
    Vráti všetky roly priradené danému kontaktu podľa jeho UserID.
    Príklad volania:
      /api/contacts/get_roles?userid=vueuser
    """
    logger.info(f"[CONTACT_ROLE] Fetching roles for user '{userid}'")

    # 1️⃣ Nájsť kontakt
    try:
        cnts = sdm_client.get_list(
            "cnt",
            attrs="id,userid,first_name,last_name,common_name",
            where=f"userid='{userid}'"
        )
        if not cnts["items"]:
            raise HTTPException(status_code=404, detail=f"Contact '{userid}' not found in SDM")
        contact = cnts["items"][0]
        contact_id = contact.get("@id") or contact.get("id")
    except Exception as e:
        logger.error(f"[CONTACT_ROLE] Error fetching contact: {e}")
        raise HTTPException(status_code=500, detail=f"Cannot find contact '{userid}'")

    # 2️⃣ Získať všetky roly
    try:
        result = sdm_client.get_list(
            "lrel_cnt_role",
            attrs="id,role.common_name,role.id",
            where=f"cnt.id={contact_id}"
        )
        roles = [
            {
                "role_id": r["role"]["id"],
                "role_name": r["role"]["common_name"]
            } for r in result.get("items", [])
        ]
        return {
            "contact": userid,
            "contact_id": contact_id,
            "role_count": len(roles),
            "roles": roles
        }
    except Exception as e:
        logger.error(f"[CONTACT_ROLE] Error fetching roles: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve roles for '{userid}'")
