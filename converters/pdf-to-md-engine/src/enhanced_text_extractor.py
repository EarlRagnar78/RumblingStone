import fitz
import pdfplumber
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from loguru import logger
from .pdf_text_operators import extract_text_with_operators

def detect_pdf_text_quality(pdf_path: Path) -> Dict:
    """Enhanced PDF text layer detection with encoding analysis"""
    try:
        doc = fitz.open(str(pdf_path))
        total_chars = 0
        readable_chars = 0
        total_pages = len(doc)
        encoding_issues = 0
        
        for page_num in range(total_pages):
            page = doc[page_num]
            # Try multiple extraction methods
            text = page.get_text("text")  # Standard text extraction
            
            if not text.strip():
                # Try dict format for better encoding handling
                text_dict = page.get_text("dict")
                text = extract_text_from_dict(text_dict)
            
            total_chars += len(text)
            
            # Check for encoding issues (strange characters)
            clean_text = clean_extracted_text(text)
            readable_chars += len(clean_text)
            
            if len(text) > 0 and len(clean_text) / len(text) < 0.7:
                encoding_issues += 1
        
        doc.close()
        
        avg_chars = total_chars / total_pages if total_pages > 0 else 0
        text_quality = readable_chars / total_chars if total_chars > 0 else 0
        has_text_layer = avg_chars > 50 and text_quality > 0.5
        
        return {
            "has_text_layer": has_text_layer,
            "avg_chars_per_page": avg_chars,
            "total_chars": total_chars,
            "readable_chars": readable_chars,
            "text_quality": text_quality,
            "encoding_issues": encoding_issues,
            "total_pages": total_pages,
            "needs_ocr_enhancement": encoding_issues > total_pages * 0.3
        }
    except Exception as e:
        logger.error(f"PDF analysis failed: {e}")
        return {"error": str(e), "has_text_layer": False}

def extract_text_with_unicode_mapping(page) -> str:
    """Extract text using ISO 32000-1 Unicode mapping and text operators"""
    try:
        # Try text-showing operators first (ISO 32000-1 9.4.3)
        operator_text = extract_text_with_operators(page)
        if operator_text and len(operator_text.strip()) > 50:
            return map_to_unicode(operator_text, "")
        
        # Fallback to dict extraction
        text_dict = page.get_text("dict")
        unicode_text = []
        
        for block in text_dict.get("blocks", []):
            if "lines" in block:
                for line in block["lines"]:
                    line_text = ""
                    for span in line.get("spans", []):
                        span_text = span.get("text", "")
                        font_name = span.get("font", "")
                        
                        if span_text:
                            mapped_text = map_to_unicode(span_text, font_name)
                            line_text += mapped_text
                    
                    if line_text.strip():
                        unicode_text.append(line_text)
        
        return "\n".join(unicode_text)
        
    except Exception as e:
        logger.warning(f"Unicode mapping failed, using fallback: {e}")
        return page.get_text()

def map_to_unicode(text: str, font_name: str) -> str:
    """Map character codes to Unicode according to ISO 32000-1"""
    if not text:
        return text
    
    unicode_mappings = {
        '\ufb01': 'fi', '\ufb02': 'fl', '\ufb00': 'ff', '\ufb03': 'ffi', '\ufb04': 'ffl',
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '--',
        '\u00a0': ' ', '\u2026': '...', '\u00ad': ''
    }
    
    result = text
    for unicode_char, replacement in unicode_mappings.items():
        result = result.replace(unicode_char, replacement)
    
    return result

def extract_text_from_dict(text_dict: Dict) -> str:
    """Extract text from PyMuPDF dict format with better encoding handling"""
    text_parts = []
    
    for block in text_dict.get("blocks", []):
        if "lines" in block:
            for line in block["lines"]:
                line_text = ""
                for span in line.get("spans", []):
                    span_text = span.get("text", "")
                    if span_text:
                        line_text += span_text
                if line_text.strip():
                    text_parts.append(line_text)
    
    return "\n".join(text_parts)

