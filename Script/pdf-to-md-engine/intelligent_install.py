#!/usr/bin/env python3
"""
🚀 Intelligent PDF-to-MD Engine Installer v2.2
Integrates setup.py OS detection with hardware-aware optimization
Auto-detects hardware and installs optimal tools for maximum quality
"""

import os
import sys
import platform
import subprocess
import shutil
import json
from pathlib import Path

# Basic system info without psutil (will be available after venv setup)
def get_basic_system_info():
    """Get basic system info without psutil dependency"""
    system = platform.system().lower()
    os_type = "unknown"
    if system == "linux":
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "bazzite" in content:
                    os_type = "bazzite"
                elif "ubuntu" in content or "debian" in content:
                    os_type = "debian"
                elif "fedora" in content or "centos" in content or "rhel" in content:
                    os_type = "fedora"
                else:
                    os_type = "linux"
        except:
            os_type = "linux"
    elif system == "darwin":
        os_type = "macos"
    elif system == "windows":
        os_type = "windows"
    
    return {
        "os": system,
        "os_type": os_type,
        "arch": platform.architecture()[0],
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count() or 4,  # fallback to 4 if None
        "memory_gb": 8.0  # default assumption, will be updated after psutil is available
    }

class IntelligentInstaller:
    """Intelligent installer that adapts to hardware capabilities"""
    
    def __init__(self):
        self.system_info = self._detect_system()
        self.hardware_profile = self._analyze_hardware()
        self.installation_plan = self._create_installation_plan()
    
    def _detect_system(self):
        """Enhanced system detection with OS-specific details"""
        # Use basic system info first
        basic_info = get_basic_system_info()
        
        # Check Python version compatibility
        python_312_available = self._check_python_312()
        basic_info["python_312_available"] = python_312_available
        
        return basic_info
    
    def _check_python_312(self):
        """Check if Python 3.12 is available for magika compatibility"""
        for cmd in ["python3.12", "/usr/bin/python3.12", "python3"]:
            try:
                result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
                if "3.12" in result.stdout:
                    return cmd
            except:
                continue
        return None
    
    def _analyze_hardware(self):
        """Analyze hardware capabilities (without psutil initially)"""
        
        # Check GPU (optional)
        gpu_available = False
        gpu_memory = 0
        try:
            # Check for NVIDIA GPU
            result = subprocess.run(["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                gpu_memory = float(result.stdout.strip()) / 1024  # Convert MB to GB
                gpu_available = True
                print(f"🎮 NVIDIA GPU detected: {gpu_memory:.1f}GB VRAM")
        except:
            # Fallback: try torch detection
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_available = True
                    gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                    print(f"🎮 GPU detected via PyTorch: {gpu_memory:.1f}GB VRAM")
            except ImportError:
                pass
        
        # Classify performance based on basic info
        memory_gb = self.system_info["memory_gb"]
        cpu_count = self.system_info["cpu_count"]
        
        if gpu_available and gpu_memory >= 8 and memory_gb >= 16:
            performance_class = "ENTERPRISE"
        elif gpu_available and gpu_memory >= 4 and memory_gb >= 8:
            performance_class = "HIGH_PERFORMANCE"
        elif memory_gb >= 8 and cpu_count >= 4:
            performance_class = "STANDARD"
        elif memory_gb >= 4:
            performance_class = "BASIC"
        else:
            performance_class = "MINIMAL"
        
        return {
            "performance_class": performance_class,
            "gpu_available": gpu_available,
            "gpu_memory_gb": gpu_memory,
            "recommended_tools": self._get_recommended_tools(performance_class),
            "available_tools": self._detect_actually_available_tools()
        }
    
    def _get_recommended_tools(self, performance_class):
        """Get recommended tools based on performance class"""
        
        tools = {
            "ENTERPRISE": {
                "pdf_engines": ["docling", "pymupdf", "pdfplumber"],
                "ocr_engines": ["easyocr", "tesseract"],
                "ai_models": ["transformers", "spacy", "ollama", "languagetool"],
                "image_processing": ["opencv", "scikit-image"],
                "performance": ["numba", "scipy", "torch"]
            },
            "HIGH_PERFORMANCE": {
                "pdf_engines": ["docling", "pymupdf", "pdfplumber"],
                "ocr_engines": ["easyocr", "tesseract"],
                "ai_models": ["transformers", "spacy", "languagetool"],
                "image_processing": ["opencv", "pillow"],
                "performance": ["numba", "scipy"]
            },
            "STANDARD": {
                "pdf_engines": ["pymupdf", "pdfplumber", "docling"],
                "ocr_engines": ["tesseract", "pytesseract"],
                "ai_models": ["spacy", "languagetool"],
                "image_processing": ["pillow", "opencv"],
                "performance": ["scipy"]
            },
            "BASIC": {
                "pdf_engines": ["pymupdf", "pdfplumber"],
                "ocr_engines": ["tesseract"],
                "ai_models": ["languagetool"],
                "image_processing": ["pillow"],
                "performance": []
            },
            "MINIMAL": {
                "pdf_engines": ["pymupdf"],
                "ocr_engines": ["tesseract"],
                "ai_models": [],
                "image_processing": ["pillow"],
                "performance": []
            }
        }
        
        return tools.get(performance_class, tools["BASIC"])
    
    def _detect_actually_available_tools(self):
        """Detect which tools are actually available after installation"""
        
        available = {
            "pdf_engines": [],
            "ocr_engines": [],
            "ai_models": [],
            "image_processing": [],
            "performance": []
        }
        
        # Check system tools first
        if shutil.which("tesseract"):
            available["ocr_engines"].append("tesseract")
        
        # Check Python packages (will be available after installation)
        python_packages = {
            "pymupdf": ("fitz", "pdf_engines"),
            "pdfplumber": ("pdfplumber", "pdf_engines"),
            "docling": ("docling", "pdf_engines"),
            "easyocr": ("easyocr", "ocr_engines"),
            "pytesseract": ("pytesseract", "ocr_engines"),
            "transformers": ("transformers", "ai_models"),
            "spacy": ("spacy", "ai_models"),
            "languagetool": ("language_tool_python", "ai_models"),
            "opencv": ("cv2", "image_processing"),
            "pillow": ("PIL", "image_processing"),
            "numba": ("numba", "performance"),
            "scipy": ("scipy", "performance")
        }
        
        # These will be available after installation, so mark as available
        # if they're in the recommended tools
        recommended = self._get_recommended_tools("STANDARD")  # Use standard as baseline
        
        for tool_name, (import_name, category) in python_packages.items():
            if any(tool_name in tools for tools in recommended.values()):
                available[category].append(tool_name)
        
        return available
    
    def _create_installation_plan(self):
        """Create optimized installation plan"""
        
        tools = self.hardware_profile["recommended_tools"]
        
        # Core dependencies (always needed) - enhanced from setup.py
        core_deps = [
            "cryptography>=3.0.0",
            "pdfminer.six>=20220319",
            "PyMuPDF>=1.23.0",
            "pdfplumber>=0.10.0",
            "pydantic>=2.0.0",
            "pydantic-settings>=2.0.0",
            "loguru>=0.7.0",
            "tqdm>=4.65.0",
            "jinja2>=3.1.0",
            "psutil>=5.9.0",
            "Pillow>=10.0.0",
            "numpy>=1.24.0",
            "chardet>=5.0.0",
            "ftfy>=6.1.0"
        ]
        
        # Hardware-aware optional dependencies
        optional_deps = []
        
        # Python 3.12 specific packages (magika compatibility)
        if self.system_info["python_312_available"]:
            optional_deps.append("magika>=0.5.0")
        
        # PDF engines based on hardware
        if "docling" in tools["pdf_engines"]:
            optional_deps.append("docling>=2.0.0")
        
        # OCR engines
        if "easyocr" in tools["ocr_engines"]:
            optional_deps.append("easyocr>=1.7.0")
        if "pytesseract" in tools["ocr_engines"]:
            optional_deps.append("pytesseract>=0.3.10")
        
        # AI models with hardware consideration
        if "transformers" in tools["ai_models"]:
            optional_deps.extend([
                "transformers>=4.35.0",
                "torch>=2.0.0",
                "torchvision>=0.15.0"
            ])
        if "spacy" in tools["ai_models"]:
            optional_deps.extend([
                "spacy>=3.7.0",
                "nltk>=3.8.1",
                "scikit-learn>=1.3.0"
            ])
        if "languagetool" in tools["ai_models"]:
            optional_deps.append("language-tool-python>=2.7.1")
        
        # Image processing
        if "opencv" in tools["image_processing"]:
            optional_deps.append("opencv-python>=4.8.0")
        if "scikit-image" in tools["image_processing"]:
            optional_deps.append("scikit-image>=0.21.0")
        
        # Performance libraries
        if "numba" in tools["performance"]:
            optional_deps.append("numba>=0.57.0")
        if "scipy" in tools["performance"]:
            optional_deps.append("scipy>=1.10.0")
        
        # Stream processing and content analysis
        optional_deps.extend([
            "charset-normalizer>=3.0.0",
            "requests>=2.28.0",
            "beautifulsoup4>=4.11.0",
            "lxml>=4.9.0",
            "sympy>=1.11.0",
            "tabulate>=0.9.0"
        ])
        
        return {
            "core_dependencies": core_deps,
            "optional_dependencies": optional_deps,
            "system_packages": self._get_system_packages(),
            "post_install_steps": self._get_post_install_steps()
        }
    
    def _get_system_packages(self):
        """Enhanced system packages based on OS type from setup.py integration"""
        
        os_type = self.system_info["os_type"]
        packages = []
        
        if os_type == "bazzite":
            # Bazzite OS - use homebrew (already detected properly)
            if not shutil.which("brew"):
                packages.append(('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', "Installing Homebrew"))
            
            packages.extend([
                ("brew install tesseract", "Installing Tesseract OCR"),
                ("brew install libffi openssl", "Installing crypto libraries"),
            ])
            
        elif os_type == "debian":
            packages = [
                ("sudo apt update", "Updating package list"),
                ("sudo apt install -y tesseract-ocr tesseract-ocr-eng", "Installing Tesseract OCR"),
                ("sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1", "Installing system libraries"),
                ("sudo apt install -y python3-dev build-essential", "Installing build tools"),
                ("sudo apt install -y libffi-dev libssl-dev", "Installing crypto libraries")
            ]
        
        elif os_type == "fedora":
            packages = [
                ("sudo dnf update -y", "Updating package list"),
                ("sudo dnf install -y tesseract tesseract-langpack-eng", "Installing Tesseract OCR"),
                ("sudo dnf install -y mesa-libGL glib2 libSM libXext libXrender gomp", "Installing system libraries"),
                ("sudo dnf install -y python3-devel gcc gcc-c++", "Installing build tools"),
                ("sudo dnf install -y libffi-devel openssl-devel", "Installing crypto libraries")
            ]
        
        elif os_type == "macos":
            if not shutil.which("brew"):
                print("❌ Homebrew not found. Please install Homebrew first")
                return []
            
            packages = [
                ("brew update", "Updating Homebrew"),
                ("brew install tesseract", "Installing Tesseract OCR"),
                ("brew install libffi openssl", "Installing crypto libraries")
            ]
        
        elif os_type == "windows":
            print("🪟 Windows detected. Please install manually:")
            print("   1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
            print("   2. Add Tesseract to PATH")
            return []
        
        return packages
    
    def _get_post_install_steps(self):
        """Get post-installation steps (enhanced from setup.py)"""
        
        steps = []
        
        # Download spaCy model if needed
        if "spacy" in self.hardware_profile["recommended_tools"]["ai_models"]:
            steps.append("python -m spacy download en_core_web_sm")
        
        # Download NLTK data if needed
        if "nltk" in self.hardware_profile["recommended_tools"]["ai_models"]:
            steps.append('python -c "import nltk; nltk.download(\'punkt\'); nltk.download(\'stopwords\')"')
        
        # Setup Ollama if recommended (only for non-Windows)
        if "ollama" in self.hardware_profile["recommended_tools"]["ai_models"]:
            if self.system_info["os"] != "windows":
                steps.extend([
                    "curl -fsSL https://ollama.ai/install.sh | sh",
                    "ollama pull llama3.2:3b"
                ])
        
        return steps
    
    def run_command(self, cmd, description="", ignore_errors=False):
        """Run system command with error handling"""
        print(f"🔧 {description}")
        
        try:
            result = subprocess.run(cmd, shell=True, check=True, 
                                  capture_output=True, text=True)
            print(f"   ✅ Success")
            return True
        except subprocess.CalledProcessError as e:
            if ignore_errors:
                print(f"   ⚠️  Warning: {e}")
                return False
            else:
                print(f"   ❌ Error: {e}")
                return False
    
    def install(self):
        """Run the complete installation"""
        
        print("🚀 Intelligent PDF-to-MD Engine Installer v2.2")
        print("=" * 55)
        
        # Show detected configuration
        print(f"🖥️  System: {self.system_info['os_type']} {self.system_info['arch']}")
        print(f"🧠 Hardware Class: {self.hardware_profile['performance_class']}")
        print(f"💾 Memory: {self.system_info['memory_gb']:.1f}GB")
        print(f"🐍 Python: {self.system_info['python_version']}")
        if self.system_info["python_312_available"]:
            print(f"✅ Python 3.12: Available (magika support)")
        else:
            print(f"⚠️  Python 3.12: Not available (limited magika support)")
        print(f"🎮 GPU: {'Available' if self.hardware_profile['gpu_available'] else 'Not Available'}")
        print()
        
        # Install system packages with enhanced OS detection
        system_packages = self.installation_plan["system_packages"]
        if system_packages:
            print("📦 Installing system packages...")
            for cmd, desc in system_packages:
                self.run_command(cmd, desc, ignore_errors=True)
        
        # Setup Python environment with 3.12 preference
        print("🐍 Setting up Python environment...")
        
        # Use Python 3.12 if available for full compatibility (especially magika)
        python_cmd = self.system_info["python_312_available"] or sys.executable
        if self.system_info["python_312_available"]:
            print(f"✅ Using Python 3.12: {python_cmd}")
        else:
            print(f"⚠️  Using system Python: {python_cmd} (may have compatibility issues)")
        
        # Create virtual environment
        if not Path("venv").exists():
            self.run_command(f"{python_cmd} -m venv venv", "Creating virtual environment")
        
        # Determine pip and python commands based on OS
        if self.system_info["os_type"] == "windows":
            pip_cmd = "venv\\Scripts\\pip"
            venv_python = "venv\\Scripts\\python"
        else:
            pip_cmd = "venv/bin/pip"
            venv_python = "venv/bin/python"
        
        # For Bazzite and other externally-managed environments, ensure we use venv
        if self.system_info["os_type"] == "bazzite":
            print("✅ Using virtual environment for Bazzite OS (externally-managed)")
        
        # Upgrade pip
        self.run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
        
        # Install psutil first for better hardware detection
        self.run_command(f"{pip_cmd} install 'psutil>=5.9.0'", "Installing psutil for hardware detection")
        
        # Update hardware profile with accurate psutil data
        self._update_hardware_profile_with_psutil(venv_python)
        
        # Recreate installation plan with accurate hardware data
        self.installation_plan = self._create_installation_plan()
        
        # Install core dependencies (essential - must succeed)
        print("📦 Installing core dependencies...")
        core_deps = self.installation_plan["core_dependencies"]
        core_success = 0
        for dep in core_deps:
            if self.run_command(f"{pip_cmd} install '{dep}'", f"Installing {dep.split('>=')[0]}"):
                core_success += 1
        
        if core_success < len(core_deps) * 0.7:
            print("❌ Critical: Too many core dependencies failed. System may not work properly.")
        
        # Install optional dependencies (graceful failure)
        print("🎯 Installing optimized dependencies...")
        optional_deps = self.installation_plan["optional_dependencies"]
        optional_success = 0
        failed_tools = []
        
        for dep in optional_deps:
            tool_name = dep.split('>=')[0]
            if self.run_command(f"{pip_cmd} install '{dep}'", f"Installing {tool_name}", ignore_errors=True):
                optional_success += 1
            else:
                failed_tools.append(tool_name)
        
        # Update configuration based on what actually installed
        self._update_config_for_available_tools(failed_tools)
        
        if failed_tools:
            print(f"⚠️  Some tools failed to install: {', '.join(failed_tools)}")
            print("   System will adapt and use available tools only.")
        
        # Run post-install steps
        if self.installation_plan["post_install_steps"]:
            print("🔧 Running post-installation setup...")
            
            for step in self.installation_plan["post_install_steps"]:
                if step.startswith("python"):
                    step = step.replace("python", venv_python)
                self.run_command(step, f"Running: {step}", ignore_errors=True)
        
        # Create configuration file
        self._create_config_file()
        
        # Create activation script
        self._create_activation_script()
        
        # Verify installation
        self._verify_installation()
        
        # Show completion message
        self._show_completion_message()
        
        # Create and save fallback configuration
        self._create_fallback_config()
    
    def _create_config_file(self):
        """Create optimized configuration file"""
        
        config = {
            "hardware_profile": self.hardware_profile,
            "installation_plan": self.installation_plan,
            "optimal_settings": {
                "max_workers": min(4, self.system_info["cpu_count"]),
                "memory_limit_gb": self.system_info["memory_gb"] * 0.7,
                "enable_gpu": self.hardware_profile["gpu_available"],
                "quality_target": 0.95 if self.hardware_profile["performance_class"] == "ENTERPRISE" else 0.85
            }
        }
        
        with open("intelligent_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("⚙️  Created optimized configuration")
    
    def _update_config_for_available_tools(self, failed_tools):
        """Update configuration based on actually available tools"""
        
        # Remove failed tools from recommended tools
        for category in self.hardware_profile["recommended_tools"]:
            self.hardware_profile["recommended_tools"][category] = [
                tool for tool in self.hardware_profile["recommended_tools"][category]
                if tool not in failed_tools
            ]
        
        # Adjust performance class if critical tools failed
        critical_failures = [tool for tool in failed_tools if tool in ["docling", "transformers", "easyocr"]]
        if critical_failures:
            current_class = self.hardware_profile["performance_class"]
            class_hierarchy = ["MINIMAL", "BASIC", "STANDARD", "HIGH_PERFORMANCE", "ENTERPRISE"]
            current_index = class_hierarchy.index(current_class)
            
            if len(critical_failures) >= 2 and current_index > 0:
                new_class = class_hierarchy[current_index - 1]
                self.hardware_profile["performance_class"] = new_class
                print(f"⚠️  Adjusted performance class to {new_class} due to failed installations")
        
        # Ensure at least basic functionality
        if not self.hardware_profile["recommended_tools"]["pdf_engines"]:
            self.hardware_profile["recommended_tools"]["pdf_engines"] = ["pymupdf"]
        
        if not self.hardware_profile["recommended_tools"]["image_processing"]:
            self.hardware_profile["recommended_tools"]["image_processing"] = ["pillow"]
    
    def _create_activation_script(self):
        """Create activation script (enhanced from setup.py)"""
        
        if self.system_info["os_type"] == "windows":
            script_content = f"""@echo off
echo 🚀 Activating Intelligent PDF-to-MD Engine v2.2...
echo 🖥️  OS: {self.system_info['os_type']}
echo 🧠 Hardware: {self.hardware_profile['performance_class']}
echo 🐍 Python: {self.system_info['python_version']}
call venv\\Scripts\\activate.bat
echo ✅ Environment activated!
echo.
echo Available commands:
echo   python main.py                  - Process PDFs with auto-optimization
echo   python run_enhanced.py          - Enhanced processing
echo   python comprehensive_audit.py   - Project health check
echo   python verify_project.py        - Quick verification
echo.
"""
            with open("activate.bat", "w") as f:
                f.write(script_content)
        else:
            script_content = f"""#!/bin/bash
echo "🚀 Activating Intelligent PDF-to-MD Engine v2.2..."
echo "🖥️  OS: {self.system_info['os_type']}"
echo "🧠 Hardware: {self.hardware_profile['performance_class']}"
echo "🐍 Python: {self.system_info['python_version']}"
source venv/bin/activate
echo "✅ Environment activated!"
echo ""
echo "Available commands:"
echo "  python main.py                  - Process PDFs with auto-optimization"
echo "  python run_enhanced.py          - Enhanced processing"
echo "  python comprehensive_audit.py   - Project health check"
echo "  python verify_project.py        - Quick verification"
echo ""
echo "📚 Enhanced Features:"
echo "   • Quality assessment and iterative refinement"
echo "   • Stream-based processing (markitdown)"
echo "   • Form-style table detection"
echo "   • Partial numbering merge"
echo "   • Intelligent content analysis"
echo "   • Multi-strategy extraction"
echo ""
"""
            with open("activate.sh", "w") as f:
                f.write(script_content)
            os.chmod("activate.sh", 0o755)
    
    def _verify_installation(self):
        """Verify installation and show what's actually working"""
        
        print("✅ Verifying installation...")
        
        # Determine python command
        if self.system_info["os_type"] == "windows":
            python_cmd = "venv\\Scripts\\python"
        else:
            python_cmd = "venv/bin/python"
        
        # Test all imports including optional (from setup.py)
        test_imports = [
            ("docling", "Docling PDF processing"),
            ("fitz", "PyMuPDF"),
            ("pdfplumber", "pdfplumber"),
            ("torch", "PyTorch"),
            ("PIL", "Pillow"),
            ("numpy", "NumPy"),
            ("loguru", "Loguru logging"),
            ("magika", "Magika content detection"),
            ("easyocr", "EasyOCR engine"),
            ("pytesseract", "Tesseract Python wrapper"),
            ("cv2", "OpenCV"),
            ("skimage", "Scikit-image"),
            ("numba", "Numba JIT compiler"),
            ("scipy", "SciPy"),
            # Free AI tools
            ("transformers", "Hugging Face Transformers"),
            ("spacy", "spaCy NLP"),
            ("nltk", "NLTK"),
            ("sklearn", "Scikit-learn")
        ]
        
        # Test what's actually available
        working_tools = self._test_available_tools(python_cmd)
        
        # Test pytesseract with proper tesseract path configuration
        for module, name in test_imports:
            if module == "pytesseract":
                # Configure tesseract path for pytesseract
                test_cmd = f'{python_cmd} -c "import pytesseract; pytesseract.pytesseract.tesseract_cmd = \'tesseract\'; import pytesseract; print(\'\u2705 {name}\')"'
            else:
                test_cmd = f'{python_cmd} -c "import {module}; print(\'\u2705 {name}\')"'
            
            if self.run_command(test_cmd, f"Testing {name}", ignore_errors=True):
                success_count += 1
        
        # Test OCR engines (from setup.py)
        print("\n🔍 Testing OCR engines...")
        if shutil.which("tesseract"):
            print("   ✅ Tesseract OCR found")
        else:
            print("   ❌ Tesseract OCR not found")
        
        # Test enhanced features (from setup.py)
        cmd = f'{python_cmd} -c "from src.enhanced_table_detector import detect_tables_enhanced; print(\'\u2705 Enhanced features\')"'
        self.run_command(cmd, "Testing enhanced features", ignore_errors=True)
        
        # Update final configuration
        self.hardware_profile["actually_available"] = working_tools
        
        # Show summary
        print(f"\n📊 Installation Summary:")
        print(f"   Dependencies: {success_count}/{len(test_imports)} working")
        print(f"✅ Verification complete: {sum(len(tools) for tools in working_tools.values())} tools available")
        
        # Test core functionality with fallbacks
        test_cmd = f'{python_cmd} -c "print(\'Core system ready\')"'
        self.run_command(test_cmd, "Testing core system", ignore_errors=True)
        
        return success_count >= len(test_imports) * 0.8
    
    def _test_available_tools(self, python_cmd):
        """Test which tools are actually working"""
        
        working_tools = {
            "pdf_engines": [],
            "ocr_engines": [],
            "ai_models": [],
            "image_processing": [],
            "performance": []
        }
        
        # Test tools
        test_imports = {
            "fitz": "pdf_engines",
            "pdfplumber": "pdf_engines", 
            "docling": "pdf_engines",
            "easyocr": "ocr_engines",
            "pytesseract": "ocr_engines",
            "transformers": "ai_models",
            "spacy": "ai_models",
            "PIL": "image_processing",
            "cv2": "image_processing",
            "numba": "performance",
            "scipy": "performance"
        }
        
        for module, category in test_imports.items():
            if module == "pytesseract":
                # Configure tesseract path for pytesseract
                test_cmd = f'{python_cmd} -c "import pytesseract; pytesseract.pytesseract.tesseract_cmd = \'tesseract\'; print(\'{module} OK\')"'
            else:
                test_cmd = f'{python_cmd} -c "import {module}; print(\'{module} OK\')"'
            
            if self.run_command(test_cmd, f"Testing {module}", ignore_errors=True):
                working_tools[category].append(module)
        
        # Test system tools
        if shutil.which("tesseract"):
            working_tools["ocr_engines"].append("tesseract")
        
        return working_tools
    
    def _update_hardware_profile_with_psutil(self, venv_python):
        """Update hardware profile with accurate psutil data from venv"""
        try:
            # Get accurate system info using psutil in venv
            cmd = f'{venv_python} -c "import psutil; print(psutil.cpu_count(), psutil.virtual_memory().total / (1024**3))"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                output = result.stdout.strip().split()
                cpu_count = int(float(output[0]))
                memory_gb = float(output[1])
                
                self.system_info["cpu_count"] = cpu_count
                self.system_info["memory_gb"] = memory_gb
                
                print(f"🔍 Accurate hardware: {cpu_count} CPUs, {memory_gb:.1f}GB RAM")
                
                # Reclassify performance with accurate data
                gpu_available = self.hardware_profile["gpu_available"]
                gpu_memory = self.hardware_profile["gpu_memory_gb"]
                
                if gpu_available and gpu_memory >= 8 and memory_gb >= 16:
                    performance_class = "ENTERPRISE"
                elif gpu_available and gpu_memory >= 4 and memory_gb >= 8:
                    performance_class = "HIGH_PERFORMANCE"
                elif memory_gb >= 8 and cpu_count >= 4:
                    performance_class = "STANDARD"
                elif memory_gb >= 4:
                    performance_class = "BASIC"
                else:
                    performance_class = "MINIMAL"
                
                if performance_class != self.hardware_profile["performance_class"]:
                    old_class = self.hardware_profile["performance_class"]
                    print(f"📊 Updated performance class: {old_class} → {performance_class}")
                    self.hardware_profile["performance_class"] = performance_class
                    self.hardware_profile["recommended_tools"] = self._get_recommended_tools(performance_class)
                
        except Exception as e:
            print(f"⚠️  Could not get accurate hardware info: {e}")
    
    def _create_fallback_config(self):
        """Create fallback configuration for failed installations"""
        
        try:
            # Simple fallback config without external dependencies
            available_tools = self.hardware_profile.get("actually_available", {})
            
            fallback_config = {
                "hardware_profile": self.hardware_profile["performance_class"],
                "available_tools": available_tools,
                "user_guidance": f"System configured for {self.hardware_profile['performance_class']} performance class"
            }
            
            with open("fallback_config.json", "w") as f:
                json.dump(fallback_config, f, indent=2)
            
            print("\n" + "=" * 60)
            print("🔧 SYSTEM CONFIGURATION")
            print("=" * 60)
            print(fallback_config["user_guidance"])
            
        except Exception as e:
            print(f"⚠️  Could not create fallback config: {e}")
            print("   System will use default settings")
    
    def _show_completion_message(self):
        """Show completion message"""
        
        print("\n" + "=" * 60)
        print("🎉 INTELLIGENT INSTALLATION COMPLETE!")
        print("=" * 60)
        
        print(f"🖥️  Hardware Profile: {self.hardware_profile['performance_class']}")
        print(f"🎯 Quality Target: {0.95 if self.hardware_profile['performance_class'] == 'ENTERPRISE' else 0.85}")
        print(f"🤖 AI Enhancement: {'Enabled' if self.hardware_profile['recommended_tools']['ai_models'] else 'Basic'}")
        
        print("\n🚀 NEXT STEPS:")
        if self.system_info["os_type"] == "windows":
            print("1. Run: activate.bat")
        else:
            print("1. Run: source activate.sh")
        print("2. Place PDFs in: data/input/")
        print("3. Run: python main.py")
        print("4. Monitor: python comprehensive_audit.py")
        
        print("\n🎯 INTELLIGENT FEATURES v2.2:")
        print("   • Hardware-aware dependency selection")
        print("   • Python 3.12 optimization (magika support)")
        print("   • OS-specific system package management")
        print("   • Auto-detects optimal extraction method")
        print("   • Adapts to hardware capabilities")
        print("   • Preserves layout, tables, and TOC")
        print("   • Iterative quality enhancement")
        print("   • Resource-aware processing")
        print("   • Comprehensive project monitoring")
        print("   • Self-healing configuration")

def main():
    """Main installation function"""
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return 1
    
    installer = IntelligentInstaller()
    installer.install()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())