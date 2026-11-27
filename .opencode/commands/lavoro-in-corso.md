---
description: Rigenera plans/LAVORO-IN-CORSO.md e riassume il lavoro in sviluppo fuori da main
---

Dalla radice del repo, rigenera l'istantanea del lavoro in corso:

```bash
python3 scripts/lavoro_in_corso.py --fetch $ARGUMENTS
```

Senza rete aggiungi `--offline`; sul PC del DM la cartella condivisa dei thread
non c'è, e la pagina lo dice da sola. Poi leggi `plans/LAVORO-IN-CORSO.md` e
riassumi in italiano, in poche righe:

1. i filoni che aspettano il DM (`aspetta-jfs`) e che cosa aspettano;
2. i filoni in corso, con le PR e il passo dopo;
3. ciò che sta «Senza filone» (PR, rami, cartelle): proponi a quale filone
   attaccarlo o se chiuderlo, senza cambiare il registro da solo;
4. ciò che è «Da aggiornare o ferme»;
5. dalla sezione «Canali della piattaforma (ADR-0099)», i componenti in
   `testing` e da quando, con quelli vicini al passaggio a stable (14 giorni e
   10 run su `main`, poi l'ok del DM), e i filoni che dichiarano un canale.

Non modificare la pagina a mano: si corregge `plans/lavoro-in-corso.json`,
poi `python3 scripts/lavoro_in_corso.py --check` e si rigenera. Ciò che è già
su `main` sta in `MEMORIA.md`.
