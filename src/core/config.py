from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    environment: str = "dev"

    database_uri: str
    jwt_secret: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
