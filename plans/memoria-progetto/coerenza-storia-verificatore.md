---
name: coerenza-storia-verificatore
[riga riservata · sha256:5002e9df]
metadata:
  type: project
  modified: 2026-11-13T23:52:32.496Z
---

`scripts/coerenza_campagna.py fatti DIR [--state] [--tattiche]` (canale testing, ADR-0125). Storia delle misure: MS-0075, MS-0087 e ESITO.md in `plans/esperimenti/coerenza-storia-2026-11-12/` e `grafo-eventi-2026-11-12/`.

**Su main:** S1, S5, S6, S7 (#379), laboratorio grafo eventi (#383), S8 tattiche del Bestiario contro `verifica_scheda --fatti` (#396: 0 violazioni su 220 menzioni, mutanti 181/183; incantesimo senza corsivo scartato).

**#419 unita il 14/11 (merge 2fc24cde sopra a3d01520, MS-0117):** `conoscenze[].dal_giorno` e `informato_da` nello schema; 27 righe su 33 con un giorno (senza: Sonjak su Sal, Ghostlord, Xal'thor sui Bracieri, Collezionista su Therysol, Therysol su Dauth, Tiri Kitor). D1-D4 e DEF-1 r.69 nel canone; il Collezionista sa dei Custodi dalla sua gilda dal Giorno 22. Regola T2 (chi informa ha una riga con giorno non successivo): 0 violazioni, confronto fra PNG e non fra fatti. T1 resta in grafo.py: mancano chiave del fatto, alias e finestra di giorni per file. Una PR di canone vuole il sì di Jfs su una card anche con la CI verde.

[riga riservata · sha256:73408cce]

**#481 (bozza, 18/11, testa efb2f782 su main 3b414589, MS-0168 e MS-0169):** (1) quickstart e Armate §4b ai Day 30-32 del Torneo di Dauth e alle finestre di state.yaml; fonte dei tre giorni: P2B-Torneo-DAUTH-DM-MASTER-REFERENCE §1.1, non state.yaml. La scelta di Jfs su questo punto l'ha riferita il coordinatore (card del canale, tocco non allegabile): la PR resta in bozza finché non tocca la card del calendario nel mio thread (cmsg_019sykApdKEBBe8D8NJyiFEGTTDeFmR4jZz99LA8omyCVF). (2) «Mirtul» → «Flamerule»: Jfs ha toccato «Sì, tutti, lettera compresa» (13:05 UTC); 31 occorrenze in 9 file, lettera di Brenna «diciannovesimo di Flamerule». Cancello `scripts/tests/test_calendario_flamerule.py`: cerca solo la parola «Mirtul» (la regola mese contro Giorno di Marcia non è stata scritta) e tollera 7 righe della #472 nel dizionario IN_ATTESA, da svuotare quando la #472 è su main. Le 3 contraddizioni candidate sui giorni del verificatore sono falsi allarmi.

**Why:** la misura dice che il verificatore rende solo sui fatti già strutturati; il collo di bottiglia è estrarre il fatto dalla prosa (RAG 3B: 0 veri su 23).

**How to apply:** niente motori logici o modelli senza un campo strutturato in state.yaml; ogni campo nuovo si verifica con una regola corta. I test non leggono `conoscenze` per posizione. Un MS fuori sequenza è bocciato: la PR in coda tiene il numero libero e rinumera al riallineo. Prima di dire «CI verde» leggere mergeable_state. Cerimonia delle 100 Asce = Day 21. Prima di citare un file di campaign/sessions o recaps come cronaca, leggere la testata: può essere canone preparato e non giocato. Vedi [[prolog-verificatore-regole]].

**Prova del lettore sulla RTX 4050 (19/11):** qwen2.5:7b via Ollama, 636 risposte; criterio di ESITO.md non raggiunto (SÌ a 499 candidati su 560 su main, a 78 domande su 79 sulle righe dei mutanti). Il RAG resta fuori dal verificatore; riprovare solo cambiando la domanda al lettore. Scritto in ESITO.md (commit 283bea10 sulla #481, MS-0170 provvisoria). Dati in /mnt/project-files/prove-4050-risultati/2026-11-19/. Jfs il 18/11 19:16 UTC: «La 481 è ok»; la #481 aspetta il turno del coordinatore e va riallineata su main (dopo la #472 svuotare IN_ATTESA nel cancello Flamerule e aggiornare il corpo della PR).
