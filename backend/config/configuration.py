from pydantic import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class Config(BaseSettings):
    """
    Configuration class for loading environment variables.
    """
    project_title: str
    database_url: str
    database_url_alembic: str
    project_environment_type: str
    backend_port: int
    is_reload: bool
    paseto_local_key: str

    email_user: str
    email_user_password: str
    contact_me_email: str

    login_url: str
    signup_verification_url: str
    email_verification_expire_minutes: int

    access_token_expire_minutes: int
    refresh_token_expire_minutes: int

    class Config:
        env_file = ".env"

@lru_cache()
def get_config():
    """
    Returns a cached instance of the Config class.
    """
    return Config()