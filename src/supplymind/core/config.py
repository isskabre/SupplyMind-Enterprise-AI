from functools import lru_cache

from pydantic import field_validator
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

    build_number: str | None = None
    git_commit: str | None = None
    build_timestamp: str | None = None
    deployment_name: str | None = None

    environment: Environment = Environment.DEVELOPMENT

    debug: bool = True
    log_level: str = "INFO"
    http_timeout_seconds: float = 10.0

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Validate and normalize the configured logging level."""

        normalized_value = value.upper()

        allowed_levels = {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if normalized_value not in allowed_levels:
            allowed_values = ", ".join(sorted(allowed_levels))
            raise ValueError(
                f"log_level must be one of: {allowed_values}"
            )

        return normalized_value

    @field_validator("http_timeout_seconds")
    @classmethod
    def validate_http_timeout_seconds(
        cls,
        value: float,
    ) -> float:
        """Validate the outbound HTTP timeout."""

        if value <= 0:
            raise ValueError(
                "http_timeout_seconds must be greater than zero."
            )

        return value

    @property
    def is_development(self) -> bool:
        """Return True when running in development."""

        return self.environment == Environment.DEVELOPMENT

    @property
    def is_testing(self) -> bool:
        """Return True when running in testing."""

        return self.environment == Environment.TEST

    @property
    def is_production(self) -> bool:
        """Return True when running in production."""

        return self.environment == Environment.PRODUCTION

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()


settings = get_settings()