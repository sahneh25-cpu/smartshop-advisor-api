from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartShop Advisor"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    ai_provider: str = "local"
    gemini_api_key: str | None = None
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
