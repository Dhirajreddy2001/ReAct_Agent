from dotenv.main import logger
from langchain_aws import ChatBedrockConverse
from cache.llm_cache import enable_llm_cache
from config.settings import(
    AWS_DEFAULT_REGION,
    BEDROCK_MODEL_ID,
    BEDROCK_TEMPERATURE,
    BEDROCK_MAX_TOKENS,
)

import logging

logger = logging.getLogger(__name__)

def load_claude():


    llm = ChatBedrockConverse(

        region_name = AWS_DEFAULT_REGION,
        model_id = BEDROCK_MODEL_ID,
        temperature=float(BEDROCK_TEMPERATURE),
        max_tokens=int(BEDROCK_MAX_TOKENS),
    )

    logger.info(f"Claude Model Initalized:  {BEDROCK_MODEL_ID}")

    return llm