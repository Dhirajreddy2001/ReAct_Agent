import logging
import sys
from config.settings import LOG_LEVEL

def setup_logging(level: str | None = None) -> None:
    """
    Configure global logging for the entire project.
    - Prints logs to stdout (so they appear in terminal and Docker)
    - Uses the LOG_LEVEL from config.settings by default
    """
    effective_level = (level or LOG_LEVEL).upper()

    logging.basicConfig(
        level=getattr(logging, effective_level, logging.INFO),
        format="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )