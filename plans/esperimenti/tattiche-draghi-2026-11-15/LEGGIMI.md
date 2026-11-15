# Tattiche dei draghi: simulazione (15/11/2026)

- `TATTICHE-PROPOSTE.md`: la proposta per ogni drago (carattere, cosa sa, quattro domande, tabella «se i PG...», misura).
- `simula_scontri.py`: il motore generico, nato da `duello-skullcrusher-2026-11-15/simula_duello.py`. Lo usa anche il thread di villain e PNG, con i suoi profili in `profili_villain.py`.
- `profili_draghi.py`: Fauci, Tyrgarun (Fase 4) e Arbitrax, ognuno con la tattica del canone e quella nuova.
- `ESITI-tabelle.md`: 20.000 prove per riga, seme 1372. `ESITI-buff4.md`: Fauci con i bonus d'attacco di Thorik e Tordek alzati di 4.

Uso: `python3 simula_scontri.py [--scontro fauci|tyrgarun|arbitrax] [--prove N] [--buff N]`
(senza `-I`: i profili si importano dalla cartella dello script).
