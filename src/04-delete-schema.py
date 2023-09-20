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
WEAVIATE_HOST = os.getenv("WEAVIATE_HOST")
WEAVIATE_URL = f'https://{os.getenv("WEAVIATE_HOST")}'
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if WEAVIATE_HOST == None:
    logging.error('WEAVIATE_HOST is not set.')
    exit(1)
if WEAVIATE_API_KEY == None:
    logging.error('WEAVIATE_API_KEY is not set.')
    exit(1)
if HUGGINGFACE_API_KEY == None:
    logging.error('HUGGINGFACE_API_KEY is not set.')
    exit(1)

logging.info(f'WEAVIATE_URL: {WEAVIATE_URL}')

auth_config = weaviate.AuthApiKey(api_key = WEAVIATE_API_KEY)

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config,
    additional_headers={
        "X-HuggingFace-Api-Key": HUGGINGFACE_API_KEY
    }
)

logging.info(f'\nWEAVIATE_URL: {WEAVIATE_URL} is_ready() = {client.is_ready()}')

logging.info(f'Deleting the Question class...')
client.schema.delete_class('Question')
