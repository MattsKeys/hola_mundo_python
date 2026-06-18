from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / "githubtoken" / "cosas_api" / "GITHUB_TOKEN.env")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL")
