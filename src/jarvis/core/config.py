from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "JARVIS-NG"
    version: str = "0.1.0-alpha.2"
    gemini_model: str = "gemini-flash-latest"

    debug: bool = True

    ai_provider: str = "gemini"
    gemini_api_key: str = ""
    ollama_host: str = "http://localhost:11434"
    openai_api_key: str = ""

    system_prompt: str = (
    "Du bist JARVIS-NG, ein intelligenter, höflicher und präziser KI-Assistent. "
    "Antworte auf Deutsch, sofern der Nutzer keine andere Sprache verwendet."
)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="JARVIS_",
        extra="ignore",
    )  


settings = Settings()