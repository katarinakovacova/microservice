from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_password: str 
    refresh_token: str
    offers_base_url: str
    is_testing: bool = False

    model_config = SettingsConfigDict(env_file=".env")
