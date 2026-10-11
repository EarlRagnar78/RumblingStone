# PIANO — L'ambiente riproducibile: la macchina come la CI

> **Stato**: 🔵 pianificato (2026-10-08), D1-D11 decise dal DM lo stesso giorno · **Classe**: G per il contratto, C per i lotti
> **Nasce da**: un brief incollato dal DM il 2026-10-08, *«Deterministic
> Developer & TTRPG Campaign Environment Bootstrapper, CI-Parity Framework, and
> Verification System»*, con la richiesta: *«verifica prima questo prompt e
> correggilo se trovi errori, imprecisioni o problemi con il repo da affrontare,
> poi parti dal piano, dall'ADR e da tutto quello che serve per realizzarlo
> davvero»*. Poi, sulle derive misurate: *«la CI è lo standard e l'ambiente
> locale deve combaciare»*.
> **Decisione**: [ADR-0081](adr/ADR-0081-il-contratto-d-ambiente.md).
> **Ordine**: dopo il lotto mappe D28 di LETTORE-E-PLAYTESTER (D4).
>
> **In breve**: la CI è il riferimento e la macchina deve combaciare con lei,
> versione per versione. Il brief chiedeva di costruire da zero cose che il repo
> ha già (una fonte unica dell'ambiente, un `doctor`, i profili, la guida, la CI
> fissata) e taceva sulla deriva che c'è davvero. Il piano tiene del brief il
> metodo (stati espliciti, prova funzionale, si toglie solo ciò che si possiede,
> il secondo giro non cambia niente) e lo applica a otto derive misurate oggi,
> estendendo `binari.py` e `dm.py` invece di affiancarli.

---

## §1 · Cosa ho guardato prima, e cosa questo piano NON rifà

| Documento o file | Cosa copre | Qui |
|---|---|---|
| [PIANO-QUALITA-DEL-CODICE](PIANO-QUALITA-DEL-CODICE.md) lotto D (✅) | `scripts/binari.py`: Python minimo, binari, librerie, catene; `dm.py doctor` ne legge | **si estende**: il registro prende versione, checksum e classe di parità. Non nasce un secondo registro |
| [ADR-0002](adr/ADR-0002-cli-unica-dm-orchestratore.md) | `dm.py` è l'unico ingresso | vincolo: l'orchestratore del brief è `dm.py ambiente`, non un eseguibile nuovo |
| [ADR-0037](adr/ADR-0037-stdlib-only-e-le-sue-eccezioni.md) | stdlib-only, tre eccezioni a runtime, due piani (`requirements.txt` per il DM, `-dev` per CI e sviluppo) | vincolo: l'orchestratore è stdlib-only. Il lock (D3) e Python 3.13 (D7) vanno scritti come emendamenti |
| [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md) | il canone si scrive solo sul ramo del gruppo | vincolo: il setup non tocca mai `campaign/` |
| [ADR-0020](adr/ADR-0020-edizione-da-stampa-su-un-secondo-binario.md), [ADR-0027](adr/ADR-0027-imposizione-con-pdfcpu.md) | typst e pdfcpu accettati come binari | il piano ne fissa versione e checksum, non rimette in discussione la scelta |
| [PIANO-PRATICHE-DI-INGEGNERIA](PIANO-PRATICHE-DI-INGEGNERIA.md) PI-3, PI-3b | Dependabot raggruppato, `pip-audit`, `dipendenze.yml` (audit e test sulle versioni minime), runner fissato a `ubuntu-24.04`, immagine Docker per digest | **non si rifà**. A3 fa convivere il lock con Dependabot e con il test delle minime |
| [`docs/guides/GUIDA-SETUP-MACCHINA.md`](../docs/guides/GUIDA-SETUP-MACCHINA.md) | la guida di setup, 234 righe | si riscrive in A7 attorno a `dm.py ambiente`. Il `SETUP.md` del brief sarebbe un doppione |
| `scripts/install-git-hooks.sh`, `.claude/hooks/session-start.sh` | hook `post-merge` e `pre-push`; il sync delle skill all'avvio | A4 ridisegna gli hook; il sync delle skill all'avvio di Claude Code resta com'è |
| `scripts/booklet-container/` | Chromium di Debian in container | resta per chi lo vuole; con D10 la versione di riferimento di Chromium è Chrome for Testing |

Perché un piano nuovo e non un lotto di PRATICHE: quel piano governa il flusso
su GitHub (rami, PR, revisione, sicurezza delle dipendenze); questo governa cosa
gira **sulla macchina** e come lo si prova uguale alla CI. Dove un lotto qui
tocca un file di PRATICHE (`ci.yml`, `dipendenze.yml`, `dependabot.yml`) lo
dichiara.

## §2 · Il brief, corretto

