import logging
from app.config import LOG_FILE, LOG_LEVEL
import os

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("sdmproxy")
logger.info(f"Logger initialized. Writing to {LOG_FILE}")
