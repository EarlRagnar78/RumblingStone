import re
import os

SOURCE_FILE = "/home/jfs/Scrivania/00-Giochi_di_ruolo/00_dnd_3.5/00_Red_hand_of_Doom_GitHub/RumblingStone/PNG/Therysol/Therysol.md"
OUTPUT_FILE = "/home/jfs/Scrivania/00-Giochi_di_ruolo/00_dnd_3.5/00_Red_hand_of_Doom_GitHub/RumblingStone/PNG/Therysol/Therysol.html"

# HTML Template with Ice/Crystal Theme (Revised CSS)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Therysol - Character Sheet</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Cinzel:wght@400;700&display=swap" rel="stylesheet">
    <style>
        @page {
            size: A4;
            margin: 0.4in;
        }

        body {
            font-family: 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.3;
            color: #1a2a3a; /* Dark Blue-Gray text */
            margin: 0;
            padding: 20px;
            /* Ice/Frost Gradient Background */
            background: linear-gradient(135deg, #f0f8ff 0%, #e6e6fa 50%, #f0ffff 100%);
        }

        .header {
            text-align: center;
            border-bottom: 3px solid #4682B4; /* Steel Blue */
            padding-bottom: 10px;
            margin-bottom: 15px;
        }

        .char-title {
            font-family: 'Cinzel Decorative', cursive;
            font-size: 26pt;
            font-weight: bold;
            color: #191970; /* Midnight Blue */
            margin: 0;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 2px #B0C4DE;
        }

        .subtitle {
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            font-weight: bold;
            font-style: italic;
            color: #4682B4; /* Steel Blue */
            margin: 5px 0;
        }

        .flavor-text {
            font-style: italic;
            text-align: center;
            color: #2F4F4F; /* Dark Slate Gray */
            font-size: 10.5pt;
            margin: 10px 0;
            padding: 8px;
            border-left: 3px solid #87CEEB; /* Sky Blue */
            border-right: 3px solid #87CEEB;
            background: rgba(135, 206, 235, 0.15);
            border-radius: 10px;
        }

        .draconic {
            font-family: 'Cinzel Decorative', cursive;
            font-size: 12pt;
            color: #008B8B; /* Dark Cyan */
            text-shadow: 0 0 3px #E0FFFF;
            font-weight: bold;
            letter-spacing: 1px;
            text-align: center;
            margin-top: 5px;
        }

        h2 {
            color: #191970; /* Midnight Blue */
            font-family: 'Cinzel', serif;
            font-size: 16pt;
            font-weight: bold;
            border-bottom: 2px solid #87CEEB;
            padding-bottom: 2px;
            margin: 15px 0 8px 0;
            text-transform: uppercase;
        }

        h3, h4 {
            color: #008B8B; /* Dark Cyan */
            font-family: 'Cinzel', serif;
            font-size: 13pt;
            font-weight: bold;
            margin: 10px 0 5px 0;
        }
        
        h4 {
            font-size: 12pt;
            border-bottom: 1px dashed #B0C4DE;
            display: inline-block;
        }

        strong {
            color: #000080; /* Navy */
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 10pt;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        th {
            background: linear-gradient(135deg, #4682B4, #5F9EA0);
            color: white;
            padding: 6px 4px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #2F4F4F;
            font-family: 'Cinzel', serif;
        }

        td {
            padding: 4px 6px;
            text-align: left;
            border: 1px solid #B0C4DE;
            background: rgba(255, 255, 255, 0.7);
        }

        tr:nth-child(even) td {
            background: rgba(240, 248, 255, 0.7); /* Alice Blue */
        }

        .stat-block {
            background: rgba(224, 255, 255, 0.2); /* Light Cyan */
            border: 2px solid #4682B4;
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
        }

        ul {
            margin: 5px 0;
            padding-left: 20px;
        }

        li {
            margin: 3px 0;
        }

        .two-column {
            column-count: 2;
            column-gap: 25px;
            text-align: justify;
        }
        
        .section-break {
            break-inside: avoid;
            page-break-inside: avoid;
        }

        /* Metadata Block */
        .meta-table td {
            background: none;
            border: none;
            padding: 2px;
            font-size: 11pt;
        }
        .meta-table {
            box-shadow: none;
            margin-bottom: 15px;
        }

        @media print {
            body { 
                background: white; 
                padding: 0;
            }
            .stat-block, table, h2, h3, h4, .flavor-text {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            .header {
                border-bottom-color: #000;
            }
        }
    </style>
</head>
<body>

    <div class="header">
        <h1 class="char-title">Therysol (ex Ysolde)</h1>
        <div class="subtitle">La Custode del Cristallo Infranto</div>
        <div class="draconic">"Theron non se n'è andato..."</div>
    </div>

    <!-- Metadata Table -->
    <table class="meta-table">
        <tr>
            <td><strong>Razza:</strong> Tiefling Mezzo-Drago (Bianco)</td>
            <td><strong>Classe:</strong> Esperto 2 / Acolita 6 (Livello 8)</td>
        </tr>
        <tr>
            <td><strong>Allineamento:</strong> Caotico Buono</td>
            <td><strong>Tipo:</strong> Esterno (Nativo, Potenziato)</td>
        </tr>
        <tr>
            <td colspan="2"><strong>GS:</strong> 9</td>
        </tr>
    </table>

    <div class="flavor-text">
        {FLAVOR_TEXT}
    </div>

    <div class="two-column">
        
        <div class="section-break">
            <h2>Punteggi Caratteristica</h2>
            {STATS_TABLE}
        </div>

        <div class="section-break">
            <h2>Combattimento & Difesa</h2>
            <div class="stat-block">
                {COMBAT_TEXT}
            </div>
        </div>

        <div class="section-break">
            <h2>Abilità (Skills)</h2>
            {SKILLS_TABLE}
        </div>

        <div class="section-break">
            <h2>Capacità Speciali & Magia</h2>
            {SPECIAL_ABILITIES}
        </div>

        <div class="section-break">
            <h2>Talenti</h2>
            {FEATS}
        </div>

        <div class="section-break">
            <h2>Equipaggiamento</h2>
            {EQUIPMENT}
        </div>
        
    </div>
    
    <div class="section-break" style="margin-top: 15px; border-top: 2px dashed #4682B4; padding-top: 10px;">
        <h3>Note per il DM</h3>
        {DM_NOTES}
    </div>

</body>
</html>
"""

def parse_markdown(md_content):
    sections = {}
    
    # Extract Flavor Text (Blockquotes)
    flavor_match = re.search(r'> (.*?)(?=\n\n|\n-)', md_content, re.DOTALL)
    sections['FLAVOR_TEXT'] = ""
    if flavor_match:
        raw_flavor = flavor_match.group(1).replace('>', '').strip()
        # Convert lines to paragraphs or breaks
        sections['FLAVOR_TEXT'] = "<p>" + raw_flavor.replace('\n\n', '</p><p>').replace('\n', '<br>') + "</p>"

    # Extract Stats Table
    # Looking for table starting with | Caratteristica |
    stats_match = re.search(r'(\| Caratteristica \|.*?)(?=\n\n|\n-)', md_content, re.DOTALL)
    if stats_match:
        md_table = stats_match.group(1)
        html_table = "<table><thead><tr><th>Caratteristica</th><th>Valore</th><th>Mod.</th><th>Note</th></tr></thead><tbody>"
        rows = md_table.strip().split('\n')[2:] # Skip header and divider
        for row in rows:
            cols = [c.strip() for c in row.split('|') if c.strip()]
            if len(cols) == 4:
                html_table += f"<tr><td>{cols[0]}</td><td style='font-weight:bold; font-size:1.1em;'>{cols[1]}</td><td>{cols[2]}</td><td>{cols[3]}</td></tr>"
        html_table += "</tbody></table>"
        sections['STATS_TABLE'] = html_table

    # Extract Combat Info
    # Between Combat & Difesa and Capacità Speciali
    combat_match = re.search(r'### \*\*Combattimento & Difesa\*\*(.*?)### \*\*Capacità', md_content, re.DOTALL)
    sections['COMBAT_TEXT'] = ""
    if combat_match:
        lines = combat_match.group(1).strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            # Bold keys
            html_line = re.sub(r'\*\*(.*?)\:\*\*', r'<strong>\1:</strong>', line)
            # Handle bullet points
            if html_line.startswith('* '):
                html_line = f"<div>&#8226; {html_line[2:]}</div>"
            else:
                html_line = f"<div>{html_line}</div>"
            sections['COMBAT_TEXT'] += html_line

    # Extract Skills Table
    skills_match = re.search(r'(\| Abilità \|.*?)(?=\n\n|\n-)', md_content, re.DOTALL)
    if skills_match:
        md_table = skills_match.group(1)
        html_table = "<table><thead><tr><th>Abilità</th><th>Totale</th><th>Gradi</th><th>Car</th><th>Note</th></tr></thead><tbody>"
        rows = md_table.strip().split('\n')[2:]
        for row in rows:
            cols = [c.strip() for c in row.split('|') if c.strip()]
            if len(cols) >= 2:
                # Basic parsing, might vary
                tr_content = "".join([f"<td>{c}</td>" for c in cols])
                html_table += f"<tr>{tr_content}</tr>"
        html_table += "</tbody></table>"
        sections['SKILLS_TABLE'] = html_table

    # Extract Special Abilities
    # From ### Capacità Speciali until ### Abilità
    # This section has H4 headers
    abilities_match = re.search(r'### \*\*Capacità Speciali & Magia\*\*(.*?)### \*\*Abilità', md_content, re.DOTALL)
    sections['SPECIAL_ABILITIES'] = ""
    if abilities_match:
        raw_text = abilities_match.group(1).strip()
        # Convert H4
        html_text = re.sub(r'#### \*\*(.*?)\*\*', r'<h4>\1</h4>', raw_text)
        # Convert lists
        html_text = re.sub(r'\n\* ', r'\n<li>', html_text)
        # Convert bold
        html_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_text)
        # Convert italic
        html_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_text)
        # Wrap lists? Simple approch: replace newlines with BR unless it's a list item
        lines = html_text.split('\n')
        final_html = ""
        in_list = False
        for line in lines:
            if "<li>" in line:
                if not in_list: final_html += "<ul>"; in_list = True
                final_html += line + "</li>"
            else:
                if in_list: final_html += "</ul>"; in_list = False
                if "<h4>" in line: final_html += line
                elif line.strip(): final_html += f"<p>{line}</p>"
        if in_list: final_html += "</ul>"
        sections['SPECIAL_ABILITIES'] = final_html

    # Feats
    feats_match = re.search(r'### \*\*Talenti\*\*(.*?)### \*\*Equipaggiamento', md_content, re.DOTALL)
    sections['FEATS'] = "<ul>"
    if feats_match:
        raw = feats_match.group(1).strip()
        # Parse numbered list
        lines = raw.split('\n')
        for line in lines:
            if re.match(r'\d\.', line):
                clean_line = re.sub(r'\d\.\s+', '', line)
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_line)
                sections['FEATS'] += f"<li>{clean_line}</li>"
    sections['FEATS'] += "</ul>"

    # Equipment
    equip_match = re.search(r'### \*\*Equipaggiamento Posseduto\*\*(.*?)### \*\*Note', md_content, re.DOTALL)
    sections['EQUIPMENT'] = "<ul>"
    if equip_match:
        raw = equip_match.group(1).strip()
        lines = raw.split('\n')
        for line in lines:
            if line.strip().startswith('*'):
                clean_line = line.strip()[1:].strip()
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_line)
                sections['EQUIPMENT'] += f"<li>{clean_line}</li>"
    sections['EQUIPMENT'] += "</ul>"

    # DM Notes
    dm_match = re.search(r'### \*\*Note per il DM.*?\*\*(.*)', md_content, re.DOTALL)
    sections['DM_NOTES'] = "<ul>"
    if dm_match:
        raw = dm_match.group(1).strip()
        lines = raw.split('\n')
        for line in lines:
            if line.strip().startswith('*'):
                clean_line = line.strip()[1:].strip()
                clean_line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', clean_line)
                sections['DM_NOTES'] += f"<li>{clean_line}</li>"
    sections['DM_NOTES'] += "</ul>"

    return sections

def main():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: Source file {SOURCE_FILE} not found.")
        return

    with open(SOURCE_FILE, 'r') as f:
        content = f.read()

    sections = parse_markdown(content)
    
    # Fill template
    html_out = HTML_TEMPLATE
    for key, value in sections.items():
        html_out = html_out.replace(f"{{{key}}}", value)

    with open(OUTPUT_FILE, 'w') as f:
        f.write(html_out)
    
    print(f"Successfully generated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
