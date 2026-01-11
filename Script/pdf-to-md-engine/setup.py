#!/usr/bin/env python3
"""
Enhanced PDF to Markdown Engine - Setup Script v2.1
Integrating best practices from pdfmd, markitdown, and docling projects
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def detect_os():
    """Detect operating system"""
    system = platform.system().lower()
    
    if system == "linux":
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "bazzite" in content:
                    return "bazzite"
                elif "ubuntu" in content or "debian" in content:
                    return "debian"
                elif "fedora" in content or "centos" in content or "rhel" in content:
                    return "fedora"
        except:
            pass
        return "linux"
    elif system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def run_command(cmd, description="", ignore_errors=False):
    """Run system command with error handling"""
    print(f"🔧 {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"   ⚠️  Warning: {e}")
            return False
        else:
            print(f"   ❌ Error: {e}")
            return False

def install_system_dependencies():
    """Install system-level dependencies based on OS"""
    os_type = detect_os()
    print(f"🖥️  Detected OS: {os_type}")
    
    if os_type == "bazzite":
        # Bazzite OS - use homebrew and toolbox
        print("🎮 Bazzite OS detected - using homebrew")
        
        if not shutil.which("brew"):
            print("📦 Installing Homebrew...")
            homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            run_command(homebrew_install, "Installing Homebrew", ignore_errors=True)
        
        commands = [
            ("brew install tesseract", "Installing Tesseract OCR"),
            ("brew install libffi openssl", "Installing crypto libraries"),
        ]
        
    elif os_type == "debian":
        commands = [
            ("sudo apt update", "Updating package list"),
            ("sudo apt install -y tesseract-ocr tesseract-ocr-eng", "Installing Tesseract OCR"),
            ("sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1", "Installing system libraries"),
            ("sudo apt install -y python3-dev build-essential", "Installing build tools"),
            ("sudo apt install -y libffi-dev libssl-dev", "Installing crypto libraries")
        ]
    
    elif os_type == "fedora":
        commands = [
            ("sudo dnf update -y", "Updating package list"),
            ("sudo dnf install -y tesseract tesseract-langpack-eng", "Installing Tesseract OCR"),
            ("sudo dnf install -y mesa-libGL glib2 libSM libXext libXrender gomp", "Installing system libraries"),
            ("sudo dnf install -y python3-devel gcc gcc-c++", "Installing build tools"),
            ("sudo dnf install -y libffi-devel openssl-devel", "Installing crypto libraries")
        ]
    
    elif os_type == "macos":
        if not shutil.which("brew"):
            print("❌ Homebrew not found. Please install Homebrew first")
            return False
        
        commands = [
            ("brew update", "Updating Homebrew"),
            ("brew install tesseract", "Installing Tesseract OCR"),
            ("brew install libffi openssl", "Installing crypto libraries")
        ]
    
    elif os_type == "windows":
        print("🪟 Windows detected. Please install manually:")
        print("   1. Download Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
        print("   2. Add Tesseract to PATH")
        return True
    
    else:
        print("❓ Unknown OS. Please install Tesseract OCR manually.")
        return True
    
    # Run installation commands
    for cmd, desc in commands:
        run_command(cmd, desc, ignore_errors=True)
    
    return True

def setup_python_environment():
    """Setup Python virtual environment with Python 3.12 for full compatibility"""
    print("\n🐍 Setting up Python environment with Python 3.12...")
    
    # Check if python3.12 is available
    python312_cmd = None
    for cmd in ["python3.12", "/usr/bin/python3.12", "python3"]:
        try:
            result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
            if "3.12" in result.stdout:
                python312_cmd = cmd
                print(f"✅ Found Python 3.12: {cmd}")
                break
        except:
            continue
    
    if not python312_cmd:
        print("⚠️  Python 3.12 not found, using system Python (may have compatibility issues)")
        python312_cmd = sys.executable
    
    # Create virtual environment with Python 3.12
    if not Path("venv").exists():
        if not run_command(f"{python312_cmd} -m venv venv", "Creating Python 3.12 virtual environment"):
            return False
    
    # Determine pip command
    if platform.system().lower() == "windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install core dependencies first
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
    
    print("📦 Installing core dependencies...")
    for dep in core_deps:
        run_command(f"{pip_cmd} install '{dep}'", f"Installing {dep.split('>=')[0]}", ignore_errors=True)
    
    # Install all optional dependencies (now compatible with Python 3.12)
    optional_deps = [
        "docling>=2.0.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "magika>=0.5.0",
        "easyocr>=1.7.0",
        "pytesseract>=0.3.10",
        "opencv-python>=4.8.0",
        "scikit-image>=0.21.0",
        "numba>=0.57.0",
        "scipy>=1.10.0",
        "charset-normalizer>=3.0.0",
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "sympy>=1.11.0",
        "tabulate>=0.9.0"
    ]
    
    print("📦 Installing all optional dependencies...")
    for dep in optional_deps:
        run_command(f"{pip_cmd} install '{dep}'", f"Installing {dep.split('>=')[0]} (optional)", ignore_errors=True)
    
    return True

def verify_installation():
    """Verify installation"""
    print("\n✅ Verifying installation...")
    
    # Determine python command
    if platform.system().lower() == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Test all imports including optional
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
        ("scipy", "SciPy")
    ]
    
    success_count = 0
    for module, name in test_imports:
        cmd = f"{python_cmd} -c \"import {module}; print('✅ {name}')\""
        if run_command(cmd, f"Testing {name}", ignore_errors=True):
            success_count += 1
    
    # Test OCR engines
    print("\n🔍 Testing OCR engines...")
    
    if shutil.which("tesseract"):
        print("   ✅ Tesseract OCR found")
    else:
        print("   ❌ Tesseract OCR not found")
    
    # Test enhanced features
    cmd = f"{python_cmd} -c \"from src.enhanced_table_detector import detect_tables_enhanced; print('✅ Enhanced features')\""
    run_command(cmd, "Testing enhanced features", ignore_errors=True)
    
    print(f"\n📊 Installation Summary:")
    print(f"   Dependencies: {success_count}/{len(test_imports)} working")
    
    return success_count >= len(test_imports) * 0.8

def create_activation_script():
    """Create activation script"""
    if platform.system().lower() == "windows":
        script_content = """@echo off
