from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Defaults are empty strings so the app can start even if a key is missing.
    """
    
    # Threat Intelligence API Keys (8+ sources)
    abuseipdb_key: str = ""
    otx_key: str = ""
    ipinfo_key: str = ""
    ipstack_key: str = ""
    ipapi_key: str = ""  # not required for free tier
    securitytrails_key: str = ""
    whoisxml_key: str = ""
    virustotal_key: str = ""
    
    # AI and News API Keys
    gemini_api_key: str = ""
    news_api_key: str = ""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
