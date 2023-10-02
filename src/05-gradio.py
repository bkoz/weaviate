import weaviate_utils
import os
import logging
import requests
import json
import gradio as gr

client = weaviate_utils.weaviate_connection()
logging.info(f'\nclient.is_ready() = {client.is_ready()}')

#
# OpenAI query
#
def generative_search(concept: str, prompt: str) -> str:
    response = (
        client.query
        .get("Question", ["question", "answer", "category"])
        .with_near_text({"concepts": [concept]})
        .with_generate(single_prompt=prompt)
        .with_limit(1)
        .do()
    )

    logging.info('==> OpenAI query')
    logging.info(json.dumps(response, indent=4))
    output = json.dumps(response, indent=4)
    result = response.get('data')['Get']['Question'][0]['_additional']['generate']['singleResult']
    return result
gr.Interface(max_lines=20, fn=generative_search, inputs=["text", "text"], outputs="text",
    examples=[["biology", "Explain {answer} as you might to a five-year-old."],
              ["biology", "Explain {answer} as you might to a graduate student."]])\
    .launch()