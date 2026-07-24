"""
Layout-Preserving PDF Processor
Inspired by marker, pdfplumber, and pymupdf4llm for better layout retention
"""

import fitz
import pdfplumber
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from loguru import logger

@dataclass
class LayoutElement:
    """Represents a layout element with position and type"""
    text: str
    bbox: Tuple[float, float, float, float]  # x0, y0, x1, y1
    element_type: str  # 'text', 'table', 'image', 'header', 'footer'
    font_size: float = 0.0
    is_bold: bool = False
    page_num: int = 0

class LayoutPreservingProcessor:
    """Process PDF while maintaining layout structure"""
    
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
    
    def extract_with_layout(self) -> str:
        """Extract text preserving layout structure"""
        markdown_parts = []
        
        for page_num in range(len(self.doc)):
            page_md = self._process_page_layout(page_num)
            if page_md:
                markdown_parts.append(page_md)
        
        return "\n\n---\n\n".join(markdown_parts)
    
    def _process_page_layout(self, page_num: int) -> str:
        """Process single page preserving layout"""
        elements = self._extract_layout_elements(page_num)
        return self._elements_to_markdown(elements)
    
    def _extract_layout_elements(self, page_num: int) -> List[LayoutElement]:
        """Extract layout elements from page with column detection"""
        elements = []
        page = self.doc[page_num]
        plumber_page = self.plumber_pdf.pages[page_num]
        
        # Extract tables first (highest priority)
        tables = plumber_page.extract_tables()
        for table in tables:
            if table:
                table_bbox = self._get_table_bbox(plumber_page, table)
                table_md = self._table_to_markdown(table)
                elements.append(LayoutElement(
                    text=table_md,
                    bbox=table_bbox,
                    element_type='table',
                    page_num=page_num
                ))
        
        # Extract text blocks with column detection
        text_elements = self._extract_text_with_columns(page, page_num, elements)
        elements.extend(text_elements)
        
        # Sort by reading order (columns, then top-to-bottom)
        elements = self._sort_by_reading_order(elements)
        
        return elements
    
    def _extract_text_with_columns(self, page, page_num: int, existing_elements: List[LayoutElement]) -> List[LayoutElement]:
        """Extract text blocks with column detection and formatting preservation"""
        text_elements = []
        blocks = page.get_text("dict")
        
        # Group blocks by columns
        page_width = page.rect.width
        column_threshold = page_width / 3  # Detect 2+ column layouts
        
        left_column = []
        right_column = []
        full_width = []
        
        for block in blocks.get("blocks", []):
            if "lines" not in block:
                continue
                
            block_bbox = block.get("bbox", (0, 0, 0, 0))
            
            # Skip if overlaps with existing elements
            if self._overlaps_with_elements(block_bbox, existing_elements):
                continue
            
            block_text, max_font_size, is_bold, is_italic = self._extract_block_text_with_formatting(block)
            if not block_text.strip():
                continue
            
            element_type = self._classify_text_element(block_text, max_font_size, block_bbox, page.rect)
            
            element = LayoutElement(
                text=block_text.strip(),
                bbox=block_bbox,
                element_type=element_type,
                font_size=max_font_size,
                is_bold=is_bold,
                page_num=page_num
            )
            
            # Column detection
            x_center = (block_bbox[0] + block_bbox[2]) / 2
            block_width = block_bbox[2] - block_bbox[0]
            
            if block_width > page_width * 0.7:  # Full width
                full_width.append(element)
            elif x_center < column_threshold:  # Left column
                left_column.append(element)
            else:  # Right column
                right_column.append(element)
        
        # Sort each column by Y position
        left_column.sort(key=lambda e: e.bbox[1])
        right_column.sort(key=lambda e: e.bbox[1])
        full_width.sort(key=lambda e: e.bbox[1])
        
        # Combine in reading order
        text_elements.extend(full_width)
        text_elements.extend(left_column)
        text_elements.extend(right_column)
        
        return text_elements
    
    def _extract_block_text_with_formatting(self, block) -> Tuple[str, float, bool, bool]:
        """Extract text from block with formatting and spacing preservation"""
        block_text = ""
        max_font_size = 0
        is_bold = False
        is_italic = False
        
        for line in block["lines"]:
            line_text = ""
            prev_x = 0
            
            for span in line.get("spans", []):
                span_text = span.get("text", "")
                if span_text:
                    # Preserve spacing based on position
                    x_pos = span.get("bbox", [0])[0]
                    if prev_x > 0 and x_pos > prev_x + 15:  # Significant gap
                        # Add spaces for alignment
                        gap_size = int((x_pos - prev_x) / 8)  # Approximate character width
                        line_text += " " * min(gap_size, 8)  # Max 8 spaces
                    
                    flags = span.get("flags", 0)
                    
                    # Apply markdown formatting
                    if flags & 16:  # Bold
                        span_text = f"**{span_text}**"
                        is_bold = True
                    if flags & 2:   # Italic
                        span_text = f"*{span_text}*"
                        is_italic = True
                    
                    line_text += span_text
                    max_font_size = max(max_font_size, span.get("size", 0))
                    prev_x = span.get("bbox", [0, 0, x_pos])[2]  # Right edge
            
            if line_text.strip():
                block_text += line_text.rstrip() + "\n"
        
        return block_text, max_font_size, is_bold, is_italic
    
    def _sort_by_reading_order(self, elements: List[LayoutElement]) -> List[LayoutElement]:
        """Sort elements by natural reading order"""
        # Group by approximate Y position (rows)
        rows = {}
        for element in elements:
            y_pos = int(element.bbox[1] / 20) * 20  # Group by 20px rows
            if y_pos not in rows:
                rows[y_pos] = []
            rows[y_pos].append(element)
        
        # Sort each row by X position, then combine rows
        sorted_elements = []
        for y_pos in sorted(rows.keys()):
            row_elements = sorted(rows[y_pos], key=lambda e: e.bbox[0])
            sorted_elements.extend(row_elements)
        
        return sorted_elements
    
    def _classify_text_element(self, text: str, font_size: float, bbox: Tuple, page_rect) -> str:
        """Classify text element type based on position and formatting"""
        page_height = page_rect.height
        y_pos = bbox[1]
        
        # Header detection (top 10% of page)
        if y_pos < page_height * 0.1:
            return 'header'
        
        # Footer detection (bottom 10% of page)
        if y_pos > page_height * 0.9:
            return 'footer'
        
        # Title detection (large font, short text)
        if font_size > 16 and len(text.split()) < 10:
            return 'title'
        
        # Heading detection (medium font, caps or title case)
        if font_size > 12 and (text.isupper() or text.istitle()):
            return 'heading'
        
        return 'text'
    
    def _overlaps_with_elements(self, bbox: Tuple, elements: List[LayoutElement]) -> bool:
        """Check if bbox overlaps with existing elements"""
        x0, y0, x1, y1 = bbox
        
        for element in elements:
            ex0, ey0, ex1, ey1 = element.bbox
            
            # Check overlap
            if not (x1 < ex0 or x0 > ex1 or y1 < ey0 or y0 > ey1):
                return True
        
        return False
    
    def _get_table_bbox(self, page, table) -> Tuple[float, float, float, float]:
        """Get bounding box for table"""
        # Simplified bbox calculation
        return (0, 0, page.width, page.height * 0.3)  # Estimate
    
    def _table_to_markdown(self, table: List[List]) -> str:
        """Convert table to markdown format"""
        if not table or not table[0]:
            return ""
        
        lines = []
        
        # Header
        header = "| " + " | ".join(str(cell or "").strip() for cell in table[0]) + " |"
        lines.append(header)
        
        # Separator
        separator = "| " + " | ".join("---" for _ in table[0]) + " |"
        lines.append(separator)
        
        # Data rows
        for row in table[1:]:
            if row:
                row_text = "| " + " | ".join(str(cell or "").strip() for cell in row) + " |"
                lines.append(row_text)
        
        return "\n".join(lines)
    
    def _elements_to_markdown(self, elements: List[LayoutElement]) -> str:
        """Convert layout elements to markdown preserving structure"""
        markdown_parts = []
        current_column = None
        
        for element in elements:
            # Detect column changes for multi-column layouts
            if self._is_column_break(element, current_column):
                if current_column is not None:
                    markdown_parts.append("\n---\n")  # Column separator
                current_column = element.bbox[0]  # X position
            
            if element.element_type == 'table':
                markdown_parts.append(element.text)
            
            elif element.element_type == 'title':
                markdown_parts.append(f"# {element.text}")
            
            elif element.element_type == 'heading':
                level = 2 if element.font_size > 14 else 3
                markdown_parts.append(f"{'#' * level} {element.text}")
            
            elif element.element_type == 'header':
                markdown_parts.append(f"*{element.text}*")
            
            elif element.element_type == 'footer':
                markdown_parts.append(f"_{element.text}_")
            
            elif element.element_type == 'text':
                # Preserve paragraph structure and formatting
                text = self._format_text_block(element.text, element.is_bold)
                markdown_parts.append(text)
        
        return "\n\n".join(filter(None, markdown_parts))
    
    def _is_column_break(self, element: LayoutElement, current_column: Optional[float]) -> bool:
        """Detect if element starts a new column"""
        if current_column is None:
            return False
        
        # Significant X position change indicates column break
        x_diff = abs(element.bbox[0] - current_column)
        return x_diff > 100  # 100px threshold
    
    def _format_text_block(self, text: str, is_bold: bool) -> str:
        """Format text block preserving line breaks and emphasis"""
        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        formatted_paragraphs = []
        for para in paragraphs:
            # Clean up line breaks within paragraphs
            para = ' '.join(para.split())
            
            if is_bold and len(para) < 200:  # Short bold text
                formatted_paragraphs.append(f"**{para}**")
            else:
                formatted_paragraphs.append(para)
        
        return '\n\n'.join(formatted_paragraphs)

def extract_pdf_with_layout(pdf_path: Path) -> str:
    """Extract PDF preserving layout structure"""
    try:
        with LayoutPreservingProcessor(pdf_path) as processor:
            return processor.extract_with_layout()
    except Exception as e:
        logger.error(f"Layout extraction failed: {e}")
        return ""