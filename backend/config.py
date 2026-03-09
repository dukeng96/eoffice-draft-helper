"""Configuration module for backend API."""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # VNPT LLM API Configuration
    VNPT_API_KEY: str = os.getenv("VNPT_API_KEY", "")
    VNPT_BASE_URL: str = os.getenv(
        "VNPT_BASE_URL",
        "https://assistant-stream.vnpt.vn/v1/"
    )
    VNPT_MODEL: str = os.getenv("VNPT_MODEL", "llm-medium-v4")

    # Redis Configuration
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SESSION_TTL_HOURS: int = int(os.getenv("SESSION_TTL_HOURS", "24"))

    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")

    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.VNPT_API_KEY:
            raise ValueError("VNPT_API_KEY is required in .env file")


settings = Settings()
