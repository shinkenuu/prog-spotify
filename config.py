from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    SPOTIPY_CLIENT_ID: str
    SPOTIPY_CLIENT_SECRET: str

    SPOTIFY_DATABASE_URI: str = (
        "mongodb://root:leaf@127.0.0.1:27018/spotify"
        "?authSource=admin&authMechanism=SCRAM-SHA-256"
    )

    PROGARCHIVES_DATABASE_URL: str = (
        "postgresql://prog:prog@127.0.0.1:5432/progarchives"
    )

    PAGINATION_INTERVAL_SECONDS: int = Field(default=3, alias="SLEEP_SECONDS")
    MIN_SECONDS_BETWEEN_REQUESTS: int = 3


settings = Settings()
