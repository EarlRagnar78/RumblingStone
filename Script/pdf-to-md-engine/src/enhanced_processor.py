import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

import datetime
import re
import os
import time
import psutil
import torch
import gc
import platform
import sys
sys.path.insert(0, '/home/jfs/.local/lib/python3.14/site-packages')
import fitz  # PyMuPDF for text extraction
from pathlib import Path
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from typing import Optional, Tuple, Dict, Any, List

# Performance optimizations
try:
    import numba
    from scipy import ndimage
    from skimage import filters, morphology
    PERFORMANCE_LIBS_AVAILABLE = True
except ImportError:
    PERFORMANCE_LIBS_AVAILABLE = False
    logger.warning("Performance libraries not available")

from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# OCR imports with fallback handling
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    logger.warning("EasyOCR not available")

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("Tesseract not available")

from src.config import settings
from src.utils import get_file_hash, clean_filename
from src.pdf_utilities import PDFUtilities
from src.enhanced_text_transformer import transform_text_enhanced
from src.enhanced_table_detector import detect_tables_enhanced, format_table_markdown
from src.enhanced_text_extractor import (
    extract_pdf_text_hybrid, 
    extract_pdf_outline_enhanced,
    should_use_ocr_enhancement,
    clean_extracted_text
)
from src.layout_processor import extract_pdf_with_layout
from src.enhanced_image_extractor import extract_images_enhanced
from src.pdf_analyzer import analyze_pdf_characteristics, get_extraction_strategy
from src.math_processor import process_enhanced_text
from src.quality_assessor import assess_extraction_quality, QualityMetrics

# Markitdown-inspired text processing
def _merge_partial_numbering_lines(text: str) -> str:
    """Merge MasterFormat-style partial numbering with following text"""
    import re
    partial_pattern = re.compile(r"^\.\d+$")
    lines = text.split("\n")
    result_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if partial_pattern.match(stripped):
            # Look for next non-empty line to merge
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            
            if j < len(lines):
                next_line = lines[j].strip()
                result_lines.append(f"{stripped} {next_line}")
                i = j + 1
            else:
                result_lines.append(line)
                i += 1
        else:
            result_lines.append(line)
            i += 1
    
    return "\n".join(result_lines)

# Initialize Jinja2
template_env = Environment(loader=FileSystemLoader("src/templates"))
template = template_env.get_template("chapter.md.j2")

def extract_images_from_pdf(pdf_path: Path, assets_dir: Path) -> Tuple[List[Path], Dict]:
    """Extract images directly from PDF using PyMuPDF with colorspace handling"""
    saved_images = []
    image_info = {}
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Handle colorspace conversion
                    if pix.n - pix.alpha > 3:  # CMYK or other complex colorspace
                        # Convert to RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    elif pix.n - pix.alpha == 1:  # Grayscale
                        # Convert to RGB for consistency
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Only save quality images
                    if pix.width > 50 and pix.height > 50:
                        image_path = assets_dir / f"page_{page_num:03d}_img_{img_index:03d}.png"
                        
                        # Use tobytes for better format control
                        img_data = pix.tobytes("png")
                        with open(image_path, "wb") as f:
                            f.write(img_data)
                        
                        saved_images.append(image_path)
                        image_info[str(image_path)] = {
                            'path': image_path,
                            'page': page_num,
                            'index': img_index,
                            'width': pix.width,
                            'height': pix.height
                        }
                    
                    pix = None
                    
                except Exception as e:
                    logger.debug(f"Skipped image {img_index} from page {page_num}: {e}")
                    continue
        
        doc.close()
        
    except Exception as e:
        logger.error(f"Failed to extract images from PDF: {e}")
    
    return saved_images, image_info

def extract_pdf_text_layer_enhanced(pdf_path: Path) -> Tuple[str, bool, Dict]:
    """Enhanced text extraction with quality analysis"""
    text, analysis = extract_pdf_text_hybrid(pdf_path)
    
    has_text_layer = analysis.get("has_text_layer", False)
    needs_ocr = should_use_ocr_enhancement(pdf_path)
    
    logger.info(f"Text extraction: {len(text)} chars, quality: {analysis.get('text_quality', 0):.2f}")
    if needs_ocr:
        logger.info("Text quality issues detected - OCR enhancement recommended")
    
    return text, has_text_layer, analysis

