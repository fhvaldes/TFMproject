from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Crear cliente de OpenAI
try:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
except OpenAIError as e:
    print(f"Failed to create OpenAI client: {e}")
    client = None

# Lista para almacenar frames codificados en base64
base64Frames = []

def generate_response(prompt_list):
    """
    Genera una respuesta de la API de OpenAI basada en la lista de prompts proporcionada.

    Args:
        prompt_list (list): Una lista de prompts para enviar a la API de OpenAI.

    Returns:
        str: El contenido del mensaje de respuesta de la API de OpenAI.
    """
    if client is None:
        return "OpenAI client is not initialized."

    message = [
        {"role": "user",
         "content": prompt_list,
         },
    ]
    parameters = {"model": "gpt-4-turbo-2024-04-09", "messages": message, "max_tokens": 2000,
                  "temperature": 0.6}

    try:
        result = client.chat.completions.create(**parameters)
        return result.choices[0].message.content
    except OpenAIError as e:
        return f"Failed to generate response: {e}"