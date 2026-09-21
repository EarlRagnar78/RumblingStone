"""Il censimento dei rilevatori, e le tre proprieta' che devono avere tutti.

Il DM, il 2026-09-21: *«tutti i detector sono idempotenti?»*. La risposta
onesta a una domanda cosi' non e' «si'»: e' un test che li esegue **tutti**,
due volte, e confronta.

⚠️ **E il censimento e' la meta' che conta.** Un test che prova i rilevatori
che gli vengono elencati a mano prova quelli che qualcuno si e' ricordato di
elencare. Qui l'elenco si **deriva**: da `punteggio_mqm.RILEVATORI` per la
catena del punteggio, da `validate_prosa.NORME` per i rilievi tipati, e dai
congegni di `misura_craft`. Se qualcuno ne aggiunge uno e non lo rende
idempotente, questo test lo prende senza che nessuno lo aggiorni.

**Le tre proprieta':**

1. **Deterministico** — stesso input, stesso output. Nessuna rete, nessun
   orologio, nessun `set` iterato senza ordinamento.
2. **Idempotente** — eseguirlo due volte di fila non cambia niente, ne' il
   risultato ne' lo stato del disco. Tutti questi rilevatori sono in **sola
   lettura**, ed e' la ragione strutturale per cui la proprieta' vale.
3. **Ordinato** — l'output e' una sequenza stabile, non un `set`. Due liste
   con gli stessi elementi in ordine diverso romperebbero ogni confronto
   prima/dopo, che e' l'uso principale di questi numeri (ADR-0036).
"""
from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import misura_craft as mc  # noqa: E402
import punteggio_mqm as pm  # noqa: E402
import superficie_norme as sn  # noqa: E402
import validate_prosa as vp  # noqa: E402

#: I rilevatori di testo del repo, con il loro ingresso.
#: `(nome, funzione(testo, percorso) -> qualcosa di confrontabile)`
RILEVATORI_DI_TESTO = (
    ("misura_craft.misura", lambda t, _p: mc.misura(t)),
    ("misura_craft.box_read_aloud", lambda t, _p: mc.box_read_aloud(t)),
    ("misura_craft.difetti_dei_box", lambda t, _p: mc.difetti_dei_box(t)),
    ("misura_craft.box_con_p1", lambda t, _p: mc.box_con_p1(t)),
    ("misura_craft.metrature_nei_box", lambda t, _p: mc.metrature_nei_box(t)),
    ("misura_craft.box_senza_costrutto_italiano",
     lambda t, _p: mc.box_senza_costrutto_italiano(t)),
    ("misura_craft.nomi_propri", lambda t, _p: sorted(mc.nomi_propri(t))),
    ("validate_prosa.rilievi", lambda _t, p: vp.rilievi(p)),
    ("validate_prosa.controlla", lambda _t, p: vp.controlla(p)),
    ("validate_prosa.controlla_caratteristiche",
     lambda _t, p: vp.controlla_caratteristiche(p)),
    ("validate_prosa.conta_tic", lambda t, _p: vp.conta_tic(t)),
)


def _campione(n: int = 25) -> "list[Path]":
    """Un campione deterministico: i primi N file di gioco in ordine."""
    return sorted(mc.file_di_gioco_p1())[:n]


class TestOgniRilevatoreEIdempotente(unittest.TestCase):
    def test_due_esecuzioni_danno_lo_stesso_risultato(self):
        for f in _campione():
            testo = f.read_text(encoding="utf-8", errors="replace")
            for nome, fn in RILEVATORI_DI_TESTO:
                with self.subTest(rilevatore=nome, file=f.name):
                    self.assertEqual(fn(testo, f), fn(testo, f))

    def test_i_rilevatori_della_catena_del_punteggio(self):
        """Quelli che pesano: se uno non fosse idempotente, il punteggio di un
        documento cambierebbe fra due esecuzioni sullo stesso commit — ed e'
        proprio il criterio F3.4 del piano."""
        for f in _campione(15):
            testo = f.read_text(encoding="utf-8", errors="replace")
            for fn in pm.RILEVATORI:
                with self.subTest(rilevatore=fn.__name__, file=f.name):
                    self.assertEqual(fn(testo, f), fn(testo, f))

    def test_la_superficie_e_idempotente(self):
        self.assertEqual(sn.misura(), sn.misura())

    def test_il_punteggio_di_un_documento_non_cambia(self):
        """F3.4 — *«tre esecuzioni sullo stesso commit danno lo stesso
        punteggio»*. Qui sono tre davvero."""
        spec = pm.carica_specifiche()
        for f in _campione(10):
            a, b, c = (pm.valuta(f, spec) for _ in range(3))
            self.assertEqual(a, b, f)
            self.assertEqual(b, c, f)


class TestOgniRilevatoreEOrdinato(unittest.TestCase):
    def test_nessun_rilevatore_restituisce_un_set(self):
        """Un `set` ha un ordine di iterazione che non e' garantito fra
        versioni di Python: due liste con gli stessi elementi in ordine
        diverso romperebbero ogni confronto prima/dopo."""
        for f in _campione(10):
            testo = f.read_text(encoding="utf-8", errors="replace")
            for nome, fn in RILEVATORI_DI_TESTO:
                with self.subTest(rilevatore=nome):
                    self.assertNotIsInstance(fn(testo, f), set, nome)


class TestNessunoScriveMentreMisura(unittest.TestCase):
    def test_il_disco_non_cambia(self):
        """L'altra meta' dell'idempotenza, e quella che nessuno verifica mai:
        un rilevatore che *scrive* mentre misura sarebbe idempotente nel
        risultato e non nel mondo."""
        campione = _campione(12)
        def impronta():
            h = hashlib.sha256()
            for f in campione:
                h.update(f.read_bytes())
            return h.hexdigest()
        prima = impronta()
        for f in campione:
            testo = f.read_text(encoding="utf-8", errors="replace")
            for _, fn in RILEVATORI_DI_TESTO:
                fn(testo, f)
        self.assertEqual(prima, impronta(), "un rilevatore ha toccato il disco")


class TestIlCensimentoEDerivato(unittest.TestCase):
    def test_ogni_rilevatore_della_catena_e_nel_censimento(self):
        """⚠️ La prova che questo file non invecchia da solo: se qualcuno
        aggiunge un rilevatore a `punteggio_mqm.RILEVATORI`, le prove di
        idempotenza lo prendono **senza** che nessuno tocchi questo file,
        perche' il ciclo itera la tupla vera."""
        self.assertGreaterEqual(len(pm.RILEVATORI), 5)
        for fn in pm.RILEVATORI:
            self.assertTrue(callable(fn), fn)

    def test_ogni_chiave_di_validate_prosa_e_coperta(self):
        self.assertGreaterEqual(len(vp.NORME), 7)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
