# PDF to Markdown Engine - Deployment Guide

## System Requirements

### Minimum Requirements
- **CPU**: 4+ cores (2 cores reserved for system)
- **RAM**: 8GB (4GB+ available for processing)
- **GPU**: Optional CUDA-compatible GPU with 4GB+ VRAM
- **Storage**: 2GB free space for models and processing
- **Python**: 3.9+

### Recommended Requirements
- **CPU**: 8+ cores for optimal parallel processing
- **RAM**: 16GB+ for large PDF processing
- **GPU**: RTX 3060/4050+ with 6GB+ VRAM
- **Storage**: 5GB+ SSD for fast I/O

## Installation Steps

### 1. Environment Setup

```bash
# Create project directory
mkdir pdf-to-md-engine
cd pdf-to-md-engine

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install docling pydantic-settings jinja2 loguru torch torchvision easyocr opencv-python

# For GPU support (if available)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 3. Configuration

Create/verify `.env` file with resource settings:

```env
# Input/Output settings
INPUT_DIR=./data/input
OUTPUT_DIR=./data/output

# Processing Settings
IMAGE_SCALE=2.0
SPLIT_BY_HEADER_LEVEL=1
OVERWRITE_EXISTING=False
LOG_LEVEL=INFO

# Performance Settings (Auto-detected if not set)
MAX_WORKERS=6          # CPU cores to use (auto: total-2)
USE_GPU=True           # Enable GPU acceleration
GPU_MEMORY_LIMIT_GB=2.0 # Reserve memory for OS
BATCH_SIZE=4           # Processing batch size
MAX_MEMORY_GB=4.0      # Maximum RAM usage
```

### 4. Directory Structure

Ensure the following directories exist:

```bash
mkdir -p data/input data/output data/processing
```

### 5. Resource Management

The engine automatically:
- **CPU**: Detects cores and reserves 2 for system
- **GPU**: Checks CUDA availability and reserves memory
- **RAM**: Monitors usage and throttles if needed
- **I/O**: Uses efficient batch processing

### 6. Usage

```bash
# Place PDF files in data/input/
cp your-document.pdf data/input/

# Run processing
python main.py

# Check results in data/output/
ls data/output/
```

## Performance Tuning

### For Low-Resource Systems
```env
MAX_WORKERS=2
USE_GPU=False
BATCH_SIZE=2
MAX_MEMORY_GB=2.0
```

### For High-Performance Systems
```env
MAX_WORKERS=12
USE_GPU=True
GPU_MEMORY_LIMIT_GB=1.0
BATCH_SIZE=8
MAX_MEMORY_GB=8.0
```

## Troubleshooting

### GPU Issues
- Check CUDA installation: `nvidia-smi`
- Verify PyTorch CUDA: `python -c "import torch; print(torch.cuda.is_available())"`
- Reduce GPU memory limit if out of memory

### Memory Issues
- Reduce `MAX_WORKERS` and `BATCH_SIZE`
- Lower `MAX_MEMORY_GB` setting
- Process smaller PDFs first

### Performance Issues
- Increase `MAX_WORKERS` if CPU usage is low
- Enable GPU if available
- Use SSD storage for better I/O

## Monitoring

The engine provides real-time feedback:
- CPU core usage
- GPU memory allocation
- Processing progress
- Resource consumption warnings