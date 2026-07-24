#!/bin/bash
# Markdown to PDF conversion using Pandoc (inspired by fusepdf)
# Usage: ./md2pdf.sh input.md output.pdf [language]

INPUT_MD="$1"
OUTPUT_PDF="$2"
LANG="${3:-en}"

if [ ! -f "$INPUT_MD" ]; then
    echo "Error: Input markdown file not found: $INPUT_MD"
    exit 1
fi

# Check if pandoc is available
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc not found. Install with: sudo apt install pandoc texlive-xetex"
    exit 1
fi

# Create header template
HEADER_TEX=$(mktemp)
cat > "$HEADER_TEX" << 'EOF'
\usepackage{sectsty}
\sectionfont{\clearpage}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[CO,CE]{PDF-to-MD Engine}
\fancyfoot[CO,CE]{Generated from Markdown}
\fancyfoot[LE,RO]{\thepage}
EOF

# Convert markdown to PDF
pandoc "$INPUT_MD" \
    --include-in-header "$HEADER_TEX" \
    -V linkcolor:blue \
    -V geometry:a4paper \
    -V geometry:margin=2cm \
    -V lang="$LANG" \
    --pdf-engine=xelatex \
    --toc \
    -o "$OUTPUT_PDF"

# Cleanup
rm "$HEADER_TEX"

if [ -f "$OUTPUT_PDF" ]; then
    echo "✅ PDF created: $OUTPUT_PDF"
else
    echo "❌ PDF creation failed"
    exit 1
fi