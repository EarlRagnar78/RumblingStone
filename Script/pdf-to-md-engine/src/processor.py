import datetime
import re
import os
import time
import psutil
import torch
from pathlib import Path
from loguru import logger
from jinja2 import Environment, FileSystemLoader
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

from src.config import settings
from src.utils import get_file_hash, clean_filename

# Initialize Jinja2
template_env = Environment(loader=FileSystemLoader("src/templates"))
template = template_env.get_template("chapter.md.j2")

class ProgressTracker:
    def __init__(self, total_steps=6):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
        self.step_times = []
        self.step_names = [
            "Hash Check",
            "PDF Conversion", 
            "Image Processing",
            "Markdown Export",
            "Chapter Splitting",
            "Final Processing"
        ]
        
    def start_step(self, step_name=None):
        if step_name:
            logger.info(f"Starting: {step_name}")
        self.step_start = time.time()
        
    def complete_step(self):
        step_time = time.time() - self.step_start
        self.step_times.append(step_time)
        self.current_step += 1
        
        progress = (self.current_step / self.total_steps) * 100
        elapsed = time.time() - self.start_time
        
        if self.current_step > 1:
            avg_step_time = sum(self.step_times) / len(self.step_times)
            remaining_steps = self.total_steps - self.current_step
            estimated_remaining = avg_step_time * remaining_steps
            
            logger.info(f"Progress: {progress:.1f}% | Elapsed: {elapsed:.1f}s | ETA: {estimated_remaining:.1f}s")
        else:
            logger.info(f"Progress: {progress:.1f}% | Elapsed: {elapsed:.1f}s")
            
    def get_eta(self):
        if len(self.step_times) < 2:
            return "Calculating..."
        avg_step_time = sum(self.step_times) / len(self.step_times)
        remaining_steps = self.total_steps - self.current_step
        return f"{avg_step_time * remaining_steps:.1f}s"

