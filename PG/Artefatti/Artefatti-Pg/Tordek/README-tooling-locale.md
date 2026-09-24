# Tooling locale (T6a, 2026-07-03 · resi portabili nel lotto 4b, 2026-09-10)

> Nota d'igiene: questi 4 file sono script/asset **usa-e-getta** che hanno
> generato/modificato le schede HTML di questa cartella durante la
> produzione, non tool riutilizzabili come `scripts/render_map_svg.py`
> (repo root). Conservati per storico/provenienza (D10), e **non spostati in
> `scripts/`** — non passano lo standard di ADR-0012 e non vanno scambiati per
> tooling generico del repo.

## Cos'è cambiato nel lotto 4b

Fino al 2026-09-10 i path erano **cablati alla scrivania di chi li scrisse**
(`/home/jfs/Scrivania/…`), quindi gli script non partivano altrove. Ora si
ricavano da `__file__` e risalgono alla radice del repo: partono ovunque sia
clonato.

⚠️ **Partendo, sovrascrivono.** Prima erano innocui perché rotti; adesso non lo
sono più. `apply_styles.py` riscrive `04_Bracieri_Gemelli_Scheda_PG_Fuoco.html`
**in place**, e quell'HTML è stato editato a mano dopo l'ultima esecuzione dello
script: rilanciarlo alla cieca perde quelle modifiche. Si esegue solo dopo aver
guardato il diff che produce.

🔎 **Un difetto trovato rendendoli portabili**: i path di `generate_therysol.py`
erano sbagliati **due volte**. Oltre alla macchina, puntavano a
`Bestiario/png/Therysol/Therysol/Therysol.md`, mentre quella cartella si è spostata di un
livello (`Bestiario/png/Therysol/Therysol/`). Finché il path era assoluto e
irraggiungibile, la seconda rottura non si poteva vedere.

| File | Cosa fa |
|---|---|
| `apply_styles.py` | ha applicato il CSS a `04_Bracieri_Gemelli_Scheda_PG_Fuoco.html` (path accanto allo script) |
| `rewrite_table.py` | ha riscritto una sezione tabella di `05_Bracieri_Gemelli_Scheda_PG_Completa.html` (path relativo) |
| `generate_therysol.py` | ha generato `Bestiario/png/Therysol/Therysol/Therysol.html` dal `.md` gemello |
| `b64_20pct.txt` | blob base64 (immagine) usato come asset di input da uno degli script sopra |

Restano **riferimento storico**, non tooling supportato: nessun test li copre,
nessun gate li esegue, e la loro idempotenza non è mai stata verificata.
