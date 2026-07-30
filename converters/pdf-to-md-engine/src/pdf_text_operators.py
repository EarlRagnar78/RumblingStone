"""
ISO 32000-1 Section 9.4.3 Text-Showing Operators Implementation
Handles PDF text operators: Tj, TJ, ', " for accurate text extraction
"""

import fitz
import struct
from typing import List, Tuple, Dict, Any
from loguru import logger

class TextShowingOperators:
    """Handle PDF text-showing operators per ISO 32000-1 9.4.3"""
    
    def __init__(self):
        self.operators = {
            'Tj': self._handle_tj,
            'TJ': self._handle_tj_array, 
            "'": self._handle_quote,
            '"': self._handle_double_quote
        }
    
    def extract_text_with_operators(self, page) -> str:
        """Extract text using text-showing operators"""
        try:
            # Get raw page content - can be None, int (xref), or list
            content = page.get_contents()
            if not content:
                return page.get_text()
            
            content_bytes = b''
            
            # Handle different content types
            if isinstance(content, list):
                for item in content:
                    if isinstance(item, int):  # xref number
                        try:
                            stream = page.parent.xref_stream(item)
                            content_bytes += stream
                        except:
                            continue
                    elif hasattr(item, 'get_data'):
                        content_bytes += item.get_data()
            elif isinstance(content, int):  # Single xref
                try:
                    content_bytes = page.parent.xref_stream(content)
                except:
                    return page.get_text()
            elif hasattr(content, 'get_data'):
                content_bytes = content.get_data()
            else:
                return page.get_text()
            
            if not content_bytes:
                return page.get_text()
            
            # Parse content stream for text operators
            text_parts = []
            lines = content_bytes.decode('latin-1', errors='ignore').split('\n')
            
            for line in lines:
                line = line.strip()
                if any(op in line for op in self.operators.keys()):
                    extracted = self._parse_text_operator(line)
                    if extracted:
                        text_parts.append(extracted)
            
            return '\n'.join(text_parts) if text_parts else page.get_text()
            
        except Exception:
            return page.get_text()
    
    def _parse_text_operator(self, line: str) -> str:
        """Parse individual text operator line"""
        try:
            # Handle Tj operator: (string) Tj
            if line.endswith(' Tj'):
                return self._extract_string_from_tj(line)
            
            # Handle TJ operator: [(string) offset ...] TJ  
            elif line.endswith(' TJ'):
                return self._extract_string_from_tj_array(line)
            
            # Handle ' operator: (string) '
            elif line.endswith(" '"):
                return self._extract_string_from_quote(line)
            
            # Handle " operator: aw ac (string) "
            elif line.endswith(' "'):
                return self._extract_string_from_double_quote(line)
                
        except Exception:
            pass
        return ""
    
    def _extract_string_from_tj(self, line: str) -> str:
        """Extract string from Tj operator: (string) Tj"""
        # Find string in parentheses
        start = line.find('(')
        end = line.rfind(')')
        if start >= 0 and end > start:
            return self._decode_pdf_string(line[start+1:end])
        return ""
    
    def _extract_string_from_tj_array(self, line: str) -> str:
        """Extract strings from TJ array: [(string) offset ...] TJ"""
        # Find array brackets
        start = line.find('[')
        end = line.rfind(']')
        if start >= 0 and end > start:
            array_content = line[start+1:end]
            strings = []
            
            # Extract strings from array
            i = 0
            while i < len(array_content):
                if array_content[i] == '(':
                    # Find matching closing parenthesis
                    paren_count = 1
                    j = i + 1
                    while j < len(array_content) and paren_count > 0:
                        if array_content[j] == '(':
                            paren_count += 1
                        elif array_content[j] == ')':
                            paren_count -= 1
                        j += 1
                    
                    if paren_count == 0:
                        string_content = array_content[i+1:j-1]
                        decoded = self._decode_pdf_string(string_content)
                        if decoded:
                            strings.append(decoded)
                        i = j
                    else:
                        i += 1
                else:
                    i += 1
            
            return ''.join(strings)
        return ""
    
    def _extract_string_from_quote(self, line: str) -> str:
        """Extract string from ' operator: (string) '"""
        return self._extract_string_from_tj(line)
    
    def _extract_string_from_double_quote(self, line: str) -> str:
        """Extract string from " operator: aw ac (string) " """
        # Find the last string in parentheses
        parts = line.split('(')
        if len(parts) >= 2:
            last_part = parts[-1]
            end = last_part.find(')')
            if end >= 0:
                return self._decode_pdf_string(last_part[:end])
        return ""
    
    def _decode_pdf_string(self, pdf_string: str) -> str:
        """Decode PDF string with proper encoding handling"""
        if not pdf_string:
            return ""
        
        try:
            # Handle escape sequences
            decoded = pdf_string.replace('\\n', '\n')
            decoded = decoded.replace('\\r', '\r') 
            decoded = decoded.replace('\\t', '\t')
            decoded = decoded.replace('\\b', '\b')
            decoded = decoded.replace('\\f', '\f')
            decoded = decoded.replace('\\(', '(')
            decoded = decoded.replace('\\)', ')')
            decoded = decoded.replace('\\\\', '\\')
            
            # Handle octal sequences \nnn
            import re
            def replace_octal(match):
                octal_str = match.group(1)
                try:
                    char_code = int(octal_str, 8)
                    return chr(char_code) if char_code < 256 else ''
                except:
                    return match.group(0)
            
            decoded = re.sub(r'\\([0-7]{1,3})', replace_octal, decoded)
            
            return decoded
            
        except Exception:
            return pdf_string
    
    def _handle_tj(self, operands: List) -> str:
        """Handle Tj operator"""
        if operands and isinstance(operands[0], str):
            return self._decode_pdf_string(operands[0])
        return ""
    
    def _handle_tj_array(self, operands: List) -> str:
        """Handle TJ operator with array"""
        if not operands or not isinstance(operands[0], list):
            return ""
        
        text_parts = []
        for item in operands[0]:
            if isinstance(item, str):
                decoded = self._decode_pdf_string(item)
                if decoded:
                    text_parts.append(decoded)
        
        return ''.join(text_parts)
    
    def _handle_quote(self, operands: List) -> str:
        """Handle ' operator (move to next line and show text)"""
        return self._handle_tj(operands)
    
    def _handle_double_quote(self, operands: List) -> str:
        """Handle " operator (set word/char spacing and show text)"""
        # Last operand is the text string
        if len(operands) >= 3:
            return self._decode_pdf_string(operands[2])
        return ""

def extract_text_with_operators(page) -> str:
    """Extract text using ISO 32000-1 text-showing operators"""
    extractor = TextShowingOperators()
    return extractor.extract_text_with_operators(page)