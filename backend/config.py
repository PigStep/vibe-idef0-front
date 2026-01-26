from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATA_DIR: str = "data"     
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)
settings = Settings()