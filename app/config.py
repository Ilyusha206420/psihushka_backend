from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import ClassVar

class Settings(BaseSettings):

    database_url: str = Field(default=..., validation_alias="DATABASE_URL")

    debug: bool = True

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8"
    )

settings = Settings()
