"""
Enhanced Image Extractor
Inspired by marker, pix2text, and pymupdf for comprehensive image extraction
"""

import fitz
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from loguru import logger
from PIL import Image
import io

@dataclass
class ExtractedImage:
    """Represents an extracted image with metadata"""
    path: Path
    bbox: Tuple[float, float, float, float]
    page_num: int
    image_type: str  # 'figure', 'diagram', 'photo', 'chart'
    confidence: float = 1.0
    width: int = 0
    height: int = 0

class EnhancedImageExtractor:
    """Extract and classify images from PDF with quality filtering"""
    
    def __init__(self, pdf_path: Path, output_dir: Path):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.doc = None
        
    def __enter__(self):
        self.doc = fitz.open(str(self.pdf_path))
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.doc:
            self.doc.close()
    
    def extract_all_images(self) -> List[ExtractedImage]:
        """Extract all quality images from PDF with merging"""
        extracted_images = []
        
        for page_num in range(len(self.doc)):
            page_images = self._extract_page_images(page_num)
            extracted_images.extend(page_images)
        
        # Merge adjacent images that might be parts of larger images
        merged_images = self._merge_adjacent_images(extracted_images)
        
        logger.info(f"Extracted {len(extracted_images)} images, merged to {len(merged_images)}")
        return merged_images
    
    def _merge_adjacent_images(self, images: List[ExtractedImage]) -> List[ExtractedImage]:
        """Merge related images on same page with position analysis"""
        if len(images) < 2:
            return images
        
        # Group by page
        pages = {}
        for img in images:
            if img.page_num not in pages:
                pages[img.page_num] = []
            pages[img.page_num].append(img)
        
        merged = []
        for page_num, page_images in pages.items():
            merged.extend(self._merge_page_images(page_images, page_num))
        
        return merged
    
    def _merge_page_images(self, page_images: List[ExtractedImage], page_num: int) -> List[ExtractedImage]:
        """Merge related images on single page"""
        if len(page_images) < 2:
            return page_images
        
        merged = []
        processed = set()
        
        for i, img in enumerate(page_images):
            if i in processed:
                continue
            
            group = [img]
            group_indices = {i}
            
            # Find spatially related images
            for j, other in enumerate(page_images):
                if j in processed or j == i:
                    continue
                if self._are_related(img, other):
                    group.append(other)
                    group_indices.add(j)
            
            processed.update(group_indices)
            
            if len(group) > 1:
                merged_img = self._create_merged_image(group, page_num)
                merged.append(merged_img if merged_img else group[0])
            else:
                merged.append(img)
        
        return merged
    
    def _are_related(self, img1: ExtractedImage, img2: ExtractedImage) -> bool:
        """Check if images are spatially related"""
        x1, y1, x2, y2 = img1.bbox
        x3, y3, x4, y4 = img2.bbox
        
        # Adjacent horizontally or vertically
        h_gap = min(abs(x2 - x3), abs(x4 - x1))
        v_gap = min(abs(y2 - y3), abs(y4 - y1))
        h_aligned = abs((y1 + y2)/2 - (y3 + y4)/2) < 15
        v_aligned = abs((x1 + x2)/2 - (x3 + x4)/2) < 15
        
        return (h_aligned and h_gap < 20) or (v_aligned and v_gap < 20)
    
    def _create_merged_image(self, images: List[ExtractedImage], page_num: int) -> Optional[ExtractedImage]:
        """Create merged image with position metadata"""
        try:
            from PIL import Image
            import json
            
            # Calculate canvas
            min_x = min(img.bbox[0] for img in images)
            min_y = min(img.bbox[1] for img in images)
            max_x = max(img.bbox[2] for img in images)
            max_y = max(img.bbox[3] for img in images)
            
            canvas_width = int(max_x - min_x)
            canvas_height = int(max_y - min_y)
            merged_img = Image.new('RGB', (canvas_width, canvas_height), 'white')
            
            # Track sources
            sources = []
            
            # Place images
            for img in images:
                pil_img = Image.open(img.path)
                rel_x = int(img.bbox[0] - min_x)
                rel_y = int(img.bbox[1] - min_y)
                merged_img.paste(pil_img, (rel_x, rel_y))
                
                sources.append({
                    'file': img.path.name,
                    'position': (rel_x, rel_y),
                    'size': (img.width, img.height),
                    'pdf_bbox': img.bbox
                })
                pil_img.close()
            
            # Save merged image and metadata
            merged_path = self.output_dir / f"merged_p{page_num:03d}_{len(images)}imgs.png"
            merged_img.save(merged_path)
            merged_img.close()
            
            # Save metadata
            with open(merged_path.with_suffix('.json'), 'w') as f:
                json.dump({
                    'page': page_num,
                    'sources': sources,
                    'canvas': (canvas_width, canvas_height),
                    'pdf_bbox': (min_x, min_y, max_x, max_y)
                }, f, indent=2)
            
            # Clean up originals
            for img in images:
                img.path.unlink(missing_ok=True)
            
            return ExtractedImage(
                path=merged_path,
                bbox=(min_x, min_y, max_x, max_y),
                page_num=page_num,
                image_type='merged',
                width=canvas_width,
                height=canvas_height
            )
            
        except Exception as e:
            logger.error(f"Merge failed: {e}")
            return None
    
    def _extract_page_images(self, page_num: int) -> List[ExtractedImage]:
        """Extract images from a single page"""
        page = self.doc[page_num]
        images = []
        
        # Get image list from page
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            try:
                # Extract image data
                xref = img[0]
                pix = fitz.Pixmap(self.doc, xref)
                
                # Skip small or low-quality images
                if not self._is_quality_image(pix):
                    pix = None
                    continue
                
                # Handle colorspace conversion
                if pix.n - pix.alpha > 3:  # CMYK or other complex colorspace
                    # Convert to RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                elif pix.n - pix.alpha == 1:  # Grayscale
                    # Convert to RGB for consistency
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                
                # Save image with proper format
                image_path = self.output_dir / f"page_{page_num:03d}_img_{img_index:03d}.png"
                
                # Use tobytes with PNG format for better compatibility
                img_data = pix.tobytes("png")
                with open(image_path, "wb") as f:
                    f.write(img_data)
                
                # Get image position on page
                img_rects = page.get_image_rects(xref)
                bbox = img_rects[0] if img_rects else page.rect
                
                # Classify image type
                image_type = self._classify_image(pix, image_path)
                
                extracted_image = ExtractedImage(
                    path=image_path,
                    bbox=(bbox.x0, bbox.y0, bbox.x1, bbox.y1),
                    page_num=page_num,
                    image_type=image_type,
                    width=pix.width,
                    height=pix.height
                )
                
                images.append(extracted_image)
                pix = None
                
            except Exception as e:
                logger.debug(f"Skipped image {img_index} from page {page_num}: {e}")
                continue
        
        return images
    
    def _is_quality_image(self, pix) -> bool:
        """Filter out low-quality or irrelevant images"""
        # Skip very small images (likely icons or decorations)
        if pix.width < 50 or pix.height < 50:
            return False
        
        # Skip very large images that are likely full-page scans
        if pix.width > 2000 and pix.height > 2000:
            return False
        
        # Check color space (skip if not RGB or grayscale)
        if pix.n - pix.alpha > 4:  # More than CMYK
            return False
        
        return True
    
    def _classify_image(self, pix, image_path: Path) -> str:
        """Classify image type using basic computer vision"""
        try:
            # Get image dimensions and basic properties
            height, width = pix.height, pix.width
            aspect_ratio = width / height
            
            # Convert pixmap to numpy array for analysis
            img_data = pix.tobytes("png")
            nparr = np.frombuffer(img_data, np.uint8)
            cv_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if cv_img is None:
                return 'unknown'
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            
            # Calculate image statistics
            mean_intensity = np.mean(gray)
            std_intensity = np.std(gray)
            
            # Edge detection for complexity analysis
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (width * height)
            
            # Classification logic
            if aspect_ratio > 2.0 or aspect_ratio < 0.5:
                return 'diagram'  # Wide or tall images are likely diagrams
            elif edge_density > 0.1:
                return 'chart'    # High edge density suggests charts/graphs
            elif std_intensity < 30:
                return 'diagram'  # Low variation suggests simple diagrams
            elif mean_intensity > 200:
                return 'figure'   # Bright images are likely figures
            else:
                return 'photo'    # Default to photo
                
        except Exception as e:
            logger.debug(f"Image classification failed: {e}")
            return 'unknown'
    
    def generate_markdown_references(self, images: List[ExtractedImage]) -> str:
        """Generate markdown with merge info"""
        if not images:
            return ""
        
        markdown_parts = ["\n## 📷 Extracted Images\n"]
        
        # Group by page
        pages = {}
        for img in images:
            if img.page_num not in pages:
                pages[img.page_num] = []
            pages[img.page_num].append(img)
        
        for page_num in sorted(pages.keys()):
            page_images = pages[page_num]
            markdown_parts.append(f"### Page {page_num + 1}\n")
            
            for img in page_images:
                rel_path = f"assets/{img.path.name}"
                
                if img.image_type == 'merged':
                    metadata_path = img.path.with_suffix('.json')
                    if metadata_path.exists():
                        try:
                            import json
                            with open(metadata_path) as f:
                                data = json.load(f)
                            
                            source_count = len(data.get('sources', []))
                            markdown_parts.append(f"![Merged Image]({rel_path})")
                            markdown_parts.append(f"*Merged from {source_count} images - {img.width}x{img.height}px*")
                            
                            markdown_parts.append("\n**Sources:**")
                            for i, src in enumerate(data.get('sources', []), 1):
                                pos = src.get('position', (0, 0))
                                size = src.get('size', (0, 0))
                                markdown_parts.append(f"- {i}. {src.get('file', 'unknown')} at ({pos[0]}, {pos[1]}) - {size[0]}x{size[1]}px")
                            markdown_parts.append("")
                            
                        except Exception:
                            markdown_parts.append(f"![{img.image_type.title()}]({rel_path})")
                            markdown_parts.append(f"*{img.image_type.title()} - {img.width}x{img.height}px*\n")
                    else:
                        markdown_parts.append(f"![{img.image_type.title()}]({rel_path})")
                        markdown_parts.append(f"*{img.image_type.title()} - {img.width}x{img.height}px*\n")
                else:
                    markdown_parts.append(f"![{img.image_type.title()}]({rel_path})")
                    markdown_parts.append(f"*{img.image_type.title()} - {img.width}x{img.height}px*\n")
        
        return "\n".join(markdown_parts)

def extract_images_enhanced(pdf_path: Path, output_dir: Path) -> Tuple[List[ExtractedImage], str]:
    """Enhanced image extraction with classification and markdown generation"""
    try:
        with EnhancedImageExtractor(pdf_path, output_dir) as extractor:
            images = extractor.extract_all_images()
            markdown_refs = extractor.generate_markdown_references(images)
            return images, markdown_refs
    except Exception as e:
        logger.error(f"Enhanced image extraction failed: {e}")
        return [], ""