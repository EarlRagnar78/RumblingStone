# ADR-0116 — typst e l'imposizione si installano da PyPI, mise esce dal repo

**Stato**: accettata (2026-11-08)
**Data**: 2026-11-08
**Decisione-fonte**: il DM (Jfs), 2026-11-08, thread «Installare typst e pdfcpu in automatico». Dopo i 504 di GitHub Releases: *«perché usi mise invece di pip? […] è una best practice?»*. Poi, sulla card, «Prova pip in testing, poi decidi». Letta la misura: *«applicalo se funziona come standard»*. Poi: *«se mise non serve più togliamo le app coinvolte e il mise […] così è pulito anche la parte di CI»*, e sulla card dell'imposizione «Misura pdfimpose, poi decidi» (*«se regge, via mise, job, renovate.json e app»*).
**Rapporti**: **supera** [ADR-0113](ADR-0113-gli-strumenti-binari-si-installano-da-un-lockfile.md) (mise, `mise.lock`, `strumenti.py`, Renovate). Cambia lo strumento di [ADR-0027](ADR-0027-imposizione-con-pdfcpu.md) da pdfcpu a pdfimpose, con la stessa regola di degradazione. È la quarta eccezione di [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md), della famiglia di Pillow: opzionale, con ripiego dichiarato. Tiene la versione fissata di [ADR-0020](ADR-0020-edizione-da-stampa-su-un-secondo-binario.md) §3 e i pacchetti vendorizzati di [ADR-0026](ADR-0026-vendoring-pacchetti-typst.md). Segue la regola del DM «si parte dallo standard di fatto, decide la misura».

## Contesto

Il giorno in cui è arrivato ADR-0113, GitHub Releases ha risposto 504 per ore a typst, a pdfcpu e allo stesso mise. githubstatus diceva «operational». La cache di ADR-0113 assorbe il guasto dal primo giro buono, ma il primo giro buono non arrivava, e i job bloccanti dipendevano comunque da GitHub per typst.

Su PyPI c'è `typst` ([messense/typst-py](https://github.com/messense/typst-py), Apache-2.0). È il compilatore ufficiale di typst dentro un modulo Python, con wheel `abi3` per Linux, macOS e Windows. PyPI serve i file da una CDN diversa da quella di GitHub Releases. Per un progetto Python, `requirements.txt` con Dependabot è lo standard di fatto, ed è quello che il repo usa già per pyyaml, Pillow e tiktoken.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Pacchetto PyPI `typst` fissato in `requirements.txt`, tutti i chiamanti attraverso `typst_motore.py`, la CLI di `mise.lock` come ripiego** (scelta) | niente GitHub Releases nei job bloccanti; Dependabot già attivo; la wheel entra da sola nel bundle `--con-ruote`; misurato identico alla CLI | binding di un manutentore singolo, non dell'organizzazione typst; la versione del pacchetto (0.15.2) non coincide con quella del compilatore (0.15.1) |
| Restare alla sola CLI di `mise.lock` (ADR-0113) con la cache | nessun cambio; la CLI è l'artefatto ufficiale | i job bloccanti dipendono da GitHub Releases finché la cache non è piena, e la cache si svuota quando cambia `mise.lock` |
| Mirror della CLI (`ghcr.io/typst/typst`) | ufficiale | misurato il 2026-11-08: binario con un altro sha256 (908d5a47… contro 29273eaa…), quindi non è lo stesso artefatto |
| Una shim `typst` fatta in casa sopra il modulo | i chiamanti restano uguali | è una CLI nostra da mantenere, che imita quella vera: il «reinventare» che il DM esclude |

## Decisione

