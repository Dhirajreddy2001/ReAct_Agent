from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable, Dict, Any
from cache.cache_class import cache, make_key
from nodes.utils import normalize
import hashlib

def _digest(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def node_cache(ttl: int = 600, key_prefix: str = "", include_plan: bool = True):
    """
    Cache a node's output. If include_plan=False, the cache key ignores plan/thought.
    """
    def deco(func: Callable[..., Any]):
        node_name = key_prefix or func.__name__

        def _make_key_from(state: Dict[str, Any], maybe_llm: Any = None) -> str:
            raw_q = state.get("input") or state.get("question") or ""
            norm_q = normalize(raw_q)

            plan = state.get("thought") or state.get("plan") or ""
            plan_part = _digest(plan) if (include_plan and plan) else "noplan"

            model_id = getattr(maybe_llm, "model_id", None) or getattr(maybe_llm, "_model_id", None) or "unknown_model"
            temperature = getattr(maybe_llm, "temperature", None)
            temp_str = str(temperature) if temperature is not None else "tNA"

            return make_key("node", node_name, norm_q, plan_part, model_id, temp_str)

        if iscoroutinefunction(func):
            @wraps(func)
            async def aw_wrapper(*args, **kwargs):
                if not args:
                    raise ValueError("node function must receive state as first positional argument")
                state = args[0]
                maybe_llm = kwargs.get("llm", None) or (len(args) >= 2 and args[1]) or None
                key = _make_key_from(state, maybe_llm)
                hit = cache.get(key)
                if hit is not None:
                    print(f"[Cache Hit] Node: {node_name}")
                    return hit
                out = await func(*args, **kwargs)
                cache.set(key, out, ttl=ttl)
                print(f"[Cache Miss] Node: {node_name}")
                return out
            return aw_wrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                raise ValueError("node function must receive state as first positional argument")
            state = args[0]
            maybe_llm = kwargs.get("llm", None) or (len(args) >= 2 and args[1]) or None
            key = _make_key_from(state, maybe_llm)
            hit = cache.get(key)
            if hit is not None:
                print(f"[Cache Hit] Node: {node_name}")
                return hit
            out = func(*args, **kwargs)
            cache.set(key, out, ttl=ttl)
            print(f"[Cache Miss] Node: {node_name}")
            return out
        return wrapper
    return deco