| Brief | Cosa dice | Correzione |
|---|---|---|
| §6 «se non esiste una fonte, creala» | una fonte unica delle versioni | esiste: `binari.py`. Le manca la **versione**: typst e pdfcpu sono dichiarati senza numero, e la CI fissa typst 0.15.1 per conto suo. Si completa la fonte (A1) |
| §9 «un CLI orchestratore» con `setup plan status doctor verify update uninstall` | un eseguibile nuovo | `dm.py ambiente` con `piano`, `setup`, `verifica`, `stato`, `aggiorna`, `rimuovi`; `dm.py doctor` resta e diventa la vista breve di `verifica` (ADR-0002) |
| §2 i tre profili | DM, Developer, Hybrid | esistono già come due piani di ADR-0037 e come `CATENE` di `binari.py`. Nomi: `dm`, `sviluppo`, `completo` |
| §5 «non forzare la parità identica» | sceglie la parità caso per caso | il DM ha scelto la regola più stretta: **la CI è lo standard, la macchina combacia**. La classe di parità resta per dire *come* si verifica, non per ammettere differenze |
| §32 `SETUP.md` | documento nuovo | si riscrive `GUIDA-SETUP-MACCHINA.md`; le matrici di verifica e di rimozione si **generano** dal registro ([ADR-0034](adr/ADR-0034-generare-dalle-tabelle.md)) |
| §33 «decision record» e §31 «architecture document» | due documenti | un ADR (0081) e questo piano |
| §35 «codice completo, nessun segnaposto», in un colpo | consegna unica | lotti piccoli, un ramo e una PR per lotto (PRATICHE D6), regola d'oro dei piani su ognuno. «Nessun segnaposto» resta vero dentro ogni lotto |
| §14 rollback transazionale | ripristino di ogni mutazione | vero per ciò che si possiede (`.venv`, binari in `~/.local/bin`, hook, stato). Per i pacchetti di sistema c'è un registro (D1, A5c), ma `apt` non ha un *undo*: la rimozione toglie solo ciò che mancava prima, dopo una simulazione mostrata |
| §19 `act` | simulare GitHub Actions in locale | **facoltativo** (D6): un modulo opzionale del profilo `sviluppo`, mai installato senza `--con act`. `act` esegue i workflow in Docker con un'immagine diversa da quella di GitHub, quindi un verde in locale è un aiuto e non una prova; il riferimento resta la CI, e l'equivalente di ogni giorno è `dm.py ambiente verifica` |
| §25 «più sistemi operativi in CI» | matrice di OS | tre piattaforme, decise dal DM (D5): Debian stable, Ubuntu stable, Bazzite. Su Bazzite l'ambiente gira in un distrobox Debian 13 (D9) |
| §17 Git LFS, GPG, chiavi SSH | integrazione | nessun `.gitattributes`, nessun LFS: `NOT_APPLICABLE`. Chiavi e credenziali si **leggono** (`gh auth status`) e non si toccano mai |
| §15 dati di campagna fuori dal repo | `~/.local/share/<project>/campaign/` | sbagliato per questo repo: il canone **è** il repo, sul ramo del gruppo (ADR-0007). Fuori dal repo va solo lo stato dell'orchestratore, in `$XDG_STATE_HOME/rumblingstone/<id-del-clone>/` |
| §0 gli stati `PASS FAIL WARN DRIFT MISSING MISMATCH UNPINNED UNKNOWN SKIPPED NOT_APPLICABLE` | vocabolario | si tiene, in inglese nel JSON (è un contratto per le macchine) e spiegato in italiano nella guida |
| lingua | il brief è in inglese | documenti in italiano (`rumblingstone-prosa-documenti`), identificatori del JSON in inglese |

## §3 · L'audit, misurato il 2026-10-08

Macchina del DM: Debian 13 (trixie), x86_64, kernel 7.1.8. CI: `ubuntu-24.04`,
Python 3.11 da `actions/setup-python@v7`. In sola lettura, nessuna
installazione.

