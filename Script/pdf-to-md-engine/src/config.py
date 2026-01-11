import os
import multiprocessing
import psutil
import torch
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    INPUT_DIR: Path
    OUTPUT_DIR: Path
    IMAGE_SCALE: float = 2.0
    SPLIT_BY_HEADER_LEVEL: int = 1
    OVERWRITE_EXISTING: bool = False
    LOG_LEVEL: str = "INFO"
    
    # Intelligent resource management
    MAX_WORKERS: int = max(1, min(multiprocessing.cpu_count() - 2, 8))
    USE_GPU: bool = torch.cuda.is_available() if 'torch' in globals() else True
    GPU_MEMORY_LIMIT_GB: float = 2.0
    BATCH_SIZE: int = 4
    MAX_MEMORY_GB: float = min(psutil.virtual_memory().total / (1024**3) * 0.6, 8.0)
    
    # Dynamic system resource thresholds
    CPU_USAGE_THRESHOLD: float = 85.0
    MEMORY_USAGE_THRESHOLD: float = 80.0
    
    # Advanced OCR Configuration
    OCR_ENGINE: str = "auto"  # auto, easyocr, tesseract, none
    OCR_LANGUAGES: str = "en"  # Comma-separated language codes
    OCR_CONFIDENCE_THRESHOLD: float = 0.7  # Minimum confidence for OCR text
    OCR_MIN_TEXT_LENGTH: int = 10  # Minimum text length to consider meaningful
    OCR_BATCH_SIZE: int = 4  # Images to process in parallel for OCR
    OCR_GPU_MEMORY_PER_BATCH: float = 1.5  # GB per OCR batch
    
    # System optimization settings
    ENABLE_ADAPTIVE_PROCESSING: bool = True
    RESOURCE_CHECK_INTERVAL: float = 0.1  # Seconds between resource checks
    THROTTLE_RECOVERY_TIME: float = 2.0  # Seconds to wait when throttling
    MEMORY_CLEANUP_THRESHOLD: int = 75  # Trigger cleanup at this memory %
    GPU_MEMORY_CLEANUP_INTERVAL: int = 10  # Cleanup GPU memory every N operations
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    def __post_init__(self):
        """Intelligent validation and adjustment based on system capabilities."""
        # CPU optimization
        total_cores = multiprocessing.cpu_count()
        if self.MAX_WORKERS >= total_cores:
            self.MAX_WORKERS = max(1, total_cores - 2)
        
        # Memory optimization
        total_memory_gb = psutil.virtual_memory().total / (1024**3)
        available_memory = psutil.virtual_memory().available / (1024**3)
        
        # Adjust settings for low-memory systems
        if total_memory_gb < 8:
            self.MAX_WORKERS = min(self.MAX_WORKERS, 2)
            self.BATCH_SIZE = min(self.BATCH_SIZE, 2)
            self.OCR_BATCH_SIZE = min(self.OCR_BATCH_SIZE, 2)
            self.MAX_MEMORY_GB = min(self.MAX_MEMORY_GB, 4.0)
            self.MEMORY_USAGE_THRESHOLD = min(self.MEMORY_USAGE_THRESHOLD, 70.0)
        
        if available_memory < 4.0:
            self.MAX_WORKERS = min(self.MAX_WORKERS, 1)
            self.OCR_BATCH_SIZE = 1
        
        # CPU optimization for low-core systems
        if total_cores <= 4:
            self.CPU_USAGE_THRESHOLD = min(self.CPU_USAGE_THRESHOLD, 75.0)
            self.MAX_WORKERS = min(self.MAX_WORKERS, 2)
        
        # GPU optimization
        if self.USE_GPU and torch.cuda.is_available():
            try:
                gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                if gpu_memory_gb < 4:
                    self.OCR_GPU_MEMORY_PER_BATCH = min(self.OCR_GPU_MEMORY_PER_BATCH, 1.0)
                    self.GPU_MEMORY_LIMIT_GB = min(self.GPU_MEMORY_LIMIT_GB, 1.0)
            except Exception:
                self.USE_GPU = False
        
        # Validate OCR settings
        if self.OCR_ENGINE not in ["auto", "easyocr", "tesseract", "none"]:
            self.OCR_ENGINE = "auto"
    
    def get_optimal_batch_size(self, task_type: str = "general") -> int:
        """Calculate optimal batch size based on available resources."""
        available_memory_gb = psutil.virtual_memory().available / (1024**3)
        
        if task_type == "ocr":
            # OCR is memory intensive
            max_batches = int(available_memory_gb / self.OCR_GPU_MEMORY_PER_BATCH)
            return max(1, min(max_batches, self.OCR_BATCH_SIZE))
        
        return self.MAX_WORKERS
    
    def should_use_gpu_for_task(self, task_type: str) -> bool:
        """Determine if GPU should be used for specific task type."""
        if not self.USE_GPU:
            return False
        
        try:
            if not torch.cuda.is_available():
                return False
            
            gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            gpu_memory_used = torch.cuda.memory_allocated(0) / (1024**3)
            available_gpu_memory = gpu_memory_gb - gpu_memory_used - self.GPU_MEMORY_LIMIT_GB
            
            task_requirements = {
                "ocr": self.OCR_GPU_MEMORY_PER_BATCH,
                "general": 1.0
            }
            
            required_memory = task_requirements.get(task_type, 1.0)
            return available_gpu_memory >= required_memory
        except Exception:
            return False
    
    def get_safe_worker_count(self, task_type: str = "general") -> int:
        """Get safe worker count based on current system state."""
        available_memory = psutil.virtual_memory().available / (1024**3)
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Task-specific memory requirements (GB per worker)
        memory_per_worker = {
            "ocr": 1.5,
            "image": 0.5,
            "chapter": 0.2,
            "general": 0.3
        }
        
        # Calculate based on memory constraints
        usable_memory = max(0.5, available_memory - 2)  # Reserve 2GB
        memory_limited_workers = int(usable_memory / memory_per_worker.get(task_type, 0.3))
        
        # Calculate based on CPU constraints
        usable_cores = max(1, multiprocessing.cpu_count() - 2)
        if cpu_percent > 80:
            usable_cores = max(1, usable_cores // 2)
        
        # Use the more restrictive limit
        safe_workers = min(memory_limited_workers, usable_cores, self.MAX_WORKERS)
        return max(1, safe_workers)

settings = Settings()
settings.__post_init__()

settings.INPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)