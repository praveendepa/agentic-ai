# from chainlit import Message

import agentic_ai.config as config

from agentic_ai.functions.llm_fn import run_model
from agentic_ai.models.memory import Memory
from agentic_ai.models.prompt import PromptData


def converse(message: str, memory=[]):
    """Converse with user

    Args:
        message: list
        memory: str

    Returns:
        str: Response from AI model
    """
    response = run_model(PromptData().get_user_agent_prompt(), message, memory, deployment_model=config.MODEL_NAME)
    return response


if __name__ == "__main__":
    msg = "find the highest purchase intention?"
    memory = []
    response = converse(msg, memory)
    print(response.content)
