"""
Math-Aware Text Processing - Inspired by pdfmd
Handles mathematical expressions, equations, and Unicode math symbols
"""
import re
from typing import Dict, List, Tuple
from loguru import logger

class MathProcessor:
    """Process mathematical content in PDF text"""
    
    def __init__(self):
        # Unicode to LaTeX mappings from pdfmd
        self.unicode_math_map = {
            # Greek letters
            'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta',
            'ε': r'\epsilon', 'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta',
            'ι': r'\iota', 'κ': r'\kappa', 'λ': r'\lambda', 'μ': r'\mu',
            'ν': r'\nu', 'ξ': r'\xi', 'π': r'\pi', 'ρ': r'\rho',
            'σ': r'\sigma', 'τ': r'\tau', 'υ': r'\upsilon', 'φ': r'\phi',
            'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
            
            # Uppercase Greek
            'Α': r'\Alpha', 'Β': r'\Beta', 'Γ': r'\Gamma', 'Δ': r'\Delta',
            'Ε': r'\Epsilon', 'Ζ': r'\Zeta', 'Η': r'\Eta', 'Θ': r'\Theta',
            'Ι': r'\Iota', 'Κ': r'\Kappa', 'Λ': r'\Lambda', 'Μ': r'\Mu',
            'Ν': r'\Nu', 'Ξ': r'\Xi', 'Π': r'\Pi', 'Ρ': r'\Rho',
            'Σ': r'\Sigma', 'Τ': r'\Tau', 'Υ': r'\Upsilon', 'Φ': r'\Phi',
            'Χ': r'\Chi', 'Ψ': r'\Psi', 'Ω': r'\Omega',
            
            # Mathematical operators
            '∫': r'\int', '∑': r'\sum', '∏': r'\prod', '√': r'\sqrt',
            '∂': r'\partial', '∇': r'\nabla', '∞': r'\infty',
            '±': r'\pm', '∓': r'\mp', '×': r'\times', '÷': r'\div',
            '≤': r'\leq', '≥': r'\geq', '≠': r'\neq', '≈': r'\approx',
            '≡': r'\equiv', '∈': r'\in', '∉': r'\notin', '⊂': r'\subset',
            '⊃': r'\supset', '∪': r'\cup', '∩': r'\cap', '∅': r'\emptyset',
            
            # Arrows
            '→': r'\rightarrow', '←': r'\leftarrow', '↑': r'\uparrow',
            '↓': r'\downarrow', '↔': r'\leftrightarrow', '⇒': r'\Rightarrow',
            '⇐': r'\Leftarrow', '⇔': r'\Leftrightarrow',
        }
        
        # Superscript/subscript mappings
        self.superscript_map = {
            '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5',
            '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁺': '+', '⁻': '-',
            '⁼': '=', '⁽': '(', '⁾': ')', 'ⁿ': 'n', 'ⁱ': 'i'
        }
        
        self.subscript_map = {
            '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
            '₆': '6', '₇': '7', '₈': '8', '₉': '9', '₊': '+', '₋': '-',
            '₌': '=', '₍': '(', '₎': ')', 'ₙ': 'n', 'ᵢ': 'i'
        }
    
    def process_math_content(self, text: str) -> str:
        """Process mathematical content in text"""
        # Detect and preserve existing LaTeX
        text = self._preserve_existing_latex(text)
        
        # Convert Unicode math to LaTeX
        text = self._convert_unicode_math(text)
        
        # Handle superscripts and subscripts
        text = self._convert_super_subscripts(text)
        
        # Detect and wrap math regions
        text = self._wrap_math_regions(text)
        
        return text
    
    def _preserve_existing_latex(self, text: str) -> str:
        """Preserve existing LaTeX math expressions"""
        # Already wrapped math should be preserved
        return text
    
    def _convert_unicode_math(self, text: str) -> str:
        """Convert Unicode math symbols to LaTeX"""
        for unicode_char, latex in self.unicode_math_map.items():
            text = text.replace(unicode_char, latex)
        return text
    
    def _convert_super_subscripts(self, text: str) -> str:
        """Convert Unicode superscripts/subscripts to LaTeX"""
        # Convert superscripts
        for sup_char, normal in self.superscript_map.items():
            if sup_char in text:
                # Find the base character before superscript
                pattern = r'(\w)' + re.escape(sup_char)
                text = re.sub(pattern, r'\1^{' + normal + '}', text)
        
        # Convert subscripts
        for sub_char, normal in self.subscript_map.items():
            if sub_char in text:
                # Find the base character before subscript
                pattern = r'(\w)' + re.escape(sub_char)
                text = re.sub(pattern, r'\1_{' + normal + '}', text)
        
        return text
    
    def _wrap_math_regions(self, text: str) -> str:
        """Detect and wrap mathematical regions with LaTeX delimiters"""
        lines = text.split('\n')
        processed_lines = []
        
        for line in lines:
            if self._is_math_line(line):
                # Wrap display math
                if not line.strip().startswith('$'):
                    line = f"$${line.strip()}$$"
            else:
                # Handle inline math
                line = self._wrap_inline_math(line)
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _is_math_line(self, line: str) -> bool:
        """Detect if a line contains primarily mathematical content"""
        line = line.strip()
        if not line:
            return False
        
        # Check for math indicators
        math_indicators = [
            r'\\[a-zA-Z]+',  # LaTeX commands
            r'\^{.*?}',      # Superscripts
            r'_{.*?}',       # Subscripts
            r'\\int',        # Integrals
            r'\\sum',        # Summations
            r'\\frac',       # Fractions
        ]
        
        math_count = sum(1 for pattern in math_indicators if re.search(pattern, line))
        total_chars = len(line)
        
        # If more than 30% of content is math-related
        return math_count > 0 and (math_count / max(total_chars / 10, 1)) > 0.3
    
    def _wrap_inline_math(self, line: str) -> str:
        """Wrap inline mathematical expressions"""
        # Look for mathematical expressions in text
        math_patterns = [
            r'([a-zA-Z]\^{[^}]+})',  # Variables with superscripts
            r'([a-zA-Z]_{[^}]+})',   # Variables with subscripts
            r'(\\[a-zA-Z]+(?:{[^}]*})*)',  # LaTeX commands
        ]
        
        for pattern in math_patterns:
            matches = re.finditer(pattern, line)
            for match in reversed(list(matches)):  # Reverse to maintain positions
                start, end = match.span()
                math_expr = match.group(1)
                if not (line[max(0, start-1)] == '$' or line[min(len(line)-1, end)] == '$'):
                    line = line[:start] + f'${math_expr}$' + line[end:]
        
        return line

