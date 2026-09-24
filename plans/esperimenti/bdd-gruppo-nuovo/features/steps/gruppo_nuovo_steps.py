"""Gli step BDD di gruppo_nuovo.feature: gli stessi controlli di test_gruppo_nuovo.py.

Esperimento della RICERCA-BDD-O-TDD (2026-09-24): non gira in CI, perche'
behave non e' una dipendenza del repo (ADR-0037). Si lancia con
`behave plans/esperimenti/bdd-gruppo-nuovo/features` da un venv con behave.
"""
from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from behave import given, then, when

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "tests"))

import yaml  # noqa: E402

import validate_state  # noqa: E402
from dmcore import gruppo_nuovo as G  # noqa: E402

MINIME = {"gruppo": "beta", "livello": 5, "righe": {},
          "pg": [{"nome": "Brunna", "razza": "Nana", "classe": "Guerriera", "livello": 5, "pf": 48}]}


def _pg_di_prima(ctx):
    return [p["pg"].split()[0] for p in ctx.stato["party"]]


def _completa(ctx, **risposte):
    ctx.base, ctx.domande = G.deriva(copy.deepcopy(ctx.stato))
    r = copy.deepcopy(MINIME)
    r["arco_partenza"] = ctx.stato["archi"][0]["arco"]
    r.update(risposte)
    ctx.nuovo = G.completa(ctx.base, ctx.domande, r)


# ── Contesto ─────────────────────────────────────────────────────────────
@given("lo stato di campagna di oggi")
def step_stato(ctx):
    ctx.stato = yaml.safe_load((ROOT / "campaign" / "state.yaml").read_text(encoding="utf-8"))


# ── Derivazione ──────────────────────────────────────────────────────────
@when("derivo lo stato del gruppo nuovo")
def step_deriva(ctx):
    _completa(ctx)


@then('le domande una alla volta sono {a:d} di "{sa}", {b:d} di "{sb}" e {c:d} di "{sc}"')
def step_conta(ctx, a, sa, b, sb, c, sc):
    conti = {}
    for d in ctx.domande:
        conti[d.sezione] = conti.get(d.sezione, 0) + 1
    assert conti == {sa: a, sb: b, sc: c}, conti


@then('ogni domanda offre "{x}", "{y}" e "{z}" e mostra il testo')
def step_scelte(ctx, x, y, z):
    for d in ctx.domande:
        assert d.scelte == (x, y, z) and d.campi and all(d.testo[c] for c in d.campi)


@then("restano {n:d} conoscenze, nessuna sul party o sui PG di prima")
def step_conoscenze(ctx, n):
    assert len(ctx.nuovo["conoscenze"]) == n, len(ctx.nuovo["conoscenze"])
    for r in ctx.nuovo["conoscenze"]:
        testo = f"{r['sa_che']} {r.get('come') or ''}"
        assert not any(p in testo for p in _pg_di_prima(ctx)), testo
        assert not re.search(r"\bparty\b", testo.lower()), testo


@then("gli artefatti sono tutti ancora lì, senza portatore")
def step_artefatti(ctx):
    assert [a["artefatto"] for a in ctx.nuovo["artefatti"]] == [a["artefatto"] for a in ctx.stato["artefatti"]]
    for a in ctx.nuovo["artefatti"]:
        assert a["portatore"] == "—" and not any(p in a["oggi"] for p in _pg_di_prima(ctx))


@then("gli echi sono vuoti e il March Clock è al giorno 1")
def step_partita(ctx):
    assert ctx.nuovo["echi"] == [] and ctx.nuovo["march_clock"]["giorno_corrente"] == 1
    for w in ctx.nuovo["march_clock"]["waypoints"]:
        assert "✅" not in w["stato"] and "SYNC POINT" not in w["stato"]
    for a in ctx.nuovo["archi"]:
        assert not (a.get("note") and any(p in a["note"] for p in _pg_di_prima(ctx)))


@then("ogni clock numerico è a zero con lo stesso massimo")
def step_clock_zero(ctx):
    prima = {v["png_id"]: v for v in ctx.stato["villain"]}
    for v in ctx.nuovo["villain"]:
        m = G.CLOCK_NUMERICO.match(str(prima[v["png_id"]]["clock"]))
        if m:
            assert v["clock"] == f"0/{m.group(2)}", v
        assert v["stato"] == "attivo" and v["tempo"] == "preparato"


@then("ogni clock che è un trigger è rimasto com'era")
def step_trigger(ctx):
    prima = {v["png_id"]: v for v in ctx.stato["villain"]}
    for v in ctx.nuovo["villain"]:
        vecchio = prima[v["png_id"]]["clock"]
        if not G.CLOCK_NUMERICO.match(str(vecchio)):
            assert v["clock"] == vecchio


@then("anagrafica dei PNG, scenari di Rethmar, villain e archi sono quelli di prima")
def step_prodotto(ctx):
    assert ctx.nuovo["png"] == ctx.stato["png"]
    assert ctx.nuovo["scenari_rethmar"] == ctx.stato["scenari_rethmar"]
    assert len(ctx.nuovo["villain"]) == len(ctx.stato["villain"])
    assert len(ctx.nuovo["archi"]) == len(ctx.stato["archi"])


