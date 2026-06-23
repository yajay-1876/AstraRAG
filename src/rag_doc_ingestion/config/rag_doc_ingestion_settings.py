from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class RAG_DocIngestionSettings(BaseSettings):
    # Settings that are used for document ingestion only
    DOCUMENTS_DIR: str
    VECTOR_STORE_DIR: str
    COLLECTION_NAME: str

    class Config:
        env_file= ".env"
        env_file_encoding= "utf-8"
        extra= "allow"