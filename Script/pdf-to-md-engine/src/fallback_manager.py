"""
Fallback Configuration System
Ensures system works even when some tools fail to install
"""

from pathlib import Path
import json
from typing import Dict, List
from loguru import logger

class FallbackManager:
    """Manages fallback configurations when tools are unavailable"""
    
    def __init__(self):
        self.fallback_configs = self._define_fallback_configs()
        self.minimal_requirements = self._define_minimal_requirements()
    
    def _define_fallback_configs(self) -> Dict:
        """Define fallback configurations for different scenarios"""
        
        return {
            "pdf_extraction": {
                "primary": ["docling", "pymupdf", "pdfplumber"],
                "fallback": ["pymupdf", "pdfplumber"],
                "minimal": ["pymupdf"]
            },
            "ocr_processing": {
                "primary": ["easyocr", "tesseract"],
                "fallback": ["tesseract", "pytesseract"],
                "minimal": ["tesseract"]
            },
            "ai_enhancement": {
                "primary": ["transformers", "spacy", "languagetool"],
                "fallback": ["spacy", "languagetool"],
                "minimal": ["languagetool"]
            },
            "image_processing": {
                "primary": ["opencv", "scikit-image", "pillow"],
                "fallback": ["opencv", "pillow"],
                "minimal": ["pillow"]
            }
        }
    
    def _define_minimal_requirements(self) -> Dict:
        """Define absolute minimal requirements for system to function"""
        
        return {
            "core_packages": [
                "PyMuPDF",  # Essential for PDF processing
                "Pillow",   # Essential for image handling
                "loguru",   # Essential for logging
                "tqdm",     # Essential for progress bars
                "psutil"    # Essential for resource monitoring
            ],
            "system_tools": [
                "python3"   # Obviously required
            ]
        }
    
    def create_fallback_config(self, available_tools: Dict, failed_tools: List[str]) -> Dict:
        """Create fallback configuration based on available tools"""
        
        config = {
            "extraction_methods": [],
            "quality_targets": {},
            "processing_options": {},
            "warnings": []
        }
        
        # PDF Extraction fallbacks
        pdf_engines = available_tools.get("pdf_engines", [])
        if "docling" in pdf_engines:
            config["extraction_methods"] = ["docling_conversion", "enhanced_text", "layout_preserving"]
        elif "pymupdf" in pdf_engines:
            config["extraction_methods"] = ["enhanced_text", "layout_preserving"]
            config["warnings"].append("Docling unavailable - using PyMuPDF fallback")
        else:
            config["extraction_methods"] = ["basic_text"]
            config["warnings"].append("Limited PDF processing - install PyMuPDF for better results")
        
        # OCR fallbacks
        ocr_engines = available_tools.get("ocr_engines", [])
        if "easyocr" in ocr_engines:
            config["processing_options"]["ocr_engine"] = "easyocr"
        elif "tesseract" in ocr_engines:
            config["processing_options"]["ocr_engine"] = "tesseract"
            config["warnings"].append("Using Tesseract OCR - install EasyOCR for better accuracy")
        else:
            config["processing_options"]["ocr_engine"] = "none"
            config["warnings"].append("No OCR available - scanned PDFs will not be processed")
        
        # AI Enhancement fallbacks
        ai_models = available_tools.get("ai_models", [])
        if "transformers" in ai_models:
            config["processing_options"]["ai_enhancement"] = "full"
        elif "spacy" in ai_models:
            config["processing_options"]["ai_enhancement"] = "basic"
            config["warnings"].append("Limited AI enhancement - install transformers for full features")
        else:
            config["processing_options"]["ai_enhancement"] = "none"
            config["warnings"].append("No AI enhancement available")
        
        # Quality targets based on available tools
        if len(failed_tools) == 0:
            config["quality_targets"] = {"minimum": 0.85, "target": 0.95}
        elif len(failed_tools) <= 2:
            config["quality_targets"] = {"minimum": 0.75, "target": 0.85}
        else:
            config["quality_targets"] = {"minimum": 0.65, "target": 0.75}
            config["warnings"].append("Many tools unavailable - quality may be reduced")
        
        return config
    
    def check_minimal_viability(self, available_tools: Dict) -> Tuple[bool, List[str]]:
        """Check if system has minimal tools to function"""
        
        issues = []
        
        # Check for essential PDF processing
        if not available_tools.get("pdf_engines"):
            issues.append("No PDF processing engines available")
        
        # Check for basic image processing
        if not available_tools.get("image_processing"):
            issues.append("No image processing libraries available")
        
        # System is viable if we have basic PDF and image processing
        is_viable = len(issues) == 0
        
        return is_viable, issues
    
    def generate_user_guidance(self, config: Dict) -> str:
        """Generate user guidance based on fallback configuration"""
        
        guidance = []
        
        if config["warnings"]:
            guidance.append("⚠️  SYSTEM WARNINGS:")
            for warning in config["warnings"]:
                guidance.append(f"   • {warning}")
            guidance.append("")
        
        guidance.append("🎯 CURRENT CAPABILITIES:")
        
        # Extraction methods
        methods = config["extraction_methods"]
        if "docling_conversion" in methods:
            guidance.append("   ✅ Advanced PDF processing (Docling)")
        elif "enhanced_text" in methods:
            guidance.append("   ✅ Enhanced text extraction (PyMuPDF)")
        else:
            guidance.append("   ⚠️  Basic text extraction only")
        
        # OCR capabilities
        ocr = config["processing_options"].get("ocr_engine", "none")
        if ocr == "easyocr":
            guidance.append("   ✅ Advanced OCR (EasyOCR)")
        elif ocr == "tesseract":
            guidance.append("   ✅ Basic OCR (Tesseract)")
        else:
            guidance.append("   ❌ No OCR available")
        
        # AI enhancement
        ai = config["processing_options"].get("ai_enhancement", "none")
        if ai == "full":
            guidance.append("   ✅ Full AI enhancement")
        elif ai == "basic":
            guidance.append("   ⚠️  Basic AI enhancement")
        else:
            guidance.append("   ❌ No AI enhancement")
        
        # Quality expectations
        target = config["quality_targets"].get("target", 0.75)
        if target >= 0.9:
            guidance.append("   🎯 Expected quality: EXCELLENT")
        elif target >= 0.8:
            guidance.append("   🎯 Expected quality: GOOD")
        else:
            guidance.append("   🎯 Expected quality: BASIC")
        
        guidance.append("")
        guidance.append("💡 TO IMPROVE QUALITY:")
        
        if "No OCR available" in str(config["warnings"]):
            guidance.append("   • Install Tesseract: sudo apt install tesseract-ocr")
        
        if "Limited AI enhancement" in str(config["warnings"]):
            guidance.append("   • Install AI tools: pip install transformers spacy")
        
        if "Docling unavailable" in str(config["warnings"]):
            guidance.append("   • Install Docling: pip install docling")
        
        return "\n".join(guidance)

