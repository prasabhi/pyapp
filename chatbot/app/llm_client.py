# Import OpenAI-compatible client
# OpenRouter supports the OpenAI SDK with a custom base URL
from openai import OpenAI

# Import configuration values (API key, site info)
from config import OPENROUTER_API_KEY, SITE_URL, SITE_NAME


# ---------------------------------------
# Create OpenRouter Client
# ---------------------------------------
# OpenAI SDK is used here, but the base_url points to OpenRouter
# This allows us to use OpenRouter as an LLM provider
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


# ---------------------------------------
# Function: Get Chatbot Response
# ---------------------------------------
def get_chat_response(message: str) -> str:
    """
    Sends a user message to the LLM via OpenRouter
    and returns the AI-generated response.

    Args:
        message (str): User input message

    Returns:
        str: Chatbot response from the LLM
    """

    # Create a chat completion request
    response = client.chat.completions.create(

        # Optional headers used by OpenRouter for analytics and ranking
        extra_headers={
            "HTTP-Referer": SITE_URL,   # Your application URL
            "X-Title": SITE_NAME,       # Application name
        },

        # LLM model hosted on OpenRouter
        model="tngtech/deepseek-r1t2-chimera:free",

        # Messages follow OpenAI chat format
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
    )

    # Extract and return the assistant's reply text
    return response.choices[0].message.content
