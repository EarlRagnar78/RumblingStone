"""Prove del simulatore dei duelli di ARC-08: i tre esiti del comandante e
l'1 e il 20 naturali sui tiri salvezza (SRD 3.5, «Automatic Failures and
Successes»)."""
import importlib.util
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
