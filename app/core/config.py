from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    # Comma-separated list, e.g. http://localhost:3000,https://myapp.vercel.app
    CORS_ORIGINS: str = (
        "http://localhost:3000,"
        "http://127.0.0.1:3000,"
        "https://smartshop-web-seven.vercel.app"
    )

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = "app/.env"
        env_file_encoding = "utf-8"

settings = Settings()