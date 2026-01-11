"""
OCR Text Layer Detection and Extraction Module

This module provides comprehensive functionality to:
1. Detect if a PDF has existing OCR text layers
2. Extract text with positional information
3. Combine with image-based OCR for better results
4. Handle various PDF text encoding issues
"""

import fitz  # PyMuPDF
import pdfplumber
import pymupdf
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import re
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)

@dataclass
class TextBlock:
    """Represents a block of text with position and metadata"""
    text: str
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    page_num: int
    font_size: float = 0.0
    font_name: str = ""
    confidence: float = 1.0  # 1.0 for extracted text, lower for OCR
    source: str = "extracted"  # "extracted" or "ocr"

@dataclass
class PageAnalysis:
    """Analysis results for a single page"""
    page_num: int
    has_text: bool
    text_coverage: float  # Percentage of page covered by text
    image_coverage: float  # Percentage of page covered by images
    text_blocks: List[TextBlock]
    needs_ocr: bool
    is_scanned: bool

class PDFTextLayerAnalyzer:
    """Comprehensive PDF text layer analysis and extraction"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.doc = None
        self.plumber_pdf = None
        
    def __enter__(self):
        self.doc = fitz.open(str(self.pdf_path))
        self.plumber_pdf = pdfplumber.open(str(self.pdf_path))
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.doc:
            self.doc.close()
        if self.plumber_pdf:
            self.plumber_pdf.close()
    
    def analyze_pdf(self) -> Dict[str, Any]:
        """Comprehensive PDF analysis"""
        results = {
            "total_pages": len(self.doc),
            "has_text_layer": False,
            "text_coverage_avg": 0.0,
            "pages_needing_ocr": [],
            "pages_with_text": [],
            "is_fully_scanned": True,
            "page_analyses": []
        }
        
        total_text_coverage = 0.0
        
        for page_num in range(len(self.doc)):
            page_analysis = self._analyze_page(page_num)
            results["page_analyses"].append(page_analysis)
            
            if page_analysis.has_text:
                results["has_text_layer"] = True
                results["pages_with_text"].append(page_num)
                results["is_fully_scanned"] = False
                
            if page_analysis.needs_ocr:
                results["pages_needing_ocr"].append(page_num)
                
            total_text_coverage += page_analysis.text_coverage
        
        results["text_coverage_avg"] = total_text_coverage / len(self.doc) if self.doc else 0
        
        logger.info(f"PDF Analysis: {results['total_pages']} pages, "
                   f"{len(results['pages_with_text'])} with text, "
                   f"{len(results['pages_needing_ocr'])} need OCR")
        
        return results
    
    def _analyze_page(self, page_num: int) -> PageAnalysis:
        """Analyze a single page for text and image content"""
        page = self.doc[page_num]
        plumber_page = self.plumber_pdf.pages[page_num]
        
        # Extract text blocks with position
        text_blocks = self._extract_text_blocks(page, page_num)
        
        # Calculate coverage
        page_rect = page.rect
        page_area = page_rect.width * page_rect.height
        
        text_area = sum(
            (block.bbox[2] - block.bbox[0]) * (block.bbox[3] - block.bbox[1])
            for block in text_blocks
        )
        text_coverage = (text_area / page_area * 100) if page_area > 0 else 0
        
        # Analyze images
        image_coverage = self._calculate_image_coverage(page, page_area)
        
        # Determine if page needs OCR
        has_meaningful_text = len([b for b in text_blocks if len(b.text.strip()) > 10]) > 0
        is_mostly_images = image_coverage > 50
        low_text_coverage = text_coverage < 20
        
        needs_ocr = (not has_meaningful_text) or (is_mostly_images and low_text_coverage)
        is_scanned = image_coverage > 80 and text_coverage < 5
        
        return PageAnalysis(
            page_num=page_num,
            has_text=len(text_blocks) > 0,
            text_coverage=text_coverage,
            image_coverage=image_coverage,
            text_blocks=text_blocks,
            needs_ocr=needs_ocr,
            is_scanned=is_scanned
        )
    
    def _extract_text_blocks(self, page, page_num: int) -> List[TextBlock]:
        """Extract text blocks with detailed positioning"""
        text_blocks = []
        
        # Method 1: PyMuPDF text extraction with formatting
        try:
            blocks = page.get_text("dict")
            for block in blocks.get("blocks", []):
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line.get("spans", []):
                            text = span.get("text", "").strip()
                            if text:
                                bbox = span.get("bbox", (0, 0, 0, 0))
                                font_size = span.get("size", 0)
                                font_name = span.get("font", "")
                                
                                text_blocks.append(TextBlock(
                                    text=text,
                                    bbox=bbox,
                                    page_num=page_num,
                                    font_size=font_size,
                                    font_name=font_name,
                                    confidence=1.0,
                                    source="extracted"
                                ))
        except Exception as e:
            logger.warning(f"PyMuPDF text extraction failed for page {page_num}: {e}")
        
        # Method 2: Fallback with simple text extraction
        if not text_blocks:
            try:
                text = page.get_text()
                if text.strip():
                    # Create a single block for the entire page
                    text_blocks.append(TextBlock(
                        text=text.strip(),
                        bbox=page.rect,
                        page_num=page_num,
                        confidence=1.0,
                        source="extracted"
                    ))
            except Exception as e:
                logger.warning(f"Fallback text extraction failed for page {page_num}: {e}")
        
        return text_blocks
    
    def _calculate_image_coverage(self, page, page_area: float) -> float:
        """Calculate percentage of page covered by images"""
        try:
            image_list = page.get_images()
            if not image_list:
                return 0.0
            
            total_image_area = 0.0
            for img_index, img in enumerate(image_list):
                try:
                    # Get image rectangle
                    img_rect = page.get_image_rects(img[0])
                    if img_rect:
                        for rect in img_rect:
                            total_image_area += rect.width * rect.height
                except Exception:
                    # Fallback: estimate based on image count
                    total_image_area += page_area * 0.1  # Assume 10% per image
            
            return min(100.0, (total_image_area / page_area * 100)) if page_area > 0 else 0.0
            
        except Exception as e:
            logger.warning(f"Image coverage calculation failed: {e}")
            return 0.0
    
    def extract_enhanced_text(self) -> Dict[int, List[TextBlock]]:
        """Extract all text with enhanced positioning and metadata"""
        enhanced_text = {}
        
        for page_num in range(len(self.doc)):
            page_analysis = self._analyze_page(page_num)
            enhanced_text[page_num] = page_analysis.text_blocks
            
        return enhanced_text
    
    def get_text_for_markdown(self) -> str:
        """Extract text optimized for markdown conversion"""
        markdown_text = []
        
        for page_num in range(len(self.doc)):
            page_analysis = self._analyze_page(page_num)
            
            if page_analysis.text_blocks:
                # Sort text blocks by position (top to bottom, left to right)
                sorted_blocks = sorted(
                    page_analysis.text_blocks,
                    key=lambda b: (b.bbox[1], b.bbox[0])  # y-coordinate first, then x
                )
                
                page_text = []
                for block in sorted_blocks:
                    # Clean and format text
                    clean_text = self._clean_text_for_markdown(block.text)
                    if clean_text:
                        # Add formatting hints based on font size
                        if block.font_size > 16:
                            clean_text = f"# {clean_text}"
                        elif block.font_size > 14:
                            clean_text = f"## {clean_text}"
                        elif block.font_size > 12:
                            clean_text = f"### {clean_text}"
                        
                        page_text.append(clean_text)
                
                if page_text:
                    markdown_text.extend(page_text)
                    markdown_text.append("")  # Page break
        
        return "\n".join(markdown_text)
    
    def _clean_text_for_markdown(self, text: str) -> str:
        """Clean extracted text for markdown formatting"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Fix common OCR issues
        text = text.replace('ﬁ', 'fi')  # ligature fixes
        text = text.replace('ﬂ', 'fl')
        text = text.replace(''', "'")    # smart quotes
        text = text.replace('"', '"')
        text = text.replace('"', '"')
        
        # Remove very short or meaningless text
        if len(text) < 3 or text.isdigit():
            return ""
        
        return text

def detect_pdf_text_layer(pdf_path: Path) -> Dict[str, Any]:
    """Quick detection of PDF text layer capabilities"""
    try:
        with PDFTextLayerAnalyzer(pdf_path) as analyzer:
            return analyzer.analyze_pdf()
    except Exception as e:
        logger.error(f"Failed to analyze PDF {pdf_path}: {e}")
        return {
            "total_pages": 0,
            "has_text_layer": False,
            "text_coverage_avg": 0.0,
            "pages_needing_ocr": [],
            "pages_with_text": [],
            "is_fully_scanned": True,
            "error": str(e)
        }

def extract_pdf_text_enhanced(pdf_path: Path) -> Tuple[str, Dict[str, Any]]:
    """Extract text from PDF with comprehensive analysis"""
    try:
        with PDFTextLayerAnalyzer(pdf_path) as analyzer:
            analysis = analyzer.analyze_pdf()
            markdown_text = analyzer.get_text_for_markdown()
            return markdown_text, analysis
    except Exception as e:
        logger.error(f"Failed to extract text from PDF {pdf_path}: {e}")
        return "", {"error": str(e)}

# Integration functions for the main processor
def should_use_existing_text_layer(pdf_path: Path) -> bool:
    """Determine if existing text layer should be used instead of OCR"""
    analysis = detect_pdf_text_layer(pdf_path)
    
    # Use existing text if:
    # - Has text layer AND
    # - Good text coverage (>30%) OR
    # - Less than 50% of pages need OCR
    has_good_text = (
        analysis.get("has_text_layer", False) and
        (analysis.get("text_coverage_avg", 0) > 30 or
         len(analysis.get("pages_needing_ocr", [])) < len(analysis.get("page_analyses", [])) * 0.5)
    )
    
    return has_good_text

def get_hybrid_extraction_strategy(pdf_path: Path) -> Dict[str, Any]:
    """Get optimal extraction strategy combining text layer and OCR"""
    analysis = detect_pdf_text_layer(pdf_path)
    
    strategy = {
        "use_text_layer": analysis.get("has_text_layer", False),
        "pages_for_ocr": analysis.get("pages_needing_ocr", []),
        "pages_with_text": analysis.get("pages_with_text", []),
        "extraction_method": "hybrid",
        "text_coverage": analysis.get("text_coverage_avg", 0)
    }
    
    # Determine primary method
    if analysis.get("text_coverage_avg", 0) > 70:
        strategy["extraction_method"] = "text_layer_primary"
    elif analysis.get("is_fully_scanned", True):
        strategy["extraction_method"] = "ocr_only"
    else:
        strategy["extraction_method"] = "hybrid"
    
    return strategy