1. **`requirements.txt`** dice `typst==0.15.2`: una versione fissata, non un pavimento (ADR-0020 §3). Dependabot la alza con una PR, e la PR passa dai cancelli di stampa.
2. **`scripts/typst_motore.py`** è l'unico punto che compila (`compila`) e interroga (`valuta`) un `.typ`:
   - usa il modulo se c'è, altrimenti la CLI trovata da `binari.trova(binari.TYPST)`;
   - `RUMBLINGSTONE_TYPST=cli` chiede la CLI, `=pypi` vieta il ripiego;
   - porta il ripiego senza tag PDF per il bug di typst 0.15.1 e passa `SOURCE_DATE_EPOCH` come data del PDF, come fa la CLI;
   - lo usano `export_booklet_typst`, `misura_stampa`, `varianti_stampa`, `validate_booklets` e `validate_corredo`.
3. **CI.**
   - I job bloccanti non scaricano più typst: arriva con `pip install -r requirements-dev.txt`.
   - `strumenti.py installa|verifica pdfcpu` installa e controlla solo pdfcpu.
   - Il job `typst-pip` (non bloccante) compila ogni booklet con la CLI e con il modulo, ed è rosso se cambiano pagine, testo o pixel.
   - Il job `strumenti` di ADR-0113 continua a confrontare mise e `strumenti.py` sulla CLI.
4. **`mise.toml` e `mise.lock` tengono la CLI di typst** come ripiego e come riferimento del confronto. Il bundle porta sia l'archivio della CLI sia la wheel.

## Misura

`plans/esperimenti/typst-pip-2026-11-08/MISURE.md`:
- 19 booklet, 856 pagine;
- testo per pagina e pixel per pagina (72 dpi; 150 dpi su tre booklet) identici;
- la query dei riquadri di `misura_stampa` identica;
- byte identici in 1 caso su 19, negli altri cambia solo la compressione Flate delle immagini;
- il modulo è circa il 30% più veloce, perché non avvia un processo.

Dopo il cambio, in locale senza la CLI passano tutti i cancelli di stampa della CI: `validate_booklets --stampa`, `validate_corredo --stampa --rigoroso`, `misura_stampa --tutti --check` e `--per-scheda`.

## Conseguenze

- I 504 di GitHub Releases non fermano più i job bloccanti per typst. pdfcpu ci passa ancora (è nella cache, e non è su PyPI).
- Un aggiornamento di typst ora lo propone Dependabot, non Renovate. Renovate continua ad aggiornare la CLI in `mise.lock`, e le due versioni possono divergere per qualche giorno: lo dice il job `typst-pip`.
- La versione del pacchetto non è quella del compilatore. Il `Creator` del PDF dice quella del compilatore, e la dice anche `python3 scripts/typst_motore.py`.
- **Quello che non è misurato:** macOS e Windows (esistono le wheel, non sono provate); la wheel dentro il bundle installata davvero senza rete.

## Seconda parte (2026-11-08): l'imposizione e l'uscita di mise

Con typst su PyPI, a mise restava solo pdfcpu. pdfcpu è Go e non è su PyPI sotto nessun nome; compilarlo con pip non ha senso, e la libreria standard di Python 3.14 non fa imposizione. Su PyPI c'è `pdfimpose` (Louis Paternault, AGPL-3.0-or-later, sopra PyMuPDF), che fa lo stesso libretto a punto metallico.

| Opzione | A favore | Contro |
|---|---|---|
| **`pdfimpose==2.10.0` in `requirements.txt`, `saddle --signature 2x1`; via mise, `mise.lock`, `strumenti.py`, `renovate.json` e i job di mise** (scelta) | un solo gestore di dipendenze (pip, con Dependabot); niente GitHub Releases in nessun job; il bundle offline è solo wheel | AGPL, e porta PyMuPDF 2.x con onnxruntime: `requirements.txt` cresce e il bundle offline passa a ~150 MB per piattaforma |
| Tenere mise solo per pdfcpu | pdfcpu è Apache-2.0 e un binario solo | due gestori, Renovate e la cache per un passo opzionale, e i 504 di GitHub Releases restano |
| pdfcpu scaricato a mano senza mise | niente mise | un installatore nostro: il «reinventare» che il DM esclude |
| pypdf e un'imposizione scritta da noi | licenza BSD | l'accoppiamento delle pagine è codice nostro da mantenere e da misurare |

