from concurrent.futures import thread
from pickletools import floatnl
import threading
import time
import hashlib
from typing import Any, Dict, Optional

from httpx import delete
from langchain_core.messages.utils import _default_text_splitter

class CacheClass:

    def __init__(self, default_ttl : int = 600, max_size: int = 1000):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._lock = threading.RLock()

    def __cleanup_expired(self) -> None:

        current_time = time.time()
        expired = [key for key,data in self.cache.items()
                if data["expires_at"] <= current_time]
        for key in expired:
            self.cache.pop(key, None)

    def _enforce_max_size(self) -> None:

        if len(self.cache) > self.max_size:
            sorted_items = sorted(
                self.cache.items(),
                key = lambda x:x[1]["created_at"]

            )
            to_remove = int(self.max_size * 0.2)
            for key, _ in sorted_items[:to_remove]:
                self.cache.pop(key, None)


    def _now(self) -> float:
        return time.time()

    def get(self, key: str) -> Optional[Any]:

        with self._lock:
            self.__cleanup_expired()
            item  = self.cache.get(key)
            if item and item["expires_at"] > self._now():
                return item["value"]
            elif item:

                self.cache.pop(key, None)

            return None

    def set(self, key: str, value:Any, ttl: Optional[int] = None) -> None:

        with self._lock:
            ttl = ttl or self.default_ttl
            now = self._now()
            self.cache[key] = {
                "value" : value,
                "created_at": now,
                "expires_at" : now + ttl
            }

            self._enforce_max_size()

    
    def delete(self, key: str) -> None:

        with self._lock:
            self.cache.pop(key, None)

    def clear(self) -> None:

        with self._lock:
            self.cache.clear()


    def stats(self) -> Dict[str, Any] :

        with self._lock:
            self.__cleanup_expired()
            return {
                "size" : len(self.cache),
                "max_size": self.max_size,
                "default_ttl" : self.default_ttl,
            }

cache = CacheClass()

def make_key(*parts: str) -> str:

    raw = ":".join(parts)
    return hashlib.md5(raw.encode()).hexdigest()