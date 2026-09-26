import os

from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text.strip()