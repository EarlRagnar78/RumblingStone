import os
import multiprocessing
import psutil
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    INPUT_DIR: Path
    OUTPUT_DIR: Path
    IMAGE_SCALE: float = 2.0
    SPLIT_BY_HEADER_LEVEL: int = 1
    OVERWRITE_EXISTING: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Smart resource management
    MAX_WORKERS: int = max(1, min(multiprocessing.cpu_count() - 2, 8))  # Conservative default
    USE_GPU: bool = True
    GPU_MEMORY_LIMIT_GB: float = 2.0  # Reserve for OS
    BATCH_SIZE: int = 4
    MAX_MEMORY_GB: float = min(psutil.virtual_memory().total / (1024**3) * 0.6, 8.0)  # 60% of RAM, max 8GB
    
    # System resource thresholds
    CPU_USAGE_THRESHOLD: float = 85.0  # Throttle if system CPU > 85%
    MEMORY_USAGE_THRESHOLD: float = 80.0  # Throttle if system RAM > 80%
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __post_init__(self):
        """Validate and adjust settings based on system resources."""
        # Ensure we don't exceed system capabilities
        total_cores = multiprocessing.cpu_count()
        if self.MAX_WORKERS >= total_cores:
            self.MAX_WORKERS = max(1, total_cores - 2)
        
        # Adjust for low-memory systems
        available_memory = psutil.virtual_memory().available / (1024**3)
        if available_memory < 4.0:  # Less than 4GB available
            self.MAX_WORKERS = min(self.MAX_WORKERS, 2)
            self.BATCH_SIZE = min(self.BATCH_SIZE, 2)
            self.MAX_MEMORY_GB = min(self.MAX_MEMORY_GB, 2.0)

settings = Settings()

# Post-initialization adjustments
settings.__post_init__()

# Ensure directories exist
settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)