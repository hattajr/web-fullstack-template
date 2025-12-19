from pydantic_settings import BaseSettings
{% if cookiecutter.database_url %}
from sqlalchemy.engine.url import make_url
{% endif %}

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"""
    VERSION: str = "1.0.0"

    # Server
    APP_HOST: str
    APP_PORT:int
    APP_WORKERS:int
    APP_HOT_RELOAD:bool
    
    {% if cookiecutter.database_url %}
    # Database
    DATABASE_URL: str
    
    @property
    def db_host(self) -> str:
        """Parse and return database host from DATABASE_URL."""
        url = make_url(self.DATABASE_URL)
        return url.host
    
    @property
    def db_port(self) -> int:
        """Parse and return database port from DATABASE_URL."""
        url = make_url(self.DATABASE_URL)
        return url.port or 5432
    
    @property
    def db_username(self) -> str:
        """Parse and return database username from DATABASE_URL."""
        url = make_url(self.DATABASE_URL)
        return url.username
    
    @property
    def db_password(self) -> str:
        """Parse and return database password from DATABASE_URL."""
        url = make_url(self.DATABASE_URL)
        return url.password
    
    @property
    def db_name(self) -> str:
        """Parse and return database name from DATABASE_URL."""
        url = make_url(self.DATABASE_URL)
        return url.database
    {% endif %}
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    LOG_FORMAT: str ="[<level>{level: <8}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_LEVEL: str = "INFO"

settings = Settings()