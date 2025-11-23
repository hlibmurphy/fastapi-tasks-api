from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Tasks API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./tasks.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()