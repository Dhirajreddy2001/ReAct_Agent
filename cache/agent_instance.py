import os
from graph import build_graph
from cache.cache_class import cache
from typing import Optional

CONFIG_VERSION = os.getenv("CONFIG_VERSION", "v1")


def get_agent():
    
    """ return an pre-compiled agent if there no change to version
       if there is  change in version number build new agent and return it
    """
    key = f"agent_instance: {CONFIG_VERSION}"

    agent  = cache.get(key)
    if agent is not None:
        return agent

    agent = build_graph()

    cache.set(key, agent, ttl = None)

    return agent