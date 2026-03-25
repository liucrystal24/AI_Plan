from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Enterprise RAG QA"
    app_env: str = "dev"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    db_path: str = "./rag.db"
    default_top_k: int = 6
    min_evidence_score: float = 0.15
    max_context_chunks: int = 8
    allowed_doc_extensions: str = ".md"
    enable_query_masking: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
