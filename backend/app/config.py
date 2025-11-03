"""Application configuration."""
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    # Database
    db_url: str = Field(
        default="mysql+asyncmy://appuser:password@localhost:3306/move_acces",
        alias="DB_URL",
    )
    db_pool_size: int = Field(default=20, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, alias="DB_MAX_OVERFLOW")
    db_pool_recycle: int = Field(default=1800, alias="DB_POOL_RECYCLE")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # Security
    app_secret: str = Field(..., alias="APP_SECRET")
    access_token_ttl_min: int = Field(default=15, alias="ACCESS_TOKEN_TTL_MIN")
    refresh_token_ttl_hours: int = Field(default=24, alias="REFRESH_TOKEN_TTL_HOURS")
    algorithm: str = "HS256"

    # Rate limiting
    rate_limit_login_per_min: int = Field(default=5, alias="RATE_LIMIT_LOGIN_PER_MIN")
    rate_limit_api_per_5min: int = Field(default=100, alias="RATE_LIMIT_API_PER_5MIN")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost", "http://localhost:3000"],
        alias="CORS_ORIGINS",
    )

    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True)

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"


settings = Settings()
