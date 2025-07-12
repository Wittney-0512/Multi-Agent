from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    AGENTS: List[str] = ["顾问", "批评者", "创新者"]
    
    class Config:
        env_file = ".env"


settings = Settings()