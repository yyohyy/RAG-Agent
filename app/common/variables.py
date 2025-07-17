from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Variable(BaseSettings):
    POSTGRES_URL: str
    REDIS_URL: str
    REDIS_MEMORY_KEY: str
    LOG_PATH: str
    LOG_LEVEL: str
    OLLAMA_LLM_MODEL: str
    OLLAMA_EMBED_MODEL: str
    QDRANT_URL: str
    QDRANT_COLLECTION: str
    TAVILY_API_KEY: str
    CHUNK_SIZE:int
    SMTP_USER: str 
    SMTP_PASS: str
    SMTP_HOST: str
    SMTP_PORT: str

    model_config = ConfigDict(
        env_file=str(Path(__file__).resolve().parents[1] / ".env")
    )

variables = Variable()