import weaviate
import os
import logging
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
    logging.info('HUGGINGFACE_API_KEY is not set.')
if OPENAI_API_KEY == None:
    logging.info('OPENAI_API_KEY is not set.')

logging.info("WEAVIATE_URL: %s", WEAVIATE_URL)
client = weaviate.Client(url = WEAVIATE_URL, auth_client_secret=auth_config)

logging.info('WEAVIATE_URL: %s, client.isReady(): %s', WEAVIATE_URL, client.is_ready())
logging.info('cluster.get_nodes_status(): %s', client.cluster.get_nodes_status())
