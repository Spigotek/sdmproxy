import os

# === SDM server ===
SDM_BASE_URL = "http://10.11.35.35:8050/caisd-rest"
SDM_USER = "vueuser"
SDM_PASSWORD = "Vue@user123!"

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "../logs")
os.makedirs(LOG_DIR, exist_ok=True)

TOKEN_FILE = os.path.join(LOG_DIR, "sdm_token.json")
TOKEN_REFRESH_INTERVAL = 3600 * 4  # 4 hours

# === Logging ===
LOG_FILE = os.path.join(LOG_DIR, "sdmproxy.log")
LOG_LEVEL = "INFO"
