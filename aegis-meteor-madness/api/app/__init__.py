from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from redis import Redis
from celery import Celery

from config import get_config

# Global singletons
engine = None
SessionLocal = None
redis_client: Redis | None = None
celery_app: Celery | None = None


def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config["REDIS_URL"],
        backend=app.config["REDIS_URL"],
        include=[
            "app.tasks.simulation_tasks",
        ],
    )
    celery.conf.update(task_track_started=True)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):  # type: ignore[override]
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask  # type: ignore[assignment]
    return celery


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ALLOWED_ORIGINS"].split(",")}},
        supports_credentials=False,
    )

    # Database setup (SQLAlchemy core + scoped session)
    global engine, SessionLocal
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], future=True)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

    # Redis and Celery
    global redis_client, celery_app
    redis_client = Redis.from_url(app.config["REDIS_URL"], decode_responses=True)
    celery_app = make_celery(app)

    # API v1
    from .api_v1 import api_v1_bp, api

    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    # Simple health endpoint
    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
