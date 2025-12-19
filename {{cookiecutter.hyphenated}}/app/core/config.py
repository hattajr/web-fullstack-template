from pydantic import Field
from pydantic_settings import BaseSettings
{% if cookiecutter.database_url %}
from sqlalchemy.engine.url import make_url
{% endif %}

class Settings(BaseSettings):
    # App
    project_name: str = "{{ cookiecutter.project_name }}"""
    version: str = "1.0.0"

    # Server
    app_host: str = Field(validation_alias="APP_HOST")
    app_port: int = Field(validation_alias="APP_PORT")
    app_workers: int = Field(validation_alias="APP_WORKERS")
    app_hot_reload: bool = Field(validation_alias="APP_HOT_RELOAD")
    
    {% if cookiecutter.database_url %}
    # Database
    database_url: str = Field(validation_alias="DATABASE_URL")
    
    @property
    def db_host(self) -> str:
        """Parse and return database host from database_url."""
        url = make_url(self.database_url)
        return url.host
    
    @property
    def db_port(self) -> int:
        """Parse and return database port from database_url."""
        url = make_url(self.database_url)
        return url.port or 5432
    
    @property
    def db_username(self) -> str:
        """Parse and return database username from database_url."""
        url = make_url(self.database_url)
        return url.username
    
    @property
    def db_password(self) -> str:
        """Parse and return database password from database_url."""
        url = make_url(self.database_url)
        return url.password
    
    @property
    def db_name(self) -> str:
        """Parse and return database name from database_url."""
        url = make_url(self.database_url)
        return url.database
    {% endif %}
    
    # Security
    secret_key: str = Field(validation_alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    log_format: str ="[<level>{level: <8}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    log_level: str = "INFO"

settings = Settings()