# ── Risposte ─────────────────────────────────────────────────────────────
@when("rispondo arco {n:d} e livello {liv:d}")
def step_arco(ctx, n, liv):
    ctx.n = n
    _completa(ctx, arco_partenza=ctx.stato["archi"][n - 1]["arco"], livello=liv)


@then('l\'arco {n:d} è in corso al livello "{liv}"')
def step_arco_in_corso(ctx, n, liv):
    a = ctx.nuovo["archi"][n - 1]
    assert a["tempo"] == "in_corso" and a["pg_livello"] == liv
    assert all(x["tempo"] == "preparato" for i, x in enumerate(ctx.nuovo["archi"]) if i != n - 1)


@then('gli archi prima dell\'{n:d} sono "{stato}"')
def step_prima(ctx, n, stato):
    assert all(a["stato"] == stato for a in ctx.nuovo["archi"][:n - 1])


@then('gli archi dopo l\'{n:d} sono "{stato}"')
def step_dopo(ctx, n, stato):
    assert all(a["stato"] == stato for a in ctx.nuovo["archi"][n:])


@when('rispondo con un PG "{nome}", "{razza}", "{classe}", livello {liv:d}, PF {pf:d}')
def step_pg(ctx, nome, razza, classe, liv, pf):
    _completa(ctx, pg=[{"nome": nome, "razza": razza, "classe": classe, "livello": liv, "pf": pf}])


@then('il party è "{nome}", classe "{classe}", PF "{pf}", attivo')
def step_party(ctx, nome, classe, pf):
    (p,) = ctx.nuovo["party"]
    assert (p["pg"], p["classe"], p["hp"], p["stato"]) == (nome, classe, pf, "attivo"), p


@when("tengo tutte le righe tranne la seconda, che svuoto, e la terza, che rivedo")
def step_tsr(ctx):
    _, domande = G.deriva(copy.deepcopy(ctx.stato))
    righe = {d.id: "tieni" for d in domande}
    righe.update({domande[1].id: "svuota", domande[2].id: "rivedi"})
    _completa(ctx, righe=righe)


@then("la prima riga è com'era")
def step_prima_riga(ctx):
    d = ctx.domande[0]
    assert all(G.trova(ctx.nuovo, d)[c] == d.testo[c] for c in d.campi)


@then("la seconda riga porta il segnaposto")
def step_seconda(ctx):
    d = ctx.domande[1]
    assert all(G.trova(ctx.nuovo, d)[c] == G.SEGNAPOSTO for c in d.campi)


@then("la terza riga è com'era e c'è una sola domanda aperta, che punta a lei")
def step_terza(ctx):
    d = ctx.domande[2]
    assert all(G.trova(ctx.nuovo, d)[c] == d.testo[c] for c in d.campi)
    (inf,) = ctx.nuovo["inferred"]
    assert inf["id"] == "INF-001" and inf["a_chi"] == "DM"
    assert inf["dove"] == f"{d.sezione}[{d.indice}].{d.campi[0]}"


@when("rispondo senza scegliere nessuna riga")
def step_nessuna(ctx):
    _completa(ctx)


@then("ogni riga è diventata una domanda aperta")
def step_tutte_aperte(ctx):
    assert len(ctx.nuovo["inferred"]) == len(ctx.domande)


@when("rispondo il minimo indispensabile")
def step_minimo(ctx):
    _completa(ctx)


@then("validate_state non trova errori")
def step_valido(ctx):
    assert validate_state.errori(ctx.nuovo, ROOT) == []


SBAGLIATE = {
    "nessun PG": {"pg": []},
    "sette PG": {"pg": [MINIME["pg"][0]] * 7},
    "livello 0": {"livello": 0},
    "un arco che non esiste": {"arco_partenza": "99 Non Esiste"},
    "un gruppo con spazi": {"gruppo": "Nome Con Spazi!"},
    "una scelta inventata": "SCELTA",
    "una riga che non esiste": {"righe": {"villain:non-esiste": "tieni"}},
    "un PG con zero PF": {"pg": [{"nome": "X", "razza": "Nano", "classe": "Guerriero",
                                  "livello": 5, "pf": 0}]},
}


@when("rispondo con {caso}")
def step_sbagliata(ctx, caso):
    base, domande = G.deriva(copy.deepcopy(ctx.stato))
    r = copy.deepcopy(MINIME)
    r["arco_partenza"] = ctx.stato["archi"][0]["arco"]
    extra = SBAGLIATE[caso]
    r.update({"righe": {domande[0].id: "forse"}} if extra == "SCELTA" else extra)
    try:
        G.completa(base, domande, r)
        ctx.rifiutata = False
    except G.RispostaNonValida:
        ctx.rifiutata = True


@then("la risposta è rifiutata")
def step_rifiutata(ctx):
    assert ctx.rifiutata


