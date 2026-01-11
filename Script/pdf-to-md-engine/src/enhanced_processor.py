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
from src.enhanced_text_extractor import (
    extract_pdf_text_hybrid, 
    extract_pdf_outline_enhanced,
    should_use_ocr_enhancement,
    clean_extracted_text
)

# Initialize Jinja2
template_env = Environment(loader=FileSystemLoader("src/templates"))
template = template_env.get_template("chapter.md.j2")

def extract_images_from_pdf(pdf_path: Path, assets_dir: Path) -> Tuple[List[Path], Dict]:
    """Extract images directly from PDF using PyMuPDF"""
    saved_images = []
    image_info = {}
    
    try:
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    image_path = assets_dir / f"page_{page_num:03d}_img_{img_index:03d}.png"
                    pix.save(str(image_path))
                    
                    saved_images.append(image_path)
                    image_info[str(image_path)] = {
                        'path': image_path,
                        'page': page_num,
                        'index': img_index,
                        'width': pix.width,
                        'height': pix.height
                    }
                
                pix = None
        
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
            if EASYOCR_AVAILABLE and self.gpu_info["available"]:
                return "easyocr"
            elif TESSERACT_AVAILABLE:
                return "tesseract"
            return "none"
        
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
    progress = ProgressTracker(8)  # Added text enhancement step
    resource_manager = SystemResourceManager()
    
    # Step 1: Hash Check & Setup
    progress.start_step("Hash Check & Setup")
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    available_gb = psutil.virtual_memory().available / (1024**3)
    logger.info(f"Initial state - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%, Available: {available_gb:.1f}GB")
    
    file_hash = get_file_hash(pdf_path)
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
    
    # Step 2: Enhanced Text Analysis
    progress.start_step("Enhanced Text Analysis")
    
    # Extract PDF outline first
    pdf_outline = extract_pdf_outline_enhanced(pdf_path)
    
    # Enhanced text extraction
    extracted_text, has_text_layer, text_analysis = extract_pdf_text_layer_enhanced(pdf_path)
    
    # Initialize enhanced OCR engine
    ocr_engine = EnhancedOCREngine(resource_manager.optimal_ocr_engine, resource_manager)
    
    progress.complete_step()
    
    # Step 3: Text Enhancement (if needed)
    progress.start_step("Text Enhancement")
    
    if has_text_layer:
        if text_analysis.get("needs_ocr_enhancement", False):
            logger.info("Enhancing text layer with OCR")
            enhanced_text = ocr_engine.enhance_text_with_ocr(extracted_text, pdf_path)
        else:
            enhanced_text = clean_extracted_text(extracted_text)
        
        # Use enhanced text as markdown
        full_md = enhanced_text
        doc = None  # Skip docling conversion
        logger.info(f"Using enhanced text layer: {len(full_md)} characters")
    else:
        logger.info("No usable text layer - using docling conversion")
        # Fall back to docling processing
        def setup_converter(resource_manager):
            """Setup docling converter with optimal settings"""
            pipeline_options = PdfPipelineOptions()
            pipeline_options.do_ocr = False  # We handle OCR separately
            pipeline_options.do_table_structure = True
            
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
                pbar.update(1)
            except Exception as e:
                logger.error(f"PDF conversion failed: {e}")
                raise
        
        del converter
        gc.collect()
    
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
        # Extract images directly from PDF using PyMuPDF
        logger.info("Extracting images directly from PDF")
        saved_images, image_info = extract_images_from_pdf(pdf_path, assets_dir)
    
    logger.info(f"Extracted {len(saved_images)} images")
    
    progress.complete_step()
    
    # Step 6: OCR Processing
    progress.start_step("OCR Processing")
    
    if image_info:
        # Helper function for OCR processing
        def process_single_image_ocr(image_path, image_info, ocr_engine):
            """Process OCR for a single image with table and text detection"""
            try:
                if ocr_engine.engine_type == "easyocr" and ocr_engine.ocr_reader:
                    results = ocr_engine.ocr_reader.readtext(str(image_path))
                    
                    # Sort by position for table detection
                    sorted_results = sorted(results, key=lambda x: (x[0][0][1], x[0][0][0]))
                    
                    text_parts = []
                    confidences = []
                    
                    # Detect table structure by grouping similar Y coordinates
                    rows = []
                    current_row = []
                    last_y = None
                    
                    for (bbox, text, confidence) in sorted_results:
                        if confidence > 0.5 and len(text.strip()) > 1:
                            y_pos = bbox[0][1]
                            
                            # Group into rows (tolerance of 10 pixels)
                            if last_y is None or abs(y_pos - last_y) < 10:
                                current_row.append((bbox[0][0], text.strip()))
                            else:
                                if current_row:
                                    rows.append(sorted(current_row, key=lambda x: x[0]))
                                current_row = [(bbox[0][0], text.strip())]
                            
                            last_y = y_pos
                            confidences.append(confidence)
                    
                    if current_row:
                        rows.append(sorted(current_row, key=lambda x: x[0]))
                    
                    # Format as table if multiple columns detected
                    if len(rows) > 1 and any(len(row) > 2 for row in rows):
                        for row in rows:
                            row_text = ' | '.join([item[1] for item in row])
                            text_parts.append(row_text)
                    else:
                        # Regular text extraction
                        for (bbox, text, confidence) in sorted_results:
                            if confidence > 0.5 and len(text.strip()) > 1:
                                text_parts.append(text.strip())
                    
                    if text_parts:
                        combined_text = '\n'.join(text_parts)
                        avg_confidence = sum(confidences) / len(confidences)
                        return combined_text, avg_confidence
                
                elif ocr_engine.engine_type == "tesseract":
                    from PIL import Image
                    img = Image.open(image_path)
                    text = pytesseract.image_to_string(img)
                    confidence = 0.8 if len(text.strip()) > 10 else 0.5
                    return text.strip(), confidence
                
                return "", 0.0
                
            except Exception as e:
                logger.error(f"OCR processing failed for {image_path}: {e}")
                return "", 0.0
        
        def process_ocr_parallel(image_info, ocr_engine, resource_manager):
            """Process OCR on images with parallel processing and quality control"""
            ocr_results = {}
            
            if not image_info or ocr_engine.engine_type == "none":
                return ocr_results
            
            # Determine optimal batch size based on system resources
            batch_size = min(4, max(1, resource_manager.cpu_count // 2))
            if ocr_engine.engine_type == "easyocr" and resource_manager.gpu_info["available"]:
                batch_size = min(8, int(resource_manager.gpu_info["memory_gb"] // 2))
            
            image_paths = list(image_info.keys())
            
            # Process in batches to manage memory
            for i in range(0, len(image_paths), batch_size):
                batch_paths = image_paths[i:i + batch_size]
                
                # Check system resources before processing batch
                memory_usage = psutil.virtual_memory().percent
                if memory_usage > 85:
                    logger.warning(f"High memory usage ({memory_usage:.1f}%), reducing batch size")
                    batch_paths = batch_paths[:max(1, len(batch_paths)//2)]
                
                # Process batch with threading
                max_workers = min(batch_size, 4)
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_path = {}
                    
                    for image_path in batch_paths:
                        future = executor.submit(process_single_image_ocr, 
                                               image_path, image_info[image_path], ocr_engine)
                        future_to_path[future] = image_path
                    
                    for future in as_completed(future_to_path):
                        image_path = future_to_path[future]
                        try:
                            ocr_text, confidence = future.result()
                            if ocr_text and confidence > settings.OCR_CONFIDENCE_THRESHOLD:
                                ocr_results[image_path] = {
                                    'text': ocr_text,
                                    'confidence': confidence,
                                    'method': ocr_engine.engine_type
                                }
                        except Exception as e:
                            logger.warning(f"OCR failed for {image_path}: {e}")
                
                # Memory cleanup between batches
                gc.collect()
                if resource_manager.gpu_info["available"]:
                    torch.cuda.empty_cache()
            
            return ocr_results
        
        gc.collect()
        if resource_manager.gpu_info["available"]:
            torch.cuda.empty_cache()
        
        ocr_results = process_ocr_parallel(image_info, ocr_engine, resource_manager)
        logger.info(f"OCR extracted text from {len(ocr_results)} images")
        
        resource_manager.cleanup_gpu_memory()
        gc.collect()
    else:
        ocr_results = {}
    
    progress.complete_step()
    
    # Step 7: Chapter Processing
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
            """Integrate OCR results into chapter content with quality control"""
            if not ocr_results:
                return chapter_content
            
            # Filter high-quality OCR results
            quality_results = {}
            for image_path, result in ocr_results.items():
                if isinstance(result, dict):
                    text = result.get('text', '')
                    confidence = result.get('confidence', 0)
                    method = result.get('method', 'unknown')
                else:
                    text = str(result)
                    confidence = 0.7
                    method = 'legacy'
                
                # Only include high-quality, meaningful text
                if (confidence > settings.OCR_CONFIDENCE_THRESHOLD and 
                    len(text.strip()) >= settings.OCR_MIN_TEXT_LENGTH):
                    quality_results[image_path] = {
                        'text': text.strip(),
                        'confidence': confidence,
                        'method': method
                    }
            
            if not quality_results:
                return chapter_content
            
            # Add OCR content section
            ocr_section = "\n\n---\n\n## 📷 Extracted Image Text\n\n"
            ocr_section += "*The following text was extracted from images using OCR technology:*\n\n"
            
            for image_path, result in quality_results.items():
                image_name = Path(image_path).name
                text = result['text']
                confidence = result['confidence']
                method = result['method']
                
                ocr_section += f"### 🖼️ {image_name}\n\n"
                ocr_section += f"**Method:** {method.upper()} | **Confidence:** {confidence:.2f}\n\n"
                ocr_section += f"> {text}\n\n"
            
            return chapter_content + ocr_section
        
        enhanced_content = _integrate_ocr_content(chapter_content, ocr_results)
        
        # Save chapter
        _save_chapter_enhanced(enhanced_content, filename, title, pdf_path.name, pdf_output_dir, i+1)
        processed_chapters.append(filename)
    
    progress.complete_step()
    
    # Step 8: Finalization
    progress.start_step("Finalizing")
    
    # Save enhanced metadata
    metadata = {
        "file_hash": file_hash,
        "processing_time": time.time() - progress.start_time,
        "text_analysis": text_analysis,
        "chapters_detected": len(chapters),
        "outline_entries": len(pdf_outline),
        "ocr_engine": ocr_engine.engine_type,
        "ocr_results_count": len(ocr_results),
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
    logger.info(f"📊 Text quality: {text_analysis.get('text_quality', 0):.2f}")
    logger.info(f"📑 Chapters: {len(chapters)}, OCR enhanced: {len(ocr_results)} images")

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