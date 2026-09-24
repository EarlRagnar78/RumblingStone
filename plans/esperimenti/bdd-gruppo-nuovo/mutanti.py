"""I 16 mutanti di RICERCA-BDD-O-TDD-2026-09 §4, applicati alle due suite.

Uso, dalla radice del repo:  python3 plans/esperimenti/bdd-gruppo-nuovo/mutanti.py <behave>
dove <behave> e' l'eseguibile di un venv con behave e pyyaml. Ogni mutazione
si applica, si lanciano le due suite, e il file si ripristina anche se qualcosa
va storto.
"""
import pathlib, subprocess, sys, time
BEHAVE = sys.argv[1]
C = "scripts/dmcore/gruppo_nuovo.py"; G = "scripts/gruppo_nuovo.py"
MUT = [
 ("M1 clock non azzerato", C, 'v["clock"] = f"0/{m.group(2)}"', 'v["clock"] = f"{m.group(1)}/{m.group(2)}"'),
 ("M2 «party» non conta nelle conoscenze", C, "                or party.search(f\"{c.get('sa_che')} {c.get('come') or ''}\"))]", "                or False)]"),
 ("M3 «PG» non e' una traccia", C, 'alternative = [re.escape(n) for n in nomi] + [r"PGs?"]', 'alternative = [re.escape(n) for n in nomi] + [r"ZZZQ"]'),
 ("M4 portatore tenuto", C, '        a["portatore"] = "—"\n', ''),
 ("M5 March Clock non riparte", C, '    mc["giorno_corrente"] = 1\n', ''),
 ("M6 echi tenuti", C, '    s["echi"] = []\n', ''),
 ("M7 senza risposta vale tieni", C, 'scelta = scelte.get(d.id, "rivedi")', 'scelta = scelte.get(d.id, "tieni")'),
 ("M8 zero PG accettati", C, 'if not 1 <= len(pg) <= MASSIMO_PG:', 'if not 0 <= len(pg) <= MASSIMO_PG:'),
 ("M9 scelta inventata accettata", C, 'if scelta not in SCELTE:', 'if False:'),
 ("M10 archi dopo marcati non giocati", C, '        elif passato:\n', '        else:\n'),
 ("M11 nome del gruppo non controllato", C, 'if not GRUPPO.match(gruppo):', 'if False:'),
 ("M12 percorso dei waypoint sbagliato", C, 'radice = "march_clock.waypoints" if d.sezione == "waypoints" else d.sezione', 'radice = d.sezione'),
 ("M13 albero sporco ignorato", G, 'if not gitio.is_clean(radice):', 'if False:'),
 ("M14 niente commit", G, '    _git(radice, "commit", "-q", "-m", f"Gruppo {gruppo}: sessione 0 (dm.py gruppo nuovo)")\n', ''),
 ("M15 Ctrl-D esce 0", G, '        print("\\n[gruppo] interrotto: niente scritto")\n            return 1', '        print("\\n[gruppo] interrotto: niente scritto")\n            return 0'),
 ("M16 PF al posto del livello nella classe", C, "{int(p['livello'])} ({p['razza'].strip()})", "{int(p['pf'])} ({p['razza'].strip()})"),
]
def gira(cmd):
    t = time.time(); r = subprocess.run(cmd, capture_output=True, text=True); return r.returncode, time.time() - t
tot = {"u": 0, "b": 0}; tu = tb = 0
for nome, f, old, new in MUT:
    p = pathlib.Path(f); orig = p.read_text(encoding="utf-8")
    assert orig.count(old) == 1, nome
    p.write_text(orig.replace(old, new), encoding="utf-8")
    try:
        ru, du = gira([sys.executable, "-m", "pytest", "-q", "-x", "scripts/tests/test_gruppo_nuovo.py"])
        rb, db = gira([BEHAVE, "-f", "null", "--stop", "plans/esperimenti/bdd-gruppo-nuovo/features"])
    finally:
        p.write_text(orig, encoding="utf-8")
    tot["u"] += ru != 0; tot["b"] += rb != 0; tu += du; tb += db
    print(f"{nome:42} unittest {'UCCISA' if ru else 'viva  '}  behave {'UCCISA' if rb else 'viva  '}")
print(f"uccise: unittest {tot['u']}/{len(MUT)} · behave {tot['b']}/{len(MUT)} · tempo unittest {tu:.0f}s · behave {tb:.0f}s")
