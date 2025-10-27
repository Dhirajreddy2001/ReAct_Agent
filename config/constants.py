import os
from dotenv import load_dotenv

load_dotenv()


DEFAULT_BEDROCK_MODEL_ID = os.getenv("MODEL_STRING")
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = os.getenv("MODEL_MAX_TOKENS")


DEFAULT_LOG_LEVEL = "INFO"