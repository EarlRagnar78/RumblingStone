# Pacchetti Typst vendorizzati

> **Perché stanno qui e non su `packages.typst.org`.** `@preview/...` fa
> scaricare il pacchetto a `typst` alla prima compilazione. Una catena di stampa
> che dipende dalla rete non è riproducibile: la build di oggi e quella dell'anno
> prossimo possono divergere senza che nessuno tocchi il repo, e su una macchina
> offline non parte affatto. Qui il pacchetto è **contenuto del repo**, con la sua
> licenza, e si aggiorna a mano. Decisione: [ADR-0026](../../../plans/adr/ADR-0026-vendoring-pacchetti-typst.md),
> sul precedente di [ADR-0010](../../../plans/adr/ADR-0010-vendoring-skill-terzi.md)
> (vendoring per cherry-pick, mai collezioni).

Il percorso è passato a `typst` con `--package-path` da
`scripts/export_booklet_typst.py` (costante `PACCHETTI`). Il layout è quello che
`typst` si aspetta: `<namespace>/<nome>/<versione>/`.

| Pacchetto | Versione | Licenza | Upstream | Serve a |
|---|---|---|---|---|
| `droplet` | 0.3.1 | MIT — © Eric Biedert | [EpicEricEE/typst-droplet](https://github.com/EpicEricEE/typst-droplet) | **capolettera annegato** (H2): l'iniziale che scende dentro il paragrafo, come nei volumi Paizo |
| `in-dexter` | 0.7.2 | Apache-2.0 — JKRB / in-dexter Contributors | [RolfBremer/in-dexter](https://github.com/RolfBremer/in-dexter) | **indice analitico** (H2): voci marcate nel testo, pagina raccolta in coda |

**Provenienza**: copiati da [`typst/packages`](https://github.com/typst/packages)
al commit `359500f2` (2026-09-02), da `packages/preview/<nome>/<versione>/`.
Tolti i file che il `typst.toml` di ciascuno già dichiara in `exclude` (asset,
test, gallery, PDF campione): non servono alla compilazione e pesano.
**Le licenze restano nei file `LICENSE`, integre** — è la condizione per cui
possiamo tenerli qui.

## Aggiornarli

Non è automatico (ADR-0010 §3) e non deve esserlo:

```sh
git clone --filter=blob:none --sparse https://github.com/typst/packages.git
cd packages && git sparse-checkout set packages/preview/droplet packages/preview/in-dexter
# copia la versione nuova accanto alla vecchia, aggiorna l'import nel .typ,
# ricompila i volumi e GUARDA le pagine. Poi togli la vecchia.
```

Due versioni possono convivere: il percorso le tiene separate. La vecchia si
toglie **dopo** che i volumi sono stati ricompilati e visti, mai prima.

## Il controllo

`scripts/tests/test_pacchetti_typst.py` verifica che ogni pacchetto dichiarato
qui esista con il suo `typst.toml` e il suo `LICENSE`, che la versione sul disco
sia quella della cartella, e — se `typst` è installato — che un documento che li
importa **compili senza rete**.
