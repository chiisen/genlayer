from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    redis_url: str = "redis://localhost:6379/0"
    redis_task_ttl: int = 3600
    openai_api_key: str = ""
    kling_api_key: str = ""
    kling_base_url: str = "https://api.klingai.com"
    app_env: str = "development"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
