import weaviate
import os
import logging
import requests
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Loads env variables from $HOME/.env
load_dotenv(override=True)

WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_DEFAULT_URL = "http://localhost:8080"
WEAVIATE_URL = os.getenv("WEAVIATE_URL", WEAVIATE_DEFAULT_URL)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if WEAVIATE_URL == WEAVIATE_DEFAULT_URL:
    logging.info('WEAVIATE_URL is not set, using http://localhost:8080')
if WEAVIATE_API_KEY == None:
    logging.info('WEAVIATE_API_KEY is not set, using anonymous access.')
    auth_config = None
else:
    logging.info('WEAVIATE_API_KEY is set, using API key access.')
    auth_config = weaviate.AuthApiKey(api_key = WEAVIATE_API_KEY)
if HUGGINGFACE_API_KEY == None:
    logging.error('HUGGINGFACE_API_KEY is not set.')
    exit(1)
if OPENAI_API_KEY == None:
    logging.error('OPENAI_API_KEY is not set, exiting!')
    exit(1)

logging.info("WEAVIATE_URL: %s", WEAVIATE_URL)

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config,
    additional_headers={
        "X-HuggingFace-Api-Key": HUGGINGFACE_API_KEY,
        "X-OpenAI-Api-Key" : OPENAI_API_KEY}
)

logging.info(f'\nWEAVIATE_URL: {WEAVIATE_URL} is_ready() = {client.is_ready()}')

#
# OpenAI query
#

# instruction for the generative module
response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_generate(single_prompt="Explain {answer} as you might to a five-year-old.")
    .with_limit(2)
    .do()
)

logging.info('==> OpenAI query')
logging.info(json.dumps(response, indent=4))

