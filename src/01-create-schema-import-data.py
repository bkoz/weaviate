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
    logging.info('OPENAI_API_KEY is not set.')

logging.info("WEAVIATE_URL: %s", WEAVIATE_URL)
client = weaviate.Client(url = WEAVIATE_URL, auth_client_secret=auth_config)

logging.info('WEAVIATE_URL: %s, client.isReady(): %s', WEAVIATE_URL, client.is_ready())
logging.info('cluster.get_nodes_status(): %s', client.cluster.get_nodes_status())

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config,
    additional_headers={
        "X-HuggingFace-Api-Key": HUGGINGFACE_API_KEY
    }
)

logging.info(f'\nWEAVIATE_URL: {WEAVIATE_URL} is_ready() = {client.is_ready()}')

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-huggingface",
    "moduleConfig": {
        "text2vec-huggingface": {},
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        # Ensure the `generative-openai` module is used for generative queries
        "generative-openai": {
          "model": "gpt-3.5-turbo",  # Optional - Defaults to `gpt-3.5-turbo`
        }
    }
}

#
# Create the class if its not there
#
try:
    logging.info(f'\nCreating a class using the text2vec-huggingface vectorizer.')
    client.schema.create_class(class_obj)
except weaviate.exceptions.UnexpectedStatusCodeException:
    logging.info("Question class already exists, skipping")

#
# Load some questions.
#
resp = requests.get(
    'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json')
data = json.loads(resp.text)  # Load data

client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:  # Initialize a batch process
    for i, d in enumerate(data):  # Batch import data
        print(f"importing question: {i+1}")
        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }
        batch.add_data_object(
            data_object=properties,
            class_name="Question"
        )