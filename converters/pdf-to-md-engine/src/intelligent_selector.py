"""
Intelligent Hardware Detection & Tool Selection System
Auto-selects best tools based on available hardware and resources
"""

import psutil
import platform
import torch
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from loguru import logger

class IntelligentToolSelector:
    """Automatically selects optimal tools based on hardware capabilities"""
    
    def __init__(self):
        self.hardware_profile = self._detect_hardware()
        self.available_tools = self._detect_available_tools()
        self.optimal_config = self._generate_optimal_config()
    
    def _detect_hardware(self) -> Dict:
        """Detect system hardware capabilities"""
        
        # CPU Information
        cpu_count = psutil.cpu_count(logical=False)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_freq = psutil.cpu_freq()
        
        # Memory Information
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_available_gb = memory.available / (1024**3)
        
        # GPU Information
        gpu_info = {"available": False, "memory_gb": 0, "name": "None", "compute_capability": None}
        if torch.cuda.is_available():
            gpu_info["available"] = True
            gpu_info["name"] = torch.cuda.get_device_name(0)
            gpu_info["memory_gb"] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            gpu_info["compute_capability"] = torch.cuda.get_device_capability(0)
        
        # Storage Information
        disk = psutil.disk_usage('/')
        disk_free_gb = disk.free / (1024**3)
        
        # System Information
        system_info = {
            "os": platform.system(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version()
        }
        
        profile = {
            "cpu": {
                "cores_physical": cpu_count,
                "cores_logical": cpu_count_logical,
                "frequency_mhz": cpu_freq.current if cpu_freq else 0,
                "performance_score": self._calculate_cpu_score(cpu_count, cpu_freq)
            },
            "memory": {
                "total_gb": memory_gb,
                "available_gb": memory_available_gb,
                "usage_percent": memory.percent
            },
            "gpu": gpu_info,
            "storage": {
                "free_gb": disk_free_gb
            },
            "system": system_info,
            "performance_class": self._classify_performance(memory_gb, gpu_info, cpu_count)
        }
        
        logger.info(f"🖥️  Hardware Profile: {profile['performance_class']}")
        logger.info(f"   CPU: {cpu_count} cores, RAM: {memory_gb:.1f}GB, GPU: {gpu_info['name']}")
        
        return profile
    
    def _calculate_cpu_score(self, cores: int, freq) -> int:
        """Calculate CPU performance score"""
        base_score = cores * 100
        if freq and freq.current:
            base_score += freq.current / 10
        return int(base_score)
    
    def _classify_performance(self, memory_gb: float, gpu_info: Dict, cpu_cores: int) -> str:
        """Classify system performance level"""
        
        if gpu_info["available"] and gpu_info["memory_gb"] >= 8 and memory_gb >= 16:
            return "HIGH_END"
        elif gpu_info["available"] and gpu_info["memory_gb"] >= 4 and memory_gb >= 8:
            return "MEDIUM_HIGH"
        elif memory_gb >= 8 and cpu_cores >= 4:
            return "MEDIUM"
        elif memory_gb >= 4:
            return "LOW_MEDIUM"
        else:
            return "LOW_END"
    
    def _detect_available_tools(self) -> Dict:
        """Detect which tools are available on the system"""
        
        tools = {
            "pdf_engines": [],
            "ocr_engines": [],
            "ai_models": [],
            "image_processors": [],
            "text_processors": []
        }
        
        # PDF Processing Engines
        try:
            import docling
            tools["pdf_engines"].append("docling")
        except ImportError:
            pass
        
        try:
            import fitz
            tools["pdf_engines"].append("pymupdf")
        except ImportError:
            pass
        
        try:
            import pdfplumber
            tools["pdf_engines"].append("pdfplumber")
        except ImportError:
            pass
        
        # OCR Engines
        if shutil.which("tesseract"):
            tools["ocr_engines"].append("tesseract")
        
        try:
            import easyocr
            tools["ocr_engines"].append("easyocr")
        except ImportError:
            pass
        
        try:
            import pytesseract
            tools["ocr_engines"].append("pytesseract")
        except ImportError:
            pass
        
        # AI Models
        try:
            import transformers
            tools["ai_models"].append("transformers")
        except ImportError:
            pass
        
        try:
            import spacy
            tools["ai_models"].append("spacy")
        except ImportError:
            pass
        
        # Check Ollama
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                tools["ai_models"].append("ollama")
        except:
            pass
        
        # Image Processing
        try:
            import cv2
            tools["image_processors"].append("opencv")
        except ImportError:
            pass
        
        try:
            from PIL import Image
            tools["image_processors"].append("pillow")
        except ImportError:
            pass
        
        # Text Processing
        try:
            import language_tool_python
            tools["text_processors"].append("languagetool")
        except ImportError:
            pass
        
        try:
            import nltk
            tools["text_processors"].append("nltk")
        except ImportError:
            pass
        
        logger.info(f"🔧 Available Tools: {sum(len(v) for v in tools.values())} total")
        
        return tools
    
    def _generate_optimal_config(self) -> Dict:
        """Generate optimal configuration based on hardware and available tools"""
        
        config = {
            "extraction_methods": [],
            "ocr_config": {},
            "ai_config": {},
            "performance_config": {},
            "quality_targets": {}
        }
        
        perf_class = self.hardware_profile["performance_class"]
        memory_gb = self.hardware_profile["memory"]["available_gb"]
        gpu_available = self.hardware_profile["gpu"]["available"]
        
        # Configure extraction methods by priority
        if "docling" in self.available_tools["pdf_engines"]:
            config["extraction_methods"].append("docling_conversion")
        
        if "pymupdf" in self.available_tools["pdf_engines"]:
            config["extraction_methods"].append("layout_preserving")
            config["extraction_methods"].append("enhanced_text")
        
        if self.available_tools["ocr_engines"]:
            config["extraction_methods"].append("ocr_primary")
        
        # Configure OCR based on hardware
        if perf_class in ["HIGH_END", "MEDIUM_HIGH"] and "easyocr" in self.available_tools["ocr_engines"]:
            config["ocr_config"] = {
                "primary_engine": "easyocr",
                "gpu_enabled": gpu_available,
                "batch_size": 4 if memory_gb > 8 else 2,
                "languages": ["en"]
            }
        elif "tesseract" in self.available_tools["ocr_engines"]:
            config["ocr_config"] = {
                "primary_engine": "tesseract",
                "gpu_enabled": False,
                "batch_size": 1,
                "languages": ["eng"]
            }
        
        # Configure AI enhancement
        if perf_class in ["HIGH_END", "MEDIUM_HIGH"]:
            config["ai_config"] = {
                "enabled": True,
                "quality_threshold": 0.75,
                "models": {
                    "text_enhancer": "google/flan-t5-base" if "transformers" in self.available_tools["ai_models"] else None,
                    "grammar_checker": "languagetool" if "languagetool" in self.available_tools["text_processors"] else None,
                    "local_llm": "llama3.2:3b" if "ollama" in self.available_tools["ai_models"] else None
                },
                "gpu_acceleration": gpu_available,
                "max_chunk_size": 1024 if memory_gb > 8 else 512
            }
        else:
            config["ai_config"] = {
                "enabled": True,
                "quality_threshold": 0.65,
                "models": {
                    "grammar_checker": "languagetool" if "languagetool" in self.available_tools["text_processors"] else None
                },
                "gpu_acceleration": False,
                "max_chunk_size": 256
            }
        
        # Performance configuration
        config["performance_config"] = {
            "max_workers": min(4, self.hardware_profile["cpu"]["cores_physical"]),
            "memory_limit_gb": memory_gb * 0.7,  # Use 70% of available memory
            "enable_gpu": gpu_available and memory_gb > 4,
            "batch_processing": perf_class in ["HIGH_END", "MEDIUM_HIGH"],
            "aggressive_cleanup": perf_class in ["LOW_END", "LOW_MEDIUM"]
        }
        
        # Quality targets based on capabilities
        if perf_class == "HIGH_END":
            config["quality_targets"] = {
                "minimum_score": 0.85,
                "target_score": 0.95,
                "enable_iterative_refinement": True,
                "max_refinement_attempts": 3
            }
        elif perf_class in ["MEDIUM_HIGH", "MEDIUM"]:
            config["quality_targets"] = {
                "minimum_score": 0.75,
                "target_score": 0.85,
                "enable_iterative_refinement": True,
                "max_refinement_attempts": 2
            }
        else:
            config["quality_targets"] = {
                "minimum_score": 0.65,
                "target_score": 0.75,
                "enable_iterative_refinement": False,
                "max_refinement_attempts": 1
            }
        
        logger.info(f"⚙️  Optimal Config Generated for {perf_class}")
        logger.info(f"   Methods: {', '.join(config['extraction_methods'][:3])}")
        logger.info(f"   AI: {'Enabled' if config['ai_config']['enabled'] else 'Disabled'}")
        logger.info(f"   Target Quality: {config['quality_targets']['target_score']}")
        
        return config
    
    def get_resource_monitor(self):
        """Get real-time resource monitoring"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_available_gb": psutil.virtual_memory().available / (1024**3),
            "gpu_memory_used": torch.cuda.memory_allocated() / (1024**3) if torch.cuda.is_available() else 0
        }
    
    def should_throttle(self) -> bool:
        """Check if processing should be throttled due to resource constraints"""
        resources = self.get_resource_monitor()
        
        # Throttle if system is under heavy load
        if resources["cpu_percent"] > 90:
            return True
        if resources["memory_percent"] > 85:
            return True
        if resources["memory_available_gb"] < 1.0:
            return True
        
        return False
    
    def adaptive_sleep(self, base_delay: float = 0.1):
        """Adaptive sleep based on system load"""
        if self.should_throttle():
            resources = self.get_resource_monitor()
            sleep_multiplier = max(resources["cpu_percent"], resources["memory_percent"]) / 100
            import time
            time.sleep(base_delay * sleep_multiplier * 2)

# Global instance
TOOL_SELECTOR = IntelligentToolSelector()

def get_optimal_config() -> Dict:
    """Get the optimal configuration for current hardware"""
    return TOOL_SELECTOR.optimal_config

def get_hardware_profile() -> Dict:
    """Get hardware profile"""
    return TOOL_SELECTOR.hardware_profile

def monitor_resources() -> Dict:
    """Monitor current resource usage"""
    return TOOL_SELECTOR.get_resource_monitor()

def should_use_gpu() -> bool:
    """Check if GPU should be used"""
    return TOOL_SELECTOR.optimal_config["performance_config"]["enable_gpu"]

def get_max_workers() -> int:
    """Get optimal number of worker threads"""
    return TOOL_SELECTOR.optimal_config["performance_config"]["max_workers"]