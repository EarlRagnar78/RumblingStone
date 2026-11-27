# ADR-0123 — La documentazione segue Diátaxis, una forma per file

**Stato**: accettata (2026-11-10)
**Data**: 2026-11-10
**Decisione-fonte**: il DM (Jfs), card del 2026-11-10 «Come entra Diátaxis nella documentazione del repo?», opzione «Riorganizzare docs/ subito». Era l'alternativa B della [misura](../esperimenti/documentazione-2026-11-10/MISURA-DIATAXIS.md); la consigliata era «regola per le nuove più etichette».
**Rapporti**: passo della documentazione della milestone v1.1.0 (regola del DM del 2026-11-09). Applica a `docs/` la regola dello standard di fatto del 2026-11-08.

## Contesto

Il 2026-11-10 `docs/guides/` aveva 14 guide. Classificando a mano ogni
sezione, 5 stavano in una forma sola e 9 mescolavano ricetta, formato dei file
e perché. Le «Guida completa» di bestiario, booklet e mappe tenevano insieme la
procedura e il formato. `docs/ARCHITETTURA.md` e `docs/RILASCIO.md` stavano
nella radice di `docs/`, fuori da ogni gruppo.

Lo standard di fatto per organizzare la documentazione tecnica è
[Diátaxis](https://diataxis.fr/), con quattro forme: tutorial, guida pratica,
riferimento, spiegazione. Lo adottano, fra gli altri, la documentazione di
Canonical (Ubuntu), di Cloudflare e di NumPy.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Quattro cartelle con i nomi di Diátaxis, guide miste spezzate, rimando al posto della sezione spostata** (scelta) | ogni file ha una forma, e chi cerca una ricetta non legge un formato; i nomi delle cartelle sono quelli dello standard; i rimandi vecchi del tipo «GUIDA-MAPPE §5.1.2» restano veri | ~170 rimandi riscritti in un colpo; tre guide perdono la loro parte di formato, e chi le leggeva intere ora apre due file |
| Regola per le guide nuove ed etichette in `docs/INDEX.md`, nessuno spostamento (la consigliata) | nessun rimando da toccare | le 9 guide miste restano miste finché qualcuno non le tocca, e potrebbe non succedere mai |
| Niente Diátaxis | nessun lavoro | le guide nuove restano senza regola |
| Cartelle con nomi italiani (`guide/`, `riferimento/`…) | coerenti con il resto del repo | non sono i nomi dello standard: chi conosce Diátaxis non li riconosce, e la regola del 2026-11-08 chiede lo standard salvo misura contraria |

## Decisione

`docs/` si divide in `tutorials/`, `how-to/`, `reference/`, `explanation/`, e
ogni file sta nella cartella della sua forma.

1. **Dove sta cosa.** Tutorial: `GUIDA-SETUP-MACCHINA`. Guide pratiche: le
   guide di bestiario, booklet, mappe, immagini, sistemi di gioco, patch del
   ramo di gruppo, condivisione, e `RILASCIO`. Riferimento: marcature, schede
   dei prompt, standard dei tool, plugin di sistema, legenda funzionale, e i
   tre file nuovi `RIFERIMENTO-BESTIARIO`, `RIFERIMENTO-BOOKLET`,
   `RIFERIMENTO-MAPPE`. Spiegazioni: `ARCHITETTURA`, `GUIDA-FLUSSO-LOCALE`, e
   i due file nuovi `CONDIVISIONE-IP-PERCHE`, `LEGENDA-FUNZIONALE-PERCHE`.
2. **Le guide miste si spezzano per sezione.** Una sezione di un'altra forma
   va nel file della sua forma e **tiene il suo numero**. Nella guida resta il
   titolo con una riga che porta al nuovo posto. Così l'ancora resta valida e
   un rimando scritto prima («GUIDA-BESTIARIO §3») porta ancora alla cosa
   giusta. Una sezione breve di un'altra forma in fondo a un file (un «Perché
   così» di poche righe) resta dov'è.
3. **Restano fuori dalle quattro forme** `docs/tools/`, che è il registro
   generato dal manifest (riferimento, ma il suo percorso è letto da
   orchestratori e dal server MCP: spostarlo romperebbe la superficie
   pubblica della v1.0.0), `docs/audit/`, che sono registri datati e
   cricchetti della CI, `docs/assets/` e `docs/INDEX.md`.
4. **I nomi dei file non cambiano**, salvo i cinque nati dalle divisioni:
   meno rimandi da riscrivere, e il nome dice già l'argomento.
5. **`docs/guides/README.md`** elenca i traslochi per chi arriva da un
   collegamento vecchio. Si toglie alla v1.2.0.
6. **Una guida nuova nasce in una forma sola**, con la riga «Forma:» in testa
   come le altre.

## Conseguenze

- Chi cerca una ricetta apre `how-to/`, chi cerca un formato apre
  `reference/`. `docs/INDEX.md` §3 elenca i file per forma.
- I rimandi a `docs/guides/…`, `docs/ARCHITETTURA.md` e `docs/RILASCIO.md` sono
  stati riscritti in tutto il repo, compresi ADR e piani chiusi: è un cambio di
  percorso, non di contenuto. `validate_docs.py` controlla che nessun
  collegamento sia rotto.
- Le tre guide spezzate iniziano con alcune righe di rimando al posto delle
  sezioni che hanno ceduto. È il prezzo dei rimandi storici che restano veri.
- La classificazione è a giudizio, non a macchina. Una sezione di confine si
  può spostare con una PR senza un ADR nuovo.

**Da rivedere se**: una guida torna a mescolare due forme per più del 20%
delle sue sezioni, oppure il sito della documentazione passa a un generatore
(MkDocs, Sphinx) che impone un'altra struttura.
