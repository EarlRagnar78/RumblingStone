#!/usr/bin/env python3
"""
build_monster_catalog.py — Scansiona la campagna e produce monster_catalog.yaml.

Sorgenti (in ordine di priorità):
  1. 00_Red Hand Of Doom/Armate-UNITA-NUOVE/*.md     (INFERRED, ha header strutturato)
  2. 00_Red Hand Of Doom/Monsters_Sheets/**/*.htm|*.html|*.pcg|*.pdf
  3. 08_La Battaglia Di Hammerfist/00_Schede_dei_Personaggi_Unita*.md  (parsing sezioni)
  4. 09_Continuazione.../Arco-*STATBLOCCHI*.md
  5. 04_tomba_di_Belkram/**, 01_LaMiniera/**, 02_*/**, 06_*/**, 07_*/** (tutte le .txt/.md/.htm con statblock)
  6. PNG/**/*.md                                     (PNG nominati)

Output:
  scripts/monster_catalog.yaml   (generated, non committare modifiche a mano)
  scripts/monster_catalog.custom.yaml  (NON sovrascritto; append-only user)

Schema record:
  - id: slug unico (fname-without-ext + short hash)
    name: display name
    cr: float o int o null
    faction: red-hand|drow-sonjak|gnoll|loxo-centaur-corrupted|githyanki-vaereth|teschio-nero-thay|rakshasa|ghostlord-undead|rethmar-defender|dauth-defender|cerchio-druid|aberration|unknown
    role: melee|ranged|caster|mount|leader|boss|fodder|...
    environment: any|underdark|forest|urban|aerial|...
    source_file: path relativo al root
    aliases: [list]
    notes: str
"""

import re
import hashlib
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "monster_catalog.yaml"
CUSTOM = Path(__file__).resolve().parent / "monster_catalog.custom.yaml"

# Heuristic CR extraction
CR_PATTERNS = [
    re.compile(r'\*\*CR\*\*[:\s]*([\d./]+)', re.IGNORECASE),
    re.compile(r'\bCR[:\s]*([\d./]+)', re.IGNORECASE),
    re.compile(r'\bGS[:\s]*([\d./]+)', re.IGNORECASE),  # italian "Grado di Sfida"
    re.compile(r'-cr(\d+)', re.IGNORECASE),             # filename cr7
    re.compile(r'cr(\d+)\b', re.IGNORECASE),
]
# Priority-ordered: first-match wins. Narrow/unique keywords (dragons, aberrations,
# named NPCs) go BEFORE broad ones (red-hand) so e.g. "Abithriax" / "Retriever"
# don't get swallowed by the hobgoblin horde.
FACTION_KEYWORDS = {
    "dragon": ["abithriax", "arbitrax", "regiarix", "ozyrrandion", "tyrgarun", "fauci di palude", "razorfiend", "drago rosso", "drago nero", "drago verde", "drago blu", "dragon adult", "dragon young", "wyrmling", "drago "],
    "aberration": ["myconid", "beholder", "bebilith", "retriever", "grell", "xorn", "black pudding", "cubo gelatinoso", "celebromorf", "phantom fungus", "antenato nanico", "mind flayer", "illithid"],
    "ghostlord-undead": ["ghostlord", "bone naga", "deathlock", "skeletal", "spectre", "allip", "lich", "ghost lion"],
    "rakshasa": ["rakshasa", "collezionista"],
    "drow-sonjak": ["drow", "sonjak", "sajak", "underdark cleric", "deep warden", "runecaster"],
    "githyanki-vaereth": ["githyanki", "gith ", "vaereth"],
    "gnoll": ["gnoll", "flind", "hyenodon", "yeenoghu"],
    "loxo-centaur-corrupted": ["loxo", "centaur", "centauro"],
    "teschio-nero-thay": ["thayan", "red wizard", "teschio nero"],
    "starsong-elf": ["starsong", "tiri-kitor", "lythiel", "maewen", "owl cavalry"],
    "cerchio-druid": ["hella", "cerchio sacro", "druida", "druid", "treant"],
    "rethmar-defender": ["rethmar", "valerius", "lorana"],
    "dauth-defender": ["dauth", "thorek", "dwarf defender", "tordek", "morlin", "rurik"],
    "hammerfist-hero": ["borin ferropugno", "dara occhiolesto", "thorin runaforte", "nala cantapietre", "tempestas", "dana forgiapietra", "lunapiena", "ventolesto", "orion pelleorsa"],
    "red-hand": ["hobgoblin", "red hand", "mano rossa", "wyrmlord", "goblin", "worg", "bugbear", "orc", "ogre", "ettin", "hell hound", "kulkor", "draxoksus", "koth", "azarr kul", "tiamat", "saarvith", "zalkatar"],
}


