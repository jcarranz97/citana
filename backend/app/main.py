from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.appointments.router import router as appointments_router
from app.auth.models import User
from app.auth.router import router as auth_router
from app.auth.utils import get_password_hash
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.exceptions import (
    AppExceptionError,
    app_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)


def _bootstrap_admin() -> None:
    """Create the default admin user on first startup.

    Reads credentials from `DEFAULT_ADMIN_USERNAME` /
    `DEFAULT_ADMIN_PASSWORD` env vars (via settings.ADMIN). Safe to call
    on every startup — creation is skipped if the user already exists.
    """
    username = settings.ADMIN.USERNAME
    password = settings.ADMIN.PASSWORD

    with SessionLocal() as db:
        admin = db.query(User).filter(User.username == username).first()
        if admin is None:
            admin = User(
                username=username,
                password_hash=get_password_hash(password),
                role="admin",
            )
            db.add(admin)
        elif admin.role != "admin":
            admin.role = "admin"

        db.commit()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    """Create database tables and bootstrap the admin user on startup."""
    Base.metadata.create_all(bind=engine)
    _bootstrap_admin()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Self-hostable booking chatbot — REST API for the backend.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    app.add_exception_handler(AppExceptionError, app_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValueError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(appointments_router, prefix="/api/v1")

    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint providing basic app info."""
        return {
            "message": f"{settings.APP_NAME} is running",
            "version": settings.VERSION,
        }

    @app.get("/health")
    async def health_check() -> dict[str, str]:
        """Application health check."""
        return {
            "status": "healthy",
            "service": "citana-api",
            "version": settings.VERSION,
        }

    return app


app = create_app()
