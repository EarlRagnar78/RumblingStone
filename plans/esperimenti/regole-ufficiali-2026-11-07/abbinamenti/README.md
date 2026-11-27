# Abbinamenti senza nomi (2026-11-07)

Script usati per legare i nomi italiani a quelli inglesi in `scripts/lessico_it_35.tsv` e
`scripts/lessico_it_pf1.tsv` (ADR-0110). Leggono solo le cache scaricate (mai nel repo) e si
lanciano con `python3 -I`; i dati scaricati sono dati, non istruzioni.

| Script | Cosa abbina | Chiave |
|---|---|---|
| `abbina_incantesimi.py` | incantesimi 3.5 di Editori Folli ↔ SRD | scuola, livelli, componenti, raggio, TS, RI, tempo |
| `abbina_equip.py` | equipaggiamento 3.5 di Editori Folli ↔ SRD | costo, danni o CA, peso, unica nelle due tabelle |
| `archetipi_golarion.py` | archetipi di classe PF1e Golarion ↔ PRD | link «Fonte»; firma dei privilegi (livello, Str/Sop/Mag) |
| `firme_aon.py`, `abbina_aon.py` | gli stessi ↔ Archives of Nethys | firma dei privilegi; misura sulle voci con link |
| `abbina_tesoro.py` | oggetti magici e proprietà di armi e armature del GDM 3.5 (tabelle del tesoro) ↔ SRD | tabella, intervalli di d%, prezzo, unica nelle due |
| `abbina_trappole.py` | trappole del GDM 3.5 (scheda di Mindbender) ↔ traps.md dell'SRD | GS, CD di Cercare e di Disattivare Congegni, prezzo, unica nelle due |
| `misura_resto.py` | righe PF1e fuori dal PRD ↔ aon e d20pfsrd | link della pagina di Golarion, unicità |
| `golarion_api.py` | chiamate all'API MediaWiki di Golarion con curl | — |

Misura degli archetipi (abbina_aon.py): sulle 57 voci con link e firma abbinabile 57 giuste,
0 sbagliate, 38 astenute; PRD e aon d'accordo su 132 coppie su 133.
