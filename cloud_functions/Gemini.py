
from xmlrpc import client
from google import genai
from dotenv import load_dotenv
import os as osBib

load_dotenv()

def call_gemini(prompt: str) -> str:
    """
    Envia um prompt e documentos (opcional) para o modelo Gemini e retorna a resposta.

    Args:
        prompt: O prompt de texto a ser enviado para o modelo.

    Returns:
        A resposta do modelo Gemini como uma string.
    """

    client = genai.Client(vertexai=True, project=osBib.getenv("PROJECT_ID"), location=osBib.getenv("LOCATION"))

    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=genai.types.GenerateContentConfig(temperature=0.2)
    )

    return response.text