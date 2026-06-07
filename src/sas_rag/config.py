from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-5.4"

    langsmith_api_key: str = ""
    langsmith_tracing: bool = False
    langsmith_project: str = "sas-rag"

    sas_rag_chroma_path: str = "data/chroma"
    sas_rag_chroma_collection: str = "sas_94_docs"
    sas_rag_source_dir: str = "docs/sas-documents"
    sas_rag_whitelist: str = "data/source_whitelist.json"
    sas_rag_ingestion_out: str = "data/ingestion/runs/latest"


settings = Settings()
