from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    # Load .env from both backend/ and project root so local/dev/docker runs all work.
    model_config = SettingsConfigDict(
        env_file=(str(BACKEND_DIR / ".env"), str(PROJECT_ROOT / ".env")),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    sarvam_api_key: str = ""
    sarvam_base_url: str = "https://api.sarvam.ai"

    livekit_api_key: str = ""
    livekit_api_secret: str = ""
    livekit_ws_url: str = ""

    s3_endpoint_url: str = ""
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    s3_access_key: str = ""
    s3_secret_key: str = ""
    recordings_dir: str = "/data/recordings"
    backend_api_url: str = "http://backend:8000"


settings = Settings()
