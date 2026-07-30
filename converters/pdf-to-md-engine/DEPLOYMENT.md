# Deployment Guide - PDF to Markdown Engine v2.0

## 🎯 Quick Deployment

### Option 1: Automatic Setup (Recommended)
```bash
# Clone and setup in one command
git clone <repository-url> pdf-to-md-engine
cd pdf-to-md-engine
chmod +x setup.sh && ./setup.sh
```

### Option 2: Manual Installation
```bash
# 1. Install core dependencies
pip install -e .

# 2. Install OCR engines (choose one)
pip install -e .[easyocr]     # GPU-accelerated
pip install -e .[tesseract]   # Lightweight
pip install -e .[ocr-full]    # Both engines

# 3. Test installation
python -c "from src.config import Settings; print('✓ Installation successful')"
```

## 🖥️ System-Specific Deployment

### Ubuntu 20.04+ / Debian 11+

```bash
#!/bin/bash
# Complete Ubuntu/Debian setup script

# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3 python3-pip python3-venv git
sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-deu
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
sudo apt install -y ffmpeg libsm6 libxext6 libfontconfig1 libxrender1 libgl1-mesa-glx

# Create virtual environment
python3 -m venv pdf-md-env
source pdf-md-env/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -e .[ocr-full,performance]

# Verify installation
python -c "from src.processor import SystemResourceManager; rm = SystemResourceManager(); print(f'✓ System ready: {rm.cpu_count} cores, {rm.total_memory:.1f}GB RAM')"
```

### Bazzite OS (Gaming Linux)

```bash
#!/bin/bash
# Bazzite OS setup with Homebrew priority and fallback options

# Option 1: Homebrew (recommended - works on immutable host)
# Install Homebrew if not present
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"
echo 'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"' >> ~/.bashrc

# Install dependencies via Homebrew
brew install python@3.11 tesseract git

# Clone and setup
git clone <repository-url> pdf-to-md-engine
cd pdf-to-md-engine
pip install -e .[ocr-full]

# Option 2: Toolbx container (if Homebrew unavailable)
toolbox create pdf-md-dev
toolbox enter pdf-md-dev

# Inside container:
sudo dnf install -y python3-pip python3-devel git tesseract tesseract-langpack-eng
sudo dnf install -y mesa-libGL glib2 libSM libXext libXrender

# Option 3: Distrobox (alternative container)
distrobox create --name pdf-md-dev --image fedora:latest
distrobox enter pdf-md-dev
# Follow container steps above

# Option 4: rpm-ostree layering (requires reboot)
sudo rpm-ostree install python3-pip python3-devel git tesseract
sudo systemctl reboot

# Option 5: Flatpak (limited functionality)
flatpak install flathub org.freedesktop.Sdk.Extension.python3
```

### CentOS 8+ / RHEL 8+ / Rocky Linux

```bash
#!/bin/bash
# Complete CentOS/RHEL setup script

# Install EPEL repository
sudo dnf install -y epel-release

# Install system dependencies
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y python3 python3-pip python3-devel git
sudo dnf install -y tesseract tesseract-langpack-eng
sudo dnf install -y mesa-libGL glib2 libSM libXext libXrender

# Create virtual environment
python3 -m venv pdf-md-env
source pdf-md-env/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -e .[ocr-full,performance]
```

```bash
#!/bin/bash
# Complete macOS setup script

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install system dependencies
brew update
brew install python@3.11 tesseract git
brew install --cask miniconda  # Optional: for better Python environment management

# Create virtual environment
python3 -m venv pdf-md-env
source pdf-md-env/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -e .[ocr-full,performance]

# For Apple Silicon Macs, install optimized PyTorch
if [[ $(uname -m) == "arm64" ]]; then
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
fi
```

### Windows 10/11

```powershell
# PowerShell script for Windows deployment

# Install Python (if not installed)
# Download from https://www.python.org/downloads/windows/

# Install Tesseract OCR
# Download from https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR

# Install Git (if not installed)
# Download from https://git-scm.com/download/win

# Create virtual environment
python -m venv pdf-md-env
pdf-md-env\Scripts\activate

# Install Python dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -e .[ocr-full,performance]

# Verify installation
python -c "from src.processor import SystemResourceManager; rm = SystemResourceManager(); print(f'System ready: {rm.cpu_count} cores, {rm.total_memory:.1f}GB RAM')"
```

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -e .[ocr-full]

# Create data directories
RUN mkdir -p data/input data/output

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Expose volume for data
VOLUME ["/app/data"]

