from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    supabase_url: str = ""
    auth_users_url: str = "http://localhost:8001"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache

def get_settings() -> Settings:
    return Settings()
