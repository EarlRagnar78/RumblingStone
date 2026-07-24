#!/usr/bin/env python3
"""
HTML to Markdown Converter with WebP Image Processing
System Engineering Best Practices Implementation

Features:
- Converts HTML files/folders to Markdown
- Converts images to WebP format
- Robust error handling and logging
- Configuration management
- Progress tracking
- Atomic operations with rollback
"""

import argparse
import logging
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

try:
    import html2text
    from PIL import Image
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Install with: pip install html2text pillow requests beautifulsoup4")
    sys.exit(1)


class Config:
    """Configuration management with validation"""
    
    def __init__(self):
        self.webp_quality = 85
        self.webp_lossless = False
        self.max_image_size = (2048, 2048)
        self.supported_image_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        self.html_extensions = {'.html', '.htm'}
        self.timeout = 30
        self.max_retries = 3
        
    def validate(self) -> bool:
        """Validate configuration parameters"""
        if not (0 <= self.webp_quality <= 100):
            raise ValueError("WebP quality must be between 0-100")
        if not isinstance(self.max_image_size, tuple) or len(self.max_image_size) != 2:
            raise ValueError("max_image_size must be a tuple of (width, height)")
        return True


class HTMLToMarkdownConverter:
    """Main converter class with robust error handling"""
    
    def __init__(self, config: Config):
        self.config = config
        self.config.validate()
        self.logger = self._setup_logging()
        self.processed_images: Set[str] = set()
        self.failed_conversions: List[str] = []
        
    def _setup_logging(self) -> logging.Logger:
        """Setup structured logging"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def convert_directory(self, input_dir: Path, output_dir: Path) -> bool:
        """Convert entire directory with atomic operations"""
        if not input_dir.exists():
            self.logger.error(f"Input directory does not exist: {input_dir}")
            return False
        
        # Create temporary directory for atomic operations
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_output = Path(temp_dir) / "output"
            temp_output.mkdir()
            
            try:
                success = self._process_directory(input_dir, temp_output)
                
                if success:
                    # Atomic move to final destination
                    if output_dir.exists():
                        shutil.rmtree(output_dir)
                    shutil.move(str(temp_output), str(output_dir))
                    self.logger.info(f"Successfully converted directory: {input_dir} -> {output_dir}")
                    return True
                else:
                    self.logger.error("Directory conversion failed, rolling back")
                    return False
                    
            except Exception as e:
                self.logger.error(f"Directory conversion failed: {e}")
                return False
    
    def _process_directory(self, input_dir: Path, output_dir: Path) -> bool:
        """Process directory contents recursively"""
        html_files = list(input_dir.rglob("*"))
        html_files = [f for f in html_files if f.suffix.lower() in self.config.html_extensions]
        
        if not html_files:
            self.logger.warning(f"No HTML files found in {input_dir}")
            return True
        
        self.logger.info(f"Processing {len(html_files)} HTML files")
        
        success_count = 0
        for html_file in html_files:
            relative_path = html_file.relative_to(input_dir)
            output_file = output_dir / relative_path.with_suffix('.md')
            
            # Create output directory structure
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.convert_file(html_file, output_file):
                success_count += 1
            else:
                self.failed_conversions.append(str(html_file))
        
        self.logger.info(f"Converted {success_count}/{len(html_files)} files successfully")
        return success_count == len(html_files)
    
    def convert_file(self, input_file: Path, output_file: Path) -> bool:
        """Convert single HTML file to Markdown with error handling"""
        try:
            self.logger.info(f"Converting: {input_file}")
            
            # Read and parse HTML
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Process images before conversion
            html_content, images_dir = self._process_images(
                html_content, input_file, output_file
            )
            
            # Convert to Markdown
            markdown_content = self._html_to_markdown(html_content)
            
            # Write output
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.logger.info(f"Successfully converted: {input_file} -> {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to convert {input_file}: {e}")
            return False
    
    def _process_images(self, html_content: str, input_file: Path, output_file: Path) -> Tuple[str, Optional[Path]]:
        """Process and convert images to WebP format"""
        soup = BeautifulSoup(html_content, 'html.parser')
        img_tags = soup.find_all('img')
        
        if not img_tags:
            return html_content, None
        
        # Create images directory
        images_dir = output_file.parent / f"{output_file.stem}_images"
        images_dir.mkdir(exist_ok=True)
        
        for img_tag in img_tags:
            src = img_tag.get('src')
            if not src:
                continue
            
            try:
                new_src = self._convert_image(src, input_file, images_dir)
                if new_src:
                    img_tag['src'] = new_src
            except Exception as e:
                self.logger.warning(f"Failed to process image {src}: {e}")
        
        return str(soup), images_dir
    
    def _convert_image(self, src: str, base_file: Path, images_dir: Path) -> Optional[str]:
        """Convert single image to WebP format"""
        # Handle relative paths
        if not src.startswith(('http://', 'https://')):
            image_path = base_file.parent / src
            if not image_path.exists():
                self.logger.warning(f"Image not found: {image_path}")
                return None
        else:
            # Download remote image
            try:
                response = requests.get(src, timeout=self.config.timeout)
                response.raise_for_status()
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(response.content)
                    image_path = Path(temp_file.name)
            except Exception as e:
                self.logger.warning(f"Failed to download image {src}: {e}")
                return None
        
        # Check if already processed
        image_key = str(image_path)
        if image_key in self.processed_images:
            return None
        
        try:
            # Convert to WebP
            with Image.open(image_path) as img:
                # Resize if too large
                if img.size[0] > self.config.max_image_size[0] or img.size[1] > self.config.max_image_size[1]:
                    img.thumbnail(self.config.max_image_size, Image.Resampling.LANCZOS)
                
                # Generate output filename
                original_name = Path(src).stem
                webp_filename = f"{original_name}.webp"
                webp_path = images_dir / webp_filename
                
                # Save as WebP
                img.save(
                    webp_path,
                    'WEBP',
                    quality=self.config.webp_quality,
                    lossless=self.config.webp_lossless
                )
                
                self.processed_images.add(image_key)
                
                # Return relative path for markdown
                return f"{images_dir.name}/{webp_filename}"
                
        except Exception as e:
            self.logger.error(f"Failed to convert image {src}: {e}")
            return None
        finally:
            # Clean up downloaded files
            if src.startswith(('http://', 'https://')) and image_path.exists():
                image_path.unlink()
    
    def _html_to_markdown(self, html_content: str) -> str:
        """Convert HTML to Markdown with optimized settings"""
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # No line wrapping
        h.unicode_snob = True
        h.escape_snob = True
        
        return h.handle(html_content)
    
    def get_summary(self) -> Dict:
        """Get conversion summary"""
        return {
            'processed_images': len(self.processed_images),
            'failed_conversions': len(self.failed_conversions),
            'failed_files': self.failed_conversions
        }


def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description="Convert HTML files/folders to Markdown with WebP images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.html output.md
  %(prog)s html_folder/ markdown_folder/
  %(prog)s --quality 90 --max-size 1920x1080 input/ output/
        """
    )
    
    parser.add_argument('input', help='Input HTML file or directory')
    parser.add_argument('output', help='Output Markdown file or directory')
    parser.add_argument('--quality', type=int, default=85, 
                       help='WebP quality (0-100, default: 85)')
    parser.add_argument('--lossless', action='store_true',
                       help='Use lossless WebP compression')
    parser.add_argument('--max-size', default='2048x2048',
                       help='Maximum image size (WxH, default: 2048x2048)')
    parser.add_argument('--timeout', type=int, default=30,
                       help='HTTP timeout for remote images (default: 30s)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Setup configuration
    config = Config()
    config.webp_quality = args.quality
    config.webp_lossless = args.lossless
    config.timeout = args.timeout
    
    # Parse max size
    try:
        width, height = map(int, args.max_size.split('x'))
        config.max_image_size = (width, height)
    except ValueError:
        print(f"Invalid max-size format: {args.max_size}. Use WxH format.")
        sys.exit(1)
    
    # Setup logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize converter
    converter = HTMLToMarkdownConverter(config)
    
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    # Determine operation mode
    if input_path.is_file():
        success = converter.convert_file(input_path, output_path)
    elif input_path.is_dir():
        success = converter.convert_directory(input_path, output_path)
    else:
        print(f"Input path does not exist: {input_path}")
        sys.exit(1)
    
    # Print summary
    summary = converter.get_summary()
    print(f"\nConversion Summary:")
    print(f"Images processed: {summary['processed_images']}")
    print(f"Failed conversions: {summary['failed_conversions']}")
    
    if summary['failed_files']:
        print("Failed files:")
        for file in summary['failed_files']:
            print(f"  - {file}")
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()