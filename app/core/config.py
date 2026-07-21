from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(validation_alias="DATABASE_URL")
    secret_key: str = Field(min_length=32, validation_alias="SECRET_KEY")
    app_name: str = Field("TaskHub API", validation_alias="APP_NAME")
    app_env: Literal["local", "dev", "test", "prod"] = Field(
        "local",
        validation_alias="APP_ENV",
    )
    debug: bool = Field(False, validation_alias="APP_DEBUG")
    algorithm: str = Field("HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        30,
        validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )


settings = Settings()
