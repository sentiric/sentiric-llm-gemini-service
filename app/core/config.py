# sentiric-llm-gemini-service/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric LLM Gemini Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    SERVICE_VERSION: str = "0.1.0"
    
    # Gemini API Ayarları
    GEMINI_API_KEY: str
    GEMINI_MODEL_ENDPOINT: str = "https://generativelanguage.googleapis.com"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()