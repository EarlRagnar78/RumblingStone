# Troubleshooting Guide - PDF to Markdown Engine v2.0

## 🔧 Quick Diagnostics

### System Check
```bash
# Check Python version
python --version  # Should be 3.9+

# Check installed packages
pip list | grep -E "(docling|PyMuPDF|pdfplumber|easyocr|pytesseract)"

# Test enhanced extraction
python test_enhanced_extraction.py
```

### Resource Check
```bash
# Check system resources
python -c "
from src.enhanced_processor import SystemResourceManager
rm = SystemResourceManager()
print(f'CPU: {rm.cpu_count} cores')
print(f'RAM: {rm.total_memory:.1f}GB')
print(f'GPU: {rm.gpu_info}')
"
```

## 🚨 Common Issues & Solutions

### 1. Installation Issues

#### Missing Dependencies
```bash
# Error: ModuleNotFoundError: No module named 'fitz'
pip install PyMuPDF

# Error: ModuleNotFoundError: No module named 'pdfplumber'
pip install pdfplumber

# Error: ModuleNotFoundError: No module named 'docling'
pip install docling>=2.0.0
```

#### System Dependencies
```bash
# Ubuntu/Debian - Missing system libraries
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng
sudo apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1

# macOS - Tesseract not found
brew install tesseract

# Windows - Tesseract not in PATH
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add installation directory to PATH
```

### 2. Text Extraction Issues

#### Poor Text Quality
```bash
# Symptoms: Garbled text, encoding issues, missing characters
# Solution: Enhanced engine automatically detects and fixes these

# Check text quality analysis
python -c "
from src.enhanced_text_extractor import extract_pdf_text_hybrid
text, analysis = extract_pdf_text_hybrid('data/input/your_file.pdf')
print(f'Text quality: {analysis.get(\"text_quality\", 0):.2f}')
print(f'Needs OCR: {analysis.get(\"needs_ocr_enhancement\", False)}')
"
```

#### No Text Extracted
```bash
# Symptoms: Empty or very short text output
# Possible causes:
# 1. PDF is image-based (scanned document)
# 2. Text layer is corrupted
# 3. Unusual encoding

# Check if PDF has text layer
python -c "
import fitz
doc = fitz.open('data/input/your_file.pdf')
page = doc[0]
text = page.get_text()
print(f'First page text length: {len(text)}')
print(f'Has text layer: {len(text) > 50}')
"

# Force OCR processing
export OCR_ENGINE=easyocr
python run_enhanced.py
```

#### Encoding Problems
```bash
# Symptoms: Strange characters like ﬁ, ", ", –
# Solution: Enhanced engine includes automatic encoding fixes

# Test encoding fixes
python -c "
from src.enhanced_text_extractor import clean_extracted_text
test_text = 'This is a ﬁle with "smart quotes" and – dashes'
cleaned = clean_extracted_text(test_text)
print(f'Original: {test_text}')
print(f'Cleaned:  {cleaned}')
"
```

### 3. Chapter Detection Issues

#### No Chapters Detected
```bash
# Symptoms: Single large markdown file instead of chapters
# Check PDF outline
python -c "
from src.enhanced_text_extractor import extract_pdf_outline_enhanced
outline = extract_pdf_outline_enhanced('data/input/your_file.pdf')
print(f'Outline entries: {len(outline)}')
for entry in outline[:5]:
    print(f'  {entry[\"level\"]} - {entry[\"title\"]}')
"

# If no outline, check for text patterns
python -c "
import re
with open('data/output/your_file/01_*.md', 'r') as f:
    text = f.read()
chapters = re.findall(r'^(CHAPTER \\d+.*|Chapter \\d+.*)', text, re.MULTILINE)
print(f'Found chapter patterns: {len(chapters)}')
"
```

#### Wrong Chapter Splits
```bash
# Symptoms: Chapters split at wrong locations
# Solution: PDF outline provides most accurate splits

# Check outline quality
python -c "
from src.enhanced_text_extractor import extract_pdf_outline_enhanced
outline = extract_pdf_outline_enhanced('data/input/your_file.pdf')
for entry in outline:
    print(f'Level {entry[\"level\"]}: {entry[\"title\"]} (page {entry.get(\"page\", \"?\")})') 
"
```

### 4. OCR Issues

#### EasyOCR Not Working
```bash
# Error: EasyOCR not available
pip install easyocr opencv-python

# GPU memory issues
export OCR_ENGINE=tesseract
# OR
export GPU_MEMORY_LIMIT_GB=2.0

# Language issues
export OCR_LANGUAGES=en,es,fr  # Add your languages
```

#### Tesseract Not Working
```bash
# Error: TesseractNotFoundError
# Ubuntu/Debian:
sudo apt install tesseract-ocr tesseract-ocr-eng

# macOS:
brew install tesseract

# Windows:
# Download and install from GitHub
# Add to PATH: C:\Program Files\Tesseract-OCR

# Test Tesseract
tesseract --version
```

