from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"""
    VERSION: str = "1.0.0"

    # Server
    APP_HOST: str
    APP_PORT:int
    APP_WORKERS:int
    APP_HOT_RELOAD:bool
    
    # Database
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    LOG_FORMAT: str ="[<level>{level: <8}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_LEVEL: str = "INFO"

settings = Settings()