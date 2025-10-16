import requests
from app.auth_manager import auth_manager
from app.config import SDM_BASE_URL
from app.utils.logger import logger


class SDMClient:
    def __init__(self):
        self.base_url = SDM_BASE_URL

    def call_sdm(self, method: str, path: str, params=None, data=None):
        token = auth_manager.get_token()
        headers = {
            "X-AccessKey": str(token),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/{path.lstrip('/')}"
        logger.info(f"[SDM CALL] {method} {url}")

        resp = requests.request(method, url, headers=headers, params=params, json=data)

        if resp.status_code >= 400:
            logger.error(f"[SDM ERROR] {resp.status_code}: {resp.text[:200]}")
            raise Exception(f"SDM call failed: {resp.status_code}: {resp.text}")

        return resp.json()

    def get(self, path: str, params=None):
        return self.call_sdm("GET", path, params=params)

    def post(self, path: str, data=None):
        return self.call_sdm("POST", path, data=data)

    def put(self, path: str, data=None):
        return self.call_sdm("PUT", path, data=data)

    def delete(self, path: str):
        return self.call_sdm("DELETE", path)


sdm_client = SDMClient()
