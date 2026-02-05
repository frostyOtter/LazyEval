from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    """

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

    # Model API Configuration
    MODEL_NAME: str = Field(..., description="Name of the model to use")
    MODEL_BASE_URL: str = Field(
        ..., description="Base URL for the OpenAI-compatible API"
    )
    MODEL_API_KEY: str = Field(..., description="API key for authentication")

    # Langfuse Configuration
    LANGFUSE_PUBLIC_KEY: str = Field(..., description="Langfuse public API key")
    LANGFUSE_SECRET_KEY: str = Field(..., description="Langfuse secret API key")
    LANGFUSE_BASE_URL: str = Field(
        default="https://cloud.langfuse.com", description="Langfuse base URL"
    )

    # HuggingFace Configuration
    HF_TOKEN: str = Field(..., description="Hugging Face API key")
    GEMINI_API_KEY: str = Field(..., description="Gemini API key")


# Global settings instance
@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()  # type: ignore


settings = get_settings()
