from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):

    APP_NAME: str
    DEBUG: bool = False

    KEYCLOAK_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_LOGIN_CLIENT_ID: str

    KEYCLOAK_ADMIN_CLIENT_ID: str
    KEYCLOAK_ADMIN_SECRET: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()