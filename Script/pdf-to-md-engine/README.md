# PDF to Markdown Engine

A high-performance PDF processing engine that converts PDFs to structured Markdown with intelligent resource management.

## Features

- **Multi-core CPU processing** with automatic core detection (leaves 2 cores for system)
- **GPU acceleration** support (CUDA) with memory management
- **Advanced OCR engines** (EasyOCR, RapidOCR, Tesseract)
- **Parallel image processing** and chapter generation
- **Smart resource allocation** to prevent system exhaustion
- **Idempotent processing** with hash-based change detection

## Project Structure

```
pdf-to-md-engine/
├── .env                    # Environment variables and performance settings
├── pyproject.toml         # Modern dependency management with OCR engines
├── README.md
├── DEPLOYMENT.md          # Detailed deployment instructions
├── src/
│   ├── config.py          # Smart resource management settings
│   ├── processor.py       # Multi-threaded processing with GPU support
│   ├── utils.py           # File operations and utilities
│   └── templates/
│       └── chapter.md.j2  # Jinja2 template for output
├── data/
│   ├── input/             # Drop your PDFs here
│   ├── processing/        # Temporary processing folder
│   └── output/            # Generated Markdown and assets
└── main.py               # Entry point
```

## Performance Features

- **CPU**: Uses all available cores minus 2 (configurable)
- **GPU**: Automatic CUDA detection with 2GB memory reservation for OS
- **Memory**: Smart allocation prevents system resource exhaustion
- **OCR**: Multiple engines with GPU acceleration when available

## Quick Start

1. Place PDFs in `data/input/`
2. Run `python main.py`
3. Find processed Markdown in `data/output/`