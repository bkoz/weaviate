import requests
import json
import os
from dotenv import load_dotenv
import weaviate

# Loads env variables from $HOME/.env
load_dotenv(override=True)

#
# Expects the following env variables to be set:
#
WEAVIATE_URL = f'https://{os.getenv("WEAVIATE_HOST")}'
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print(f'OPENAI_API_KEY = {OPENAI_API_KEY}')
print(f'\nWEAVIATE_URL: {WEAVIATE_URL}')

auth_config = weaviate.AuthApiKey(api_key = WEAVIATE_API_KEY)
# client = weaviate.Client(url = WEAVIATE_URL, auth_client_secret=auth_config)

client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=auth_config,
    additional_headers={
        "X-HuggingFace-Api-Key": HUGGINGFACE_API_KEY,
        "X-OpenAI-Api-Key" : OPENAI_API_KEY}
)

print(f'\nWEAVIATE_URL: {WEAVIATE_URL} is_ready() = {client.is_ready()}')

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
    print(f'\nCreating a class using the text2vec-huggingface vectorizer.')
    client.schema.create_class(class_obj)
except weaviate.exceptions.UnexpectedStatusCodeException:
    print("Question class already exists, skipping")

# print(client.schema.get()['classes'])

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

#
# Queries
#
result = client.query.get("Question", ["question", "answer"]).with_additional(
    ["score"]).with_hybrid("Venus", alpha=0.25, properties=["question"]).with_limit(3).do()

print(json.dumps(result, indent=4))

response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_where({
        "path": ["category"],
        "operator": "Equal",
        "valueText": "ANIMALS"
    })
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4))

response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text({"concepts": ["biology"]})
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4))

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


print(f'==> OpenAI query')
print(json.dumps(response, indent=4))

print(f'\nDeleting the Question class...\n')
client.schema.delete_class('Question')
