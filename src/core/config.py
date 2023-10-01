from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    environment: str = "dev"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
