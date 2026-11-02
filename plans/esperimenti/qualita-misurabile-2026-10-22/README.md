# Calibrazione delle misure di prosa sui voti ciechi del DM

Prova del 2026-10-22 per il lotto 7 di
[PIANO-AVVENTURE-COMMUNITY](../../PIANO-AVVENTURE-COMMUNITY-2026-10.md).

- `COPPIE-VOTATE.json`: le 38 coppie votate alla cieca dal DM (giro 2: 16,
  giro 3: 9, prova scrittura-italiana: 13), con la versione vincente e la
  perdente. Le coppie votate «=» restano fuori.
- `calibra_prosa.py`: diciassette misure prese dalla letteratura (§2 della
  ricerca) o già nel repo, e per ognuna quante volte è più alta nella versione
  vincente. Si rifà con
  `python3 plans/esperimenti/qualita-misurabile-2026-10-22/calibra_prosa.py plans/esperimenti/qualita-misurabile-2026-10-22/COPPIE-VOTATE.json`.
- `CALIBRAZIONE.txt`: l'uscita.

Esito: nessuna misura prevede il voto (p ≥ 0,057). Lettura in
[RICERCA-QUALITA-MISURABILE-2026-10](../../RICERCA-QUALITA-MISURABILE-2026-10.md) §3.