# Run the application
CMD ["python", "main.py", "data/input"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  pdf-to-md:
    build: .
    volumes:
      - ./data:/app/data
      - ./config:/app/config
    environment:
      - LOG_LEVEL=INFO
      - MAX_WORKERS=4
      - USE_GPU=false  # Set to true if GPU support needed
    restart: unless-stopped
    
  # Optional: GPU-enabled version
  pdf-to-md-gpu:
    build: .
    runtime: nvidia
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - USE_GPU=true
    volumes:
      - ./data:/app/data
    profiles:
      - gpu
```

### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Process files
docker-compose exec pdf-to-md python main.py data/input/document.pdf

# View logs
docker-compose logs -f pdf-to-md
```

## ☁️ Cloud Deployment

### AWS EC2

```bash
#!/bin/bash
# AWS EC2 deployment script

# Launch EC2 instance (Ubuntu 22.04 LTS)
# Recommended: t3.large or larger (2+ vCPU, 8GB+ RAM)

# Connect and setup
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install -y python3-pip git tesseract-ocr
git clone <your-repo> pdf-to-md-engine
cd pdf-to-md-engine

# Install application
pip3 install -e .[ocr-full]

# Setup systemd service
sudo tee /etc/systemd/system/pdf-to-md.service > /dev/null <<EOF
[Unit]
Description=PDF to Markdown Engine
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/pdf-to-md-engine
ExecStart=/usr/bin/python3 main.py data/input
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable pdf-to-md
sudo systemctl start pdf-to-md
```

### Google Cloud Platform

```bash
#!/bin/bash
# GCP Compute Engine deployment

# Create VM instance
gcloud compute instances create pdf-to-md-engine \
    --zone=us-central1-a \
    --machine-type=n1-standard-2 \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB

# SSH and setup
gcloud compute ssh pdf-to-md-engine --zone=us-central1-a

# Follow Ubuntu installation steps above
```

### Azure VM

```bash
#!/bin/bash
# Azure VM deployment

# Create resource group
az group create --name pdf-to-md-rg --location eastus

# Create VM
az vm create \
    --resource-group pdf-to-md-rg \
    --name pdf-to-md-vm \
    --image Ubuntu2204 \
    --size Standard_B2s \
    --admin-username azureuser \
    --generate-ssh-keys

# SSH and setup
az vm show --resource-group pdf-to-md-rg --name pdf-to-md-vm --show-details --query publicIps -o tsv
ssh azureuser@<public-ip>

# Follow Ubuntu installation steps above
```

## 🔧 Production Configuration

### Environment Variables
```bash
# Production .env configuration
LOG_LEVEL=INFO
MAX_WORKERS=auto
USE_GPU=auto
CPU_USAGE_THRESHOLD=80
MEMORY_USAGE_THRESHOLD=75

# OCR settings for production
OCR_ENGINE=auto
OCR_CONFIDENCE_THRESHOLD=0.8
OCR_BATCH_SIZE=4

# Security settings
OVERWRITE_EXISTING=false
```

### Monitoring Setup
```bash
# Install monitoring tools
pip install prometheus-client grafana-api

# Setup log rotation
sudo tee /etc/logrotate.d/pdf-to-md > /dev/null <<EOF
/var/log/pdf-to-md/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 ubuntu ubuntu
}
EOF
```

### Performance Tuning
```bash
# System-level optimizations

# Increase file descriptor limits
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize memory settings
echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "vm.vfs_cache_pressure=50" | sudo tee -a /etc/sysctl.conf

# Apply changes
sudo sysctl -p
```

## 🚨 Troubleshooting Deployment

### Common Deployment Issues

#### 1. Permission Errors
```bash
# Fix file permissions
sudo chown -R $USER:$USER /path/to/pdf-to-md-engine
chmod +x main.py
chmod +x setup.sh
```

#### 2. Missing System Dependencies
```bash
# Ubuntu/Debian
sudo apt install -y build-essential python3-dev libffi-dev

# CentOS/RHEL
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y python3-devel libffi-devel
```

#### 3. GPU Driver Issues
```bash
# Check NVIDIA drivers
nvidia-smi

# Install CUDA toolkit (Ubuntu)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit
```

#### 4. Memory Issues in Production
```bash
# Monitor memory usage
watch -n 1 'free -h && ps aux --sort=-%mem | head -10'

# Adjust swap if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Health Checks
```bash
# System health check script
#!/bin/bash
echo "=== PDF-to-MD Engine Health Check ==="

# Check Python installation
python3 --version || echo "❌ Python not found"

# Check dependencies
python3 -c "import torch; print(f'✓ PyTorch: {torch.__version__}')" 2>/dev/null || echo "❌ PyTorch not available"
python3 -c "import docling; print('✓ Docling available')" 2>/dev/null || echo "❌ Docling not available"

# Check OCR engines
python3 -c "import easyocr; print('✓ EasyOCR available')" 2>/dev/null || echo "⚠️ EasyOCR not available"
tesseract --version >/dev/null 2>&1 && echo "✓ Tesseract available" || echo "⚠️ Tesseract not available"

# Check GPU
python3 -c "import torch; print(f'✓ CUDA available: {torch.cuda.is_available()}')" 2>/dev/null

# Check system resources
python3 -c "
from src.processor import SystemResourceManager
rm = SystemResourceManager()
print(f'✓ System: {rm.cpu_count} cores, {rm.total_memory:.1f}GB RAM')
print(f'✓ GPU: {rm.gpu_info[\"name\"]} ({rm.gpu_info[\"memory_gb\"]:.1f}GB)')
print(f'✓ Optimal OCR: {rm.optimal_ocr_engine}')
" 2>/dev/null || echo "❌ System check failed"

echo "=== Health Check Complete ==="
```

## 📊 Performance Benchmarks

### Expected Performance (per PDF page)
- **Text-only pages**: 0.5-2 seconds
- **Image-heavy pages**: 2-10 seconds  
- **OCR processing**: +1-5 seconds per image
- **GPU acceleration**: 2-3x faster OCR

### Scaling Guidelines
- **Small files** (< 50 pages): Any system configuration
- **Medium files** (50-200 pages): 8GB+ RAM, 4+ cores recommended
- **Large files** (200+ pages): 16GB+ RAM, 8+ cores, GPU recommended
- **Batch processing**: Scale horizontally with multiple instances

This deployment guide ensures reliable installation across different environments with proper monitoring and troubleshooting capabilities.