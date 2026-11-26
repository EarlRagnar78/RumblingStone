"""Prove del simulatore dei duelli di ARC-08: i tre esiti del comandante,
l'1 e il 20 naturali sui tiri salvezza (SRD 3.5, «Automatic Failures and
Successes»), e l'orog della guardia nera letto dalla sua scheda del Bestiario."""
import importlib.util
import re
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "simula_scontri_epici", Path(__file__).with_name("simula_scontri_epici.py"))
sim = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sim)


def _capo(pf, fuga, iniz):
    def fn():
        return [sim.Nemico("capo", pf, 1, [], rifl=0, iniz=iniz, fuga=fuga, ruolo="boss")]
    return fn


def _esiti(fn, n=200, **kw):
    sim.R.seed(11)
    return [sim.duello(fn, ["Yrsa"], **kw)["esito"] for _ in range(n)]


def test_il_capo_portato_a_zero_non_e_una_fuga():
    # 1 pf, agisce per ultimo: il primo colpo a segno lo abbatte prima del suo turno
    esiti = _esiti(_capo(1, 0.5, -100))
    assert "fugge" not in esiti
    assert esiti.count("abbattuto") > 150


def test_il_capo_sotto_soglia_al_suo_turno_fugge():
    # agisce per primo ed e' gia' sotto la soglia: fugge con tutti i suoi pf
    assert set(_esiti(_capo(1000, 2000, 100))) == {"fugge"}


def test_nessuno_dei_due_esiti():
    assert set(_esiti(_capo(100000, 0, 0), n=20, round_max=2)) == {None}


def test_tiro_salvezza_uno_naturale_fallisce_sempre(monkeypatch):
    monkeypatch.setattr(sim.R, "randint", lambda a, b: 1)
    assert sim.riflessi(40, ts=30, cd=10) == 40
    assert sim.riflessi(40, ts=30, cd=10, eludere=True) == 40


def test_tiro_salvezza_venti_naturale_riesce_sempre(monkeypatch):
    monkeypatch.setattr(sim.R, "randint", lambda a, b: 20)
    assert sim.riflessi(40, ts=0, cd=40) == 20
    assert sim.riflessi(40, ts=0, cd=40, eludere=True) == 0


def _dadi(*primi):
    """randint finto: prima i valori dati, poi sempre 1 (i dadi dei danni)."""
    coda = iter(primi)
    return lambda a, b: next(coda, 1)


def test_conferma_del_critico_uno_naturale_non_conferma(monkeypatch):
    # la conferma e' un altro tiro per colpire: l'1 naturale manca sempre
    # (SRD 3.5, «Combat I», Attack Roll e Critical Hits)
    monkeypatch.setattr(sim.R, "randint", _dadi(20, 1))
    assert sim.colpo(100, 10, (1, 4), 0) == 1


def test_conferma_del_critico_venti_naturale_conferma(monkeypatch):
    # il 20 naturale colpisce sempre, anche contro una CA che il bonus non tocca
    monkeypatch.setattr(sim.R, "randint", _dadi(20, 20))
    assert sim.colpo(0, 1000, (1, 4), 0) == 2


# --- l'orog del simulatore e' quello del Bestiario --------------------
_RADICE = Path(__file__).resolve().parents[3]
_OROG = _RADICE / "Bestiario/mostri/orog-guardia-nera-guerriero6-cr7.md"


def _scheda_orog():
    """I numeri dell'orog dal recinto ```statblocco della sua scheda."""
    blocco = re.search(r"```statblocco\n(.*?)```", _OROG.read_text(encoding="utf-8"), re.S).group(1)

    def campo(regex):
        return re.search(regex, blocco, re.M).groups()

    (ca,) = campo(r"^ca: (\d+)")
    (pf,) = campo(r"^pf: (\d+)")
    (dv,) = campo(r"^pf-dado: (\d+)d")
    (rifl,) = campo(r"^ts: .*Rifl ([+-]\d+)")
    (iniz,) = campo(r"^iniziativa: ([+-]\d+)")
    a1, a2, dmg = campo(r"ascia bipenne \+1 \+(\d+)/\+(\d+) \(1d12\+(\d+)/x3\)")
    return dict(ca=int(ca), pf=int(pf), dv=int(dv), rifl=int(rifl), iniz=int(iniz),
                att=(int(a1), int(a2)), dmg=int(dmg))


def _orog(avanzati):
    return [n for n in sim.grimjaw(avanzati)() if n.nome.startswith("orog")]


def _attesi(s, k):
    # Attacco Poderoso -3 (+6 danni a due mani), Tattico Superiore +2 a colpire;
    # dal round 2 anche la Furia Comandante, +2 a colpire e ai danni
    primo = [(s["att"][0] - 3 + 2 + k, (1, 12), s["dmg"] + 6 + k, 20, 3, ""),
             (s["att"][1] - 3 + 2 + k, (1, 12), s["dmg"] + 6 + k, 20, 3, "")]
    poi = [(b + 2, dd, f + 2, mn, ml, t) for (b, dd, f, mn, ml, t) in primo]
    return primo, poi


def test_orog_del_simulatore_e_quello_del_bestiario():
    s = _scheda_orog()
    primo, poi = _attesi(s, 0)
    orog = _orog(False)
    assert len(orog) == 4
    for o in orog:
        assert (o.pfmax, o.ca, o.rifl, o.iniz) == (s["pf"], s["ca"], s["rifl"], s["iniz"])
        assert o.primo == primo
        assert o.attacchi == poi


def test_orog_avanzato_e_la_scheda_con_l_archetipo_pf1e():
    # Avanzato PF1e, regole rapide: +2 a tutti i tiri e ai danni, +4 alla CA, +2 pf per DV
    s = _scheda_orog()
    primo, poi = _attesi(s, 2)
    for o in _orog(True):
        assert (o.pfmax, o.ca, o.rifl, o.iniz) == (s["pf"] + 2 * s["dv"], s["ca"] + 4, s["rifl"] + 2, s["iniz"] + 2)
        assert o.primo == primo
        assert o.attacchi == poi
