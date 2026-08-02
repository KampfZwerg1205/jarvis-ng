from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "JARVIS-NG"
    version: str = "0.1.0-alpha.2"

    openai_api_key: str = ""
    gemini_api_key: str = ""

    ollama_url: str = "http://localhost:11434"

    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()