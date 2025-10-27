# cache/llm_cache.py
import os
from typing import Any, Optional
from langchain.globals import set_llm_cache
from langchain.cache import SQLiteCache
from langchain_core.caches import BaseCache

DEBUG_CACHE = os.getenv("DEBUG_CACHE", "false").lower() == "true"


class VerboseSQLiteCache(BaseCache):
    """
    Wrapper around SQLiteCache that logs HIT/MISS/STORE.
    Implements both sync and async APIs required by BaseCache.
    """

    def __init__(self, database_path: str):
        self._inner = SQLiteCache(database_path=database_path)
        self._db_path = database_path

    # ------------- Required SYNC API (LangChain BaseCache) -------------

    def get(self, prompt: Any, llm_string: str) -> Optional[Any]:
        """Return cached value if present, else None."""
        val = self._inner.get(prompt, llm_string) \
              if hasattr(self._inner, "get") else self._inner.lookup(prompt, llm_string)
        if DEBUG_CACHE:
            tag = "HIT" if val is not None else "MISS"
            print(f"[LLM Cache {tag}] model={llm_string[:60]}...")
        return val

    def set(self, prompt: Any, llm_string: str, return_val: Any) -> None:
        """Store a value in cache."""
        if DEBUG_CACHE:
            print(f"[LLM Cache STORE] model={llm_string[:60]}...")
        if hasattr(self._inner, "set"):
            self._inner.set(prompt, llm_string, return_val)
        else:
            self._inner.update(prompt, llm_string, return_val)

    def clear(self) -> None:
        """Clear all cached items."""
        if hasattr(self._inner, "clear"):
            self._inner.clear()
        else:
            # Fallback: recreate the inner cache file
            from langchain.cache import SQLiteCache as _SQLiteCache
            self._inner = _SQLiteCache(database_path=self._db_path)

    # ------------- Required ASYNC API (LangChain BaseCache) -------------

    async def aget(self, prompt: Any, llm_string: str) -> Optional[Any]:
        # Delegate to sync to keep it simple
        return self.get(prompt, llm_string)

    async def aset(self, prompt: Any, llm_string: str, return_val: Any) -> None:
        self.set(prompt, llm_string, return_val)

    async def aclear(self) -> None:
        self.clear()

    # ------------- Back-compat shims (older code paths) ----------------
    # If something still calls lookup/update, keep them working.

    def lookup(self, prompt: Any, llm_string: str) -> Optional[Any]:
        return self.get(prompt, llm_string)

    def update(self, prompt: Any, llm_string: str, return_val: Any) -> None:
        self.set(prompt, llm_string, return_val)


def enable_llm_cache() -> None:
    """
    Enable a persistent LLM cache using SQLite (verbose).
    MUST be called before any LLM is created.
    """
    db_path = os.getenv("LLM_CACHE_PATH", ".lc_cache.sqlite3")
    set_llm_cache(VerboseSQLiteCache(database_path=db_path))
    print(f"[LLM Cache] SQLite cache enabled at {db_path} (verbose={DEBUG_CACHE})")
