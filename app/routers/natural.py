from fastapi import APIRouter, HTTPException, Request
from app.sdm_client import sdm_client
from app.core.memory import memory
from app.utils.logger import logger
import re, datetime

router = APIRouter(prefix="/api/natural", tags=["natural language"])

INTENT_MAP = {
    "incident": "cr",
    "incidenty": "cr",
    "požiadavka": "cr",
    "požiadavky": "cr",
    "problem": "prob",
    "problém": "prob",
    "change": "chg",
    "zmena": "chg",
    "kontakt": "cnt",
    "kontakty": "cnt",
}

STATUS_MAP = {
    "otvoren": "Open",
    "vyriešen": "Resolved",
    "uzavret": "Closed",
    "čakaj": "Pending",
    "nov": "New"
}

PRIORITY_MAP = {"1": "1", "2": "2", "3": "3", "4": "4", "5": "5"}


def parse_date_range(query: str):
    now = datetime.datetime.utcnow()
    if "dnes" in query:
        start = now.replace(hour=0, minute=0, second=0)
        return f"open_date >= '{start.isoformat()}'"
    elif "včera" in query:
        start = now - datetime.timedelta(days=1)
        return f"open_date >= '{start.isoformat()}' AND open_date < '{now.isoformat()}'"
    elif "týždeň" in query or "tyzden" in query:
        start = now - datetime.timedelta(days=7)
        return f"open_date >= '{start.isoformat()}'"
    elif "mesiac" in query:
        start = now - datetime.timedelta(days=30)
        return f"open_date >= '{start.isoformat()}'"
    return None


def compute_processing_time(item):
    """Vypočíta dobu spracovania v hodinách (ak sú dostupné dátumy)."""
    try:
        open_date_str = item.get("open_date")
        close_date_str = item.get("close_date")
        if not open_date_str:
            return None
        open_dt = datetime.datetime.fromisoformat(open_date_str.replace("Z", "+00:00"))
        close_dt = (
            datetime.datetime.fromisoformat(close_date_str.replace("Z", "+00:00"))
            if close_date_str
            else datetime.datetime.utcnow()
        )
        delta = close_dt - open_dt
        return round(delta.total_seconds() / 3600, 2)
    except Exception:
        return None


@router.post("/query")
async def natural_query(request: Request):
    """
    Dynamická interpretácia dotazov s výpočtom trvania spracovania.
    """
    try:
        data = await request.json()
        query = data.get("query", "").lower()
        user = request.client.host or "anonymous"
        logger.info(f"[NATURAL] ({user}) Query: {query}")

        # === Určenie objektu ===
        obj = next((INTENT_MAP[k] for k in INTENT_MAP if k in query), "cr")

        # === Zostavenie WHERE filtra ===
        filters = []

        for k, v in STATUS_MAP.items():
            if k in query:
                if "nie" in query or "nie sú" in query or "nejsou" in query:
                    filters.append(f"status.sym != '{v}'")
                else:
                    filters.append(f"status.sym = '{v}'")

        for k, v in PRIORITY_MAP.items():
            if re.search(rf"priorit[aey]?\s*{k}", query):
                filters.append(f"priority.sym = '{v}'")

        date_filter = parse_date_range(query)
        if date_filter:
            filters.append(date_filter)

        user_match = re.search(r"(pre|užívateľ|používateľ)\s+([a-zA-Z0-9_.-]+)", query)
        if user_match:
            username = user_match.group(2)
            filters.append(f"affected_contact.userid = '{username}'")

        if not filters:
            filters.append("active_flag = 1")

        where_clause = " AND ".join(filters)

        attrs = "id,ref_num,summary,status,priority,assignee,category,open_date,last_mod_dt,close_date"

        path = f"{obj}?OP=GET_LIST&attrs={attrs}&WHERE={where_clause}&size=50"
        logger.info(f"[NATURAL] Query path: {path}")

        result = sdm_client.call_sdm(path)
        collection = next((result[k] for k in result if k.startswith("collection_")), {})
        items = collection.get(obj, [])
        if isinstance(items, dict):
            items = [items]

        for item in items:
            item["processing_time_hours"] = compute_processing_time(item)

        if items:
            memory.remember(user, "last_object", obj)
            memory.remember(user, f"{obj}_id", items[0].get("@id"))

        return {
            "query": query,
            "object": obj,
            "where": where_clause,
            "count": len(items),
            "items": items,
        }

    except Exception as e:
        logger.error(f"[NATURAL] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Natural query failed: {e}")
