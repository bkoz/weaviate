import weaviate
import os
from dotenv import load_dotenv

# Loads env variables from $HOME/.env
load_dotenv(override=True)

WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
WEAVIATE_URL = f'https://{os.getenv("WEAVIATE_HOST")}'
print(f'\nWEAVIATE_URL: {WEAVIATE_URL}\n')

auth_config = weaviate.AuthApiKey(api_key = WEAVIATE_API_KEY)
client = weaviate.Client(url = WEAVIATE_URL, auth_client_secret=auth_config)

print(f'\nWEAVIATE_URL: {WEAVIATE_URL} is_ready() = {client.is_ready()}')
print(f'\ncluster.get_nodes_status(): {client.cluster.get_nodes_status()}\n')