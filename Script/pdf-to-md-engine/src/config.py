from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    INPUT_DIR: Path
    OUTPUT_DIR: Path
    IMAGE_SCALE: float = 2.0
    SPLIT_BY_HEADER_LEVEL: int = 1
    OVERWRITE_EXISTING: bool = False
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Ensure directories exist
settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)