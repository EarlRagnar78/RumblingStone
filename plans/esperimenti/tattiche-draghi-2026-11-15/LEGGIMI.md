# Tattiche dei draghi: simulazione (15/11/2026)

- `TATTICHE-PROPOSTE.md`: la proposta per ogni drago (carattere, cosa sa, quattro domande, tabella «se i PG...», misura).
- `simula_scontri.py`: il motore generico, nato da `duello-skullcrusher-2026-11-15/simula_duello.py`. Lo usa anche il thread di villain e PNG, con i suoi profili in `profili_villain.py`.
- `profili_draghi.py`: Fauci, Tyrgarun (Fase 4) e Arbitrax, ognuno con la tattica del canone e quella nuova.
- `ESITI-tabelle.md`: 20.000 prove per riga, seme 1372. `ESITI-buff4.md`: Fauci con i bonus d'attacco di Thorik e Tordek alzati di 4.
- Corredo dei draghi (card del DM del 21/11/2026): i profili e le tabelle qui restano quelli del 15/11. Le misure del corredo sono state fatte con due script fuori dal repo (`/mnt/project-files/draghi-corredo-2026-11-21/misura_fauci.py` e `misura_tyr.py`, seme 1372) che cambiano CA e TS dei profili con `dataclasses.replace`. Fauci con fuga a 112 e corredo solo difensivo (CA +2/+4, TS +2/+3, 4.000 prove per riga): gli esiti si spostano di 1-3 punti, dentro il rumore. Tyrgarun in Fase 4 con anello di protezione +3 e mantello della resistenza +3 (CA 40, TS +3): ucciso nel 21-40% degli scontri invece del 23-45%, almeno un PG morto da 0 a 1 punto in più. Il motore non modella pergamene e pozioni, e le stime dei PG sono quelle di prima del 21/11.

Uso: `python3 simula_scontri.py [--scontro fauci|tyrgarun|arbitrax] [--prove N] [--buff N]`
(senza `-I`: i profili si importano dalla cartella dello script).
