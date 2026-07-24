"""
Enhanced PDF Analyzer - Detects PDF characteristics and selects optimal extraction methods
"""

import fitz
import pdfplumber
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from loguru import logger
import re

@dataclass
class PDFCharacteristics:
    """PDF document characteristics and metadata"""
    version: str
    page_count: int
    has_text_layer: bool
    has_images: bool
    has_forms: bool
    has_annotations: bool
    has_bookmarks: bool
    is_encrypted: bool
    is_linearized: bool
    is_tagged: bool
    is_scanned: bool
    text_coverage: float
    image_coverage: float
    table_count: int
    font_count: int
    color_space: str
    creation_method: str
    pdf_standard: str
    accessibility_compliant: bool
    optimal_extraction_method: str
    extraction_confidence: float

class PDFAnalyzer:
    """Comprehensive PDF analysis for optimal tool selection"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.doc = None
        self.plumber_pdf = None
    
    def __enter__(self):
        try:
            self.doc = fitz.open(str(self.pdf_path))
            self.plumber_pdf = pdfplumber.open(str(self.pdf_path))
            return self
        except Exception as e:
            logger.error(f"Failed to open PDF: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.doc:
            self.doc.close()
        if self.plumber_pdf:
            self.plumber_pdf.close()
    
    def analyze(self) -> PDFCharacteristics:
        """Comprehensive PDF analysis"""
        try:
            # Basic metadata
            version = self._get_pdf_version()
            page_count = len(self.doc)
            
            # Document properties
            has_text_layer = self._analyze_text_layer()
            has_images = self._analyze_images()
            has_forms = self._analyze_forms()
            has_annotations = self._analyze_annotations()
            has_bookmarks = self._analyze_bookmarks()
            is_encrypted = self.doc.is_encrypted
            is_linearized = self._check_linearization()
            is_tagged = self._check_tagged_pdf()
            
            # Content analysis
            is_scanned, text_coverage, image_coverage = self._analyze_content_distribution()
            table_count = self._count_tables()
            font_count = self._count_fonts()
            color_space = self._analyze_color_space()
            
            # Creation and compliance
            creation_method = self._detect_creation_method()
            pdf_standard = self._detect_pdf_standard()
            accessibility_compliant = self._check_accessibility()
            
            # Optimal method selection
            method_data = {
                'version': version,
                'has_text_layer': has_text_layer,
                'is_scanned': is_scanned,
                'text_coverage': text_coverage,
                'has_bookmarks': has_bookmarks,
                'has_images': has_images,
                'table_count': table_count,
                'is_tagged': is_tagged,
                'creation_method': creation_method
            }
            optimal_method, confidence = self._select_optimal_method(method_data)
            
            return PDFCharacteristics(
                version=version,
                page_count=page_count,
                has_text_layer=has_text_layer,
                has_images=has_images,
                has_forms=has_forms,
                has_annotations=has_annotations,
                has_bookmarks=has_bookmarks,
                is_encrypted=is_encrypted,
                is_linearized=is_linearized,
                is_tagged=is_tagged,
                is_scanned=is_scanned,
                text_coverage=text_coverage,
                image_coverage=image_coverage,
                table_count=table_count,
                font_count=font_count,
                color_space=color_space,
                creation_method=creation_method,
                pdf_standard=pdf_standard,
                accessibility_compliant=accessibility_compliant,
                optimal_extraction_method=optimal_method,
                extraction_confidence=confidence
            )
            
        except Exception as e:
            logger.error(f"PDF analysis failed: {e}")
            return self._create_fallback_characteristics()
    
    def _get_pdf_version(self) -> str:
        """Get PDF version"""
        try:
            metadata = self.doc.metadata
            version = metadata.get('format', 'PDF-1.4')
            if version.startswith('PDF-'):
                return version
            return f"PDF-{self.doc.pdf_version()}"
        except:
            return "PDF-1.4"
    
    def _analyze_text_layer(self) -> bool:
        """Analyze if PDF has meaningful text layer"""
        try:
            total_chars = 0
            for page_num in range(min(5, len(self.doc))):  # Check first 5 pages
                page = self.doc[page_num]
                text = page.get_text()
                total_chars += len(text.strip())
            
            avg_chars_per_page = total_chars / min(5, len(self.doc))
            return avg_chars_per_page > 100  # Threshold for meaningful text
        except:
            return False
    
    def _analyze_images(self) -> bool:
        """Check if PDF contains images"""
        try:
            for page_num in range(min(3, len(self.doc))):
                page = self.doc[page_num]
                if page.get_images():
                    return True
            return False
        except:
            return False
    
    def _analyze_forms(self) -> bool:
        """Check for interactive forms"""
        try:
            return bool(self.doc.form_fields())
        except:
            return False
    
    def _analyze_annotations(self) -> bool:
        """Check for annotations"""
        try:
            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                if page.annots():
                    return True
            return False
        except:
            return False
    
    def _analyze_bookmarks(self) -> bool:
        """Check for bookmarks/outline"""
        try:
            toc = self.doc.get_toc()
            return len(toc) > 0
        except:
            return False
    
    def _check_linearization(self) -> bool:
        """Check if PDF is linearized (fast web view)"""
        try:
            # Check PDF header for linearization hints
            with open(self.pdf_path, 'rb') as f:
                header = f.read(1024).decode('latin-1', errors='ignore')
                return '/Linearized' in header
        except:
            return False
    
    def _check_tagged_pdf(self) -> bool:
        """Check if PDF is tagged for accessibility"""
        try:
            # Check for StructTreeRoot in catalog
            catalog = self.doc.pdf_catalog()
            return '/StructTreeRoot' in str(catalog)
        except:
            return False
    
    def _analyze_content_distribution(self) -> Tuple[bool, float, float]:
        """Analyze text vs image content distribution"""
        try:
            total_text_area = 0
            total_image_area = 0
            total_page_area = 0
            
            sample_pages = min(5, len(self.doc))
            
            for page_num in range(sample_pages):
                page = self.doc[page_num]
                page_rect = page.rect
                page_area = page_rect.width * page_rect.height
                total_page_area += page_area
                
                # Analyze text blocks
                blocks = page.get_text("dict")
                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        bbox = block.get("bbox", (0, 0, 0, 0))
                        block_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                        total_text_area += block_area
                
                # Analyze images
                images = page.get_images()
                for img in images:
                    try:
                        img_rects = page.get_image_rects(img[0])
                        for rect in img_rects:
                            total_image_area += rect.width * rect.height
                    except:
                        # Estimate image area
                        total_image_area += page_area * 0.1
            
            if total_page_area == 0:
                return False, 0.0, 0.0
            
            text_coverage = (total_text_area / total_page_area) * 100
            image_coverage = (total_image_area / total_page_area) * 100
            
            # Consider scanned if high image coverage and low text coverage
            is_scanned = image_coverage > 70 and text_coverage < 20
            
            return is_scanned, text_coverage, image_coverage
            
        except Exception as e:
            logger.warning(f"Content analysis failed: {e}")
            return False, 0.0, 0.0
    
    def _count_tables(self) -> int:
        """Count tables in PDF"""
        try:
            table_count = 0
            sample_pages = min(5, len(self.plumber_pdf.pages))
            
            for page_num in range(sample_pages):
                page = self.plumber_pdf.pages[page_num]
                tables = page.extract_tables()
                table_count += len(tables) if tables else 0
            
            return table_count
        except:
            return 0
    
    def _count_fonts(self) -> int:
        """Count unique fonts used"""
        try:
            fonts = set()
            sample_pages = min(3, len(self.doc))
            
            for page_num in range(sample_pages):
                page = self.doc[page_num]
                blocks = page.get_text("dict")
                for block in blocks.get("blocks", []):
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line.get("spans", []):
                                font = span.get("font", "")
                                if font:
                                    fonts.add(font)
            
            return len(fonts)
        except:
            return 0
    
    def _analyze_color_space(self) -> str:
        """Analyze primary color space"""
        try:
            # Check first few pages for color information
            has_color = False
            for page_num in range(min(3, len(self.doc))):
                page = self.doc[page_num]
                images = page.get_images()
                for img in images:
                    try:
                        pix = fitz.Pixmap(self.doc, img[0])
                        if pix.n > 2:  # More than grayscale
                            has_color = True
                        pix = None
                        break
                    except:
                        continue
                if has_color:
                    break
            
            return "RGB" if has_color else "Grayscale"
        except:
            return "Unknown"
    
    def _detect_creation_method(self) -> str:
        """Detect how PDF was created"""
        try:
            metadata = self.doc.metadata
            creator = metadata.get('creator', '').lower()
            producer = metadata.get('producer', '').lower()
            
            # Common creation methods
            if 'scan' in creator or 'scan' in producer:
                return "Scanned"
            elif 'word' in creator or 'office' in creator:
                return "Office Suite"
            elif 'latex' in creator or 'tex' in creator:
                return "LaTeX"
            elif 'indesign' in creator or 'acrobat' in creator:
                return "Professional Publishing"
            elif 'print' in creator or 'driver' in producer:
                return "Print Driver"
            elif 'web' in creator or 'html' in creator:
                return "Web/HTML"
            else:
                return "Unknown"
        except:
            return "Unknown"
    
    def _detect_pdf_standard(self) -> str:
        """Detect PDF standard compliance"""
        try:
            # Check for PDF/A, PDF/X, PDF/E compliance
            catalog = str(self.doc.pdf_catalog())
            
            if '/OutputIntents' in catalog:
                if 'PDF/A' in catalog:
                    return "PDF/A"
                elif 'PDF/X' in catalog:
                    return "PDF/X"
                elif 'PDF/E' in catalog:
                    return "PDF/E"
            
            return "Standard PDF"
        except:
            return "Standard PDF"
    
    def _check_accessibility(self) -> bool:
        """Check accessibility compliance"""
        try:
            # Basic accessibility checks
            has_structure = self._check_tagged_pdf()
            has_bookmarks = self._analyze_bookmarks()
            
            # Check for alt text on images (simplified)
            has_alt_text = False
            try:
                for page_num in range(min(3, len(self.doc))):
                    page = self.doc[page_num]
                    if '/Alt' in str(page.get_contents()):
                        has_alt_text = True
                        break
            except:
                pass
            
            return has_structure and (has_bookmarks or has_alt_text)
        except:
            return False
    
    def _select_optimal_method(self, characteristics: Dict) -> Tuple[str, float]:
        """Select optimal extraction method based on characteristics"""
        
        # Method scoring system
        methods = {
            'layout_preserving': 0.0,
            'enhanced_text': 0.0,
            'docling_conversion': 0.0,
            'ocr_primary': 0.0
        }
        
        # Layout preserving method scoring
        if characteristics['has_text_layer']:
            methods['layout_preserving'] += 40
        if characteristics['table_count'] > 0:
            methods['layout_preserving'] += 30
        if characteristics['is_tagged']:
            methods['layout_preserving'] += 20
        if characteristics['text_coverage'] > 50:
            methods['layout_preserving'] += 10
        
        # Enhanced text method scoring
        if characteristics['has_text_layer']:
            methods['enhanced_text'] += 35
        if characteristics['has_bookmarks']:
            methods['enhanced_text'] += 25
        if not characteristics['is_scanned']:
            methods['enhanced_text'] += 20
        if characteristics['creation_method'] in ['Office Suite', 'LaTeX']:
            methods['enhanced_text'] += 15
        
        # Docling conversion scoring
        if characteristics['version'] >= 'PDF-1.4':
            methods['docling_conversion'] += 20
        if characteristics.get('has_images', False):
            methods['docling_conversion'] += 25
        if characteristics['table_count'] > 0:
            methods['docling_conversion'] += 20
        if not characteristics['is_scanned']:
            methods['docling_conversion'] += 15
        
        # OCR primary scoring
        if characteristics['is_scanned']:
            methods['ocr_primary'] += 60
        if not characteristics['has_text_layer']:
            methods['ocr_primary'] += 40
        if characteristics['text_coverage'] < 20:
            methods['ocr_primary'] += 30
        if characteristics['creation_method'] == 'Scanned':
            methods['ocr_primary'] += 20
        
        # Select best method
        best_method = max(methods, key=methods.get)
        confidence = methods[best_method] / 100.0
        
        # Ensure minimum confidence
        if confidence < 0.3:
            best_method = 'enhanced_text'  # Safe fallback
            confidence = 0.5
        
        return best_method, min(confidence, 1.0)
    
    def _create_fallback_characteristics(self) -> PDFCharacteristics:
        """Create fallback characteristics when analysis fails"""
        return PDFCharacteristics(
            version="PDF-1.4",
            page_count=0,
            has_text_layer=False,
            has_images=False,
            has_forms=False,
            has_annotations=False,
            has_bookmarks=False,
            is_encrypted=False,
            is_linearized=False,
            is_tagged=False,
            is_scanned=True,
            text_coverage=0.0,
            image_coverage=0.0,
            table_count=0,
            font_count=0,
            color_space="Unknown",
            creation_method="Unknown",
            pdf_standard="Standard PDF",
            accessibility_compliant=False,
            optimal_extraction_method="ocr_primary",
            extraction_confidence=0.3
        )

def analyze_pdf_characteristics(pdf_path: Path) -> PDFCharacteristics:
    """Analyze PDF and return characteristics for optimal tool selection"""
    try:
        with PDFAnalyzer(pdf_path) as analyzer:
            return analyzer.analyze()
    except Exception as e:
        logger.error(f"PDF analysis failed for {pdf_path}: {e}")
        return PDFCharacteristics(
            version="PDF-1.4", page_count=0, has_text_layer=False,
            has_images=False, has_forms=False, has_annotations=False,
            has_bookmarks=False, is_encrypted=False, is_linearized=False,
            is_tagged=False, is_scanned=True, text_coverage=0.0,
            image_coverage=0.0, table_count=0, font_count=0,
            color_space="Unknown", creation_method="Unknown",
            pdf_standard="Standard PDF", accessibility_compliant=False,
            optimal_extraction_method="ocr_primary", extraction_confidence=0.3
        )

def get_extraction_strategy(characteristics: PDFCharacteristics) -> Dict[str, Any]:
    """Get detailed extraction strategy based on PDF characteristics"""
    
    strategy = {
        'primary_method': characteristics.optimal_extraction_method,
        'confidence': characteristics.extraction_confidence,
        'fallback_methods': [],
        'preprocessing_steps': [],
        'postprocessing_steps': [],
        'expected_quality': 'high' if characteristics.extraction_confidence > 0.7 else 'medium',
        'processing_time_estimate': 'fast',
        'resource_requirements': 'low'
    }
    
    # Set fallback methods
    if characteristics.optimal_extraction_method == 'layout_preserving':
        strategy['fallback_methods'] = ['enhanced_text', 'docling_conversion']
    elif characteristics.optimal_extraction_method == 'enhanced_text':
        strategy['fallback_methods'] = ['layout_preserving', 'docling_conversion']
    elif characteristics.optimal_extraction_method == 'docling_conversion':
        strategy['fallback_methods'] = ['enhanced_text', 'ocr_primary']
    else:  # ocr_primary
        strategy['fallback_methods'] = ['docling_conversion', 'enhanced_text']
    
    # Preprocessing recommendations
    if characteristics.is_encrypted:
        strategy['preprocessing_steps'].append('decrypt')
    if characteristics.text_coverage < 30:
        strategy['preprocessing_steps'].append('ocr_enhancement')
    if characteristics.table_count > 0:
        strategy['preprocessing_steps'].append('table_detection')
    
    # Postprocessing recommendations
    if characteristics.creation_method == 'Scanned':
        strategy['postprocessing_steps'].append('text_cleaning')
    if not characteristics.has_bookmarks and characteristics.page_count > 10:
        strategy['postprocessing_steps'].append('chapter_detection')
    if characteristics.has_images:
        strategy['postprocessing_steps'].append('image_extraction')
    
    # Adjust estimates based on characteristics
    if characteristics.is_scanned or characteristics.optimal_extraction_method == 'ocr_primary':
        strategy['processing_time_estimate'] = 'slow'
        strategy['resource_requirements'] = 'high'
    elif characteristics.table_count > 5 or characteristics.page_count > 100:
        strategy['processing_time_estimate'] = 'medium'
        strategy['resource_requirements'] = 'medium'
    
    return strategy