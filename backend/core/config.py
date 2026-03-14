from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    RATE_LIMIT: int = 100
    RATE_LIMIT_WINDOW: int = 60
    GEOIP2_DB_PATH: str = "geoipdata/GeoLite2-City.mmdb"
    RABBITMQ_URL: str
    ALLOWED_ORIGINS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()