ENV_KEYWORDS = {
    "underdark": ["underdark", "deep", "ainin", "dovil", "brieyn", "drow"],
    "forest": ["druid", "treant", "cerchio", "hella", "starsong", "ranger"],
    "urban": ["militia", "city guard", "valerius", "rethmar"],
    "aerial": ["dragon", "drago", "wyvern", "manticore", "gufo"],
    "swamp": ["razorfiend", "black dragon", "drago nero", "fauci", "regiarix", "rhest"],
    "dungeon": ["belkram", "miniera", "duergar", "tomba"],
    "plain": ["gnoll", "centaur", "loxo", "shaar"],
    "mountain": ["hill giant", "giant", "eagis", "hammerfist"],
}

# Priority-ordered: first-match wins. "flier" goes first so dragons/manticores
# aren't mis-tagged as caster/boss.
ROLE_KEYWORDS = {
    "flier": ["dragon", "drago", "manticore", "wyvern", "gufo celestiale"],
    "caster-arcane": ["wizard", "sorcerer", "runecaster", "red wizard", "stregone", "arcimago"],
    "caster-divine": ["cleric", "priest", "druid", "shaman", "warpriest", "chierico", "druida", "arci-druido"],
    "boss": ["wyrmlord", "matrona", "chieftain", "commander", "captain", "capo ", "signore", " boss"],
    "mount": ["mount ", "cavalcatura"],
    "melee-heavy": ["fighter", "barbarian", "knight", "defender", "greatsword", "greataxe"],
    "ranged": ["ranger", "archer", "longbow", "crossbow"],
    "fodder": ["warrior", "regular", "militia", "fanteria"],
}

def slugify(s):
    s = re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
    return s[:80]

