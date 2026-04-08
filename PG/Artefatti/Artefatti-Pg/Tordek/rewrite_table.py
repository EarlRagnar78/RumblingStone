import re

file_path = '05_Bracieri_Gemelli_Scheda_PG_Completa.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the section to replace
start_marker = '<div class="section-title">La Danza degli Elementi (Poteri Attivati)</div>'
end_marker_str = 'Tiro unico (1d20 + For + Saltare). Salto potenziato. Atterraggio: <strong>2d6 Fuoco</strong> in raggio 3m\n            (Riflessi CD dimezza).\n        </div>\n    </div>'

start_idx = content.find(start_marker)
if start_idx == -1:
    print("Start marker not found.")
    exit(1)

# Find the exact end of the specific block
end_idx = content.find(end_marker_str, start_idx)
if end_idx == -1:
    print("End marker not found")
    exit(1)
end_idx += len(end_marker_str)

section_content = content[start_idx:end_idx]

# Parse the power blocks
powers = []
pattern = r'<div class="power-block">.*?<span class="power-title">(.*?)</span>.*?<span class="power-usage">(.*?)</span>.*?<div class="power-action">(.*?)</div>.*?<div class="power-description">\s*(.*?)\s*</div>\s*</div>'
matches = re.finditer(pattern, section_content, re.DOTALL)

for match in matches:
    title, usage, action, desc = match.groups()
    powers.append({
        'title': title.strip(),
        'usage': usage.strip(),
        'action': action.strip(),
        'desc': desc.strip()
    })

if not powers:
    print("No power blocks parsed. Check regex.")
    exit(1)

# Generate new CSS and Table
new_css = """
        /* New Table Style for Poteri Attivabili */
        .table-attivabili {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0 20px 0;
            font-size: 10pt;
        }

        .table-attivabili th {
            background: linear-gradient(135deg, #8b0000, #ff4500);
            color: white;
            padding: 6px 4px;
            text-align: center;
            font-weight: bold;
            border: 1px solid #800000;
        }

        .table-attivabili td {
            padding: 6px 4px;
            text-align: left;
            border: 1px solid #ff4500;
            background: rgba(255, 245, 238, 0.85); /* Seashell background */
            vertical-align: top;
        }

        .table-attivabili tr:nth-child(even) td {
            background: rgba(255, 228, 225, 0.85); /* MistyRose background */
        }
"""

table_html = '<div class="section-title">Poteri Attivabili</div>\n'
table_html += '<table class="table-attivabili">\n'
table_html += '    <tr>\n        <th>Potere</th>\n        <th>Usi</th>\n        <th>Azione</th>\n        <th>Effetto</th>\n    </tr>\n'

for p in powers:
    table_html += f'    <tr>\n'
    table_html += f'        <td style="font-weight:bold; color:#8b0000;">{p["title"]}</td>\n'
    table_html += f'        <td style="text-align:center;">{p["usage"]}</td>\n'
    table_html += f'        <td style="text-align:center;">{p["action"]}</td>\n'
    table_html += f'        <td>{p["desc"]}</td>\n'
    table_html += f'    </tr>\n'
table_html += '</table>\n'

# Insert new CSS just before </style> or right before the replaced content
# Let's cleanly inject CSS in the head if possible
css_inject_idx = content.find('</style>')
if css_inject_idx != -1:
    content = content[:css_inject_idx] + new_css + content[css_inject_idx:]
else:
    table_html = "<style>" + new_css + "</style>\n" + table_html

# Replace content
new_full_content = content[:start_idx] + table_html + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_full_content)

print(f"Successfully converted {len(powers)} power blocks into a table with distinct styling.")
