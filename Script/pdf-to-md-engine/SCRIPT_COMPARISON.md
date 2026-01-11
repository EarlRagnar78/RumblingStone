# Script Comparison - PDF to Markdown Engine

## 📄 **main.py vs run_enhanced.py**

Both scripts are **functionally identical** - they both use the enhanced processor. The difference is only in presentation:

### **main.py** (Simple)
```python
from src.enhanced_processor import process_pdf

def main():
    pdfs = list(settings.INPUT_DIR.glob("*.pdf"))
    for pdf in pdfs:
        process_pdf(pdf)
```

### **run_enhanced.py** (Verbose)
```python
from src.enhanced_processor import process_pdf

def main():
    logger.info("🚀 Enhanced PDF processing starting...")
    logger.info("🔧 Features: Enhanced text extraction, OCR enhancement, better chapter detection")
    
    for pdf in pdfs:
        logger.info(f"📄 Processing: {pdf.name}")
        process_pdf(pdf)
        logger.success(f"✅ Completed: {pdf.name}")
```

**Result**: Both produce identical output, `run_enhanced.py` just has more emoji and status messages.

---

## 🔍 **Chapter Detection Issue**

Your PDF has **11 outline entries** but only **2 chapters** were created. This suggests:

1. **Outline structure problem** - The outline entries might be nested or have different levels
2. **Content matching issue** - The algorithm can't find content for each outline entry

### **Expected Structure:**
- Introduction
- Chapter 1, 2, 3, 4, 5
- Appendix I, II
- Web Enhancement

### **Current Result:**
- Only 2 chapters detected from 11 outline entries

---

## 🖼️ **Image Extraction Issue**

**Problem**: When using text layer (high quality text), image extraction was skipped.

**Fix Applied**: Now always extracts images using either:
1. **Docling method** (if using docling conversion)
2. **Direct PDF extraction** (using PyMuPDF when using text layer)

---

## 🔧 **Fixes Applied:**

1. **Enhanced Chapter Detection**: Now creates one chapter per outline entry
2. **Always Extract Images**: Images extracted even with good text layer
3. **Better Content Matching**: Improved algorithm to find content for each chapter

---

## 🚀 **Test the Fixes:**

```bash
# Clear previous output
rm -rf data/output/adventure-redhandofdoom06-12-ocr/

# Run with fixes
python run_enhanced.py
```

**Expected Results:**
- ✅ **11 chapters** (one per outline entry)
- ✅ **Images extracted** from PDF
- ✅ **Better chapter organization**