def detect_chapter_structure(text: str, outline: List[Dict] = None) -> List[str]:
    """Enhanced chapter detection using multiple methods"""
    
    # Method 1: Use PDF outline if available
    if outline:
        logger.info(f"Using PDF outline with {len(outline)} entries")
        return split_by_outline_enhanced(text, outline)
    
    # Method 2: Pattern-based detection
    chapter_patterns = [
        r'^(# .+)$',  # Markdown headers
        r'^(## .+)$',  # Level 2 headers
        r'^([A-Z][A-Z ]{10,})$',  # ALL CAPS headers
        r'^(CHAPTER \d+.*)$',  # Chapter numbering
        r'^(Chapter \d+.*)$',  # Chapter numbering (title case)
        r'^(PART [IVX]+.*)$',  # Part numbering
        r'^(Part [IVX]+.*)$',  # Part numbering (title case)
        r'^(APPENDIX [A-Z]+.*)$',  # Appendix
        r'^(Appendix [A-Z]+.*)$',  # Appendix (title case)
        r'^(Web Enhancement.*)$',  # Web enhancements
    ]
    
    for pattern in chapter_patterns:
        chapters = re.split(pattern, text, flags=re.MULTILINE)
        if len(chapters) > 3:  # Found meaningful splits
            logger.info(f"Found {len(chapters)//2} chapters using pattern: {pattern}")
            return format_chapter_splits(chapters)
    
    # Method 3: Page break detection
    chapters = re.split(r'\n\s*\n\s*\n\s*\n', text)  # Multiple line breaks
    if len(chapters) > 5:
        logger.info(f"Split into {len(chapters)} sections by page breaks")
        return chapters
    
    # Method 4: Keep as single document
    logger.info("No clear chapter structure found - keeping as single document")
    return [text]

def split_by_outline_enhanced(text: str, outline: List[Dict]) -> List[str]:
    """Split text using enhanced PDF outline"""
    if not outline:
        return [text]
    
    chapters = []
    text_lines = text.split('\n')
    total_lines = len(text_lines)
    
    # Split text proportionally based on outline entries
    for i, bookmark in enumerate(outline):
        title = bookmark['title']
        level = bookmark['level']
        
        # Create markdown header
        header = f"{'#' * min(level, 6)} {title}"
        
        # Calculate content range for this chapter
        start_pos = i * total_lines // len(outline)
        end_pos = (i + 1) * total_lines // len(outline)
        
        # Extract content for this chapter
        chapter_lines = text_lines[start_pos:end_pos]
        
        # Build chapter content
        chapter_content = f"{header}\n\n"
        if chapter_lines:
            chapter_content += '\n'.join(chapter_lines)
        
        chapters.append(chapter_content)
    
    return chapters if chapters else [text]

def extract_content_between_markers(text: str, start_marker: str, end_marker: str) -> str:
    """Extract content between two markers (simplified implementation)"""
    # This is a basic implementation - you might need more sophisticated logic
    lines = text.split('\n')
    content_lines = []
    capturing = False
    
    for line in lines:
        if start_marker.lower() in line.lower():
            capturing = True
            continue
        elif end_marker.lower() in line.lower():
            break
        elif capturing:
            content_lines.append(line)
    
    return '\n'.join(content_lines)

def extract_content_from_marker(text: str, start_marker: str) -> str:
    """Extract content from marker to end"""
    lines = text.split('\n')
    content_lines = []
    capturing = False
    
    for line in lines:
        if start_marker.lower() in line.lower():
            capturing = True
            continue
        elif capturing:
            content_lines.append(line)
    
    return '\n'.join(content_lines)

def format_chapter_splits(chapters: List[str]) -> List[str]:
    """Format chapter splits from regex results"""
    formatted = []
    
    for i in range(0, len(chapters), 2):
        if i + 1 < len(chapters):
            header = chapters[i].strip()
            content = chapters[i + 1].strip()
            
            if header and content:
                # Ensure header is properly formatted
                if not header.startswith('#'):
                    header = f"# {header}"
                
                formatted.append(f"{header}\n\n{content}")
    
    return formatted if formatted else chapters