def clean_extracted_text(text: str) -> str:
    """Clean and fix common OCR/encoding issues"""
    if not text:
        return ""
    
    # Fix common ligature issues
    text = text.replace('ﬁ', 'fi')
    text = text.replace('ﬂ', 'fl')
    text = text.replace('ﬀ', 'ff')
    text = text.replace('ﬃ', 'ffi')
    text = text.replace('ﬄ', 'ffl')
    
    # Fix smart quotes and dashes
    text = text.replace(''', "'")
    text = text.replace(''', "'")
    text = text.replace('"', '"')
    text = text.replace('"', '"')
    text = text.replace('–', '-')
    text = text.replace('—', '--')
    
    # Remove excessive whitespace but preserve paragraph breaks
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs to single space
    text = re.sub(r'\n[ \t]+', '\n', text)  # Remove leading whitespace on lines
    text = re.sub(r'[ \t]+\n', '\n', text)  # Remove trailing whitespace on lines
    
    # Fix broken words across lines (common OCR issue)
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)
    
    return text.strip()

def extract_pdf_outline_enhanced(pdf_path: Path) -> List[Dict]:
    """Extract PDF outline with better title cleaning"""
    try:
        doc = fitz.open(str(pdf_path))
        outline = doc.get_toc()
        doc.close()
        
        if not outline:
            return []
        
        enhanced_outline = []
        for item in outline:
            level, title, page = item
            
            # Clean the title
            clean_title = clean_extracted_text(title)
            
            # Skip empty or very short titles
            if len(clean_title) < 2:
                continue
                
            enhanced_outline.append({
                'level': level,
                'title': clean_title,
                'page': page,
                'original_title': title
            })
        
        logger.info(f"Found {len(enhanced_outline)} outline entries")
        return enhanced_outline
        
    except Exception as e:
        logger.warning(f"Failed to extract PDF outline: {e}")
        return []

def extract_pdf_text_hybrid(pdf_path: Path) -> Tuple[str, Dict]:
    """Hybrid text extraction combining multiple methods"""
    analysis = detect_pdf_text_quality(pdf_path)
    
    if not analysis.get("has_text_layer", False):
        return "", analysis
    
    # Try pdfplumber first (better for tables and layout)
    text_plumber = extract_with_pdfplumber(pdf_path)
    
    # Try PyMuPDF as fallback/enhancement
    text_pymupdf = extract_with_pymupdf(pdf_path)
    
    # Choose the better extraction or combine them
    if len(text_plumber) > len(text_pymupdf) * 1.2:
        final_text = text_plumber
        method = "pdfplumber"
    elif len(text_pymupdf) > len(text_plumber) * 1.2:
        final_text = text_pymupdf
        method = "pymupdf"
    else:
        # Combine both methods for best results
        final_text = combine_extractions(text_plumber, text_pymupdf)
        method = "hybrid"
    
    # Clean the final text
    final_text = clean_extracted_text(final_text)
    
    analysis["extraction_method"] = method
    analysis["final_length"] = len(final_text)
    
    logger.info(f"Extracted {len(final_text)} characters using {method} method")
    return final_text, analysis