# ── Contratto e terminale ────────────────────────────────────────────────
@when('chiedo il modulo con "dm.py gruppo nuovo --domande"')
def step_domande(ctx):
    ctx.esito = subprocess.run([sys.executable, "scripts/dm.py", "gruppo", "nuovo", "--domande"],
                               cwd=ROOT, capture_output=True, text=True)


@then('l\'uscita è JSON con le righe di "{a}", "{b}" e "{c}"')
def step_json(ctx, a, b, c):
    assert ctx.esito.returncode == 0, ctx.esito.stderr
    dati = json.loads(ctx.esito.stdout)
    assert {d["sezione"] for d in dati["righe"]} == {a, b, c}
    assert dati["campi"]["pg"]["massimo"] == 6


@when("compilo il modulo in terminale tenendo tutte le righe tranne l'ultima")
def step_terminale(ctx):
    _, domande = G.deriva(copy.deepcopy(ctx.stato))
    ctx.n_domande = len(domande)
    righe = ["gamma", "1", "", "1", "Kael", "Umano", "Mago", "", "20"] + ["1"] * (len(domande) - 1) + [""]
    ctx.esito = subprocess.run([sys.executable, "scripts/gruppo_nuovo.py", "--dry-run"], cwd=ROOT,
                               input="\n".join(righe) + "\n", capture_output=True, text=True)


@then("il resoconto dice tutte le righe tenute tranne una da rivedere")
def step_resoconto(ctx):
    assert ctx.esito.returncode == 0, ctx.esito.stderr
    assert f"righe: {ctx.n_domande - 1} tenute, 0 svuotate, 1 da rivedere" in ctx.esito.stdout


@when("interrompo il modulo a metà")
def step_ctrl_d(ctx):
    ctx.esito = subprocess.run([sys.executable, "scripts/gruppo_nuovo.py", "--dry-run"], cwd=ROOT,
                               input="delta\n1\n", capture_output=True, text=True)


@then("il comando esce 1 e dice che non ha scritto niente")
def step_niente(ctx):
    assert ctx.esito.returncode == 1 and "niente scritto" in ctx.esito.stdout


# ── Da capo a fondo ──────────────────────────────────────────────────────
def _copia_git(ctx, sporco: bool):
    from test_new_group import _copia
    ctx.tmp = tempfile.TemporaryDirectory()
    ctx.radice = Path(ctx.tmp.name)
    _copia(ctx.radice)
    (ctx.radice / ".gitignore").unlink()
    shutil.copy(ROOT / ".gitignore", ctx.radice / ".gitignore")
    for cmd in (["init", "-q", "-b", "main"], ["config", "user.email", "t@t"],
                ["config", "user.name", "t"], ["add", "-A"], ["commit", "-q", "-m", "base"]):
        subprocess.run(["git", *cmd], cwd=ctx.radice, check=True, capture_output=True)
    if sporco:
        (ctx.radice / "campaign" / "sporco.md").write_text("x\n", encoding="utf-8")


@given("una copia del repo sotto git")
def step_copia(ctx):
    _copia_git(ctx, sporco=False)


@given("una copia del repo sotto git con un file non committato")
def step_copia_sporca(ctx):
    _copia_git(ctx, sporco=True)


@when('lancio "dm.py gruppo nuovo" con il file di risposte')
def step_lancio(ctx):
    r = copy.deepcopy(MINIME)
    r["arco_partenza"] = ctx.stato["archi"][0]["arco"]
    f = Path(tempfile.mkdtemp()) / "r.json"
    f.write_text(json.dumps(r), encoding="utf-8")
    ctx.esito = subprocess.run([sys.executable, "scripts/gruppo_nuovo.py", "--answers", str(f),
                                "--repo-root", str(ctx.radice)],
                               cwd=ctx.radice, capture_output=True, text=True)


def _ramo(ctx):
    return subprocess.run(["git", "branch", "--show-current"], cwd=ctx.radice,
                          capture_output=True, text=True).stdout.strip()


@then('sono sul ramo "{ramo}" e campaign/ è committato')
def step_ramo(ctx, ramo):
    assert ctx.esito.returncode == 0, ctx.esito.stdout + ctx.esito.stderr
    assert _ramo(ctx) == ramo
    assert subprocess.run(["git", "status", "--porcelain", "--", "campaign"], cwd=ctx.radice,
                          capture_output=True, text=True).stdout == ""


@then('group.yaml dice "{riga}" e render_state --check è verde')
def step_group(ctx, riga):
    assert riga in (ctx.radice / "campaign" / "group.yaml").read_text(encoding="utf-8")
    assert subprocess.run([sys.executable, "scripts/render_state.py", "--check"],
                          cwd=ctx.radice, capture_output=True).returncode == 0
    ctx.tmp.cleanup()


@then('il comando esce 1 e resto sul ramo "{ramo}"')
def step_resto(ctx, ramo):
    assert ctx.esito.returncode == 1 and _ramo(ctx) == ramo
    ctx.tmp.cleanup()
