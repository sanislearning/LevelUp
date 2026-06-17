from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    PORT: int = 5000
    MONGODB_URI: str = Field(..., description="MongoDB connection URI")
    ANTHROPIC_API_KEY: str = Field(..., description="Anthropic API key for AI features")
    ENVIRONMENT: str = "development"
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()  # type: ignore[call-arg]