def extract_with_pdfplumber(pdf_path: Path) -> str:
    """Extract text using pdfplumber with table and spacing preservation"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_pages = []
            for page in pdf.pages:
                page_content = []
                
                # Extract tables first with better formatting
                tables = page.extract_tables()
                table_areas = []
                
                if tables:
                    for i, table in enumerate(tables):
                        table_md = format_table_as_markdown(table)
                        if table_md:
                            page_content.append(f"\n{table_md}\n")
                            # Track table areas to avoid text overlap
                            try:
                                table_bbox = page.within_bbox(page.bbox).extract_tables()[i]
                                if hasattr(table_bbox, 'bbox'):
                                    table_areas.append(table_bbox.bbox)
                            except:
                                pass
                
                # Extract text with preserved spacing
                chars = page.chars
                if chars:
                    # Group characters by lines based on Y position
                    lines = {}
                    for char in chars:
                        y = round(char['y0'], 1)
                        if y not in lines:
                            lines[y] = []
                        lines[y].append(char)
                    
                    # Sort lines by Y position (top to bottom)
                    sorted_lines = []
                    for y in sorted(lines.keys(), reverse=True):
                        # Sort characters in line by X position
                        line_chars = sorted(lines[y], key=lambda c: c['x0'])
                        line_text = ""
                        prev_x = 0
                        
                        for char in line_chars:
                            # Add spacing based on position
                            if prev_x > 0 and char['x0'] > prev_x + 10:
                                spaces = int((char['x0'] - prev_x) / 6)  # Approximate character width
                                line_text += " " * min(spaces, 10)  # Max 10 spaces
                            
                            line_text += char['text']
                            prev_x = char['x1']
                        
                        if line_text.strip():
                            sorted_lines.append(line_text.rstrip())
                    
                    if sorted_lines:
                        page_content.append("\n".join(sorted_lines))
                else:
                    # Fallback to regular text extraction
                    page_text = page.extract_text(layout=True) or ""
                    if page_text.strip():
                        page_content.append(page_text)
                
                if page_content:
                    text_pages.append("\n\n".join(page_content))
            
            return "\n\n".join(text_pages)
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}")
        return ""

def extract_with_pymupdf(pdf_path: Path) -> str:
    """Extract text using PyMuPDF with enhanced formatting preservation"""
    try:
        doc = fitz.open(str(pdf_path))
        text_pages = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Extract with formatting using dict format
            blocks = page.get_text("dict")
            page_text = format_blocks_with_markdown(blocks)
            
            if page_text.strip():
                text_pages.append(page_text)
        
        doc.close()
        return "\n\n".join(text_pages)
        
    except Exception as e:
        logger.warning(f"PyMuPDF extraction failed: {e}")
        return ""

def format_blocks_with_markdown(blocks: dict) -> str:
    """Convert text blocks to markdown preserving formatting and spacing"""
    markdown_lines = []
    
    for block in blocks.get("blocks", []):
        if "lines" not in block:
            continue
            
        for line in block["lines"]:
            line_text = ""
            prev_x = 0
            
            for span in line.get("spans", []):
                text = span.get("text", "")
                if not text:
                    continue
                    
                # Preserve spacing based on position
                x_pos = span.get("bbox", [0])[0]
                if prev_x > 0 and x_pos > prev_x + 20:  # Significant gap
                    # Add tabs/spaces for alignment
                    gap_size = int((x_pos - prev_x) / 20)
                    line_text += "\t" * min(gap_size, 4)  # Max 4 tabs
                
                # Apply formatting based on span properties
                flags = span.get("flags", 0)
                font_size = span.get("size", 12)
                
                # Bold (flag 16)
                if flags & 16:
                    text = f"**{text}**"
                # Italic (flag 2)
                if flags & 2:
                    text = f"*{text}*"
                # Large text as headers
                if font_size > 16:
                    text = f"# {text}"
                elif font_size > 14:
                    text = f"## {text}"
                    
                line_text += text
                prev_x = span.get("bbox", [0, 0, x_pos])[2]  # Right edge
            
            if line_text.strip():
                markdown_lines.append(line_text.rstrip())
    
    return "\n".join(markdown_lines)

def format_table_as_markdown(table: List[List]) -> str:
    """Convert table data to markdown format with better alignment"""
    if not table or not table[0]:
        return ""
    
    # Clean and prepare table data
    clean_table = []
    for row in table:
        if row and any(str(cell or "").strip() for cell in row):
            clean_row = [str(cell or "").strip() for cell in row]
            clean_table.append(clean_row)
    
    if not clean_table:
        return ""
    
    # Calculate column widths for alignment
    col_widths = [0] * len(clean_table[0])
    for row in clean_table:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))
    
    markdown_lines = []
    
    # Header row
    header_cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(clean_table[0])]
    header = "| " + " | ".join(header_cells) + " |"
    markdown_lines.append(header)
    
    # Separator row with proper alignment
    separator_cells = ["-" * max(3, col_widths[i]) for i in range(len(clean_table[0]))]
    separator = "| " + " | ".join(separator_cells) + " |"
    markdown_lines.append(separator)
    
    # Data rows
    for row in clean_table[1:]:
        if len(row) == len(col_widths):
            data_cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(row)]
            row_text = "| " + " | ".join(data_cells) + " |"
            markdown_lines.append(row_text)
    
    return "\n".join(markdown_lines)

def combine_extractions(text1: str, text2: str) -> str:
    """Intelligently combine two text extractions"""
    if not text1:
        return text2
    if not text2:
        return text1
    
    # Split into lines for comparison
    lines1 = text1.split('\n')
    lines2 = text2.split('\n')
    
    # Use the extraction with more content as base
    if len(lines1) >= len(lines2):
        return text1
    else:
        return text2

def should_use_ocr_enhancement(pdf_path: Path) -> bool:
    """Determine if OCR enhancement is needed"""
    analysis = detect_pdf_text_quality(pdf_path)
    return analysis.get("needs_ocr_enhancement", False) or analysis.get("text_quality", 1.0) < 0.8