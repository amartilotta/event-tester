from enum import Enum
from functools import lru_cache
from os import environ, getcwd

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

project_root = getcwd()
load_dotenv(f"{project_root}/.env")


class ENV(str, Enum):
    DEV = "dev"
    TEST = "test"
    QA = "qa"
    STG = "stg"
    PROD = "prod"


class Settings(BaseSettings):
    # General
    HOST: str = "0.0.0.0"
    APP_PORT: int = 8400
    DEBUG_PORT: int = 8401
    DEBUG_MODE: bool = bool(environ.get("DEBUG", False))
    ENVIRONMENT: ENV = ENV.DEV
    ROOT_PATH: str = ""

    # Project
    PROJECT_NAME: str = "event-tester"
    PROJECT_VERSION: str = "not-found"
    PROJECT_DESCRIPTION: str = ""

    # Database
    DATABASE_HOST: str = "mongodb-event-tester"
    DATABASE_PORT: int = 27017
    DATABASE_NAME: str = "event_tester"
    DATABASE_USER: str = "root"
    DATABASE_PASSWORD: str = "root"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
