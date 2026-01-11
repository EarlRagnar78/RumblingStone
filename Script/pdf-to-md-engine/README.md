# PDF to Markdown Engine v2.0 - Enhanced Edition

🚀 **Intelligent PDF to Markdown converter** with enhanced text extraction, OCR integration, and better chapter detection.

## ✨ Key Features

- **🔍 Enhanced Text Extraction** - Hybrid approach using PyMuPDF + pdfplumber for better text quality
- **📖 Smart Chapter Detection** - Uses PDF outline/bookmarks for accurate chapter structure
- **🔧 OCR Enhancement** - Improves existing text layers instead of replacing them
- **🧠 Intelligent Resource Management** - Auto-detects system capabilities and optimizes performance
- **⚡ GPU Acceleration** - CUDA support with conservative memory management
- **📊 Real-time Monitoring** - System resource tracking with adaptive throttling
- **🎯 Quality Assessment** - Text quality analysis and encoding fixes
- **🔄 Parallel Processing** - Multi-threaded with dynamic worker allocation

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.9+
- **RAM**: 4GB (8GB+ recommended)
- **CPU**: 2+ cores (4+ cores recommended)
- **Storage**: 2GB free space

### Recommended for Optimal Performance
- **RAM**: 16GB+
- **CPU**: 8+ cores
- **GPU**: NVIDIA GPU with 4GB+ VRAM (RTX series recommended)
- **Storage**: SSD with 10GB+ free space

## 📦 Installation

### 1. Install Dependencies
```bash
# Install core dependencies
pip install -r requirements.txt

# For development
pip install -e .
```

### 2. System-Specific Setup

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
```

#### macOS
```bash
brew install tesseract
```

#### Windows
Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

## 🚀 Quick Start

### Basic Usage
```bash
# Process PDFs in input directory
python main.py

# Use enhanced processing
python run_enhanced.py

# Test enhanced extraction
python test_enhanced_extraction.py
```

### Configuration
Create/edit `.env` file:
```bash
# Paths
INPUT_DIR=data/input
OUTPUT_DIR=data/output

# Processing
MAX_WORKERS=auto
USE_GPU=auto
OCR_ENGINE=auto

# OCR Settings
OCR_LANGUAGES=en
OCR_CONFIDENCE_THRESHOLD=0.7
```

## 🔍 Enhanced Features

### Text Extraction Improvements
- **Hybrid Extraction**: Combines PyMuPDF and pdfplumber for best results
- **Encoding Fixes**: Handles ligatures (ﬁ→fi), smart quotes, and UTF-8 issues
- **Quality Analysis**: Assesses text quality and recommends OCR enhancement
- **Text Cleaning**: Removes artifacts and normalizes formatting

### Chapter Detection Enhancements
- **PDF Outline Support**: Uses PDF bookmarks for accurate chapter structure
- **Pattern Recognition**: Detects various chapter formats (Chapter X, Part I, etc.)
- **Smart Splitting**: Handles complex document structures
- **Title Extraction**: Automatically extracts meaningful chapter titles

### OCR Enhancement
- **Layer Improvement**: Enhances existing text instead of replacing it
- **Selective Processing**: Only processes problematic text areas
- **Quality Scoring**: Confidence-based text inclusion
- **Artifact Detection**: Identifies and fixes OCR issues

## 📊 Project Structure

```
pdf-to-md-engine/
├── src/
│   ├── config.py                    # Configuration management
│   ├── enhanced_processor.py        # Main enhanced processing pipeline
│   ├── enhanced_text_extractor.py   # Enhanced text extraction
│   ├── pdf_text_analyzer.py         # Text quality analysis
│   ├── utils.py                     # Utility functions
│   └── templates/
│       └── chapter.md.j2            # Chapter template
├── data/
│   ├── input/                       # Input PDFs
│   ├── output/                      # Generated markdown
│   └── processing/                  # Temporary files
├── main.py                          # Main entry point
├── run_enhanced.py                  # Enhanced processing script
├── test_enhanced_extraction.py      # Test enhanced features
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Missing dependencies
pip install -r requirements.txt

# PyMuPDF installation issues
pip install --upgrade PyMuPDF

# pdfplumber issues
pip install --upgrade pdfplumber
```

#### 2. OCR Engine Issues
```bash
# EasyOCR not available
pip install easyocr opencv-python

# Tesseract not found
# Ubuntu: sudo apt install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from GitHub releases
```

#### 3. GPU Memory Issues
```bash
# CUDA out of memory
export GPU_MEMORY_LIMIT_GB=2.0
export OCR_GPU_MEMORY_PER_BATCH=1.0
```

#### 4. Text Extraction Issues
```bash
# Poor text quality
# The enhanced engine automatically detects and fixes common issues:
# - Encoding problems (ligatures, smart quotes)
# - OCR artifacts
# - Formatting inconsistencies
```

#### 5. Chapter Detection Problems
```bash
# No chapters detected
# The enhanced engine tries multiple methods:
# 1. PDF outline/bookmarks (most accurate)
# 2. Pattern-based detection
# 3. Page break analysis
# 4. Single document fallback
```

### Performance Optimization

#### For Low-Memory Systems (< 8GB RAM)
```bash
export MEMORY_USAGE_THRESHOLD=70
export MAX_WORKERS=2
export OCR_ENGINE=tesseract
```

#### For High-Performance Systems (16GB+ RAM)
```bash
export CPU_USAGE_THRESHOLD=90
export OCR_BATCH_SIZE=8
export OCR_ENGINE=easyocr
```

### Debug Mode
```bash
# Enable detailed logging
python main.py --log-level DEBUG

# Test text extraction
python test_enhanced_extraction.py

# Check system capabilities
python -c "from src.enhanced_processor import SystemResourceManager; rm = SystemResourceManager(); print(f'System: {rm.cpu_count} cores, {rm.total_memory:.1f}GB RAM')"
```

## 🔄 Output Structure

```
output/
├── document_name/
│   ├── assets/
│   │   ├── img_001.png
│   │   └── img_002.png
│   ├── 01_front_cover.md
│   ├── 02_introduction.md
│   ├── 03_chapter_1.md
│   └── .receipt              # Processing metadata
```

### Enhanced Metadata
The `.receipt` file now includes:
- Text quality analysis
- Chapter detection method used
- OCR enhancement results
- Processing performance metrics

## 🆕 What's New in v2.0

### Enhanced Text Extraction
- Hybrid PyMuPDF + pdfplumber approach
- Automatic encoding issue detection and fixing
- Text quality scoring and analysis
- Smart OCR enhancement recommendations

### Better Chapter Detection
- PDF outline/bookmark support
- Multiple detection strategies
- Improved title extraction
- Better handling of complex document structures

### Improved OCR Integration
- Text layer enhancement instead of replacement
- Selective processing of problematic areas
- Better confidence scoring
- Reduced false positives

### Performance Improvements
- More efficient resource usage
- Better memory management
- Faster processing for text-heavy documents
- Reduced OCR overhead

## 🤝 Contributing

1. Fork the repository
2. Install development dependencies: `pip install -r requirements.txt`
3. Make your changes
4. Test with: `python test_enhanced_extraction.py`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run debug mode for detailed logs
3. Test with `test_enhanced_extraction.py`
4. Check system requirements and dependencies