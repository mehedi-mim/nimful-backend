from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    project_title: str
    database_url: str
    database_url_alembic: str
    project_environment_type: str
    backend_port: int
    is_reload: bool
    class Config:
        env_path = ".env"


@lru_cache()
def get_config():
    return Config()
