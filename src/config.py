import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return ("postgresql+asyncpg://admin:gLjjGw6caBQIZn1eZ1cOjlrzxlkehgLg@dpg-cre2685svqrc73fd3o30-a.oregon-postgres.render.com/dashboard_db_qnpf")

