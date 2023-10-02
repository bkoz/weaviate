import weaviate
import os
import logging
from dotenv import load_dotenv

def weaviate_connection() -> weaviate.Client:
    """
    Description:
       Connect to the weaviate server.
       Reads the following environment variables:
       WEAVIATE_API_KEY
       WEAVIATE_URL
       HUGGINGFACE_API_KEY
       OPENAI_API_KEY

    Returns:
        weaviate.Client: The client connection object
    """
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
    
    try:
        client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=auth_config,
        additional_headers={
            "X-HuggingFace-Api-Key": HUGGINGFACE_API_KEY,
            "X-OpenAI-Api-Key" : OPENAI_API_KEY}
        )
    except:
        logging.error('Weaviate connection error, exiting!')
        exit(1)


    return client
