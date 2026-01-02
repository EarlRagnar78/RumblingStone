pdf-to-md-engine/
├── .env # Environment variables (Secrets/Paths)
├── .gitignore
├── pyproject.toml # Modern dependency management
├── README.md
├── src/
│ ├── __init__.py
│ ├── config.py # Pydantic settings management
│ ├── processor.py # Core processing logic
│ ├── utils.py # Hashing and file ops
│ └── templates/
│ └── chapter.md.j2 # Jinja2 template for output files
├── data/
│ ├── input/ # Drop your PDFs here
│ ├── processing/ # Temp folder (optional)
│ └── output/ # Final Markdown and Images go here
└── main.py # Entry point script