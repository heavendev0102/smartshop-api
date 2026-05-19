from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = False

    @property
    def database_url_sync(self) -> str:
        """Sync URL for Alembic (psycopg2)."""
        url = self.DATABASE_URL
        if url.startswith("postgresql+asyncpg://"):
            return url.replace("postgresql+asyncpg://", "postgresql://", 1)
        if url.startswith("postgres+asyncpg://"):
            return url.replace("postgres+asyncpg://", "postgresql://", 1)
        return url

    # Comma-separated list, e.g. http://localhost:3000,https://myapp.vercel.app
    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000,"
        "https://smartshop-web-seven.vercel.app"
    )

    model_config = SettingsConfigDict(
        env_file="app/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()