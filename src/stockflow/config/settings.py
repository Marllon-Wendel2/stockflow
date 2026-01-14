from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kaggle_dataset_login: str
    login_email: str
    password: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
