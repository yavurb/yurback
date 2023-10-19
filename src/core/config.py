from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    port: int = 8000
    environment: str = "dev"

    database_uri: str
    jwt_secret: str

    # AWS
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_s3_bucket: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
