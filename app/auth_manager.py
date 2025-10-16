import os
import json
import time
import requests
from xml.etree import ElementTree as ET
from app.config import SDM_BASE_URL, SDM_USER, SDM_PASSWORD, TOKEN_FILE, TOKEN_REFRESH_INTERVAL
from app.utils.logger import logger


class AuthManager:
    def __init__(self):
        self.token_file = TOKEN_FILE
        self.token = None
        self.expires_at = 0
        self.load_token()

    def load_token(self):
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as f:
                    data = json.load(f)
                if data.get("access_key") and data.get("expires_at", 0) > time.time():
                    self.token = data["access_key"]
                    self.expires_at = data["expires_at"]
                    logger.info(f"[AUTH] Loaded cached token ({self.token})")
                    return
            except Exception as e:
                logger.warning(f"[AUTH] Could not read token cache: {e}")
        logger.info("[AUTH] No valid cached token found — will request new one")

    def save_token(self, key: str, expires: int):
        try:
            with open(self.token_file, "w") as f:
                json.dump({"access_key": key, "expires_at": expires}, f)
            logger.info(f"[AUTH] Token saved (expires at {expires})")
        except Exception as e:
            logger.error(f"[AUTH] Could not save token: {e}")

    def get_token(self):
        if self.token and self.expires_at > time.time():
            return self.token
        return self.fetch_new_token()

    def fetch_new_token(self):
        url = f"{SDM_BASE_URL}/rest_access"
        headers = {
            "Content-Type": "application/xml",
            "Accept": "application/xml",
        }

        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<rest_access>
  <user>{SDM_USER}</user>
  <password>{SDM_PASSWORD}</password>
</rest_access>"""

        logger.info(f"[AUTH] Requesting new SDM token from {url}")
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code != 201:
            logger.error(f"[AUTH] Authentication failed ({response.status_code}): {response.text}")
            raise Exception(f"SDM XML login failed ({response.status_code})")

        xml_root = ET.fromstring(response.text)
        access_key = xml_root.findtext("access_key")
        exp_date = xml_root.findtext("expiration_date")

        if not access_key:
            raise Exception("Missing access_key in SDM XML response")

        expires_at = int(exp_date) if exp_date else int(time.time() + TOKEN_REFRESH_INTERVAL)
        self.token = access_key
        self.expires_at = expires_at
        self.save_token(access_key, expires_at)
        logger.info(f"[AUTH] New SDM AccessKey acquired: {access_key}")
        return access_key


auth_manager = AuthManager()
