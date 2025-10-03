import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class BaseConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", "postgresql+psycopg2://aegis:aegis@localhost:5432/aegis"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    NASA_API_KEY: str = os.getenv("NASA_API_KEY", "DEMO_KEY")

    CORS_ALLOWED_ORIGINS: str = os.getenv(
        "CORS_ALLOWED_ORIGINS", "http://localhost:5173"
    )

    RESTX_MASK_SWAGGER: bool = False
    ERROR_404_HELP: bool = False


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


def get_config() -> type[BaseConfig]:
    env = os.getenv("FLASK_ENV", "development").lower()
    return DevelopmentConfig if env == "development" else ProductionConfig
