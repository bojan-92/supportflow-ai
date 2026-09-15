from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SupportFlow AI"
    app_env: str = "local"


settings = Settings()