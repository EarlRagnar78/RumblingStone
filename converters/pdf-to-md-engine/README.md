# PDF to Markdown Engine v2.1 - Enhanced Edition

🚀 **Intelligent PDF to Markdown converter** with **quality assessment and iterative refinement** integrating best practices from **pdfmd**, **markitdown**, and **docling** projects for superior text extraction, table detection, and document processing.

## ✨ Key Features

- **🔍 Multi-Strategy Text Extraction** - Combines PyMuPDF, pdfplumber, and docling with intelligent method selection
- **📊 Enhanced Table Detection** - Form-style, bordered, and ASCII table detection inspired by markitdown
- **🌊 Stream Processing** - Unified interface for files, streams, and URLs with intelligent content detection
- **📖 Smart Chapter Detection** - PDF outline/bookmarks with pattern-based fallbacks
- **🔧 OCR Enhancement** - Selective text layer improvement with confidence scoring
- **🧠 Intelligent Resource Management** - Auto-detects system capabilities and optimizes performance
- **⚡ GPU Acceleration** - CUDA support with conservative memory management
- **📊 Real-time Monitoring** - System resource tracking with adaptive throttling
- **🎯 Quality Assessment** - **NEW v2.1** - Automatic quality scoring and iterative refinement
- **🔄 Iterative Refinement** - **NEW v2.1** - Applies secondary methods when quality < 75%
- **🔄 Parallel Processing** - Multi-threaded with dynamic worker allocation

## 🏗️ Architecture Integration

