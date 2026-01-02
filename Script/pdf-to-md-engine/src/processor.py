import datetime
import re
from pathlib import Path
from loguru import logger
from jinja2 import Environment, FileSystemLoader

from docling.document_converter import DocumentConverter
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

from src.config import settings
from src.utils import get_file_hash, clean_filename

# Initialize Jinja2
template_env = Environment(loader=FileSystemLoader("src/templates"))
template = template_env.get_template("chapter.md.j2")

def setup_converter():
    """Configure Docling pipeline options."""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_page_images = False
    pipeline_options.generate_picture_images = True # Extract figures/images
    pipeline_options.images_scale = settings.IMAGE_SCALE
    
    return DocumentConverter(
        format_options={
            InputFormat.PDF: {"pipeline_options": pipeline_options}
        }
    )

def process_pdf(pdf_path: Path):
    """
    Main logic:
    1. Check Hash (Idempotency)
    2. Convert PDF
    3. Save Assets
    4. Split Text
    5. Render Templates
    """
    file_hash = get_file_hash(pdf_path)
    
    # Create specific output folder for this PDF based on name
    safe_name = clean_filename(pdf_path.stem)
    pdf_output_dir = settings.OUTPUT_DIR / safe_name
    assets_dir = pdf_output_dir / "assets"
    
    # Idempotency Check: Look for a receipt file
    receipt_file = pdf_output_dir / ".receipt"
    if receipt_file.exists() and not settings.OVERWRITE_EXISTING:
        with open(receipt_file, "r") as f:
            stored_hash = f.read().strip()
        if stored_hash == file_hash:
            logger.info(f"Skipping {pdf_path.name} (Unchanged)")
            return

    logger.info(f"Processing {pdf_path.name}...")
    
    # Clean and Re-create directories
    if pdf_output_dir.exists():
        import shutil
        shutil.rmtree(pdf_output_dir)
    pdf_output_dir.mkdir(parents=True)
    assets_dir.mkdir()

    # 1. Convert
    converter = setup_converter()
    result = converter.convert(pdf_path)
    doc = result.document

    # 2. Save Images & Update References
    # Docling internally maps images. We need to save them and map the filename.
    image_map = {}
    
    for i, picture in enumerate(doc.pictures):
        img = picture.get_image(doc)
        if img:
            img_filename = f"img_{i:03d}.png"
            img_path = assets_dir / img_filename
            img.save(img_path)
            # We map the internal object ID to the relative path for Markdown replacement
            # Note: Docling's markdown export handles references automatically, 
            # but we ensure the files exist here.
    
    # 3. Get Full Markdown
    full_md = doc.export_to_markdown()
    
    # 4. Split by Chapter (Robust Logic)
    # This regex splits by Headers (# Title)
    # It looks for lines starting with # followed by space
    chapters = re.split(r'(^# .+)', full_md, flags=re.MULTILINE)
    
    # The first element might be pre-header text (preamble)
    if chapters and not chapters[0].startswith('#'):
        preamble = chapters.pop(0)
        if preamble.strip():
            _save_chapter(preamble, "00_preamble", "Preamble", pdf_path.name, pdf_output_dir)

    chapter_count = 1
    # Iterate in pairs (Header, Content)
    for i in range(0, len(chapters), 2):
        if i + 1 >= len(chapters): break
        
        header_line = chapters[i].strip()
        content = chapters[i+1]
        
        # Clean title from "# Title" -> "Title"
        title = header_line.lstrip("#").strip()
        safe_title = clean_filename(title)
        filename = f"{chapter_count:02d}_{safe_title}"
        
        # Reconstruct content with header included or excluded based on preference
        # Here we pass it to the template
        _save_chapter(content, filename, title, pdf_path.name, pdf_output_dir, chapter_count)
        chapter_count += 1

    # 5. Write Receipt (Idempotency)
    with open(receipt_file, "w") as f:
        f.write(file_hash)
    
    logger.success(f"Finished {pdf_path.name}")

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