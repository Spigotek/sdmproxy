import time
from collections import defaultdict
from app.utils.logger import logger

class ContextMemory:
    """
    Jednoduchá pamäťová vrstva pre konverzačné dotazy.
    Uchováva informácie o posledných objektoch (napr. incident, kontakt) podľa používateľa.
    """

    def __init__(self):
        self.memory = defaultdict(dict)
        self.ttl = 600  # 10 minút

    def _cleanup(self):
        now = time.time()
        for user in list(self.memory.keys()):
            for key, value in list(self.memory[user].items()):
                if now - value["timestamp"] > self.ttl:
                    del self.memory[user][key]

    def remember(self, user: str, key: str, value):
        """Uloží kontext (napr. incident_id, kontakt_id)."""
        self._cleanup()
        self.memory[user][key] = {"value": value, "timestamp": time.time()}
        logger.info(f"[MEMORY] {user}: {key} = {value}")

    def recall(self, user: str, key: str):
        """Vráti poslednú uloženú hodnotu."""
        self._cleanup()
        if key in self.memory[user]:
            return self.memory[user][key]["value"]
        return None

    def clear(self, user: str):
        """Vymaže všetky kontexty pre používateľa."""
        if user in self.memory:
            del self.memory[user]
            logger.info(f"[MEMORY] Cleared for {user}")

memory = ContextMemory()
