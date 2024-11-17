# from azure.identity import DefaultAzureCredential
from langchain.schema import HumanMessage, SystemMessage
# from langchain_openai import AzureChatOpenAI
from typing import Union, List
# from langchain.embeddings import AzureOpenAIEmbeddings

import numpy as np
import tiktoken

from openai import OpenAI
from typing import List, Optional, Tuple
import json


def run_model(
    system_message_content: str = "",
    human_message_content: str = "",
    history_message: list = [],
    deployment_model="gpt-3.5-turbo",
    ):
    """
    `Runs the Azure Chat OpenAI model with the given system and human messages content.

    Args:
        system_message_content (str): The content of the system message.
        human_message_content (str): The content of the human message. Defaults to "".
        history_message (list, optional): Chat history of the genai model. Defaults to [].
    Returns:
        response (str): responses from the genai model.
    """

    client = OpenAI()

    response = client.chat.completions.create(
        model = deployment_model,
        messages=[
            {
            "role": "system",
            "content": f'{system_message_content}'
            },
            {
            "role": "user",
            "content": f'{human_message_content}'
            }
        ],
        temperature=0.0,
        max_tokens=200,
        top_p=1
        )

    return response


# def get_embeddings(text: str) -> List[float]:
#     """
#     Get embeddings for the given text using Azure OpenAI service.

#     Args:
#         text (str): The text to embed.

#     Returns:
#         List[float]: The embeddings vectors for the text.
#     """
#     GENAI_PROXY = "https://genai-platform-dev.pg.com/stg/v1"
#     COGNITIVE_SERVICES = "https://cognitiveservices.azure.com/.default"
#     OPEN_API_VERSION = "2023-05-15"
#     HEADERS = {
#         "userid": "zou.qy@pg.com",
#         "project-name": "CustomAnalysis",
#     }

#     credential = DefaultAzureCredential(exclude_interactive_browser_credential=False)
#     token = credential.get_token(COGNITIVE_SERVICES).token

#     embeddings = AzureOpenAIEmbeddings(
#         azure_endpoint=GENAI_PROXY,
#         deployment="TEXT-EMBEDDING-ADA-002",
#         api_version=OPEN_API_VERSION,
#         api_key=token,
#         default_headers=HEADERS,
#     )

#     return embeddings.embed_query(text)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def token_cal(model="text-embedding-ada-002", cost_per_token=0.1 / 1000000, text=""):
    encoding = tiktoken.encoding_for_model(model)
    length = len(encoding.encode(text))
    return f"cost: {length * cost_per_token:.7f}"

def parse_response_for_query(response: str) -> Tuple[Optional[str], Optional[str]]:
    """
    This function parses a given response string to extract and return an explanation
    and an SQL query if present. It expects the SQL query to be enclosed within JSON
    format. If the response does not contain a query in JSON format, it returns the
    entire response as an explanation and `None` for the query.

    Parameters:
        response (str): The response string that potentially contains an explanation
                        and a SQL query in JSON format.

    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing the explanation and the
                                             SQL query if found, otherwise `None` for the
                                             query.
    """
    # Check if the response contains JSON-formatted data
    if '{' in response and '}' in response:
        json_data = '{' + response.split('{')[1].split('}')[0] + '}'
        # Clean up the JSON data by removing unnecessary characters
        json_data = json_data.replace('```json', '```').strip().replace('\n', '')
        data = json.loads(json_data)
        return data.get('question'), data.get('explanation'), data.get('query').replace('```', '')
    else:
        # If no JSON data is found, return the entire response as an explanation
        return response, None


if __name__ == "__main__":
    system_message_content = "You are a helpful assistant"
    human_message_content = "Tell me what is the difference between cat and dog"
    history_message = []
    response = run_model(system_message_content, human_message_content, history_message=[])
    print(f"answer: {response.content}")

    history_message.append(HumanMessage(content=human_message_content))
    history_message.append(response)
    human_message_content = "how about horse compare to them"
    response = run_model(system_message_content, human_message_content)
    print(f"answer: {response.content}")