| Componente | Profilo | Locale | CI | Fissato? | Stato |
|---|---|---|---|---|---|
| Python | tutti | 3.13.5 (`/usr/bin/python3`, e il `.venv`) | 3.11 | pavimento `PYTHON_MINIMO = (3, 11)` | **MISMATCH** |
| pyyaml, Pillow, tiktoken | dm | 6.0.3, 12.3.0, 0.14.0 nel `.venv` | l'ultima che pip trova | solo `>=` | **UNPINNED** |
| pytest, pymupdf | sviluppo | 9.1.1, 1.28.2 nel `.venv` | l'ultima | solo `>=` | **UNPINNED** |
| pip-audit | sviluppo | assente nel `.venv` | installato | `>=2.10.1` | **MISSING** in locale |
| typst | dm (stampa) | 0.15.1 in `~/.local/bin` | 0.15.1, scaricato senza checksum | nella CI sì, nel registro no; `binari.py` consiglia `releases/latest` | **UNPINNED** nella fonte |
| pdfcpu | dm (libretto) | 0.11.0 in `~/.local/bin` | non installato | no | **UNKNOWN** in CI |
| Chromium | dm (PDF, PNG) | Chromium 150 (`/usr/bin/chromium`) e Chrome 154 | quello dell'immagine del runner, mai registrato | no | **UNKNOWN** |
| pandoc, xelatex | dm (recap PDF) | pandoc 3.1.11.1, xelatex assente | non usati | no | **WARN**: catena «recap in PDF» non pronta qui |
| shellcheck | sviluppo | presente; **4 avvisi in 2 file** su 26 script (2× SC2115, 2× SC2164) | `continue-on-error` **e** `\|\| true` | no | **WARN**: non può mai bocciare |
| Docker | opzionale | 29.8.1 | job in `dipendenze.yml` | immagine per digest | PASS |
| git, gh | tutti | 2.47.3, 2.46.0 | del runner | no | PASS |
| hook git | sviluppo | **nessuno installato**, `core.hooksPath` vuoto | non usati | — | **MISSING**; `install-git-hooks.sh` sovrascrive hook altrui senza guardare |
| Git LFS, submodule | — | nessuno | nessuno | — | `NOT_APPLICABLE` |
| `build/` (14 MB di mirror) e mirror degli agenti | — | ignorati | — | — | PASS: `git status` pulito |

Il Python di sistema delle tre piattaforme, verificato il 2026-10-08: Debian 13
→ 3.13 (sulla macchina del DM), Ubuntu 24.04 → 3.12, Ubuntu 26.04 → 3.14,
Fedora 43/44 sotto Bazzite → 3.14. **Non c'è una versione nativa comune**: da
qui la D7.

## §4 · Il contratto: la CI è lo standard

**La regola (DM, 2026-10-08)**: la CI definisce le versioni; la macchina
combacia. Un aggiornamento entra **prima in CI**, con una PR che lo prova, e
solo dopo arriva sulla macchina con `dm.py ambiente aggiorna`. Entra quando c'è
una correzione di sicurezza o una funzione che vale il cambio; mai «perché è
uscita».

| Componente | Riferimento | Come combacia | Classe di verifica |
|---|---|---|---|
| Python | **3.13**, la versione di Debian stable (D7) | Debian: di sistema. Ubuntu 24.04: deadsnakes in locale, `setup-python` in CI. Bazzite: dentro il distrobox Debian 13 | VERSIONE (minore esatta) |
| librerie Python | il lock con hash (D3) | `.venv` creato dal lock, `--require-hashes` | VERSIONE (byte per byte) |
| typst, pdfcpu | versione nel registro (A1) | binario statico in `~/.local/bin`, checksum verificato | VERSIONE |
| Chromium | **Chrome for Testing** a una versione fissa (D10) | stessa build su tutte e tre le piattaforme, a livello utente, checksum nel registro | VERSIONE |
| shellcheck | versione nel registro | pacchetto della distro o binario statico | VERSIONE, bloccante in CI (A6) |
| hook, `core.hooksPath` | `.githooks/` nel repo | `setup` li attiva | CONFIGURAZIONE |
| `pip-audit` | nel lock di sviluppo | nel `.venv` del profilo `sviluppo` | VERSIONE |
| pandoc, xelatex, Blender, ComfyUI | nessuno | si dichiarano | SOLO-LOCALE, finché il DM non li vuole in CI |

**La regola di Python per Dependabot e per chi aggiorna** (D7): si sale di
versione minore quando sale Debian stable, mai prima. Dependabot propone le
librerie; la versione di Python non è sua, e un test confronta `ci.yml` col
registro.

## §5 · Le piattaforme

| Piattaforma | Come si installa | Come la prova la CI |
|---|---|---|
| **Debian stable** (oggi 13) | nativo; `apt` per i pacchetti di sistema, col registro di A5c | job in `container: debian:13`, immagine fissata per digest |
| **Ubuntu stable** (oggi 24.04 LTS; la 26.04 con una PR che la prova, D8) | nativo; `apt` col registro, Python 3.13 da deadsnakes | il runner `ubuntu-24.04` |
| **Bazzite** | un distrobox Debian 13 (D9): dentro si comporta come Debian, con lo stesso registro; fuori il sistema immutabile non si tocca | job che crea il distrobox con podman su un runner Ubuntu e ci esegue `setup` e `verifica`. **Bazzite stesso resta `UNKNOWN` in CI**: la prova sull'host vero è a mano, sulla macchina del DM |

Una piattaforma diversa da queste tre si ferma prima di toccare niente e lo
dice.

## §6 · Lotti

Ogni lotto ha un ramo e una PR sua (PRATICHE D6). Nessuno parte prima che il
lotto mappe D28 sia chiuso (D4).

### A0 · Il brief corretto, l'audit e il contratto ✅
`[engine: Opus 5, sessione principale · effort: alto · qualità: il DM riconosce la deriva e decide D1-D10]`
Questo documento e ADR-0081.

