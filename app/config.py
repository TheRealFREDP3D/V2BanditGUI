from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    ollama_host: str = Field("http://localhost:11434", env="OLLAMA_HOST")
    gemini_api_key: str = Field("", env="GEMINI_API_KEY")
    rate_limit: str = "1/90second"

    class Config:
        env_file = ".env"

settings = Settings()