from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Orman Yangını Erken Uyarı Sistemi API"
    VERSION: str = "1.0.0"
    
    # Veritabanı
    DATABASE_URL: str
    REDIS_URL: str
    
    # API Anahtarları
    NASA_FIRMS_API_KEY: str
    OPENWEATHERMAP_API_KEY: str
    SENTINEL_HUB_CLIENT_ID: str
    SENTINEL_HUB_CLIENT_SECRET: str
    
    # Bildirim
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    SENDGRID_API_KEY: str
    FROM_EMAIL: str
    
    # Uygulama Ayarları
    SECRET_KEY: str
    ALLOWED_ORIGINS: str
    RISK_CHECK_INTERVAL_MINUTES: int = 15
    HIGH_RISK_THRESHOLD: int = 70
    CRITICAL_RISK_THRESHOLD: int = 85
    
    @property
    def get_allowed_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
