from functools import lru_cache
from typing import Any, Optional
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


@lru_cache()
def get_env(key: str, default: Any = None, required: bool = False) -> Optional[str]:
    """
    Get environment variable with caching and validation.
    """
    value = os.getenv(key, default)
    if required and value is None:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


def get_debug() -> bool:
    """Get DEBUG flag as boolean"""
    return get_env("DEBUG", "false").lower() in {"1", "yes", "true"}


def get_mongodb_url() -> str:
    """Get MongoDB connection URL"""
    return get_env("MONGODB_URL", required=True)


def get_app_db_name() -> str:
    """Get MongoDB database name"""
    return get_env("MONGODB_APP_DB_NAME", required=True)
