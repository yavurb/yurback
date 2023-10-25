from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    environment: str = "dev"

    database_uri: str
    jwt_secret: str

    # AWS
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_s3_bucket: str | None = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
