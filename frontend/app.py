import chainlit as cl
from reasonedge import DeepReasonerClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()

REASONING_ALGORITHMS_OPTIONS = {
    "Chain of Thought": "chain_of_thought",
    "Reasoning via Planning": "reasoning_via_planning",
    "Tree of Thought": "tree_of_thought"
}

# Initialize the client
client = DeepReasonerClient(
    api_key=os.getenv("REASONER_API_KEY"),
    base_url="https://deepreasoner.azure-api.net",
    api_version="/"
)

import chainlit as cl
from chainlit.input_widget import Select, Switch, Slider

# Configure logging
logging.basicConfig(level=logging.INFO)

@cl.on_chat_start
async def start():
    settings = await cl.ChatSettings(
        [
            Select(
                id="ReasoningAlgorithm",
                label="Reasoning Algorithm",
                values=["Chain of Thought", "Reasoning via Planning", "Tree of Thought"],
                initial_index=0,
            ),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=1,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()


@cl.on_settings_update
async def setup_agent(settings):
    logging.info("on_settings_update: %s", settings)

    cl.user_session.set("settings", {
        "reasoning_algorithm": REASONING_ALGORITHMS_OPTIONS[settings["ReasoningAlgorithm"]],
        "temperature": settings["Temperature"],
        "reasoning_algorithm_full_name": settings["ReasoningAlgorithm"]
    })


@cl.step(type="llm", name="Reasoning")
async def reason(prompt: str, temperature: float, reasoning_algorithm: str):
    # Call the reasoning API using the client
    settings = cl.user_session.get("settings")
    result = await cl.make_async(client.reason)(
        prompt=prompt,
        temperature=settings["temperature"],
        reasoning_algorithm=settings["reasoning_algorithm"]
        )
    response = result['response']

    return response

@cl.on_message
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends the message to the reasoning API using DeepReasonerClient.

    Args:
        message: The user's message.
    """
    settings = cl.user_session.get("settings")
    prompt = message.content

    # Check if settings is None
    if settings is None:
        temperature = 0.7
        reasoning_algorithm = "chain_of_thought"
        reasoning_algorithm_full_name = "Chain of Thought"
    else:
        temperature = settings["temperature"]
        reasoning_algorithm = settings["reasoning_algorithm"]
        reasoning_algorithm_full_name = settings["reasoning_algorithm_full_name"]

    try:
        with cl.Step(type="llm", name=reasoning_algorithm_full_name + " To Reason") as step:
            result = await cl.make_async(client.reason)(
                prompt=prompt,
                temperature=temperature,
                reasoning_algorithm=reasoning_algorithm
            )
            logging.info("Result: %s", result)
            response = result['response']

        await cl.Message(content=response).send()
        
    except Exception as e:
        # Handle any errors
        await cl.Message(content=f"Error: {str(e)}").send()
        # Handle any errors
        await cl.Message(content=f"Error: {str(e)}").send()
