from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import List
from urllib.parse import quote_plus
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str
    app_version: str
    app_description: str = "CIVIC DATA LAB"
    app_title:str

    docs_url: str | None = "/docs"
    redoc_url: str | None = "/redoc"
    openapi_url: str | None = "/openapi.json"

    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    webhook_secret: str
    api_key: str
    cors_origins: List[str] = ["*"]

    session_secret_key: str
    secret_key: str
    log_level: str = "INFO"
    server_host:str="127.0.0.1"
    server_port:int=8000
    server_reload:bool=True
    jwt_secret: str
    jwt_algorithm: str = "HS512"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    reset_token_expire_minutes:int = 10

    @property
    def database_url(self) -> str:
        password = quote_plus(self.db_password)
        return (
            f"postgresql://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid"
    )


settings = Settings()