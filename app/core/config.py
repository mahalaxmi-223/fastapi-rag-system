from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Ignore .env keys that don't map to a field, so Phase 0's settings
    # can coexist with keys (CHROMA_PERSIST_DIR, QDRANT_URL, ...) that
    # will be wired up in later phases.
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    APP_NAME: str = "RAG-System"
    ENVIRONMENT: str = "development"


settings = Settings()
