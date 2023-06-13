import sys
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator

if "pytest" in sys.modules:
    _ENV_FILE = "env.TEST"
else:
    _ENV_FILE = ".env"


class DBConfig(BaseSettings):
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "custom_bot_db"
    DATABASE_URL: Optional[PostgresDsn] = None

    class Config:
        case_sensitive = True

    @validator("DATABASE_URL", pre=True, allow_reuse=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB', '')}",
        )


class Config(DBConfig):
    PROJECT_NAME: str = "LLM_Magic"
    OPENAI_API_KEY: str = "placeholder"
    MOCK_GENERATE: bool = False

    class Config:
        env_file: str = _ENV_FILE


api_config = Config()
db_config = DBConfig()