### Misura dell'imposizione

`plans/esperimenti/typst-pip-2026-11-08/MISURE.md` (seguito), con `confronta_imposizione.py` e `esito-imposizione.txt`. Su tutti i 19 booklet A5 del repo, 1.590 pagine:
- `pdfcpu booklet` (v0.11.0, come in `dm.py`) e `pdfimpose saddle --signature 2x1` danno lo **stesso accoppiamento delle pagine** su ogni facciata (testo per mezza facciata, Jaccard ≥ 0,99);
- lo **stesso foglio fisico A4**, con le pagine A5 a grandezza vera: pdfcpu lo scrive verticale con le pagine una sopra l'altra, pdfimpose orizzontale con le pagine affiancate (839,1 × 595,3 pt);
- con `--format A4` pdfimpose ingrandisce le pagine dell'1,4% (851 × 599,7): per questo non si usa;
- due esecuzioni non danno gli stessi byte, come con pdfcpu: il libretto resta fuori dal repo.

### Cosa cambia

1. `dm.py volume --imposto` chiama `python -m pdfimpose saddle --signature 2x1`; se `pdfimpose` manca, dice come installarlo e la catena prosegue (ADR-0027). pdfimpose non scala le pagine: un volume A4 darebbe fogli A3. Per questo `dm.py` riduce prima un volume più grande dell'A5 a pagine A5 con PyMuPDF (`show_pdf_page`, 71%), come faceva pdfcpu, e il libretto resta su fogli A4. Il volume composto in A5 (`--formato a5`) passa com'è, ed è quello da preferire. Trovato provando `dm.py volume --imposto` sull'Abbazia, che è A4: la misura dei 19 booklet A5 non lo poteva vedere.
2. `binari.py`: `PDFCPU` esce; resta il binario `typst` come ripiego di `typst_motore`. `typst-py` e `pdfimpose` sono librerie del registro, e le catene «edizione da stampa» e «libretto imposto» le chiedono.
3. Escono dal repo `mise.toml`, `mise.lock`, `renovate.json`, `scripts/strumenti.py` e il suo test, i job `strumenti` e `typst-pip`, la cache degli archivi. La CI controlla solo che la catena usi il modulo PyPI.
4. Il bundle del rilascio è `scripts/bundle_offline.py`: per piattaforma, le wheel di `requirements.txt` in un zip riproducibile con `BUNDLE.json`, poi SHA256SUMS e Sigstore come prima. `installa` verifica ogni wheel e fa `pip install --no-index`. Provato in locale su linux-x64: costruito, installato in un `.venv` vuoto senza proxy, `import typst, pdfimpose` riuscito.
5. `ambiente.py` non scarica più typst: arriva col `.venv`. Il registro sa ancora togliere la CLI installata prima.
6. **L'app Renovate su GitHub** la disinstalla il DM: da qui non si può.

### Conseguenze della seconda parte

- Un aggiornamento di typst o di pdfimpose lo propone solo Dependabot, e lo provano i cancelli di stampa della CI (`validate_booklets --stampa`, `validate_corredo --stampa --rigoroso`, `misura_stampa --check`). Il confronto con la CLI (`typst-pip`) non c'è più: la CLI non è più fissata da nessuna parte.
- AGPL entra fra le dipendenze di esecuzione, non solo di sviluppo. È uno strumento che gira sulla macchina di chi stampa e non entra nei PDF: non tocca il codice MIT né i volumi (LICENSES.md).
- **Quello che non è misurato:** il bundle su macOS e Windows; pdfimpose sui volumi A4 (si impongono solo gli A5).

**Da rivedere se**: un aggiornamento di typst cambia un booklet nei cancelli di stampa; typst-py smette di seguire i rilasci di typst per più di un mese (si torna a una CLI fissata, con un ADR nuovo); il progetto typst pubblica un pacchetto PyPI suo; pdfimpose smette di essere mantenuto o PyMuPDF rende il bundle troppo pesante (si guarda a pypdf).
