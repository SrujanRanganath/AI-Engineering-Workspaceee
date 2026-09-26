from config import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)


def ask_llm(prompt: str) -> str:
    """
    Send a prompt to Gemini and return the generated text.
    """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text.strip()
