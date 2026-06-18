import os
import logging
from typing import List, Dict, Generator
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(override=True)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Constantes de configuración
MODEL_GEMINI = 'gemini-2.5-flash' 
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
MODEL_OLLAMA = 'qwen2.5' 
OLLAMA_URL = "http://localhost:11434/v1"

# Inicialización de clientes
gemini_client = OpenAI(api_key=GOOGLE_API_KEY or "dummy_key", base_url=GEMINI_URL)
ollama_client = OpenAI(base_url=OLLAMA_URL, api_key="ollama")

SYSTEM_MESSAGE = "Sos un asistente de IA llamado Gandalf, con la sabiduría y humor de un mago de Tolkien..."

def chat(message: str, history: List[Dict[str, str]]) -> Generator[str, None, None]:
    formatted_history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": SYSTEM_MESSAGE}] + formatted_history + [{"role": "user", "content": message}]
    
    try:
        if not GOOGLE_API_KEY: raise ValueError("API Key faltante")
        stream = gemini_client.chat.completions.create(model=MODEL_GEMINI, messages=messages, stream=True)
        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content
                yield response
    except Exception as e:
        logging.warning(f"Fallback activado: {e}")
        response = "*(La conexión con Valinor se ha debilitado. Recurriendo a mi magia local...)*\n\n"
        yield response
        try:
            stream_local = ollama_client.chat.completions.create(model=MODEL_OLLAMA, messages=messages, stream=True)
            for chunk in stream_local:
                if chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content
                    yield response
        except Exception as e_local:
            yield f"Error crítico: {e_local}"

with gr.Blocks(title="Gandalf AI") as demo:
    gr.Markdown("# 🧙‍♂️ Gandalf AI")
    gr.Markdown("Asistente experto con respaldo local automático.")
    gr.ChatInterface(fn=chat)

if __name__ == "__main__": 
    demo.launch(theme="soft")