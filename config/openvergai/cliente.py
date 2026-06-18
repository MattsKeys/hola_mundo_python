from openai import OpenAI
from .configuracion_modelo import GITHUB_TOKEN

client = OpenAI(
    api_key=GITHUB_TOKEN,
    base_url="https://models.github.ai/inference"
)