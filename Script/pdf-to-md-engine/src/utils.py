import hashlib
from pathlib import Path

def get_file_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of a file for idempotency checks."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read in chunks to handle large PDF files efficiently
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def clean_filename(text: str) -> str:
    """Sanitize strings to be safe filenames."""
    return "".join([c if c.isalnum() else "_" for c in text]).strip("_").lower()