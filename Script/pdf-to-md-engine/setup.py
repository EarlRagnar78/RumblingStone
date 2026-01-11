#!/usr/bin/env python3
"""
Enhanced PDF to Markdown Engine - Setup Script
Automatic installation with OS detection and dependency management
"""
import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def detect_os():
    """Detect operating system and return setup commands"""
    system = platform.system().lower()
    
    if system == "linux":
        # Detect Linux distribution
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "bazzite" in content:
                    return "bazzite"
                elif "ubuntu" in content or "debian" in content:
                    return "debian"
                elif "fedora" in content or "centos" in content or "rhel" in content:
                    return "fedora"
                elif "arch" in content:
                    return "arch"
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
    print(f"   Running: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        if ignore_errors:
            print(f"   ⚠️  Warning: {e}")
            return False
        else:
            print(f"   ❌ Error: {e}")
            if e.stderr:
                print(f"   Details: {e.stderr.strip()}")
            return False

def install_system_dependencies():
    """Install system-level dependencies based on OS"""
    os_type = detect_os()
    print(f"🖥️  Detected OS: {os_type}")
    
    if os_type == "bazzite":
        # Bazzite OS (immutable gaming Linux) - use homebrew and toolbox
        print("🎮 Bazzite OS detected - using homebrew and toolbox")
        
        # Check for homebrew first
        if not shutil.which("brew"):
            print("📦 Installing Homebrew...")
            homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            if not run_command(homebrew_install, "Installing Homebrew", ignore_errors=True):
                print("⚠️  Homebrew installation failed, trying toolbox approach")
        
        # Bazzite-specific commands using homebrew and toolbox
        commands = [
            ("brew install tesseract", "Installing Tesseract OCR via Homebrew"),
            ("brew install libffi openssl", "Installing crypto libraries via Homebrew"),
        ]
        
        # Alternative: use toolbox for system packages
        toolbox_commands = [
            ("toolbox create pdf-engine || true", "Creating toolbox container"),
            ("toolbox run -c pdf-engine sudo dnf install -y tesseract tesseract-langpack-eng", "Installing Tesseract in toolbox"),
            ("toolbox run -c pdf-engine sudo dnf install -y python3-devel gcc gcc-c++", "Installing build tools in toolbox"),
        ]
        
        # Try homebrew first, fallback to toolbox
        success = True
        for cmd, desc in commands:
            if not run_command(cmd, desc, ignore_errors=True):
                success = False
        
        if not success:
            print("🔧 Homebrew failed, trying toolbox approach...")
            for cmd, desc in toolbox_commands:
                run_command(cmd, desc, ignore_errors=True)
    
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
    
    elif os_type == "arch":
        commands = [
            ("sudo pacman -Sy", "Updating package list"),
            ("sudo pacman -S --noconfirm tesseract tesseract-data-eng", "Installing Tesseract OCR"),
            ("sudo pacman -S --noconfirm mesa glib2 libsm libxext libxrender", "Installing system libraries"),
            ("sudo pacman -S --noconfirm base-devel", "Installing build tools")
        ]
    
    elif os_type == "macos":
        if not shutil.which("brew"):
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
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
        print("   3. Install Visual Studio Build Tools if needed")
        return True
    
    else:
        print("❓ Unknown OS. Please install Tesseract OCR manually.")
        return True
    
    # Run installation commands
    success = True
    for cmd, desc in commands:
        if not run_command(cmd, desc, ignore_errors=True):
            success = False
    
    return success

def setup_python_environment():
    """Setup Python virtual environment and install dependencies"""
    print("\n🐍 Setting up Python environment...")
    
    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        if not run_command(f"{sys.executable} -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine pip command based on OS
    if platform.system().lower() == "windows":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Upgrade pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install core dependencies
    core_deps = [
        "wheel",
        "setuptools",
        "cryptography>=3.0.0",
        "pdfminer.six>=20220319",
        "docling>=2.0.0",
        "PyMuPDF>=1.23.0",
        "pdfplumber>=0.10.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        "loguru>=0.7.0",
        "jinja2>=3.1.0",
        "tqdm>=4.65.0",
        "psutil>=5.9.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "chardet>=5.0.0",
        "ftfy>=6.1.0"
    ]
    
    print("📦 Installing core dependencies...")
    for dep in core_deps:
        if not run_command(f"{pip_cmd} install '{dep}'", f"Installing {dep.split('>=')[0]}", ignore_errors=True):
            print(f"   ⚠️  Failed to install {dep}, continuing...")
    
    # Install OCR dependencies
    print("\n🔍 Installing OCR dependencies...")
    ocr_deps = [
        "pytesseract>=0.3.10",
        "opencv-python>=4.8.0"
    ]
    
    for dep in ocr_deps:
        run_command(f"{pip_cmd} install '{dep}'", f"Installing {dep.split('>=')[0]}", ignore_errors=True)
    
    # Try to install EasyOCR (may fail on some systems)
    print("🚀 Attempting to install EasyOCR (GPU-accelerated)...")
    run_command(f"{pip_cmd} install easyocr>=1.7.0", "Installing EasyOCR", ignore_errors=True)
    
    return True

def verify_installation():
    """Verify that all components are working"""
    print("\n✅ Verifying installation...")
    
    # Determine python command
    if platform.system().lower() == "windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    # Test core imports
    test_imports = [
        ("docling", "Docling PDF processing"),
        ("fitz", "PyMuPDF"),
        ("pdfplumber", "pdfplumber"),
        ("cryptography", "Cryptography"),
        ("torch", "PyTorch"),
        ("PIL", "Pillow"),
        ("numpy", "NumPy"),
        ("loguru", "Loguru logging"),
        ("pydantic", "Pydantic"),
        ("jinja2", "Jinja2 templates")
    ]
    
    success_count = 0
    for module, name in test_imports:
        cmd = f"{python_cmd} -c \"import {module}; print('✅ {name}')\""
        if run_command(cmd, f"Testing {name}", ignore_errors=True):
            success_count += 1
        else:
            print(f"   ❌ {name} not available")
    
    # Test OCR engines
    print("\n🔍 Testing OCR engines...")
    
    # Test Tesseract
    if shutil.which("tesseract"):
        print("   ✅ Tesseract OCR found")
        run_command("tesseract --version", "Tesseract version", ignore_errors=True)
    else:
        print("   ❌ Tesseract OCR not found in PATH")
    
    # Test EasyOCR
    cmd = f"{python_cmd} -c \"import easyocr; print('✅ EasyOCR available')\""
    if not run_command(cmd, "Testing EasyOCR", ignore_errors=True):
        print("   ⚠️  EasyOCR not available (optional)")
    
    # Test project structure
    print("\n📁 Verifying project structure...")
    required_files = [
        "main.py",
        "src/enhanced_processor.py",
        "src/enhanced_text_extractor.py",
        "src/config.py",
        "requirements.txt"
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} missing")
    
    print(f"\n📊 Installation Summary:")
    print(f"   Core dependencies: {success_count}/{len(test_imports)} working")
    print(f"   OCR engines: {'Tesseract' if shutil.which('tesseract') else 'None'}")
    
    return success_count >= len(test_imports) * 0.8  # 80% success rate

def create_activation_script():
    """Create convenient activation script"""
    if platform.system().lower() == "windows":
        script_content = """@echo off
echo 🚀 Activating PDF-to-MD Engine environment...
call venv\\Scripts\\activate.bat
echo ✅ Environment activated!
echo.
echo Available commands:
echo   python main.py              - Process PDFs in data/input/
echo   python run_enhanced.py      - Run enhanced processing
echo   python verify_project.py    - Verify installation
echo.
"""
        with open("activate.bat", "w") as f:
            f.write(script_content)
        print("📝 Created activate.bat")
    
    else:
        script_content = """#!/bin/bash
echo "🚀 Activating PDF-to-MD Engine environment..."
source venv/bin/activate
echo "✅ Environment activated!"
echo ""
echo "Available commands:"
echo "  python main.py              - Process PDFs in data/input/"
echo "  python run_enhanced.py      - Run enhanced processing"
echo "  python verify_project.py    - Verify installation"
echo ""
"""
        with open("activate.sh", "w") as f:
            f.write(script_content)
        os.chmod("activate.sh", 0o755)
        print("📝 Created activate.sh")

def main():
    """Main setup function"""
    print("🚀 PDF to Markdown Engine v2.0 - Enhanced Setup")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required. Current version:", sys.version)
        return 1
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install system dependencies
    print("\n" + "=" * 60)
    print("📦 SYSTEM DEPENDENCIES")
    print("=" * 60)
    
    if not install_system_dependencies():
        print("⚠️  Some system dependencies failed to install")
        print("   You may need to install them manually")
    
    # Setup Python environment
    print("\n" + "=" * 60)
    print("🐍 PYTHON ENVIRONMENT")
    print("=" * 60)
    
    if not setup_python_environment():
        print("❌ Failed to setup Python environment")
        return 1
    
    # Verify installation
    print("\n" + "=" * 60)
    print("✅ VERIFICATION")
    print("=" * 60)
    
    if verify_installation():
        print("\n🎉 Installation completed successfully!")
    else:
        print("\n⚠️  Installation completed with some issues")
        print("   Check the messages above for details")
    
    # Create activation script
    create_activation_script()
    
    # Final instructions
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    
    os_type = detect_os()
    
    if os_type == "bazzite":
        print("🎮 Bazzite OS Instructions:")
        print("1. If using homebrew: source ~/.bashrc or restart terminal")
        print("2. If using toolbox: toolbox enter pdf-engine")
        print("3. Run: source activate.sh")
        print("4. Place PDFs in: data/input/")
        print("5. Run: python main.py")
        print("\n📝 Note: On Bazzite, dependencies are installed via homebrew or toolbox")
    elif platform.system().lower() == "windows":
        print("1. Run: activate.bat")
        print("2. Place PDFs in: data\\input\\")
        print("3. Run: python main.py")
    else:
        print("1. Run: source activate.sh")
        print("2. Place PDFs in: data/input/")
        print("3. Run: python main.py")
    
    print("\n📚 Documentation:")
    print("   README.md           - Full documentation")
    print("   TROUBLESHOOTING.md  - Common issues and solutions")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())