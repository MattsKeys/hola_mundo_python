from openai import OpenAI

from .prompt import SYSTEM_PROMPT
from .cliente import client
from .modelos import GPT41
from .parametros import TEMPERATURE
from .configuracion_modelo import GITHUB_TOKEN, DEFAULT_MODEL

def preguntar(prompt_usuario):
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ]

    respuesta = client.chat.completions.create(

    model=DEFAULT_MODEL,

    messages=messages,

    temperature=TEMPERATURE

    )

    return respuesta.choices[0].message.content