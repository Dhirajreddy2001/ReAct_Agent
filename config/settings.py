import os
from pickletools import floatnl
from site import ENABLE_USER_SITE
from dotenv import load_dotenv
from config.constants import (
    DEFAULT_BEDROCK_MODEL_ID,
    DEFAULT_TEMPERATURE,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_TOKENS
    
)

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_REGION")

if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_DEFAULT_REGION:
    raise EnvironmentError("Missing AWS Credentials or import error from .env file")

BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID") or os.getenv("MODEL_STRING", DEFAULT_BEDROCK_MODEL_ID)


def _as_float(key:str, default:float) -> float:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        raise ValueError(f"Environmental Varibale {key} must be number got: {ValueError}")

def _as_int(key: str, default : int ) -> int:
    val = os.getenv(key)

    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        raise ValueError(f"Environment variable {key} must be an integer {ValueError}")

BEDROCK_TEMPERATURE = _as_float("BEDROCK_TEMPRATURE", DEFAULT_TEMPERATURE)
BEDROCK_MAX_TOKENS = _as_int("BEDROCK_MAX_TOKENS", DEFAULT_MAX_TOKENS)

APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)