from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    """Authentication related settings."""

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    TOKEN_URL: str = "auth/login"

    class Config:
        """Configuration for environment variable prefix."""

        env_prefix = "AUTH_"


class AdminSettings(BaseSettings):
    """Default admin user settings — used by the bootstrap on first deploy."""

    USERNAME: str = "admin"
    PASSWORD: str = "citana-admin"

    class Config:
        """Configuration for environment variable prefix."""

        env_prefix = "DEFAULT_ADMIN_"


class Settings(BaseSettings):
    """Application configuration settings."""

    APP_NAME: str = "Citana API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    DATABASE_URL: str = (
        "postgresql://citana_user:citana_password@localhost:5432/citana_db"
    )

    SECRET_KEY: str = "change-me-in-production"

    ALLOWED_HOSTS: list[str] = ["http://localhost:3000", "http://localhost:2011"]

    AUTH: AuthSettings = AuthSettings()
    ADMIN: AdminSettings = AdminSettings()

    class Config:
        """Configuration for environment file."""

        env_file = ".env"


settings = Settings()