### A1 · Il registro porta versione e checksum ⬜
`[engine: Sonnet 5 · effort: medio · qualità: un test boccia la CI se installa una versione diversa dal registro, e boccia un checksum sbagliato]`
- `Binario` prende `versione`, `classe`, `profili`, e per piattaforma `url` e `sha256`.
- typst, pdfcpu, shellcheck e Chrome for Testing col numero; via `releases/latest` dalle istruzioni di `binari.py`.
- Chrome for Testing: prima dell'adozione la licenza passa dal gate di `rumblingstone-edizione`; la versione si sceglie dal canale *Stable* delle sue API e si registra.
- `python3 scripts/binari.py --versione typst` e `--sha256 typst linux-x86_64`: la CI legge da qui invece di dichiarare `TYPST_VERSION` per conto suo, e verifica il checksum prima di `install`.
- I checksum si copiano dalle release ufficiali dove ci sono, e si verificano sul file scaricato prima del commit; dove la release non li pubblica, si calcolano su un download e si dichiara che sono nostri.
- Mutazione: cambiare la versione nel workflow fa fallire il test.

### A2 · Python 3.13 e le tre piattaforme in CI 🟡
`[engine: Sonnet 5 · effort: medio · qualità: i job Debian 13, Ubuntu 24.04 e distrobox verdi su main; un test boccia se ci.yml e il registro divergono]`
- `PYTHON_MINIMO` e `setup-python` passano a 3.13, con l'emendamento ad ADR-0037 e il commento di `binari.py` che spiega perché 3.13. Se qualcosa si rompe sul passaggio, il lotto lo corregge.
- `dipendenze.yml` passa a 3.13 nello stesso lotto, o il test delle minime proverebbe un'altra versione.
- 🟡 **2026-10-10, PR #231**: fatta la parte Python, prima del lotto mappe D28, perché la PR di Dependabot #228 (numpy 2.5, scipy 1.18) non si installava su 3.11. `PYTHON_MINIMO`, `ci.yml`, `dipendenze.yml`, le due guide e l'emendamento ad ADR-0037 sono a 3.13. Restano il job Debian 13 in container e il test che boccia se `ci.yml` e il registro divergono oltre il minimo.
- Il job Debian 13 in container gira i due corridori di test; i gate editoriali restano nel job principale (non dipendono dalla piattaforma).
- Il job Bazzite è in A6, perché ha bisogno di `dm.py ambiente setup`.

### A3 · Il lock con hash, e la regola degli aggiornamenti ⬜
`[engine: Sonnet 5 · effort: alto · qualità: pip install --require-hashes riesce su Debian 13 e Ubuntu 24.04; Dependabot apre una PR che aggiorna il lock; dipendenze.yml prova ancora le minime]`
- I `>=` di oggi restano la **dichiarazione** (il pavimento che `dipendenze.yml` prova); il lock si genera con `pip-compile --generate-hashes` su Python 3.13 (pip-tools, BSD-3, solo sviluppo: la licenza passa da `rumblingstone-edizione`).
- Da misurare nel lotto, prima di scegliere la forma: Dependabot aggiorna un lock di `pip-compile` solo se trova i file `.in` accanto ai `.txt`. Le due strade sono rinominare i pavimenti in `requirements.in` e `requirements-dev.in` (i `.txt` diventano i lock) o tenere i nomi e aggiungere un `requirements.lock` che Dependabot non aggiorna. La prima cambia il comando d'installazione e gli script che leggono i `.txt` (`dipendenze.yml` ne fa il parsing); la seconda lascia il lock indietro.
- La CI installa dal lock. Da quel momento CI e macchina hanno gli stessi pacchetti, byte per byte.
- La regola di §4 scritta in `dependabot.yml` e nella guida: le PR di sicurezza entrano appena verdi, quelle di versione solo con una ragione scritta nella PR.

### A4 · Gli hook, ridisegnati ⬜
`[engine: Sonnet 5 · effort: medio · qualità: test su un clone temporaneo: un hook preesistente sopravvive a setup e rimuovi; il secondo setup non cambia niente; pre-commit sotto i 5 secondi su un commit tipico, misurato]`

Gli hook stanno in `.githooks/` nel repo e si attivano con `core.hooksPath`,
registrando il valore di prima. Se `core.hooksPath` punta già altrove, o ci
sono hook non nostri in `.git/hooks/`, `setup` si ferma e lo dice. Tutti si
saltano con `--no-verify`: la CI resta il cancello. La proposta, approvata con D11:

| Hook | Cosa fa | Blocca? | Perché in locale |
|---|---|---|---|
| `pre-commit` | solo sui file in stage: `shellcheck` sugli `.sh`, `py_compile` sui `.py`, nessun file sotto `build/` o oltre 5 MB, nessuna riga che somigli a un token (stesso schema della scansione dei segreti di GitHub) | sì | sono gli errori che la CI boccia e che si vedono in un secondo; un segreto fermato qui non arriva mai su GitHub |
| `pre-push` | la regola d'oro dei piani (c'è già); `dm.py ambiente verifica --rapido` (versioni contro il registro, niente prove funzionali); i test di `scripts/tests` se il push tocca `scripts/` | la regola d'oro e i test sì; la verifica avvisa | un push con l'ambiente fuori registro produce risultati che la CI non riprodurrà |
| `post-merge` e `post-checkout` | il sync delle skill (c'è già); se sono cambiati il lock o `binari.py`, scrive «l'ambiente non combacia più: `dm.py ambiente aggiorna`» | no, e non installa mai da solo | è il punto in cui la CI cambia e la macchina resta indietro |

Il tempo dei test in `pre-push` si misura nel lotto: se supera un minuto, si
passa a un sottoinsieme dichiarato.

### A5 · `dm.py ambiente` ⬜
Si taglia in quattro, perché il primo pezzo è utile da solo.

> **Anticipato il 2026-10-09, fuori lotto.** Il DM, installando sulla sua
> Debian 13: *«ci sono pacchetti richiesti che non sono installati, perché non
> si possono includere così l'ambiente di sviluppo è completo?»*. Il profilo
> `completo` esiste già in forma minima:
> - `requirements-completo.txt`: `bpy`, `torch` per CPU e `piq`, sopra
>   `requirements-dev.txt`; un test lo tiene allineato a `binari.py`;
> - la riga `apt` per Debian 13 in GUIDA-SETUP-MACCHINA §5;
> - `bpy` nel registro, e `doctor` che non dà più «blender assente» quando il
>   modulo c'è.
>
> Sono ancora da fare la verifica di versioni e checksum, il lock e la
> scrittura dei pacchetti di sistema (A1, A3, A5c). Sulla macchina del DM,
> quel giorno, `misura_resa.py --check` ha dato lo stesso verde della CI.
>
> **Poi, lo stesso giorno, A5c e una parte di A5d.** Il DM: *«manca blender,
> comfyui e typst; prevedere anche un rollback così si può pulire il sistema»*.
> `scripts/ambiente.py` (`dm.py ambiente`) fa `piano`, `installa
> [--con blender,comfyui,typst]`, `stato`, `rimuovi [--venv]` e `adotta
> --apt-dal`, come li descrive A5c:
> - `dpkg` fotografato prima e dopo, e il registro possiede la differenza;
> - in rimozione la simulazione si mostra prima; mai `autoremove` né `purge`;
> - un pacchetto nostro da cui dipende altro resta.
>
> Il criterio di qualità di A5c è provato con un sistema finto
> (`test_ambiente_registro.py`), non ancora in un container Debian 13 vero:
> quello resta ad A6. `adotta` è nuovo rispetto al piano: affida al registro ciò
> che il DM aveva installato a mano prima che lo script esistesse.
>
> **La prima prova vera, sulla Debian 13 del DM, lo stesso pomeriggio.**
> - `adotta --apt-dal 2026-10-09` ha messo nel registro 103 pacchetti
>   installati a mano quel giorno;
> - `installa --con blender,comfyui` ha installato Blender (16 pacchetti nel
>   registro) e ha lasciato stare chromium, pandoc, maven e gli altri, già
>   presenti;
> - `doctor` è verde su ogni dipendenza, e `gate_locale.py --rapido` dà 49
>   passi, 0 rossi, 0 avvisi;
> - ComfyUI si è fermato: distrobox non monta `/srv`, e dentro il box
>   `COMFYUI_DIR=/srv/comfyui` non esisteva. Corretto in `setup-distrobox.sh`,
>   che ora monta la cartella e ricrea un box che non la vede.
>
> `rimuovi` non è ancora stato provato su una macchina vera.
>
> Il tool ha `side_effects.system` nel manifest, e così non esce dal server
> MCP nemmeno con `--allow-write`. Mancano ancora le versioni fissate con
> checksum (A1), il lock (A3), `aggiorna`, gli hook (A4) e Bazzite.

**A5a · leggere: `piano`, `verifica`, `stato`** `[engine: Sonnet 5 · effort: alto · qualità: --json deterministico (due giri, stesso output a parità di macchina), exit code documentati, test con un PATH finto per ogni stato del vocabolario]`
- `--profilo dm|sviluppo|completo`, `--json`, `--verboso`, `--silenzioso`, `--rapido`.
- Per ogni componente: presenza, versione contro il registro, percorso, architettura, duplicati nel PATH, prova funzionale (typst compila una pagina, pdfcpu impone due pagine, Chrome for Testing stampa un PDF di prova, il `.venv` importa i moduli, `gh auth status` senza stampare il token). I file di prova vanno nella cartella temporanea del sistema e si cancellano.
- Codici d'uscita: 0 tutto l'obbligatorio PASS; 1 un obbligatorio FAIL, MISSING o MISMATCH; 2 (`binari.MANCA`) un obbligatorio UNKNOWN. Gli avvisi non cambiano il codice, salvo `--rigoroso`.
- Riconosce la piattaforma da `/etc/os-release` e il distrobox dalla sua variabile d'ambiente.
- `dm.py doctor` resta e in fondo rimanda a `ambiente verifica`.

**A5b · scrivere, a livello utente: `setup`** `[engine: Sonnet 5 · effort: alto · qualità: in CI, setup due volte; il secondo giro riporta zero mutazioni; un fallimento a metà ripristina e lascia il log]`
- Lo stato in `$XDG_STATE_HOME/rumblingstone/<id>/stato.json`, dove `<id>` è un hash del percorso del clone: due clone o due worktree non si pestano.
- Cosa possiede: il `.venv` (dal lock, con `pip-audit` nel profilo `sviluppo`), typst, pdfcpu e Chrome for Testing in `~/.local/` (scaricati, checksum verificato, poi installati; mai `curl | sh`), gli hook di A4. Prima di ogni mutazione: guarda, decide se è suo, confronta, cambia solo se serve, riverifica.
- Il piano si mostra raggruppato e si conferma una volta per gruppo; `--non-interattivo` richiede che ogni scelta opzionale sia scritta sulla riga (`--con pdfcpu`), mai un default che installa.
- `--offline`: usa solo ciò che c'è e dice cosa manca. Non ripiega mai su una versione non fissata.
- Un binario già presente con la versione giusta non si reinstalla e non diventa nostro.
- **ComfyUI** per la hero map (`scripts/comfyui-local/`, `rumblingstone-mapmaking` regola 8) è un modulo opzionale del profilo `dm`, SOLO-LOCALE. Il DM, il 2026-10-08: *non adesso*, si fa qui. Misurato quel giorno sulla macchina del DM: RTX A2000 con **4 GB** di VRAM (la guida del repo presume 8 GB: SDXL con `--lowvram` gira, lento), **11 GB** liberi in `/home` contro i ~15 GB di ComfyUI, PyTorch CUDA, un checkpoint SDXL e un ControlNet; `/srv` ha 58 GB. Su Debian gli script di Distrobox non partono così come sono. Nel repo restano solo le mappe approvate: il clone, i pesi e `rendered/hero/` sono già ignorati da git. I pesi passano dal gate di licenza (ADR-0019).
- `act` (D6) è un modulo opzionale del profilo `sviluppo`: si installa solo con `--con act`, e `verifica` lo prova eseguendo un workflow minimo.
- Su Bazzite, fuori dal distrobox, `setup` crea il distrobox Debian 13 (immagine per digest) e si rilancia dentro; il sistema ospite non si tocca.

**A5c · i pacchetti di sistema, col registro (D1)** `[engine: Sonnet 5 · effort: alto · qualità: in un container Debian 13 e uno Ubuntu 24.04: installa un pacchetto che mancava e uno che c'era; rimuovi toglie il primo, lascia il secondo, e lo stato finale di dpkg è quello di partenza]`

Come Debian e Ubuntu tengono il conto, e cosa si prende da loro:
- `dpkg` registra lo stato di ogni pacchetto; `apt-mark showmanual` distingue chi l'ha chiesto da chi è arrivato come dipendenza; `/var/log/apt/history.log` scrive ogni transazione con la riga di comando e i pacchetti installati. **`apt` non ha un *undo*** (a differenza di `dnf history undo` su Fedora): il registro va tenuto da noi.
- Prima: `dpkg-query -W` dei pacchetti del profilo, salvato nello stato.
- Installazione: `sudo apt-get install --no-install-recommends` con l'elenco mostrato per intero prima della conferma. Mai `apt-get upgrade` per installare un pacchetto.
- Dopo: di nuovo `dpkg-query -W`; la differenza (pacchetti chiesti più le dipendenze arrivate) è ciò che possediamo, ciascuno con versione e origine. Un PPA aggiunto (deadsnakes su Ubuntu) entra nel registro come file in `/etc/apt/sources.list.d/`.
- Rimozione: `apt-get -s remove` dei soli pacchetti posseduti, mostrato prima; poi `sudo apt-get remove` di quell'elenco, mai `autoremove` (toglierebbe anche dipendenze orfane non nostre), mai `purge` salvo richiesta. Un pacchetto posseduto da cui ora dipende altro si lascia, e si dice perché. Il PPA si toglie se l'abbiamo aggiunto noi.
- Il registro si confronta con `history.log` a ogni `stato`: se qualcuno ha toccato a mano un pacchetto posseduto, lo stato è DRIFT, non un errore.

**A5d · `aggiorna` e `rimuovi`** `[engine: Sonnet 5 · effort: medio · qualità: in CI, setup → rimuovi → verifica; restano solo ciò che c'era prima e il repo intatto]`
- `aggiorna` mostra la differenza fra lo stato e il registro e la applica come `setup`.
- `rimuovi` toglie solo ciò che lo stato dice nostro, ripristina `core.hooksPath`, passa per A5c per i pacchetti di sistema; non tocca chiavi, credenziali, configurazione git dell'utente, contenuto del repo. Su Bazzite toglie il distrobox che ha creato.

### A6 · La CI prova il contratto ⬜
`[engine: Sonnet 5 · effort: medio · qualità: il job fallisce se un secondo setup cambia qualcosa, se rimuovi lascia residui, se git status non è pulito, se shellcheck dà un avviso]`
- Job su Debian 13 (container), Ubuntu 24.04 e distrobox Debian 13 su runner Ubuntu: `ambiente setup --profilo completo --non-interattivo` due volte, `verifica --json` allegato come artefatto, `rimuovi`, `git status --porcelain` vuoto.
- pdfcpu e Chrome for Testing si installano e si provano in CI: il libretto imposto e un PDF di booklet escono davvero.
- La CI registra le versioni che ha usato nel JSON, ed è quello il riferimento che `verifica` confronta in locale.
- shellcheck **bloccante**: si correggono i 4 avvisi di oggi, si tolgono `continue-on-error` e `|| true`, e si allarga a tutti gli `.sh` tracciati (oggi guarda solo `scripts/*.sh`).

### A7 · La guida e le matrici ⬜
`[engine: Sonnet 5 · effort: medio · qualità: validate_docs verde; le due matrici si rigenerano identiche (--check in CI)]`
- `GUIDA-SETUP-MACCHINA.md` riscritta attorno a `dm.py ambiente`, una sezione per piattaforma, esempi veri copiati dall'output.
- Matrice di verifica e matrice di rimozione generate dal registro, fra marcatori, con `--check`.
- Una riga in `scripts/README-automation.md` e in `rumblingstone-automation`.

### A8 · Il rapporto finale ⬜
`[engine: Opus 5, sessione principale · effort: alto · qualità: ogni tappa del ciclo di §7 ha esito ed evidenza; nessun PASS senza prova]`
Compresa la prova a mano su un Bazzite vero, che la CI non può fare.

## §7 · Validazione

Il piano è chiuso quando questo ciclo è passato **e lo dice la CI**, non la
macchina di chi scrive:

| Tappa | Atteso | Chi lo prova |
|---|---|---|
| macchina vuota (container) | `verifica` dà MISSING sugli obbligatori, exit 1 | A6 |
| `piano` | elenco raggruppato, nessuna mutazione | A5a, test |
| `setup` | tutti gli obbligatori PASS, sulle tre piattaforme | A6 |
| prova funzionale | typst, pdfcpu, Chrome for Testing producono un file valido | A5a, A6 |
| flusso di sviluppo | i due corridori di test verdi su Python 3.13 | A2 |
| flusso del DM | `validate_booklets --stampa`, `validate_corredo --stampa` | CI esistente |
| GitHub | `gh auth status` letto senza segreti nel log | A5a; a mano sulla macchina del DM |
| `git status` pulito | nessun file nuovo nel repo | A6 |
| secondo `setup` | zero mutazioni | A6 |
| `aggiorna` | differenza mostrata, applicata, riverificata | A5d |
| `rimuovi` | restano solo le cose preesistenti, dpkg come prima | A5c, A6 |
| Bazzite host | il distrobox nasce e `verifica` passa dentro | A8, a mano |

Un criterio vale per tutto il piano: **la CI di `main` resta verde**.

## §8 · Decisioni

<!-- decisioni-dm: AMBIENTE -->

| # | Lotto | Domanda |
|---|---|---|
| ~~D1~~ | A5c | ✅ **Decisa il 2026-10-08, risposta del DM: sì, col registro di ciò che si installa** (*«magari mettendo un registro di cosa installato così si può disinstallare nella procedura con sudo»*). **Fin dove arriva il setup automatico?** Pacchetti di sistema dopo conferma; il registro segue come Debian e Ubuntu tengono il conto (A5c) |
| ~~D2~~ | A2 | ✅ **Decisa il 2026-10-08, risposta del DM, poi corretta: una versione sola, vedi D7.** La prima risposta era «CI su 3.11 e 3.13»; il DM l'ha cambiata lo stesso giorno |
| ~~D3~~ | A3 | ✅ **Decisa il 2026-10-08, risposta del DM: lock con hash** (*«pip deve bloccare le versioni a meno di una correzione di sicurezza»*). La CI è lo standard: un aggiornamento entra prima in CI, poi in locale |
| ~~D4~~ | tutti | ✅ **Decisa il 2026-10-08, risposta del DM: dopo D28.** Il piano parte dopo il lotto mappe D28; in questa sessione solo piano, ADR e tracciatura |
| ~~D5~~ | A2, A6 | ✅ **Decisa il 2026-10-08, risposta del DM: Debian stable, Ubuntu stable, Bazzite.** **Quali piattaforme si supportano?** |
| ~~D6~~ | A5b | ✅ **Decisa il 2026-10-08, risposta del DM: facoltativo** (*«d6 ok facoltativo»*, dopo la spiegazione). **`act` per simulare la CI in locale?** Modulo opzionale del profilo `sviluppo`, versione e checksum nel registro come gli altri binari; il suo verde non sostituisce la CI |
| ~~D7~~ | A2 | ✅ **Decisa il 2026-10-08, risposta del DM: 3.13 ovunque.** **Quale versione di Python, visto che Debian 13 ha 3.13, Ubuntu 24.04 3.12, Ubuntu 26.04 e Bazzite 3.14?** La versione di Debian stable; si sale quando sale Debian, e la regola vale per Dependabot |
| ~~D8~~ | A2 | ✅ **Decisa il 2026-10-08, risposta del DM: 24.04, poi 26.04 con una PR.** **Quale Ubuntu stable?** |
| ~~D9~~ | A5b | ✅ **Decisa il 2026-10-08, risposta del DM: distrobox Debian 13.** **Come si installa su Bazzite, che è immutabile?** |
| ~~D10~~ | A1 | ✅ **Decisa il 2026-10-08, risposta del DM: Chrome for Testing fissato.** **Da dove viene il Chromium uguale in CI e in locale?** La licenza passa dal gate di `rumblingstone-edizione` prima dell'adozione |
| ~~D11~~ | A4 | ✅ **Decisa il 2026-10-08, risposta del DM: sì** (*«d11 ok»*). **Gli hook proposti in A4 vanno bene?** `pre-commit` bloccante su shellcheck, compilazione, file pesanti e token; `pre-push` con regola d'oro, verifica rapida dell'ambiente e test; `post-merge` che avvisa quando l'ambiente non combacia più. A4 li costruisce come scritti |

<!-- eco: AMBIENTE 2026-10-08 -->
- **Decise**: D1 pacchetti di sistema con conferma e registro · D2 superata da D7 · D3 lock con hash, aggiornamenti prima in CI · D4 dopo D28 · D5 Debian stable, Ubuntu stable, Bazzite · D6 `act` facoltativo · D7 Python 3.13 ovunque · D8 Ubuntu 24.04, poi 26.04 con una PR · D9 distrobox Debian 13 su Bazzite · D10 Chrome for Testing fissato · D11 gli hook di A4, come proposti
- **Aperte**: la forma del lock (file `.in` o `.lock` a parte) si misura in A3; la licenza di Chrome for Testing e di pip-tools al gate di `edizione`
- **Cambiate**: D1 dalla proposta «solo livello utente» a «sistema con registro»; D2 da «3.11 e 3.13» a «solo 3.13»; D3 dalla proposta «restano i `>=`» al lock; D6 dalla proposta «no» a «facoltativo»; shellcheck da «non bloccante finché gli avvisi non sono a zero» a bloccante subito; pdfcpu e Chromium da «decidere in A6» a «provati in CI»
- **Dedotto da me**: che «.env» nel messaggio del DM sia il `.venv`; che «facoltativo» per `act` voglia dire modulo opzionale fissato come gli altri, non installato di default; che Bazzite stesso resti `UNKNOWN` in CI e si provi a mano (la CI prova il distrobox, non l'host); che per D1 la rimozione non usi mai `autoremove` né `purge`; che i `>=` restino come pavimento dichiarato accanto al lock; che il passaggio a 3.13 tocchi anche `dipendenze.yml`

## §9 · Ordine

A1 → A2 → A3 → A4 → A5a → A5b → A5c → A5d → A6 → A7 → A8. A1 viene prima
perché ogni lotto dopo legge la versione dal registro. A5a si può usare da solo
appena esce, ed è già una risposta a «la mia macchina è come la CI?».

## Checklist di avanzamento

- [x] A0 · brief corretto, audit, contratto, ADR-0081, D1-D10
- [ ] A1 · versione e checksum nel registro, CI che legge da lì
- [ ] A2 · Python 3.13 e le tre piattaforme in CI — 🟡 Python 3.13 fatto (PR #231), manca il job Debian 13
- [ ] A3 · lock con hash e regola degli aggiornamenti
- [ ] A4 · hook ridisegnati (D11)
- [~] A5a · `ambiente piano/verifica/stato` (2026-10-09: `piano` e `stato` in `ambiente.py`; manca `verifica` con versioni e checksum, che aspetta A1)
- [ ] A5b · `ambiente setup` a livello utente, distrobox su Bazzite
- [~] A5c · pacchetti di sistema col registro (2026-10-09: `ambiente.py`, provato con un sistema finto; manca la prova in container di A6)
- [~] A5d · `aggiorna` e `rimuovi` (2026-10-09: `rimuovi [--venv]` col registro, provato con un sistema finto e mai su una macchina vera; manca `aggiorna`)
- [ ] A6 · la CI prova il contratto, shellcheck bloccante
- [ ] A7 · guida e matrici generate
- [ ] A8 · rapporto finale, Bazzite a mano