class EnhancedOCREngine:
    """Enhanced OCR with text layer improvement capabilities"""
    
    def __init__(self, engine_type: str, resource_manager):
        self.engine_type = engine_type
        self.resource_manager = resource_manager
        self.ocr_reader = None
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Initialize OCR engine with better error handling"""
        if self.engine_type == "easyocr" and EASYOCR_AVAILABLE:
            try:
                gpu_enabled = False
                if self.resource_manager.gpu_info["memory_gb"] > 6:
                    gpu_enabled = self.resource_manager.should_use_gpu(2.0)
                
                self.ocr_reader = easyocr.Reader(
                    settings.OCR_LANGUAGES.split(','),
                    gpu=gpu_enabled
                )
                # Compact RNN weights to prevent memory fragmentation
                if hasattr(self.ocr_reader, 'recognizer') and hasattr(self.ocr_reader.recognizer, 'model'):
                    for module in self.ocr_reader.recognizer.model.modules():
                        if hasattr(module, 'flatten_parameters'):
                            module.flatten_parameters()
                logger.info(f"EasyOCR initialized (GPU: {gpu_enabled})")
            except Exception as e:
                logger.error(f"EasyOCR initialization failed: {e}")
                self.engine_type = "tesseract"
        
        if self.engine_type == "tesseract" and TESSERACT_AVAILABLE:
            try:
                pytesseract.get_tesseract_version()
                logger.info("Tesseract OCR initialized")
            except Exception as e:
                logger.error(f"Tesseract initialization failed: {e}")
                self.engine_type = "none"
    
    def enhance_text_with_ocr(self, text: str, pdf_path: Path) -> str:
        """Enhance existing text layer with OCR for problematic areas"""
        if self.engine_type == "none":
            return text
        
        # Identify problematic text areas (garbled characters, etc.)
        problematic_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if self._is_problematic_text(line):
                problematic_lines.append(i)
        
        if not problematic_lines:
            logger.info("No problematic text areas found")
            return text
        
        logger.info(f"Found {len(problematic_lines)} problematic text lines to enhance with OCR")
        
        # For now, return the cleaned text
        # In a full implementation, you'd extract images from those areas and OCR them
        return clean_extracted_text(text)
    
    def _is_problematic_text(self, text: str) -> bool:
        """Detect if text line has encoding/OCR issues"""
        if not text.strip():
            return False
        
        # Check for high ratio of non-ASCII characters
        non_ascii = sum(1 for c in text if ord(c) > 127)
        if len(text) > 0 and non_ascii / len(text) > 0.3:
            return True
        
        # Check for common OCR artifacts
        ocr_artifacts = ['�', '□', '■', '▪', '▫']
        if any(artifact in text for artifact in ocr_artifacts):
            return True
        
        # Check for excessive punctuation or symbols
        punct_ratio = sum(1 for c in text if not c.isalnum() and not c.isspace()) / len(text)
        if punct_ratio > 0.5:
            return True
        
        return False

def process_pdf_enhanced(pdf_path: Path):
    """Enhanced PDF processing with better text extraction and chapter detection"""
    # Import resource management classes locally to avoid circular imports
    import gc
    import time
    import json
    import shutil
    
    class ProgressTracker:
        def __init__(self, total_steps):
            self.total_steps = total_steps
            self.current_step = 0
            self.start_time = time.time()
        
        def start_step(self, name):
            self.current_step += 1
            logger.info(f"Step {self.current_step}/{self.total_steps}: {name}")
        
        def complete_step(self):
            pass
    
    class SystemResourceManager:
        def __init__(self):
            self.cpu_count = psutil.cpu_count()
            self.total_memory = psutil.virtual_memory().total / (1024**3)
            self.gpu_info = self._detect_gpu()
            self.optimal_ocr_engine = self._select_ocr_engine()
        
        def _detect_gpu(self):
            try:
                if torch.cuda.is_available():
                    return {
                        "available": True,
                        "name": torch.cuda.get_device_name(0),
                        "memory_gb": torch.cuda.get_device_properties(0).total_memory / 1e9
                    }
            except:
                pass
            return {"available": False, "name": "None", "memory_gb": 0}
        
        def _select_ocr_engine(self):
            # Priority: Layout processor > EasyOCR > Tesseract > None
            return "layout_first"  # Always try layout preservation first
        
        def should_use_gpu(self, memory_gb_needed):
            return (self.gpu_info["available"] and 
                   self.gpu_info["memory_gb"] > memory_gb_needed)
        
        def cleanup_gpu_memory(self):
            if self.gpu_info["available"]:
                torch.cuda.empty_cache()
                gc.collect()
        
        def monitor_resources(self):
            """Monitor current system resource usage"""
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'should_throttle': cpu_percent > 85 or memory.percent > 80
            }
        
        def adaptive_sleep(self, base_delay=0.1):
            """Adaptive sleep based on system load"""
            resources = self.monitor_resources()
            if resources['should_throttle']:
                sleep_time = base_delay * (1 + resources['cpu_percent'] / 100)
                time.sleep(min(sleep_time, 2.0))  # Cap at 2 seconds
    
    # Initialize systems
    progress = ProgressTracker(9)  # Added quality assessment step
    resource_manager = SystemResourceManager()
    
    # Step 1: Hash Check & Setup
    progress.start_step("Hash Check & Setup")
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    available_gb = psutil.virtual_memory().available / (1024**3)
    logger.info(f"Initial state - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%, Available: {available_gb:.1f}GB")
    
    # Enhanced PDF validation
    if not PDFUtilities.validate_pdf(pdf_path):
        logger.error(f"Invalid PDF file: {pdf_path}")
        return
    
    file_hash = PDFUtilities.get_pdf_checksum(pdf_path)
    page_count = PDFUtilities.get_page_count(pdf_path)
    logger.info(f"PDF: {page_count} pages, checksum: {file_hash}")
    safe_name = clean_filename(pdf_path.stem)
    pdf_output_dir = settings.OUTPUT_DIR / safe_name
    assets_dir = pdf_output_dir / "assets"
    
    receipt_file = pdf_output_dir / ".receipt"
    if receipt_file.exists() and not settings.OVERWRITE_EXISTING:
        with open(receipt_file, "r") as f:
            import json
            stored_data = json.loads(f.read())
        if stored_data.get("file_hash") == file_hash:
            logger.info(f"Skipping {pdf_path.name} (Unchanged)")
            return

    if pdf_output_dir.exists():
        import shutil
        shutil.rmtree(pdf_output_dir)
    pdf_output_dir.mkdir(parents=True)
    assets_dir.mkdir()
    
    progress.complete_step()
    
    # Step 2: PDF Analysis & Strategy Selection
    progress.start_step("PDF Analysis & Strategy Selection")
    
    # Comprehensive PDF analysis
    pdf_characteristics = analyze_pdf_characteristics(pdf_path)
    extraction_strategy = get_extraction_strategy(pdf_characteristics)
    
    logger.info(f"📋 PDF Analysis Results:")
    logger.info(f"   Version: {pdf_characteristics.version}")
    logger.info(f"   Pages: {pdf_characteristics.page_count}")
    logger.info(f"   Text Layer: {pdf_characteristics.has_text_layer}")
    logger.info(f"   Scanned: {pdf_characteristics.is_scanned}")
    logger.info(f"   Tables: {pdf_characteristics.table_count}")
    logger.info(f"   Creation: {pdf_characteristics.creation_method}")
    logger.info(f"   Standard: {pdf_characteristics.pdf_standard}")
    logger.info(f"   Optimal Method: {pdf_characteristics.optimal_extraction_method} (confidence: {pdf_characteristics.extraction_confidence:.2f})")
    
    # Extract PDF outline first
    pdf_outline = extract_pdf_outline_enhanced(pdf_path)
    
    # Enhanced text extraction
    extracted_text, has_text_layer, text_analysis = extract_pdf_text_layer_enhanced(pdf_path)
    
    # Initialize enhanced OCR engine
    ocr_engine = EnhancedOCREngine(resource_manager.optimal_ocr_engine, resource_manager)
    
    progress.complete_step()
    
    # Step 3: Intelligent Method Selection & Text Enhancement
    progress.start_step("Intelligent Method Selection & Text Enhancement")
    
    # Use PDF characteristics to select optimal method
    extraction_method = pdf_characteristics.optimal_extraction_method
    
    if extraction_method == "layout_preserving" and has_text_layer:
        # Method 1: Layout-preserving extraction (BEST for structured documents)
        layout_text = extract_pdf_with_layout(pdf_path)
        if layout_text and len(layout_text) > 1000:  # Meaningful content
            # Apply enhanced transformations and processing
            layout_text = transform_text_enhanced(layout_text)
            full_md = process_enhanced_text(layout_text)
            logger.info(f"✅ Using layout-preserving extraction: {len(full_md)} characters")
        else:
            # Fallback to next best method
            extraction_method = extraction_strategy['fallback_methods'][0]
            logger.info(f"Layout extraction insufficient, falling back to {extraction_method}")
    
    if extraction_method == "enhanced_text" and has_text_layer:
        # Method 2: Enhanced text extraction (GOOD for text-heavy documents)
        if text_analysis.get("needs_ocr_enhancement", False):
            enhanced_text = ocr_engine.enhance_text_with_ocr(extracted_text, pdf_path)
        else:
            enhanced_text = clean_extracted_text(extracted_text)
        
        # Apply enhanced transformations and processing
        enhanced_text = transform_text_enhanced(enhanced_text)
        full_md = process_enhanced_text(enhanced_text)
        logger.info(f"✅ Using enhanced text extraction: {len(full_md)} characters")
        doc = None  # Skip docling conversion
    
    elif extraction_method == "docling_conversion" or not has_text_layer:
        # Method 3: Docling conversion (GOOD for complex layouts)
        logger.info(f"Using docling conversion (reason: {extraction_method})")
        
        def setup_converter(resource_manager):
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = pdf_characteristics.is_scanned
            pipeline_options.do_table_structure = pdf_characteristics.table_count > 0
            
            return DocumentConverter(
                format_options={
                    InputFormat.PDF: pipeline_options
                }
            )
        
        gc.collect()
        if resource_manager.gpu_info["available"]:
            torch.cuda.empty_cache()
        
        converter = setup_converter(resource_manager)
        
        with tqdm(desc="Converting PDF", unit="page") as pbar:
            try:
                result = converter.convert(pdf_path)
                doc = result.document
                full_md = doc.export_to_markdown()
                # Apply markitdown-inspired post-processing
                full_md = _merge_partial_numbering_lines(full_md)
                pbar.update(1)
            except Exception as e:
                logger.error(f"PDF conversion failed: {e}")
                # Final fallback to OCR
                extraction_method = "ocr_primary"
                full_md = "# OCR Processing Required\n\nDocument requires OCR processing."
                doc = None
        
        if 'converter' in locals():
            del converter
        gc.collect()
    
    else:
        # Method 4: OCR Primary (for scanned documents)
        logger.info("Using OCR primary method for scanned document")
        extraction_method = "ocr_primary"
        full_md = "# Scanned Document\n\nProcessing with OCR..."
        doc = None
    
    progress.complete_step()
    
    # Step 4: Enhanced Chapter Detection
    progress.start_step("Chapter Detection")
    
    chapters = detect_chapter_structure(full_md, pdf_outline)
    logger.info(f"Detected {len(chapters)} chapters/sections")
    
    progress.complete_step()
    
    # Step 5: Image Processing (always extract images for completeness)
    progress.start_step("Image Processing")
    
    # Always try to extract images, even when using text layer
    if doc is not None:
        # Helper function for image processing
        def save_image_element(element, image_path):
            """Save individual image element"""
            try:
                element.image.save(image_path)
                return True
            except Exception as e:
                logger.error(f"Error saving image to {image_path}: {e}")
                return False
        
        def process_images_parallel(doc, assets_dir, resource_manager, progress):
            """Process images from docling document with parallel processing"""
            saved_images = []
            image_info = {}
            
            # Extract all images from document
            images_to_process = []
            for element in doc.texts:
                if hasattr(element, 'image') and element.image:
                    images_to_process.append(element)
            
            if not images_to_process:
                return saved_images, image_info
            
            # Process images with threading for I/O operations
            max_workers = min(4, len(images_to_process))
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_element = {}
                
                for i, element in enumerate(images_to_process):
                    image_path = assets_dir / f"img_{i:03d}.png"
                    future = executor.submit(save_image_element, element, image_path)
                    future_to_element[future] = (element, image_path)
                
                for future in as_completed(future_to_element):
                    element, image_path = future_to_element[future]
                    try:
                        success = future.result()
                        if success:
                            saved_images.append(image_path)
                            image_info[str(image_path)] = {
                                'path': image_path,
                                'element': element,
                                'bbox': getattr(element, 'bbox', None),
                                'page': getattr(element, 'page', 0)
                            }
                    except Exception as e:
                        logger.warning(f"Failed to save image {image_path}: {e}")
            
            return saved_images, image_info
        
        saved_images, image_info = process_images_parallel(doc, assets_dir, resource_manager, progress)
        gc.collect()
    else:
        # Use enhanced image extraction
        extracted_images, image_markdown = extract_images_enhanced(pdf_path, assets_dir)
        saved_images = [img.path for img in extracted_images]
        image_info = {str(img.path): {
            'path': img.path,
            'bbox': img.bbox,
            'page': img.page_num,
            'type': img.image_type,
            'width': img.width,
            'height': img.height
        } for img in extracted_images}
    
    logger.info(f"Extracted {len(saved_images)} images")
    
    progress.complete_step()
    
    # Step 6: Smart OCR Processing (Text Only)
    progress.start_step("Smart OCR Processing (Text Only)")
    
    # Only extract TEXT from images, not save images
    ocr_text_results = {}
    
    if extraction_method != "layout_preserving" and image_info:
        # OCR for text extraction only when layout preservation failed
        def extract_text_from_image_ocr(image_path, ocr_engine):
            """Extract only text from image, don't save image"""
            try:
                if ocr_engine.engine_type == "easyocr" and ocr_engine.ocr_reader:
                    results = ocr_engine.ocr_reader.readtext(str(image_path))
                    
                    # Extract text with position for layout preservation
                    text_blocks = []
                    for (bbox, text, confidence) in results:
                        if confidence > 0.6 and len(text.strip()) > 2:
                            y_pos = bbox[0][1]
                            x_pos = bbox[0][0]
                            text_blocks.append((y_pos, x_pos, text.strip()))
                    
                    # Sort by position (top-to-bottom, left-to-right)
                    text_blocks.sort(key=lambda x: (x[0], x[1]))
                    
                    # Combine text preserving layout
                    combined_text = '\n'.join([block[2] for block in text_blocks])
                    avg_confidence = sum(r[2] for r in results) / len(results) if results else 0
                    
                    return combined_text, avg_confidence
                
                elif ocr_engine.engine_type == "tesseract":
                    from PIL import Image
                    img = Image.open(image_path)
                    text = pytesseract.image_to_string(img, config='--psm 6')
                    confidence = 0.8 if len(text.strip()) > 10 else 0.5
                    return text.strip(), confidence
                
                return "", 0.0
                
            except Exception as e:
                logger.error(f"OCR text extraction failed for {image_path}: {e}")
                return "", 0.0
        
        # Process OCR for text extraction only
        for image_path in list(image_info.keys())[:5]:  # Limit to first 5 images
            ocr_text, confidence = extract_text_from_image_ocr(image_path, ocr_engine)
            if ocr_text and confidence > 0.6:
                ocr_text_results[image_path] = {
                    'text': ocr_text,
                    'confidence': confidence,
                    'method': ocr_engine.engine_type
                }
        
        logger.info(f"Extracted text from {len(ocr_text_results)} images via OCR")
    else:
        logger.info(f"Skipping OCR - using {extraction_method} method")
    
    progress.complete_step()
    
    # Step 8: Quality Assessment & Refinement
    progress.start_step("Quality Assessment & Refinement")
    
    # Assess quality of extracted content
    combined_content = "\n\n".join([chapter_content for chapter_content in chapters])
    quality_metrics = assess_extraction_quality(combined_content, {
        'pdf_characteristics': {
            'page_count': pdf_characteristics.page_count,
            'has_images': pdf_characteristics.has_images,
        },
        'text_analysis': text_analysis,
        'extraction_strategy': {'method_used': extraction_method},
        'ocr_text_results': len(ocr_text_results)
    })
    
    logger.info(f"📊 Quality Assessment:")
    logger.info(f"   Overall Score: {quality_metrics.overall_score:.2f}")
    logger.info(f"   Text: {quality_metrics.text_completeness:.2f}, Structure: {quality_metrics.structure_preservation:.2f}")
    logger.info(f"   Tables: {quality_metrics.table_quality:.2f}, Images: {quality_metrics.image_coverage:.2f}")
    
    # Apply refinement if needed
    if quality_metrics.needs_refinement and quality_metrics.recommended_method:
        logger.info(f"🔄 Quality below threshold ({quality_metrics.overall_score:.2f} < 0.75)")
        logger.info(f"   Applying refinement with: {quality_metrics.recommended_method}")
        
        # Apply secondary method for refinement
        refined_content = _apply_refinement_method(
            pdf_path, quality_metrics.recommended_method, chapters, resource_manager
        )
        
        if refined_content:
            # Re-assess quality
            refined_quality = assess_extraction_quality(refined_content, {
                'pdf_characteristics': {'page_count': pdf_characteristics.page_count, 'has_images': pdf_characteristics.has_images},
                'text_analysis': text_analysis,
                'extraction_strategy': {'method_used': f"{extraction_method}+{quality_metrics.recommended_method}"},
                'ocr_text_results': len(ocr_text_results)
            })
            
            # Use refined content if quality improved
            if refined_quality.overall_score > quality_metrics.overall_score:
                chapters = refined_content.split("\n\n---\n\n")
                quality_metrics = refined_quality
                extraction_method = f"{extraction_method}+{quality_metrics.recommended_method}"
                logger.success(f"✅ Refinement improved quality: {refined_quality.overall_score:.2f}")
            else:
                logger.info(f"⚠️ Refinement did not improve quality, keeping original")
    else:
        logger.success(f"✅ Quality acceptable: {quality_metrics.overall_score:.2f}")
    
    progress.complete_step()
    
    # Step 9: Chapter Processing
    progress.start_step("Chapter Processing")
    
    # Process chapters with better naming
    processed_chapters = []
    
    for i, chapter_content in enumerate(chapters):
        # Extract title from chapter content
        lines = chapter_content.split('\n')
        title = "Chapter"
        
        for line in lines[:5]:  # Check first 5 lines for title
            line = line.strip()
            if line and (line.startswith('#') or len(line) > 10):
                title = line.lstrip('#').strip()
                if len(title) > 100:
                    title = title[:100] + "..."
                break
        
        safe_title = clean_filename(title)
        filename = f"{i+1:02d}_{safe_title}"
        
        # Integrate OCR content
        def _integrate_ocr_content(chapter_content, ocr_results):
            """Integrate OCR text results into chapter content"""
            if not ocr_results:
                return chapter_content
            
            # Add OCR text section only if we have meaningful content
            quality_results = {}
            for image_path, result in ocr_results.items():
                text = result.get('text', '')
                confidence = result.get('confidence', 0)
                
                if confidence > 0.6 and len(text.strip()) >= 10:
                    quality_results[image_path] = result
            
            if not quality_results:
                return chapter_content
            
            # Add OCR text section
            ocr_section = "\n\n---\n\n## 📝 Additional Text Content\n\n"
            ocr_section += "*Text extracted from document images:*\n\n"
            
            for image_path, result in quality_results.items():
                text = result['text']
                confidence = result['confidence']
                method = result['method']
                
                ocr_section += f"**{method.upper()}** (confidence: {confidence:.2f}):\n\n"
                ocr_section += f"{text}\n\n"
            
            return chapter_content + ocr_section
        
        enhanced_content = _integrate_ocr_content(chapter_content, ocr_text_results)
        
        # Save chapter
        _save_chapter_enhanced(enhanced_content, filename, title, pdf_path.name, pdf_output_dir, i+1)
        processed_chapters.append(filename)
    
    progress.complete_step()
    
    # Step 10: Finalization
    progress.start_step("Finalizing")
    
    # Save enhanced metadata with PDF analysis
    metadata = {
        "file_hash": file_hash,
        "processing_time": time.time() - progress.start_time,
        "pdf_characteristics": {
            "version": pdf_characteristics.version,
            "page_count": pdf_characteristics.page_count,
            "has_text_layer": pdf_characteristics.has_text_layer,
            "is_scanned": pdf_characteristics.is_scanned,
            "table_count": pdf_characteristics.table_count,
            "creation_method": pdf_characteristics.creation_method,
            "pdf_standard": pdf_characteristics.pdf_standard,
            "accessibility_compliant": pdf_characteristics.accessibility_compliant,
            "text_coverage": pdf_characteristics.text_coverage,
            "image_coverage": pdf_characteristics.image_coverage
        },
        "extraction_strategy": {
            "method_used": extraction_method,
            "optimal_method": pdf_characteristics.optimal_extraction_method,
            "confidence": pdf_characteristics.extraction_confidence,
            "expected_quality": extraction_strategy['expected_quality'],
            "fallback_methods": extraction_strategy['fallback_methods']
        },
        "text_analysis": text_analysis,
        "chapters_detected": len(chapters),
        "outline_entries": len(pdf_outline),
        "ocr_engine": ocr_engine.engine_type,
        "ocr_text_results": len(ocr_text_results),
        "quality_metrics": {
            "overall_score": quality_metrics.overall_score,
            "text_completeness": quality_metrics.text_completeness,
            "structure_preservation": quality_metrics.structure_preservation,
            "table_quality": quality_metrics.table_quality,
            "image_coverage": quality_metrics.image_coverage,
            "refinement_applied": quality_metrics.needs_refinement
        },
        "system_info": {
            "cpu_cores": resource_manager.cpu_count,
            "memory_gb": resource_manager.total_memory,
            "gpu_name": resource_manager.gpu_info["name"]
        }
    }
    
    with open(receipt_file, "w") as f:
        f.write(json.dumps(metadata, indent=2))
    
    # Final cleanup
    resource_manager.cleanup_gpu_memory()
    gc.collect()
    
    total_time = time.time() - progress.start_time
    progress.complete_step()
    
    logger.success(f"✅ Enhanced processing completed for {pdf_path.name} in {total_time:.1f}s")
    logger.info(f"📈 PDF: {pdf_characteristics.version}, {pdf_characteristics.creation_method}, {pdf_characteristics.pdf_standard}")
    logger.info(f"🎯 Method: {extraction_method} (confidence: {pdf_characteristics.extraction_confidence:.2f})")
    logger.info(f"📁 Chapters: {len(chapters)}, OCR text: {len(ocr_text_results)} extracts")
    logger.info(f"🏆 Final Quality Score: {quality_metrics.overall_score:.2f} ({'EXCELLENT' if quality_metrics.overall_score > 0.9 else 'GOOD' if quality_metrics.overall_score > 0.75 else 'ACCEPTABLE' if quality_metrics.overall_score > 0.6 else 'NEEDS IMPROVEMENT'})")

