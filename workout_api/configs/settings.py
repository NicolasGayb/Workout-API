from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_URL: str = Field(default='postgresql+asyncpg://workout:workout123@localhost/workout')

settings = Settings()