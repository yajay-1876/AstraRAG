import os

from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings

class AgentSettings(BaseSettings):
    GROQ_API_KEY        : str
    VECTOR_STORE_DIR    : str
    COLLECTION_NAME     : str
    MODEL_NAME          : str
    MODEL_TEMPERATURE   : float

    class Config:
        env_file          = ".env"
        env_file_encoding = "utf-8"
        extra             = "allow"