class TableProcessor:
    """Enhanced table processing inspired by pdfmd"""
    
    def __init__(self):
        self.table_patterns = [
            r'\|.*\|',  # Pipe-separated
            r'[\t ]{2,}',  # Tab/space separated
        ]
    
    def detect_tables(self, text: str) -> List[Tuple[int, int]]:
        """Detect table regions in text"""
        lines = text.split('\n')
        table_regions = []
        current_table_start = None
        
        for i, line in enumerate(lines):
            if self._is_table_line(line):
                if current_table_start is None:
                    current_table_start = i
            else:
                if current_table_start is not None:
                    # End of table
                    if i - current_table_start >= 2:  # Minimum 2 lines for table
                        table_regions.append((current_table_start, i-1))
                    current_table_start = None
        
        # Handle table at end of text
        if current_table_start is not None:
            table_regions.append((current_table_start, len(lines)-1))
        
        return table_regions
    
    def _is_table_line(self, line: str) -> bool:
        """Check if line appears to be part of a table"""
        line = line.strip()
        if not line:
            return False
        
        # Check for table indicators
        if '|' in line and line.count('|') >= 2:
            return True
        
        # Check for multiple columns separated by spaces/tabs
        parts = re.split(r'\s{2,}', line)
        return len(parts) >= 3
    
    def format_table_markdown(self, lines: List[str]) -> str:
        """Format detected table as markdown"""
        if not lines:
            return ""
        
        # Determine if pipe-separated or space-separated
        if '|' in lines[0]:
            return self._format_pipe_table(lines)
        else:
            return self._format_space_table(lines)
    
    def _format_pipe_table(self, lines: List[str]) -> str:
        """Format pipe-separated table"""
        formatted_lines = []
        
        for i, line in enumerate(lines):
            # Clean up the line
            line = line.strip()
            if not line.startswith('|'):
                line = '|' + line
            if not line.endswith('|'):
                line = line + '|'
            
            formatted_lines.append(line)
            
            # Add separator after header
            if i == 0:
                cols = line.count('|') - 1
                separator = '|' + '---|' * cols
                formatted_lines.append(separator)
        
        return '\n'.join(formatted_lines)
    
    def _format_space_table(self, lines: List[str]) -> str:
        """Format space-separated table as pipe table"""
        rows = []
        
        for line in lines:
            parts = re.split(r'\s{2,}', line.strip())
            rows.append(parts)
        
        if not rows:
            return ""
        
        # Create markdown table
        formatted_lines = []
        
        # Header
        header = '| ' + ' | '.join(rows[0]) + ' |'
        formatted_lines.append(header)
        
        # Separator
        separator = '|' + '---|' * len(rows[0])
        formatted_lines.append(separator)
        
        # Data rows
        for row in rows[1:]:
            # Pad row to match header length
            while len(row) < len(rows[0]):
                row.append('')
            
            row_line = '| ' + ' | '.join(row) + ' |'
            formatted_lines.append(row_line)
        
        return '\n'.join(formatted_lines)

def process_enhanced_text(text: str) -> str:
    """Process text with math, table, and transformation enhancements"""
    # First apply text transformations (header/footer removal, etc.)
    from .enhanced_text_transformer import transform_text_enhanced
    text = transform_text_enhanced(text)
    
    # Process mathematical content
    math_processor = MathProcessor()
    text = math_processor.process_math_content(text)
    
    # Process tables with enhanced detection (markitdown inspired)
    from .enhanced_table_detector import detect_tables_enhanced, format_table_markdown
    table_detections = detect_tables_enhanced(text)
    
    if table_detections:
        # Replace detected tables with formatted markdown
        for detection in reversed(table_detections):  # Reverse to maintain positions
            if detection.grid:
                formatted_table = format_table_markdown(detection.grid)
                # Simple replacement - enhanced version would use better text mapping
                table_text = '\n'.join('|'.join(row) for row in detection.grid)
                text = text.replace(table_text, formatted_table)
    
    return text