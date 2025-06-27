from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR/'llm_chat.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # raw CSVs of keys -> list[str]
    PROVIDER_KEYS = {
        "openai":     [k.strip() for k in os.getenv("OPENAI_API_KEYS", "").split(",") if k],
        "anthropic":  [k.strip() for k in os.getenv("ANTHROPIC_API_KEYS", "").split(",") if k],
        "google":     [k.strip() for k in os.getenv("GOOGLE_API_KEYS", "").split(",") if k],
    }