def _apply_refinement_method(pdf_path: Path, method: str, original_chapters: List[str], resource_manager) -> Optional[str]:
    """Apply secondary extraction method for quality refinement"""
    try:
        if method == "docling_conversion":
            from docling.document_converter import DocumentConverter
            from docling.datamodel.pipeline_options import PdfPipelineOptions
            from docling.datamodel.base_models import InputFormat
            
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = True
            pipeline_options.do_table_structure = True
            
            converter = DocumentConverter(format_options={InputFormat.PDF: pipeline_options})
            result = converter.convert(pdf_path)
            refined_md = result.document.export_to_markdown()
            return _merge_partial_numbering_lines(refined_md)
            
        elif method == "layout_preserving":
            layout_text = extract_pdf_with_layout(pdf_path)
            if layout_text:
                return process_enhanced_text(transform_text_enhanced(layout_text))
                
        elif method == "enhanced_text":
            text, analysis = extract_pdf_text_hybrid(pdf_path)
            if text:
                return process_enhanced_text(transform_text_enhanced(clean_extracted_text(text)))
                
    except Exception as e:
        logger.warning(f"Refinement method {method} failed: {e}")
    
    return None

def _save_chapter_enhanced(content, filename, title, source, output_dir, index=0):
    """Enhanced chapter saving with better formatting"""
    rendered = template.render(
        title=title,
        content=content,
        source_file=source,
        date=datetime.date.today().isoformat(),
        index=index
    )
    
    # Fix image paths to be relative to assets folder
    rendered = re.sub(r'\]\((?!assets/)', '](assets/', rendered)
    
    output_file = output_dir / f"{filename}.md"
    output_file.write_text(rendered, encoding="utf-8")
    logger.debug(f"Saved chapter: {output_file}")

# Export the enhanced function
process_pdf = process_pdf_enhanced