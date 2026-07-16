from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Atlas"
    app_version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///atlas.db"

    # Market Data Providers
    fmp_api_key: str | None = None
    alpha_vantage_api_key: str | None = None

    # Metadata refresh policy
    metadata_cache_days: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ATLAS_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
