"""Application configuration using environment variables."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "move_acces"
    DB_USER: str = "root"
    DB_PASS: str = ""

    # JWT
    JWT_SECRET: str = "change_me"
    JWT_ALG: str = "HS256"
    ACCESS_EXPIRE_MIN: int = 15
    REFRESH_EXPIRE_DAYS: int = 15

    # CORS
    CORS_ORIGINS: list[str] = ["*"]

    @property
    def DATABASE_URL(self) -> str:
        """Build MySQL database URL."""
        return f"mysql+mysqldb://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
