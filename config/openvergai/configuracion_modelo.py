from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")

API_KEYS = [
    os.getenv("API_MARKINIOS"),
    os.getenv("API_MATI"),
    os.getenv("API_EMA"),
    os.getenv("API_JUAN"),
]

# Elimina las que estén vacías o sean None
API_KEYS = [key for key in API_KEYS if key]

API_KEY = API_KEYS[0]
