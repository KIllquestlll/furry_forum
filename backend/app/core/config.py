# Conntection web-server library
from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field

# Conntection core library
import os

# Path to backend file (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))

class Settings(BaseSettings):
    # Main settings
    DB_HOST: str
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # Other settings
    SECRET_KEY: str
    DEBUG: bool = True
    
    @computed_field
    @property
    def database_url(self) -> str:
        # postgres+asyncpg://user:password@host:port/dbname
        return f"postgres+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR,".env"),
        env_file_encoding="utf-8",
        extra='ignore',
    )


settings = Settings()