### **Integrated Projects**
- **[pdfmd](https://github.com/VikParuchuri/pdfmd)** - Modular pipeline architecture, mathematical content processing
- **[markitdown](https://github.com/microsoft/markitdown)** - Stream processing, form-style table detection, content analysis
- **[docling](https://github.com/DS4SD/docling)** - Advanced PDF parsing, layout analysis, OCR integration

### **Best Practices Applied**
- **Stream-based processing** with intelligent content detection
- **Multi-strategy table detection** for various document types
- **Partial numbering merge** for MasterFormat-style documents
- **Modular converter architecture** with priority-based selection
- **Graceful fallbacks** for optional dependencies

## 🖥️ System Requirements

### Minimum Requirements
- **Python**: 3.13 (la Python di Debian stable, ADR-0099)
- **RAM**: 4GB (8GB+ recommended)
- **CPU**: 2+ cores (4+ cores recommended)
- **Storage**: 2GB free space

### Recommended for Optimal Performance
- **RAM**: 16GB+
- **CPU**: 8+ cores
- **GPU**: NVIDIA GPU with 4GB+ VRAM (RTX series recommended)
- **Storage**: SSD with 10GB+ free space

## 📦 Installation

### Quick Setup (Recommended)
```bash
# Automated setup with dependency management
python setup.py

# Activate environment
source activate.sh  # Linux/macOS
# or
activate.bat        # Windows
```

### Manual Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install optional dependencies
pip install magika easyocr scikit-image numba  # Optional but recommended
```

### System Dependencies

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
Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

## 🚀 Quick Start

### Basic Usage
```bash
# Process PDFs in input directory
python main.py

# Use enhanced processing with verbose output
python run_enhanced.py

# Test enhanced extraction features
python test_enhanced_extraction.py
```

### Stream Processing (New)
```python
from src.stream_converter import convert_pdf_stream
from src.unified_converter import convert_pdf_enhanced

# Stream-based conversion
result = convert_pdf_stream("document.pdf")
print(result.markdown)

# Enhanced conversion with analysis
result = convert_pdf_enhanced("document.pdf")
print(f"Method: {result.extraction_method}, Confidence: {result.confidence}")
```

### Quality Assessment (New)
```python
from src.quality_assessor import assess_extraction_quality

# Assess extraction quality
quality = assess_extraction_quality(markdown_content, metadata)
print(f"Overall Score: {quality.overall_score:.2f}")
print(f"Needs Refinement: {quality.needs_refinement}")
print(f"Recommended Method: {quality.recommended_method}")
```

## 🔍 Enhanced Features v2.1

### Stream-Based Processing (markitdown inspired)
- **Unified Interface**: Handles files, streams, URLs uniformly
- **Content Detection**: Uses magika for intelligent format detection
- **Graceful Fallbacks**: Works without optional dependencies
- **Metadata Preservation**: Rich metadata throughout pipeline

### Enhanced Table Detection
- **Form-Style Detection**: Analyzes word positions for borderless tables
- **Multi-Strategy Approach**: Form → Bordered → ASCII tables
- **Content Classification**: Distinguishes tables from paragraphs
- **Confidence Scoring**: Quality assessment for each detection

### Text Processing Improvements
- **Partial Numbering Merge**: Handles MasterFormat-style documents (`.1`, `.2`)
- **Mathematical Content**: Unicode to LaTeX conversion (α→\alpha, ∫→\int)
- **Header/Footer Removal**: Intelligent pattern detection
- **Encoding Fixes**: Handles ligatures, smart quotes, UTF-8 issues

### Intelligent Method Selection
- **PDF Analysis**: Comprehensive document characteristics detection
- **Strategy Selection**: Optimal method based on PDF properties
- **Fallback Chain**: Multiple methods with confidence scoring
- **Performance Optimization**: Resource-aware processing

## 📊 Project Structure

```
pdf-to-md-engine/
├── src/
│   ├── config.py                     # Configuration management
│   ├── enhanced_processor.py         # Main processing pipeline
│   ├── enhanced_text_extractor.py    # Multi-method text extraction
│   ├── enhanced_table_detector.py    # Form-style table detection
│   ├── stream_converter.py           # Stream-based processing
│   ├── unified_converter.py          # Unified conversion interface
│   ├── pdf_analyzer.py               # PDF characteristics analysis
│   ├── layout_processor.py           # Layout-preserving extraction
│   ├── math_processor.py             # Mathematical content processing
│   ├── enhanced_image_extractor.py   # Advanced image extraction
│   ├── pdf_utilities.py              # Ghostscript integration
│   └── templates/
│       └── chapter.md.j2             # Chapter template
├── data/
│   ├── input/                        # Input PDFs
│   ├── output/                       # Generated markdown
│   └── processing/                   # Temporary files
├── main.py                           # Main entry point
├── run_enhanced.py                   # Enhanced processing script
├── setup.py                          # Automated setup
├── requirements.txt                  # Dependencies
├── README.md                         # This file
├── TROUBLESHOOTING.md                # Troubleshooting guide
├── MARKITDOWN_INTEGRATION.md         # Integration details
└── CHANGELOG.md                      # Version history
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Missing dependencies
pip install -r requirements.txt

# Optional dependencies
pip install magika easyocr scikit-image numba
```

#### 2. OCR Engine Issues
```bash
# Tesseract not found
# Ubuntu: sudo apt install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from GitHub releases

# EasyOCR issues
pip install easyocr opencv-python
```

#### 3. GPU Memory Issues
```bash
# CUDA out of memory
export GPU_MEMORY_LIMIT_GB=2.0
export OCR_GPU_MEMORY_PER_BATCH=1.0
```

#### 4. Performance Optimization

**For Low-Memory Systems (< 8GB RAM)**
```bash
export MEMORY_USAGE_THRESHOLD=70
export MAX_WORKERS=2
export OCR_ENGINE=tesseract
```

**For High-Performance Systems (16GB+ RAM)**
```bash
export CPU_USAGE_THRESHOLD=90
export OCR_BATCH_SIZE=8
export OCR_ENGINE=easyocr
```

### Debug Mode
```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
python main.py

# Test enhanced features
python test_enhanced_extraction.py

# Verify installation
python verify_project.py
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
The `.receipt` file includes:
- PDF characteristics analysis
- Extraction method used and confidence
- Processing performance metrics
- Table detection results
- OCR enhancement details

## 🆕 What's New in v2.1

### Quality Assessment & Iterative Refinement
- **Automatic Quality Scoring** - Comprehensive 4-metric assessment (text, structure, tables, images)
- **Intelligent Refinement** - Applies secondary extraction methods when quality < 75%
- **Quality Improvement Tracking** - Logs before/after scores, only keeps improvements
- **Enhanced Logging** - Shows detailed quality metrics and final rating (EXCELLENT/GOOD/ACCEPTABLE)

### Stream Processing Integration
- Unified interface for files, streams, and URLs
- Intelligent content detection with magika
- Graceful fallbacks for optional dependencies
- Rich metadata preservation

### Enhanced Table Detection
- Form-style table detection for borderless tables
- Multi-strategy approach with confidence scoring
- Better content classification
- Improved markdown formatting

### Text Processing Improvements
- Partial numbering merge for MasterFormat documents
- Mathematical content processing with Unicode conversion
- Better header/footer detection and removal
- Enhanced encoding issue handling

### Architecture Enhancements
- Modular converter architecture
- Priority-based method selection
- Comprehensive PDF analysis
- Resource-aware processing

## 🤝 Contributing

1. Fork the repository
2. Install development dependencies: `python setup.py`
3. Make your changes
4. Test with: `python test_enhanced_extraction.py`
5. Submit a pull request

## 📚 References

- **[pdfmd](https://github.com/VikParuchuri/pdfmd)** - Modular PDF processing pipeline
- **[markitdown](https://github.com/microsoft/markitdown)** - Microsoft's document conversion toolkit
- **[docling](https://github.com/DS4SD/docling)** - IBM's document understanding library
- **[PyMuPDF](https://github.com/pymupdf/PyMuPDF)** - PDF manipulation library
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** - PDF text and table extraction

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run debug mode: `LOG_LEVEL=DEBUG python main.py`
3. Test with: `python test_enhanced_extraction.py`
4. Review `TROUBLESHOOTING.md` for detailed solutions
5. Check system requirements and dependencies