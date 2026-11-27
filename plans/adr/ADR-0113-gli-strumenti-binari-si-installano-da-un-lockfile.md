# ADR-0113 — Gli strumenti binari si installano da un lockfile, con lo sha256, anche in bundle

**Stato**: **superata** da [ADR-0116](ADR-0116-typst-si-installa-da-pypi.md) il 2026-11-08: typst e l'imposizione arrivano da PyPI, e mise, `mise.lock`, `strumenti.py` e Renovate sono usciti dal repo. Prima: proposta (2026-11-08); D1 decisa dal DM il 2026-11-08 («Dopo 14 giorni e 10 run»), D3 risolta con lo script di avvio dell'ambiente (2026-11-08), D2 al DM
**Data**: 2026-11-08
**Decisione-fonte**: il DM (Jfs), 2026-11-08, nel thread «Rendere i regolamenti plugin attivabili»: *«scarica typst 0.15.1 ma bisogna fare un automatismo che permette l'installazione in automatico al variare dei pacchetti […] usa l'architettura a microkernel e design guidato dai dati […] la migliore, la più std in assoluto e la più verificabile ed automatizzabile»*; *«tutto quello che serve deve essere scaricato come bundle con tutti i requisiti, vedi ad esempio come è fatto e l'idea di gsamuele78/iemod-fetch»*; *«se ci sono delle scelte di sviluppo […] usa sempre la versione migliore adottata dalla comunità degli sviluppatori e standard de facto»*.
**Rapporti**: attua il §3 di [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) (versione fissata, mai «latest») e la versione citata di [ADR-0027](ADR-0027-imposizione-con-pdfcpu.md) (pdfcpu v0.11.0); segue [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (mise entra in testing) e [ADR-0100](ADR-0100-il-rilascio-e-una-pr.md) (i bundle vanno nel rilascio con SHA256SUMS e Sigstore); [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (l'installatore è solo libreria standard).

## Contesto

La versione di typst era scritta **due volte** in `.github/workflows/ci.yml` (`TYPST_VERSION`, due job), `scripts/ambiente.py` la leggeva dal YAML con una regex e `scripts/binari.py` consigliava `releases/latest`, cioè il contrario di ADR-0020 §3. L'archivio si scaricava con `curl` **senza controllare lo sha256**. pdfcpu non si installava da nessuna parte: in CI l'imposizione non è mai stata provata. Nei container delle sessioni cloud ogni binario si scaricava a mano, ogni volta. Nessun bot poteva proporre l'aggiornamento: Dependabot non legge né un `env:` di un workflow né mise.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **`mise.toml` + `mise.lock` come dati, due lettori: mise (standard di fatto) e `scripts/strumenti.py` (kernel stdlib); bundle per piattaforma nel rilascio; Renovate per gli aggiornamenti** (scelta) | i file sono il formato standard di mise, che Renovate sa aggiornare (lockfile compreso); il kernel non ha bisogno di un binario in più dove mise non c'è (sessioni cloud, chi non lo usa); due implementazioni indipendenti si controllano a vicenda sui byte; il bundle installa senza rete, come in iemod-fetch | il formato di `mise.lock` è di mise: se cambia (`lockfile_version`), il kernel va adeguato (il test lo dice); Renovate è un'app da installare (passo del DM) |
| Solo mise (`jdx/mise-action` in CI, `mise install` ovunque) | una sola implementazione, la più diffusa | nel container cloud mise è un binario da scaricare e da far girare prima di tutto il resto, e lì l'esecuzione di binari scaricati è bloccata se il DM non la chiede ogni volta (misurato il 2026-11-08); niente bundle offline senza scrivere comunque del codice |
| asdf + `.tool-versions` | storico, molti plugin | nessun lockfile con checksum: i plugin sono script shell che scaricano quello che vogliono; mise è il suo successore compatibile |
| aqua (`aqua.yaml` + `aqua-checksums.json`) | checksum e registro firmato, Renovate lo supporta | meno diffuso di mise fuori dal mondo Go; un binario in più ovunque, stesso problema del container |
| Nix / devbox | riproducibilità totale | richiede Nix installato (non su Bazzite senza layering, non nel container), curva ripida; sproporzionato per due binari statici |
| Script nostro con versioni e sha256 in un JSON nostro | nessuna dipendenza | formato inventato: nessun bot lo aggiorna, nessuno strumento esterno lo legge; è il «reinventare la ruota» che il DM esclude |
| Dependabot | già in uso | non supporta né mise né versioni in `env:` di un workflow |

## Decisione

**Le versioni dei binari esterni stanno solo in `mise.toml`; URL e sha256 per piattaforma stanno in `mise.lock`, generato da `mise lock`. Chi installa legge quei due file e rifiuta un archivio con un altro sha256.**

1. **Dati.** `mise.toml` in radice: `[tools]` con chiavi esplicite di backend (`"aqua:typst/typst" = "0.15.1"`, `"github:pdfcpu/pdfcpu" = "0.11.0"`, perché pdfcpu non è nel registro aqua), versioni esatte, `[settings] lockfile = true, locked = true` e `lockfile_platforms` (linux-x64, linux-arm64, macos-arm64, windows-x64). `mise.lock` (`lockfile_version = 3`) con `url` e `checksum = "sha256:…"` per ogni piattaforma. Uno strumento nuovo è una riga e un `mise lock`, nessuna riga di codice.
2. **Kernel.** `scripts/strumenti.py` (solo stdlib, `tomllib`) sa fare cinque cose generiche: leggere i dati, scaricare, verificare lo sha256, estrarre **un** file (quello col nome dello strumento; gli estrattori per formato sono la sola parte a plugin), registrarlo in `.strumenti/installati.json`. Non conosce typst né pdfcpu. È idempotente: se lo sha registrato torna, non scarica. `binari.trova()` guarda `.strumenti/bin` **prima** del PATH; `ambiente.py` e `binari.py` leggono versione e istruzioni da qui.
3. **CI.** I job bloccanti installano con `strumenti.py installa --github-path` e `verifica` (la versione detta dal binario deve essere quella fissata). Il job `strumenti` (canale **testing**, ADR-0099) usa `jdx/mise-action` con mise fissato per versione e sha256, controlla che `mise.lock` sia quello che `mise lock` scriverebbe, e che **mise e strumenti.py installino gli stessi byte**.
4. **Bundle.** Il workflow Release costruisce per ogni piattaforma `rumblingstone-strumenti-<os>-<arch>-<tag>.zip`, sul modello di iemod-fetch: gli archivi originali di upstream (con le loro licenze, stesso sha256 del lockfile), le wheel di `requirements.txt` per Python 3.13 su quella piattaforma, `mise.toml`, `mise.lock`, `strumenti.py` e `BUNDLE.json` con lo sha256 di ogni file. Lo zip è riproducibile (nomi ordinati, `SOURCE_DATE_EPOCH`, permessi fissi), va in `SHA256SUMS` ed è attestato con Sigstore come l'archivio delle skill. Senza rete: `strumenti.py installa --bundle <zip> [--con-ruote]`.
5. **Aggiornamenti.** `renovate.json` abilita **solo** il manager `mise` (pip, Actions e Docker restano a Dependabot) con una PR di gruppo il lunedì. La PR passa dal job `strumenti`, che boccia un lockfile non rigenerato.
6. **Sessioni cloud.** L'hook SessionStart esegue `strumenti.py installa --silenzioso` (solo con `CLAUDE_CODE_REMOTE=true`) e una regola `permissions.allow` per `python3 scripts/strumenti.py`. La modifica di `.claude/` è un passo del DM (D3).

## Conseguenze

- Una versione si cambia in un posto, e la CI la verifica: un URL di un'altra versione, uno sha256 sbagliato, un lockfile non rigenerato sono rossi.
- L'installazione in CI diventa **più severa** di prima (prima `curl` senza checksum), a parità di byte: il typst installato ha lo stesso sha256 di quello che usciva dal `curl` di prima.
- pdfcpu entra in CI per la prima volta, alla versione misurata da ADR-0027; il salto a 0.16.x lo propone Renovate, con la sua misura.
- **Quello che non diventa gratis.** Il formato di `mise.lock` può cambiare con mise (mise 2026.11.4 avvisa già che `lockfile_version = 3` non è l'ultimo e propone `mise lock --upgrade`; si resta su 3 finché il kernel non legge il formato nuovo, misurato): il test `test_strumenti` e il job `strumenti` lo dicono, il kernel va adeguato a mano. Il bundle con le wheel è riproducibile **sullo stesso giorno**, non per sempre: `requirements.txt` dice `>=`, quindi le wheel scelte cambiano quando escono versioni nuove (lo dice `BUNDLE.json`). Fissarle richiede un lock delle dipendenze Python, che è un'altra decisione. Renovate ospitato esegue `mise lock` senza permessi in più solo in *safe mode* (`MISE_SAFE=1`, mise ≥ 2026.7.12, letto nel sorgente di Renovate 44.222.4): per questo `mise.toml` chiede `min_version = "2026.7.12"` e `renovate.json` fissa `constraints.mise` alla versione della CI; se la safe mode non basta, la PR resta rossa al job `strumenti` finché qualcuno non esegue `mise lock`.

### Dopo i 504 del 2026-11-08 (PR #338, #341)

Il giorno stesso della #338 GitHub Releases ha risposto 504 per ore, a typst, a pdfcpu e al binario di mise, mentre githubstatus diceva «operational». Lezioni, tutte applicate:

- **Ritenti.** `strumenti.py` fa 7 tentativi in circa 2 minuti (`ATTESE = (2, 4, 8, 16, 30, 60)`); il job `strumenti` ha `MISE_HTTP_RETRIES=8`.
- **Cache che si riempie anche a job rosso.** `actions/cache` salva solo se il job finisce verde, quindi il primo run buono non arrivava mai. Si usano `actions/cache/restore` e `actions/cache/save` separati, il save con `if: always()` e solo se la cartella non è vuota; chiave `strumenti-<sha di mise.lock>-<sha del contenuto>`, restore per prefisso. `STRUMENTI_CACHE` è `.strumenti-cache` nel workspace (gitignored) e `strumenti.py` usa un archivio in cache **solo se il suo sha256 è quello di `mise.lock`**: una cache corrotta o di un'altra versione si riscarica. Vale nei job validate, strumenti e misura di stampa e nel Release.
- **Nessun mirror.** `ghcr.io/typst/typst:0.15.1` ha un binario con un altro sha256 (908d5a47… contro 29273eaa…): non è lo stesso artefatto e non si usa.
- **Check richiesti.** Sul ramo main il ruleset chiede solo «Validate skills & scripts» e «Build skill packages»; CodeQL è il *default setup* di GitHub, non si configura da un workflow.
- **Anche mise sotto Renovate.** La versione di mise nel job `strumenti` (`version: vX.Y.Z`, la forma del tag, che `mise-action` accetta togliendo la v) e il suo sha256 li aggiorna un `customManager` regex con il datasource `github-release-attachments`: trova lo sha corrente nel `SHASUMS256.txt` del tag, lo rimappa sul tag nuovo e riscrive entrambi. Un secondo `customManager` aggiorna `constraints.mise`. Tutto nello stesso gruppo «strumenti binari», con `minimumReleaseAge` di 3 giorni (un rilascio ritirato entro tre giorni non arriva).
- **Sessioni cloud (D3).** Al posto dell'hook in `.claude/` (bloccato come auto-modifica) lo script di avvio dell'ambiente cloud esegue `strumenti.py installa --silenzioso` se il repo c'è; non blocca l'avvio se la rete manca.

- **typst da PyPI (2026-11-08): [ADR-0116](ADR-0116-typst-si-installa-da-pypi.md).** Il binding `typst` di PyPI (0.15.2, compilatore 0.15.1 dentro) non passa da GitHub Releases. Sui 19 booklet (856 pagine) dà testo e pixel identici alla CLI ([misura](../esperimenti/typst-pip-2026-11-08/MISURE.md)). Il DM l'ha fatto diventare lo standard: per typst il punto 3 qui sopra vale solo per il ripiego e per il confronto, pdfcpu resta com'è.

**Da rivedere se**: il job `strumenti` trova byte diversi fra mise e strumenti.py; oppure dopo 14 giorni e 10 run verdi (si promuove mise nei job bloccanti, D1); oppure Renovate in 4 settimane non apre PR con il lockfile aggiornato (si passa a un Renovate in GitHub Actions con `allowedUnsafeExecutions`, D2); oppure mise cambia licenza (oggi MIT).

### Decisioni aperte al DM

- **D1.** ✅ **Decisa (DM, 2026-11-08): (a)**. mise sale nei job bloccanti dopo 14 giorni e 10 run in testing senza differenze di byte, come vuole ADR-0099. Le alternative erano (a) e (b) subito.
- **D2.** Chi aggiorna: (a) l'app Renovate ospitata, che installi tu su gsamuele78/RumblingStone *(consigliata)*; (b) Renovate in un workflow nostro con un token tuo come segreto.
- **D3.** ✅ **Risolta (2026-11-08)**: l'installazione nelle sessioni cloud la fa lo script di avvio dell'ambiente, configurato dal DM fuori dal repo; il patch di `.claude/` non serve più.