echo 🚀 Activating PDF-to-MD Engine v2.1...
call venv\\Scripts\\activate.bat
echo ✅ Environment activated!
echo.
echo Available commands:
echo   python main.py              - Process PDFs
echo   python run_enhanced.py      - Enhanced processing
echo   python verify_project.py    - Verify installation
echo.
"""
        with open("activate.bat", "w") as f:
            f.write(script_content)
    else:
        script_content = """#!/bin/bash
echo "🚀 Activating PDF-to-MD Engine v2.1..."
source venv/bin/activate
echo "✅ Environment activated!"
echo ""
echo "Available commands:"
echo "  python main.py              - Process PDFs"
echo "  python run_enhanced.py      - Enhanced processing"
echo "  python verify_project.py    - Verify installation"
echo ""
"""
        with open("activate.sh", "w") as f:
            f.write(script_content)
        os.chmod("activate.sh", 0o755)

def main():
    """Main setup function"""
    print("🚀 PDF to Markdown Engine v2.1 - Enhanced Setup")
    print("Integrating best practices from pdfmd, markitdown, and docling")
    print("=" * 70)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        return 1
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install system dependencies
    print("\n📦 SYSTEM DEPENDENCIES")
    print("=" * 30)
    install_system_dependencies()
    
    # Setup Python environment
    print("\n🐍 PYTHON ENVIRONMENT")
    print("=" * 25)
    if not setup_python_environment():
        print("❌ Failed to setup Python environment")
        return 1
    
    # Verify installation
    print("\n✅ VERIFICATION")
    print("=" * 15)
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
    else:
        print("\n⚠️  Installation completed with some issues")
    
    # Create activation script
    create_activation_script()
    
    # Final instructions
    print("\n🎯 NEXT STEPS")
    print("=" * 15)
    
    if platform.system().lower() == "windows":
        print("1. Run: activate.bat")
        print("2. Place PDFs in: data\\input\\")
        print("3. Run: python main.py")
    else:
        print("1. Run: source activate.sh")
        print("2. Place PDFs in: data/input/")
        print("3. Run: python main.py")
    
    print("\n📚 Enhanced Features:")
    print("   • Quality assessment and iterative refinement")
    print("   • Stream-based processing (markitdown)")
    print("   • Form-style table detection")
    print("   • Partial numbering merge")
    print("   • Intelligent content analysis")
    print("   • Multi-strategy extraction")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())