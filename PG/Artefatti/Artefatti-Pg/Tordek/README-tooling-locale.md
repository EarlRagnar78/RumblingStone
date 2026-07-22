# Tooling locale (T6a, 2026-07-03)

> Nota d'igiene: questi 4 file sono script/asset **usa-e-getta** che hanno
> generato/modificato le schede HTML di questa cartella durante la
> produzione, non tool riutilizzabili come `scripts/render_map_svg.py`
> (repo root). Percorsi assoluti hardcoded alla macchina originale
> (`/home/jfs/Scrivania/...`): **non eseguibili così come sono** in un altro
> ambiente. Conservati per storico/provenienza (D10), non spostati in
> `scripts/` per non farli passare per tooling generico del repo.

| File | Cosa fa |
|---|---|
| `apply_styles.py` | ha applicato il CSS a `04_Bracieri_Gemelli_Scheda_PG_Fuoco.html` (path assoluto hardcoded) |
| `rewrite_table.py` | ha riscritto una sezione tabella di `05_Bracieri_Gemelli_Scheda_PG_Completa.html` (path relativo) |
| `generate_therysol.py` | ha generato `Bestiario/png/Therysol/Therysol.html` dal `.md` gemello (path assoluto hardcoded, fuori da questa cartella) |
| `b64_20pct.txt` | blob base64 (immagine) usato come asset di input da uno degli script sopra |

Se serve rigenerare una di queste schede, trattare lo script come
riferimento/pseudocodice e aggiornare i path prima di eseguirlo.
