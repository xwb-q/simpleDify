import os
from typing import Optional
from pydantic_settings import BaseSettings

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dify-like Backend"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./dify.db"
    QWEN_API_KEY: str = os.environ.get("QWEN_API_KEY", "")
    QWEN_BASE_URL: str = os.environ.get("QWEN_BASE_URL", "")
    
    class Config:
        case_sensitive = True
        env_file = ".env"  # Automatically load from .env file
        env_file_encoding = "utf-8"

settings = Settings()