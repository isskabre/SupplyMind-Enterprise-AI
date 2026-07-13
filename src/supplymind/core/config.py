from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from supplymind import __version__
from supplymind.core.enums import Environment

class Settings(BaseSettings):
    """
    Central application configuration.

    Values can come from:
    - Environment variables
    - .env file
    - Default values defined below
    """

    app_name: str = "SupplyMind Enterprise AI"
    app_version: str = __version__

    environment: Environment = Environment.DEVELOPMENT

    debug: bool = True

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """
    return Settings()


settings = get_settings()