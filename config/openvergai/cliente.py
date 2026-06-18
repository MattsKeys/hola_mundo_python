from openai import OpenAI
from .configuracion_modelo import API_KEY

client = OpenAI(
    api_key=API_KEY,
    base_url="https://models.github.ai/inference"
)