def monitor_system_resources():
    """Monitor system resources and return usage percentages."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    return cpu_percent, memory_percent

def should_throttle():
    """Check if processing should be throttled due to high system usage."""
    cpu_percent, memory_percent = monitor_system_resources()
    
    if cpu_percent > settings.CPU_USAGE_THRESHOLD:
        logger.warning(f"High CPU usage detected: {cpu_percent:.1f}% - Throttling processing")
        return True
    
    if memory_percent > settings.MEMORY_USAGE_THRESHOLD:
        logger.warning(f"High memory usage detected: {memory_percent:.1f}% - Throttling processing")
        return True
    
    return False

def adaptive_sleep():
    """Adaptive sleep based on system load."""
    cpu_percent, memory_percent = monitor_system_resources()
    
    if cpu_percent > 90 or memory_percent > 90:
        time.sleep(2.0)  # Long pause for critical load
    elif cpu_percent > 80 or memory_percent > 80:
        time.sleep(1.0)  # Medium pause for high load
    elif cpu_percent > 70 or memory_percent > 70:
        time.sleep(0.5)  # Short pause for moderate load

def setup_gpu_optimization():
    """Configure GPU settings with conservative resource management."""
    if settings.USE_GPU and torch.cuda.is_available():
        try:
            device = torch.device("cuda")
            # Get GPU memory info
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024**3)  # GB
            available_memory = gpu_memory - settings.GPU_MEMORY_LIMIT_GB
            
            if available_memory > 1.0:  # Need at least 1GB for processing
                # Conservative memory allocation
                memory_fraction = min(available_memory / gpu_memory, 0.7)  # Max 70% of GPU memory
                torch.cuda.set_per_process_memory_fraction(memory_fraction)
                
                logger.info(f"GPU acceleration enabled. Using {available_memory:.1f}GB of {gpu_memory:.1f}GB GPU memory")
                
                # Set environment variables for optimal GPU usage
                os.environ["CUDA_VISIBLE_DEVICES"] = "0"
                os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:256,expandable_segments:True"
                return device
            else:
                logger.warning(f"Insufficient GPU memory. Available: {available_memory:.1f}GB, Required: >1GB")
        except Exception as e:
            logger.warning(f"GPU setup failed: {e}. Falling back to CPU.")
    
    logger.info(f"Using CPU with {settings.MAX_WORKERS} workers (system has {psutil.cpu_count()} cores)")
    return torch.device("cpu")

def setup_converter():
    """Configure Docling pipeline options with performance optimizations."""
    device = setup_gpu_optimization()
    
    return DocumentConverter()

def process_images_parallel(doc, assets_dir, progress_tracker=None):
    """Process and save images in parallel with progress tracking."""
    def save_image(args):
        i, picture = args
        try:
            if should_throttle():
                adaptive_sleep()
            
            img = picture.get_image(doc)
            if img:
                img_filename = f"img_{i:03d}.png"
                img_path = assets_dir / img_filename
                img.save(img_path)
                return img_filename
        except Exception as e:
            logger.warning(f"Failed to save image {i}: {e}")
        return None
    
    cpu_percent, memory_percent = monitor_system_resources()
    max_workers = settings.MAX_WORKERS
    
    if cpu_percent > 70 or memory_percent > 70:
        max_workers = max(1, max_workers // 2)
        logger.info(f"Reducing image workers to {max_workers} due to system load")
    
    # Process with progress bar
    with ThreadPoolExecutor(max_workers=min(max_workers, len(doc.pictures))) as executor:
        image_args = list(enumerate(doc.pictures))
        futures = [executor.submit(save_image, args) for args in image_args]
        
        saved_images = []
        with tqdm(total=len(futures), desc="Processing images", unit="img") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    saved_images.append(result)
                pbar.update(1)
    
    logger.info(f"Saved {len(saved_images)} images")
    return saved_images

def process_chapters_parallel(chapters, pdf_path, pdf_output_dir, progress_tracker=None):
    """Process chapters in parallel with progress tracking."""
    def save_chapter_wrapper(args):
        i, (header_line, content) = args
        try:
            if should_throttle():
                adaptive_sleep()
            
            title = header_line.lstrip("#").strip()
            safe_title = clean_filename(title)
            filename = f"{i+1:02d}_{safe_title}"
            _save_chapter(content, filename, title, pdf_path.name, pdf_output_dir, i+1)
            return filename
        except Exception as e:
            logger.error(f"Failed to process chapter {i+1}: {e}")
            return None
    
    chapter_pairs = []
    for i in range(0, len(chapters), 2):
        if i + 1 < len(chapters):
            chapter_pairs.append((chapters[i].strip(), chapters[i+1]))
    
    cpu_percent, memory_percent = monitor_system_resources()
    max_workers = settings.MAX_WORKERS
    
    if cpu_percent > 70 or memory_percent > 70:
        max_workers = max(1, max_workers // 2)
        logger.info(f"Reducing chapter workers to {max_workers} due to system load")
    
    # Process with progress bar
    with ThreadPoolExecutor(max_workers=min(max_workers, len(chapter_pairs))) as executor:
        chapter_args = list(enumerate(chapter_pairs))
        futures = [executor.submit(save_chapter_wrapper, args) for args in chapter_args]
        
        processed_chapters = []
        with tqdm(total=len(futures), desc="Processing chapters", unit="ch") as pbar:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    processed_chapters.append(result)
                pbar.update(1)
    
    logger.info(f"Processed {len(processed_chapters)} chapters")
    return processed_chapters

def process_pdf(pdf_path: Path):
    """
    Main logic with time estimation and progress tracking:
    1. Check Hash (Idempotency)
    2. Monitor system resources  
    3. Convert PDF with progress
    4. Save Assets with progress bars
    5. Split Text
    6. Render Templates with progress
    """
    # Initialize progress tracker
    progress = ProgressTracker()
    
    # Step 1: Hash Check
    progress.start_step("Hash Check & Setup")
    cpu_percent, memory_percent = monitor_system_resources()
    logger.info(f"System resources - CPU: {cpu_percent:.1f}%, Memory: {memory_percent:.1f}%")
    
    if cpu_percent > 90 or memory_percent > 90:
        logger.warning("System under heavy load. Consider closing other applications.")
        time.sleep(3)
    
    file_hash = get_file_hash(pdf_path)
    safe_name = clean_filename(pdf_path.stem)
    pdf_output_dir = settings.OUTPUT_DIR / safe_name
    assets_dir = pdf_output_dir / "assets"
    
    receipt_file = pdf_output_dir / ".receipt"
    if receipt_file.exists() and not settings.OVERWRITE_EXISTING:
        with open(receipt_file, "r") as f:
            stored_hash = f.read().strip()
        if stored_hash == file_hash:
            logger.info(f"Skipping {pdf_path.name} (Unchanged)")
            return

    if pdf_output_dir.exists():
        import shutil
        shutil.rmtree(pdf_output_dir)
    pdf_output_dir.mkdir(parents=True)
    assets_dir.mkdir()
    
    progress.complete_step()
    
    # Step 2: PDF Conversion
    progress.start_step("PDF Conversion")
    converter = setup_converter()
    
    with tqdm(desc="Converting PDF", unit="page") as pbar:
        result = converter.convert(pdf_path)
        doc = result.document
        pbar.update(1)
    
    progress.complete_step()
    
    if should_throttle():
        logger.info("Pausing for system recovery...")
        adaptive_sleep()

    # Step 3: Image Processing
    progress.start_step("Image Processing")
    if doc.pictures:
        saved_images = process_images_parallel(doc, assets_dir, progress)
    else:
        logger.info("No images found")
    progress.complete_step()
    
    # Step 4: Markdown Export
    progress.start_step("Markdown Export")
    with tqdm(desc="Exporting markdown", unit="doc") as pbar:
        full_md = doc.export_to_markdown()
        pbar.update(1)
    progress.complete_step()
    
    # Step 5: Chapter Splitting
    progress.start_step("Chapter Processing")
    chapters = re.split(r'(^# .+)', full_md, flags=re.MULTILINE)
    
    if chapters and not chapters[0].startswith('#'):
        preamble = chapters.pop(0)
        if preamble.strip():
            _save_chapter(preamble, "00_preamble", "Preamble", pdf_path.name, pdf_output_dir)

    if len(chapters) > 1:
        processed_chapters = process_chapters_parallel(chapters, pdf_path, pdf_output_dir, progress)
    else:
        logger.info("No chapters found")
    progress.complete_step()

    # Step 6: Final Processing
    progress.start_step("Finalizing")
    with open(receipt_file, "w") as f:
        f.write(file_hash)
    
    final_cpu, final_memory = monitor_system_resources()
    total_time = time.time() - progress.start_time
    
    progress.complete_step()
    
    logger.success(f"✅ Completed {pdf_path.name} in {total_time:.1f}s")
    logger.info(f"Final resources - CPU: {final_cpu:.1f}%, Memory: {final_memory:.1f}%")

def _save_chapter(content, filename, title, source, output_dir, index=0):
    """Render Jinja template and save file."""
    rendered = template.render(
        title=title,
        content=content,
        source_file=source,
        date=datetime.date.today().isoformat(),
        index=index
    )
    
    # Fix Image Paths in content to be relative to assets folder
    # Docling exports generic paths, we need to ensure they point to ./assets/
    # This is a simplified regex replacement for the example
    rendered = rendered.replace("](", "](assets/") 
    
    (output_dir / f"{filename}.md").write_text(rendered, encoding="utf-8")