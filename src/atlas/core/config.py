from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Atlas"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///atlas.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ATLAS_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
