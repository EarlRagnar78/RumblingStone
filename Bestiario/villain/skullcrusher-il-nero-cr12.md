# Skullcrusher il Nero — drago nero ancestrale [POINTER — statblocco nell'arco] [RIMANDO]
**Key stats**: → `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md` e `07_il Portale Della Forgia Eterna/ERRATA-ARC07-35-Verification.md` §2.3 (i numeri stanno li'; duplicarli qui creerebbe una seconda copia che diverge alla prima errata — ADR-0021).

**Faction**: orda-antica-372dr | **Role**: flier | **Environment**: aerial | **CR**: 12
> 🕰️ **Fazione d'epoca.** L'assedio di Hammerfist e' del **~372 DR**, mille anni
> prima della Mano Rossa: tenerli insieme farebbe proporre a `suggest_encounter`
> un incontro che mescola due ere e non puo' esistere. `orda-antica-372dr`
> esisteva gia' per Balvar Fuocospento, il consigliere della stessa orda.
**Source**: `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P5-FASTPLAY.md` (statblocco giocabile, GS 12: CA 27, PF 240, soffio acido 12d4 CD 24; battaglia antica di ~372 DR)
**Status**: POINTER — NON duplicare lo statblock qui. Usare sempre il file d'arco.

## Summary

**Il capostipite della stirpe di Fauci di Palude**, mille anni prima della campagna. Cadde sotto Aegis Fang impugnata da **Thorgrim Barbadiferro**; i PG lo affrontano nel viaggio a ~372 DR, e la Corona mostra le due immagini sovrapposte — questo drago adesso, e Fauci di Palude sopra una Hammerfist che brucia.

⚠️ **La fonte sta dentro `_ARCHIVIO/`, e non e' una copia.** `ARC07-MATRICE-VERSIONI.md` la dichiara **MASTER** (D8: il power-up e' voluto). Gli archivi restano fuori dall'**indicizzazione** — una copia farebbe un record doppio, ed e' la regola che `test_archivi_non_indicizzati.py` prova a rovescio — ma un master dichiarato deve restare **raggiungibile**: e' quello che fa questo POINTER, senza indicizzare l'archivio.

Questa voce esiste perche' `build_monster_catalog.py` e `suggest_encounter.py` scansionano `Bestiario/` per popolare il pool degli incontri: senza, una creatura con statistiche scritte non e' raggiungibile da nessuno strumento. Ogni modifica va fatta nel file d'arco.

## Notes

🔎 **Lo statblocco sta nel FASTPLAY, non nella sintesi.** La prima stesura di questa voce puntava a `07_il Portale Della Forgia Eterna/_ARCHIVIO/PortaleForgia-P6-INTEGRAZIONE-Completa.md`, che il drago lo **nomina** soltanto; i numeri stanno in `-P5-FASTPLAY.md`, e `07_il Portale Della Forgia Eterna/ERRATA-ARC07-35-Verification.md` §2.3 lo dichiara per esteso. L'ha trovato il cancello di D18, che vedeva due voci «Skullcrusher il Nero».

✅ **GS 12 — deciso dal DM il 2026-09-17.** La riga di `PortaleForgia-P6-INTEGRAZIONE-Completa.md` diceva `CR 11` e quella di `Mappe/ARC07-MAPPE-DEFINITIVO.md` r.558 diceva **GS 12**: vale il secondo, e il file d'archivio porta adesso l'errata accanto alla riga.

🔴 **Terzo «Skullcrusher» del repo**, e i tre non vanno confusi: *Grom Skullcrusher* (Barbaro 14, Torneo di Dauth), *Ogre Skullcrusher* (GS 5), e questo drago. E' la forma d'errore che `test_grom_non_e_l_ogre_skullcrusher` gia' presidia.
