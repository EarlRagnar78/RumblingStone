import re
import os

# --- Configuration ---
input_path = '/home/jfs/Scrivania/00-Giochi_di_ruolo/00_dnd_3.5/00_Red_hand_of_Doom_GitHub/RumblingStone/PG/Artefatti/Artefatti-Pg/Tordek/04_Bracieri_Gemelli_Scheda_PG_Fuoco.html'
output_path = input_path # Overwrite safely

# --- New CSS ---
css_content = """
    <style>
        @page {
            size: A4;
            margin: 0.5in;
        }

        body {
            font-family: 'Times New Roman', serif;
            font-size: 12pt;
            line-height: 1.4;
            color: #2c1810;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #f8f6f0 0%, #ede8dc 100%);
        }

        .header {
            text-align: center;
            border-bottom: 3px solid #8B0000;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .class-title {
            font-size: 24pt;
            font-weight: bold;
            color: #8B0000;
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }

        .subtitle {
            font-size: 14pt;
            font-style: italic;
            color: #A0522D;
            margin: 5px 0;
        }

        .dwarven {
            font-family: 'Cinzel Decorative', cursive;
            font-size: 14pt;
            color: #B22222;
            text-shadow: 0 0 4px #FF4500;
            font-weight: bold;
            font-style: normal;
            letter-spacing: 1px;
            text-align: center;
            margin: 15px 0;
        }

        h2 {
            color: #8B0000;
            font-size: 16pt;
            font-weight: bold;
            border-bottom: 2px solid #DAA520;
            padding-bottom: 3px;
            margin: 20px 0 10px 0;
            text-transform: uppercase;
        }

        h3 {
            color: #A0522D;
            font-size: 14pt;
            font-weight: bold;
            margin: 15px 0 8px 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 11pt;
        }

        th {
            background: linear-gradient(135deg, #8B0000, #A52A2A);
            color: white;
            padding: 8px 4px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #650000;
        }

        td {
            padding: 6px 4px;
            text-align: center;
            border: 1px solid #DAA520;
            background: rgba(248, 246, 240, 0.8);
        }

        tr:nth-child(even) td {
            background: rgba(237, 232, 220, 0.8);
        }

        .stat-block, .requirements {
            background: rgba(139, 0, 0, 0.05);
            border: 2px solid #8B0000;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            text-align: center;
        }

        .synergy-box {
            background: rgba(255, 69, 0, 0.05);
            border: 2px solid #FF4500;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
        }

        .artifact-image {
            display: block;
            margin: 0 auto 20px auto;
            max-width: 40%; 
            height: auto;
            border: 3px double #8B4513;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
        }

        .two-column {
            column-count: 2;
            column-gap: 30px;
            text-align: justify;
        }
        
        .one-column {
            text-align: justify;
        }

        ul {
            margin: 8px 0;
            padding-left: 20px;
        }

        li {
            margin: 4px 0;
        }
        
        /* Print optimization */
        @media print {
            .stat-block, .synergy-box, table {
                page-break-inside: avoid;
            }
        }
    </style>
"""

# --- HTML Template ---
html_start = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bracieri Gemelli di Moradin (Fuoco)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&display=swap" rel="stylesheet">
    {css}
</head>
<body>
"""

html_header = """
    <div class="header">
        <h1 class="class-title">Bracieri Gemelli di Moradin</h1>
        <div class="subtitle">Stato: Risveglio della Fiamma</div>
        <div class="dwarven">"Una forgia senza fuoco non crea."</div>
    </div>
"""

# --- Execution ---
print("Reading original file...")
with open(input_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract Image
print("Extracting image...")
img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*>', content)
if not img_match:
    print("ERROR: No image found!")
    exit(1)
img_src = img_match.group(1)
html_image = f'<img src="{img_src}" class="artifact-image">'

# 2. Extract Body Content (everything AFTER the image tag)
# The previous inspection showed the stat block is the first thing after the image.
# We will grab everything from the end of the img tag to the end of the file (before </body>)
start_index = img_match.end()
end_index = content.rfind('</body>')
if end_index == -1: end_index = len(content)

raw_body_content = content[start_index:end_index].strip()

# 3. Clean up and Restructure Body content
# The content seems to be in a flat list of divs/paragraphs.
# We want to wrap the main text description in .one-column or .two-column if long.
# The 'stat-block' div is already there, we might just keep it or enhance it.
# We will inject the raw content but make sure it uses our new CSS classes.
# The original file used `style="text-align: justify;"` on a wrapper div. We can strip that wrapper if we want, or simple wrap everything in a container.

# Let's wrap the prose content in a content div
html_content_body = f"""
    <div class="one-column">
        {raw_body_content}
    </div>
"""

# 4. Assemble
final_html = html_start.format(css=css_content) + html_header + html_image + html_content_body + "\n</body>\n</html>"

print("Writing new file...")
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Done.")
