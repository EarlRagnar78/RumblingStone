"""
Enhanced Table Detection - Inspired by MarkItDown's form detection
Multi-strategy table detection with intelligent content analysis
"""
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TableDetection:
    """Detected table with metadata"""
    grid: List[List[str]]
    detection_type: str  # "form", "bordered", "ascii"
    confidence: float = 0.0
    
    @property
    def n_rows(self) -> int:
        return len(self.grid)
    
    @property
    def n_cols(self) -> int:
        return max((len(row) for row in self.grid), default=0)

class EnhancedTableDetector:
    """Multi-strategy table detection with form analysis"""
    
    def __init__(self):
        self.partial_numbering = re.compile(r"^\\.\\d+$")
        self.cell_split = re.compile(r"[ \\t]{2,}")
    
    def detect_tables_in_text(self, text: str) -> List[TableDetection]:
        """Detect tables using multiple strategies"""
        lines = [line.strip() for line in text.split('\\n') if line.strip()]
        if len(lines) < 2:
            return []
        
        detections = []
        
        # Strategy 1: Form-style detection (markitdown inspired)
        form_table = self._detect_form_table(lines)
        if form_table:
            detections.append(TableDetection(
                grid=form_table,
                detection_type="form",
                confidence=0.9
            ))
        
        # Strategy 2: Bordered tables
        if not detections:
            bordered = self._detect_bordered_table(lines)
            if bordered:
                detections.append(TableDetection(
                    grid=bordered,
                    detection_type="bordered",
                    confidence=0.8
                ))
        
        # Strategy 3: ASCII tables
        if not detections:
            ascii_table = self._detect_ascii_table(lines)
            if ascii_table:
                detections.append(TableDetection(
                    grid=ascii_table,
                    detection_type="ascii",
                    confidence=0.7
                ))
        
        return detections
    
    def _detect_form_table(self, lines: List[str]) -> Optional[List[List[str]]]:
        """Detect form-style tables by analyzing word positions"""
        # Analyze line structure
        structured_lines = []
        for line in lines:
            # Skip partial numbering lines (e.g., ".1", ".2")
            if self.partial_numbering.match(line.strip()):
                continue
            
            # Split by multiple spaces/tabs
            parts = self.cell_split.split(line)
            if len(parts) >= 3:  # At least 3 columns
                structured_lines.append(parts)
        
        if len(structured_lines) < 3:  # Need at least 3 rows
            return None
        
        # Check if it's structured data (short cells, not paragraphs)
        long_cell_count = 0
        total_cells = 0
        
        for row in structured_lines:
            for cell in row:
                if cell.strip():
                    total_cells += 1
                    if len(cell.strip()) > 30:  # Long text suggests paragraphs
                        long_cell_count += 1
        
        # If >30% cells are long, probably not a table
        if total_cells > 0 and long_cell_count / total_cells > 0.3:
            return None
        
        # Normalize to rectangular grid
        max_cols = max(len(row) for row in structured_lines)
        normalized = []
        for row in structured_lines:
            if len(row) < max_cols:
                row = row + [''] * (max_cols - len(row))
            normalized.append([cell.strip() for cell in row])
        
        return normalized
    
    def _detect_bordered_table(self, lines: List[str]) -> Optional[List[List[str]]]:
        """Detect tables with | or ¦ delimiters"""
        pipe_lines = [line for line in lines if '|' in line or '¦' in line]
        if len(pipe_lines) < 2:
            return None
        
        grid = []
        for line in pipe_lines:
            line = line.replace('¦', '|')
            
            # Skip separator lines
            if re.match(r'^[\\s|:\\-]+$', line):
                continue
            
            cells = [c.strip() for c in line.split('|')]
            
            # Remove empty first/last cells
            if cells and not cells[0]:
                cells = cells[1:]
            if cells and not cells[-1]:
                cells = cells[:-1]
            
            if cells and len(cells) >= 2:
                grid.append(cells)
        
        if len(grid) < 2:
            return None
        
        # Normalize grid
        max_cols = max(len(row) for row in grid)
        normalized = []
        for row in grid:
            if len(row) < max_cols:
                row = row + [''] * (max_cols - len(row))
            normalized.append(row)
        
        return normalized
    
    def _detect_ascii_table(self, lines: List[str]) -> Optional[List[List[str]]]:
        """Detect whitespace-separated tables"""
        split_lines = [self.cell_split.split(line) for line in lines]
        is_row = [len(cells) >= 2 for cells in split_lines]
        
        if sum(is_row) < 2:
            return None
        
        # Find table boundaries
        first_row = next(i for i, flag in enumerate(is_row) if flag)
        last_row = next(i for i in range(len(is_row) - 1, -1, -1) if is_row[i])
        
        core_lines = split_lines[first_row:last_row + 1]
        core_flags = is_row[first_row:last_row + 1]
        
        # Determine column count
        row_counts = [len(cells) for cells, flag in zip(core_lines, core_flags) if flag]
        target_cols = max(set(row_counts), key=row_counts.count)
        
        if target_cols < 2:
            return None
        
        grid = []
        for cells in core_lines:
            if len(cells) < target_cols:
                cells = cells + [''] * (target_cols - len(cells))
            elif len(cells) > target_cols:
                head = cells[:target_cols - 1]
                tail = ' '.join(cells[target_cols - 1:]).strip()
                cells = head + [tail]
            
            cleaned = [c.strip() for c in cells]
            if any(cleaned):
                grid.append(cleaned)
        
        return grid if len(grid) >= 2 else None

def detect_tables_enhanced(text: str) -> List[TableDetection]:
    """Enhanced table detection with form analysis"""
    detector = EnhancedTableDetector()
    return detector.detect_tables_in_text(text)

def format_table_markdown(grid: List[List[str]]) -> str:
    """Format table grid as markdown with proper alignment"""
    if not grid or not grid[0]:
        return ""
    
    n_cols = len(grid[0])
    col_widths = [0] * n_cols
    
    for row in grid:
        for i, cell in enumerate(row):
            if i < n_cols:
                col_widths[i] = max(col_widths[i], len(cell))
    
    lines = []
    
    # Header
    header_cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(grid[0])]
    header = "| " + " | ".join(header_cells) + " |"
    lines.append(header)
    
    # Separator
    separator_cells = ["-" * max(3, col_widths[i]) for i in range(n_cols)]
    separator = "| " + " | ".join(separator_cells) + " |"
    lines.append(separator)
    
    # Data rows
    for row in grid[1:]:
        if len(row) == n_cols:
            data_cells = [cell.ljust(col_widths[i]) for i, cell in enumerate(row)]
            row_text = "| " + " | ".join(data_cells) + " |"
            lines.append(row_text)
    
    return "\\n".join(lines)