#### Poor OCR Results
```bash
# Low confidence scores
export OCR_CONFIDENCE_THRESHOLD=0.5  # Lower threshold

# Wrong language detection
export OCR_LANGUAGES=en  # Specify exact language

# Test OCR on sample image
python -c "
import easyocr
reader = easyocr.Reader(['en'])
result = reader.readtext('path/to/test/image.png')
for detection in result:
    print(f'Text: {detection[1]}, Confidence: {detection[2]:.2f}')
"
```

### 5. Performance Issues

#### Slow Processing
```bash
# Check system load
htop  # Linux/macOS
# Task Manager on Windows

# Reduce workers
export MAX_WORKERS=2

# Disable GPU if causing issues
export USE_GPU=false

# Use lighter OCR
export OCR_ENGINE=tesseract
```

#### Memory Issues
```bash
# Error: Out of memory
export MEMORY_USAGE_THRESHOLD=60
export MAX_WORKERS=1

# For large PDFs, process in smaller batches
# Split PDF first or process pages individually
```

#### GPU Issues
```bash
# CUDA out of memory
export GPU_MEMORY_LIMIT_GB=1.0
export OCR_GPU_MEMORY_PER_BATCH=0.5

# GPU not detected
python -c "
import torch
print(f'CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'GPU: {torch.cuda.get_device_name(0)}')
    print(f'Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB')
"
```

### 6. File System Issues

#### Permission Errors
```bash
# Error: Permission denied
chmod +x main.py run_enhanced.py
sudo chown -R $USER:$USER ./data/

# Windows: Run as Administrator or check folder permissions
```

#### Path Issues
```bash
# Error: File not found
# Check paths in .env file
cat .env

# Verify input directory
ls -la data/input/

# Create missing directories
mkdir -p data/input data/output data/processing
```

## 🔍 Advanced Debugging

### Enable Debug Logging
```bash
# Set debug level
export LOG_LEVEL=DEBUG
python run_enhanced.py

# Or modify .env file
echo "LOG_LEVEL=DEBUG" >> .env
```

### Test Individual Components
```bash
# Test text extraction only
python -c "
from src.enhanced_text_extractor import extract_pdf_text_hybrid
text, analysis = extract_pdf_text_hybrid('data/input/test.pdf')
print(f'Extracted {len(text)} characters')
print(f'Analysis: {analysis}')
"

# Test chapter detection
python -c "
from src.enhanced_processor import detect_chapter_structure
from src.enhanced_text_extractor import extract_pdf_outline_enhanced
outline = extract_pdf_outline_enhanced('data/input/test.pdf')
chapters = detect_chapter_structure('sample text', outline)
print(f'Detected {len(chapters)} chapters')
"

# Test OCR engine
python -c "
from src.enhanced_processor import EnhancedOCREngine, SystemResourceManager
rm = SystemResourceManager()
ocr = EnhancedOCREngine('easyocr', rm)
print(f'OCR engine: {ocr.engine_type}')
"
```

### Performance Profiling
```bash
# Time the processing
time python run_enhanced.py

# Memory usage monitoring
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1e6:.1f}MB')
"
```

## 🛠️ Configuration Tuning

### For Different System Types

#### Low-End Systems (< 8GB RAM, < 4 cores)
```bash
# .env settings
MAX_WORKERS=1
MEMORY_USAGE_THRESHOLD=60
CPU_USAGE_THRESHOLD=70
OCR_ENGINE=tesseract
USE_GPU=false
OCR_BATCH_SIZE=1
```

#### Mid-Range Systems (8-16GB RAM, 4-8 cores)
```bash
# .env settings
MAX_WORKERS=4
MEMORY_USAGE_THRESHOLD=75
CPU_USAGE_THRESHOLD=80
OCR_ENGINE=auto
USE_GPU=auto
OCR_BATCH_SIZE=4
```

#### High-End Systems (16GB+ RAM, 8+ cores, GPU)
```bash
# .env settings
MAX_WORKERS=8
MEMORY_USAGE_THRESHOLD=85
CPU_USAGE_THRESHOLD=90
OCR_ENGINE=easyocr
USE_GPU=true
OCR_BATCH_SIZE=8
GPU_MEMORY_LIMIT_GB=4.0
```

## 📞 Getting Help

### Before Reporting Issues
1. Run `python test_enhanced_extraction.py`
2. Check system requirements
3. Enable debug logging
4. Try with a simple PDF first
5. Check the troubleshooting steps above

### Information to Include
- Python version: `python --version`
- System info: OS, RAM, CPU, GPU
- Error messages (full traceback)
- PDF characteristics (size, type, source)
- Configuration settings (.env file)
- Debug logs

### Test Files
Create a minimal test case:
```bash
# Test with a simple PDF
python -c "
import fitz
doc = fitz.new()
page = doc.new_page()
page.insert_text((100, 100), 'Test Chapter 1\\nThis is test content.')
doc.save('test_simple.pdf')
doc.close()
"

# Process the test file
python run_enhanced.py
```