def create_adaptive_config(available_tools: Dict, failed_tools: List[str] = None) -> Dict:
    """Create adaptive configuration based on available tools"""
    
    if failed_tools is None:
        failed_tools = []
    
    manager = FallbackManager()
    
    # Check if system is viable
    is_viable, issues = manager.check_minimal_viability(available_tools)
    
    if not is_viable:
        logger.error("System not viable:")
        for issue in issues:
            logger.error(f"  • {issue}")
        return {"viable": False, "issues": issues}
    
    # Create fallback configuration
    config = manager.create_fallback_config(available_tools, failed_tools)
    config["viable"] = True
    
    # Generate user guidance
    guidance = manager.generate_user_guidance(config)
    config["user_guidance"] = guidance
    
    # Log configuration
    logger.info("🔧 Adaptive configuration created")
    if config["warnings"]:
        logger.warning(f"System warnings: {len(config['warnings'])}")
    
    return config

def save_fallback_config(config: Dict, config_path: Path = None):
    """Save fallback configuration to file"""
    
    if config_path is None:
        config_path = Path("fallback_config.json")
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Fallback configuration saved to {config_path}")

def load_fallback_config(config_path: Path = None) -> Dict:
    """Load fallback configuration from file"""
    
    if config_path is None:
        config_path = Path("fallback_config.json")
    
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load fallback config: {e}")
        return {}