def short_hash(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()[:6]

def guess_faction(text):
    t = text.lower()
    for fac, kws in FACTION_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return fac
    return "unknown"

def guess_env(text):
    t = text.lower()
    for env, kws in ENV_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return env
    return "any"

def guess_role(text):
    t = text.lower()
    for role, kws in ROLE_KEYWORDS.items():
        for kw in kws:
            if kw in t:
                return role
    return "generalist"

def extract_cr(text, fname=""):
    for pat in CR_PATTERNS:
        m = pat.search(text)
        if m:
            val = m.group(1)
            try:
                if '/' in val:
                    num, den = val.split('/')
                    return float(num) / float(den)
                return float(val)
            except ValueError:
                continue
    # fallback: filename
    for pat in CR_PATTERNS[-2:]:
        m = pat.search(fname)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                continue
    return None

def extract_name(content, fname):
    # First try H1 markdown
    m = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if m:
        name = m.group(1).strip()
        name = re.sub(r'\[.*?\]', '', name).strip()  # strip [INFERRED] tag
        return name
    # fallback: filename cleaned
    base = Path(fname).stem
    return base.replace('-', ' ').replace('_', ' ').title()

def read_file_safe(path):
    for enc in ('utf-8', 'latin-1', 'cp1252'):
        try:
            return path.read_text(encoding=enc, errors='ignore')
        except Exception:
            continue
    return ""

def should_skip(path):
    skip_dirs = {'.git', 'node_modules', '.claude', '.cursor', '.windsurf', '.gemini', '.chatgpt', '.agents', '.github', 'Immagini', 'immage_campaign', 'Mappe', 'Musica', 'skills', 'Script', 'Old', 'png_La_mano_rossa_del_destino_files'}
    for part in path.parts:
        if part in skip_dirs or part.endswith('_files'):
            return True
    return False

def scan_directory(root):
    records = []
    valid_ext = {'.md', '.txt', '.htm', '.html', '.pcg'}
    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if should_skip(path.relative_to(ROOT)):
            continue
        if path.suffix.lower() not in valid_ext:
            continue
        # Only include files that look like statblocks
        content = read_file_safe(path)
        rel = str(path.relative_to(ROOT))
        rel_lower = rel.lower()

        # Hard blocklist: non-monster paths/filenames that leak via CR-in-text
        BLOCK_SUBSTR = [
            'build/',
            'campaign-party',
            'treasure&xp',
            'treasure_xp',
            'villans.md',
            'readme',
            'indice',
            'overview',
            'house-rules',
            'campaign-coherence',
            'dm-player-strategy',
            'regolamento',
            'atlante visivo',
            'guida-agli-scontri',
            'to-be_integrated',
            'sidemissions',
            'cheat-sheet',
            'minimappa',
            'hooks',
            'mappe-',
            '-mappe',
            'timeline',
            'consequenze', 'conseguenze', 'esiti',
        ]
        if any(b in rel_lower for b in BLOCK_SUBSTR):
            continue

        is_statblock_folder = any(k in rel for k in [
            'Monsters_Sheets', 'Armate-UNITA-NUOVE', 'STATBLOCCHI', 'Schede_dei_Personaggi',
            'PNG/', 'LaMiniera', 'Belkram', 'Celebromorfosi',
        ])
        # Strict statblock signature: need BOTH an HP-like stat AND an AC-like stat
        # (or an explicit CR token). Avoids false positives from narrative docs
        # that only happen to mention "HP" or "CR" in prose.
        head = content[:4000]
        has_hp = re.search(r'\b(HP|PF|hp|Hit Points|Punti Ferita)[:\s]*\d+', head) is not None
        has_ac = re.search(r'\b(AC|CA|Armor Class|Classe Armatura)[:\s]*\d+', head) is not None
        has_cr_explicit = re.search(r'(\*\*CR\*\*|\bCR[:\s]+\d|\bGS[:\s]+\d|Challenge Rating)', head, re.IGNORECASE) is not None
        has_stat = (has_hp and has_ac) or has_cr_explicit
        if not (is_statblock_folder or has_stat):
            continue
        cr = extract_cr(content, path.name)
        if cr is None:
            continue  # no CR → can't use in encounter builder
        name = extract_name(content, path.name)
        faction = guess_faction(name + " " + rel + " " + content[:500])
        env = guess_env(content[:500] + " " + rel)
        role = guess_role(content[:500] + " " + name)
        rec_id = f"{slugify(name)}-{short_hash(rel)}"
        notes_m = re.search(r'\*\*Notes\*\*[:\s]*(.+?)$', content, re.MULTILINE)
        notes = notes_m.group(1).strip() if notes_m else ""
        records.append({
            "id": rec_id,
            "name": name,
            "cr": cr,
            "faction": faction,
            "role": role,
            "environment": env,
            "source_file": rel,
            "notes": notes[:200],
        })
    return records

def to_yaml(records):
    """Minimal YAML writer (no external deps)."""
    lines = ["# Auto-generated by scripts/build_monster_catalog.py",
             "# Do NOT edit by hand. Add custom monsters in monster_catalog.custom.yaml",
             f"# Total records: {len(records)}",
             "monsters:"]
    for r in sorted(records, key=lambda x: (x['faction'], x['cr'] or 0, x['name'])):
        lines.append(f"  - id: {r['id']}")
        lines.append(f"    name: {json.dumps(r['name'], ensure_ascii=False)}")
        lines.append(f"    cr: {r['cr'] if r['cr'] is not None else '~'}")
        lines.append(f"    faction: {r['faction']}")
        lines.append(f"    role: {r['role']}")
        lines.append(f"    environment: {r['environment']}")
        lines.append(f"    source_file: {json.dumps(r['source_file'], ensure_ascii=False)}")
        if r['notes']:
            lines.append(f"    notes: {json.dumps(r['notes'], ensure_ascii=False)}")
    return "\n".join(lines) + "\n"

def main():
    print(f"[catalog] Scanning {ROOT} ...", file=sys.stderr)
    records = scan_directory(ROOT)
    print(f"[catalog] Found {len(records)} monster records.", file=sys.stderr)
    OUT.write_text(to_yaml(records), encoding='utf-8')
    print(f"[catalog] Wrote {OUT}", file=sys.stderr)
    if not CUSTOM.exists():
        CUSTOM.write_text(
            "# monster_catalog.custom.yaml — user-edited append-only list.\n"
            "# Same schema as monster_catalog.yaml. Merged at read-time by\n"
            "# suggest_encounter.py. Not overwritten by build_monster_catalog.py.\n"
            "monsters: []\n", encoding='utf-8')
        print(f"[catalog] Created empty {CUSTOM}", file=sys.stderr)

if __name__ == "__main__":
    main()
