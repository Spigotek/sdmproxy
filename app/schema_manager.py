import os, json, requests
from app.auth_manager import auth_manager
from app.config import SDM_BASE_URL
from app.utils.logger import logger

SCHEMA_CACHE_DIR = "/opt/sdmproxy/cache/schemas"
os.makedirs(SCHEMA_CACHE_DIR, exist_ok=True)

# --- aliasy medzi prirodzenými názvami a SDM atribútmi ---
FIELD_ALIASES = {
    # všeobecné
    "title": ["summary", "sym", "description"],
    "description": ["sym", "description"],
    "details": ["description", "sym"],
    "category": ["category", "cr_cat", "chg_cat", "iss_cat", "prob_cat"],
    "status": ["status", "cr_stat", "chg_stat", "iss_stat"],
    "type": ["type", "cr_type", "chg_type", "iss_type"],
    "priority": ["priority", "pri"],
    "urgency": ["urgency", "urg", "urgency_code"],
    "impact": ["impact", "imp", "impact_code"],
    "sla": ["sla", "slalist"],
    # request / incident
    "requester": ["customer", "requester", "contact"],
    "assignee": ["assignee", "analyst", "owner"],
    "group": ["group", "group_id", "support_group"],
    # kontakty
    "contact": ["cnt", "contact", "requested_by"],
    "email": ["email_address", "email"],
    "phone": ["phone_number", "phone"],
    # role / user
    "role": ["role", "access_role", "user_role"],
    "tenant": ["tenant", "tenancy"],
}

# --- číselníky (možno doplniť podľa tvojej SDM inštalácie) ---
ENUM_MAPPINGS = {
    "priority": {"1": 504, "2": 503, "3": 502, "4": 501, "5": 500},
    "urgency": {"1": 300, "2": 301, "3": 302},
    "impact": {"1": 400, "2": 401, "3": 402},
}

class SchemaManager:
    def __init__(self):
        self.cache = {}

    def get_schema_path(self, object_name):
        return os.path.join(SCHEMA_CACHE_DIR, f"{object_name}.json")

    def load_schema_from_cache(self, object_name):
        path = self.get_schema_path(object_name)
        if os.path.exists(path):
            with open(path, "r") as f:
                schema = json.load(f)
                self.cache[object_name] = schema
                return schema
        return None

    def fetch_schema_from_sdm(self, object_name):
        logger.info(f"[SCHEMA] Fetching schema for {object_name}...")
        token = auth_manager.get_token()
        url = f"{SDM_BASE_URL}/{object_name}?OP=GET_SCHEMA"
        headers = {"X-AccessKey": str(token), "Accept": "application/json"}
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            raise Exception(f"Cannot fetch schema for {object_name}: {r.status_code}")
        data = r.json()
        attrs = []
        for attr in data.get(f"{object_name}_schema", {}).get("attribute", []):
            attrs.append({
                "name": attr.get("@name"),
                "type": attr.get("@type"),
                "required": attr.get("@required") == "true",
                "srel": attr.get("@srel_attr")
            })
        schema = {"object": object_name, "attributes": attrs}
        with open(self.get_schema_path(object_name), "w") as f:
            json.dump(schema, f, indent=2)
        self.cache[object_name] = schema
        return schema

    def get_schema(self, object_name):
        if object_name in self.cache:
            return self.cache[object_name]
        schema = self.load_schema_from_cache(object_name)
        if schema:
            return schema
        return self.fetch_schema_from_sdm(object_name)

    def map_alias(self, field, schema):
        field_lower = field.lower()
        # presné zhody
        for attr in schema["attributes"]:
            if attr["name"].lower() == field_lower:
                return attr["name"]
        # aliasy
        for canonical, aliases in FIELD_ALIASES.items():
            if field_lower == canonical or field_lower in aliases:
                for attr in schema["attributes"]:
                    if attr["name"].lower() in aliases:
                        return attr["name"]
        return None

    def normalize_payload(self, object_name, payload: dict):
        schema = self.get_schema(object_name)
        normalized = {}
        attrs = {a["name"]: a for a in schema["attributes"]}

        for key, value in payload.items():
            mapped = self.map_alias(key, schema)
            if not mapped:
                logger.warning(f"[SCHEMA] Unknown field {key} for {object_name}, skipping.")
                continue
            attr_def = attrs.get(mapped)
            if not attr_def:
                continue

            # typová transformácia
            if mapped in ENUM_MAPPINGS:
                val_map = ENUM_MAPPINGS[mapped]
                if str(value) in val_map:
                    normalized[mapped] = val_map[str(value)]
                    continue

            # SREL handling (relations)
            if attr_def.get("srel"):
                if isinstance(value, dict) and "id" in value:
                    normalized[mapped] = {"id": value["id"]}
                else:
                    normalized[mapped] = {"common_name": value}
            else:
                normalized[mapped] = value

        logger.info(f"[SCHEMA] Normalized payload for {object_name}: {normalized}")
        return normalized

schema_manager = SchemaManager()
