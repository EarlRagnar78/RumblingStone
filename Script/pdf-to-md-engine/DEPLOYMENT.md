5. Deployment Instructions

To deploy this project:

    Initialize:
    code Bash

    
mkdir pdf-to-md-engine
cd pdf-to-md-engine
# Paste the folder structure and files above

  

Environment Setup (The 2025 Way):
Using uv (fastest) or standard venv.
code Bash

    
# Standard way
python -m venv .venv
source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
pip install docling pydantic-settings jinja2 loguru

  

Run:

    Place a PDF in data/input.

    Run python main.py.

Result:
Check data/output. You will see a folder named after your PDF. Inside, you will find numbered Markdown files (01_chapter.md, 02_chapter.md) and an assets folder containing the PNGs.