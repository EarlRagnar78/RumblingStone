# ADR-0099 — La piattaforma di sviluppo ha tre canali, come Debian

**Stato**: accettata dal DM il 2026-10-23 (D1-D5 di [PIANO-PIATTAFORMA-DI-SVILUPPO](../PIANO-PIATTAFORMA-DI-SVILUPPO.md): *«D1-d5 ok»*)
**Data**: 2026-10-23
**Decisione-fonte**: tre messaggi del DM del 2026-10-23. *«una versione sola di python e scegli la stable supportata, in pratica lo stesso concetto del kernel Linux che viene applicato in Debian […] e usa librerie esterne python che sono standard de facto e che migliorano il progetto, e anche i tool standard de facto, misurando il miglioramento»*; *«applica la stessa filosofia per tutti i tools e le CI e i test […] una piattaforma di sviluppo completa e integrata»*; *«tutti i tool e pipeline […] mappe, prosa, struttura […] il meccanismo di selezione deve essere tipo quello usato dalla Debian per la scelta e migrazione del kernel Linux»*.
**Rapporti**: estende [ADR-0081](ADR-0081-il-contratto-d-ambiente.md) (la CI è lo standard, `binari.py` è il registro, Python 3.13); rispetta [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md) (ciò che il DM esegue resta stdlib più le eccezioni dichiarate); applica [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) agli strumenti: uno strumento senza misura non entra.

## Contesto

Il repo ha già quasi tutti i pezzi di una piattaforma: una CI di 58 passi che
è lo standard (ADR-0081), un registro dei binari e delle librerie
(`scripts/binari.py`) con le catene che li usano, Python 3.13 in CI, Dependabot
a gruppi, `pip-audit`, i due corridori dei test, gli hook decisi e non ancora
costruiti (A4 di AMBIENTE). Manca la regola con cui un componente **entra,
sale, si aggiorna ed esce**. Oggi ognuno è entrato con un ADR suo (pytest con
l'emendamento ad ADR-0037, tcod e scipy con ADR-0084, fonttools con ADR-0085,
torch con ADR-0086) e la stessa domanda si è risposta ogni volta da capo. Il
DM chiede una regola sola, quella che Debian usa per il kernel: si sceglie una
versione stabile e supportata, ci si resta, si corregge solo dove serve, e si
migra a ogni rilascio.

La misura del 2026-10-23
([MISURE](../esperimenti/piattaforma-2026-10-23/MISURE.md)) dice tre cose che
pesano sulla decisione. 3.13 è ancora la Python di Debian stable, ma da
ottobre 2026 upstream la tiene solo per la sicurezza. La metà dei 15 minuti
della CI è la stessa suite di test eseguita due volte. E degli strumenti «de
facto» provati, uno trova bug veri (ruff, su `converters/`), uno ne trova zero
in 328 rilievi (mypy), uno accelera molto un passo che pesa poco (uv).

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Tre canali con promozione misurata** (scelta) | una regola sola per librerie, binari, strumenti, azioni CI, runner e container; ogni entrata ha una misura prima e dopo; un componente nuovo non può rompere `main` il primo giorno | più lenta: uno strumento utile aspetta almeno due settimane prima di bocciare; serve tenere un registro dei canali |
| Adottare in blocco lo stack «moderno» (uv, ruff con molte regole, mypy stretto, pre-commit) | è quello che usano molti progetti Python nel 2026, e si fa in un giorno | misurato qui: 1.672 rilievi di ruff quasi tutti di stile, 328 di mypy senza un bug a runtime nel campione, pre-commit che scarica dalla rete; il costo è certo e il guadagno no |
| Lasciare le cose come stanno, un ADR per ogni componente | nessun lavoro nuovo; ha funzionato per tcod, scipy, fonttools | la domanda «entra o no?» si rifà ogni volta, e nessuno dice quando un componente esce o quando si migra la versione di Python |
| Seguire le versioni più nuove (Python 3.14, `latest` ovunque) | funzioni nuove prima | è il contrario di ciò che il DM ha chiesto, e `bpy` vuole 3.13 esatta |

## Decisione

**Ogni componente della piattaforma sta in uno di tre canali, e sale solo con
una misura.** Un componente è tutto ciò che una pipeline del repo esegue e che
il repo non scrive: l'interprete, le librerie Python, i binari (typst, pdfcpu,
Chromium, shellcheck, Blender), gli strumenti di sviluppo (pytest, ruff,
pip-audit), le azioni e il runner della CI, l'immagine Docker, i modelli e le
skill di terzi.

1. **unstable**: si prova a mano, in un ramo o in `plans/esperimenti/`. Non
   sta nei `requirements*.txt` del repo e non gira in CI. Ci stanno oggi spaCy
   e Stanza (PR #264, #270), il LLM locale (ADR-0089), mypy e pyright.
2. **testing**: gira in CI come passo **non bloccante**, con la versione
   fissata, e se è una libreria sta in `requirements-dev.txt`. Entra da
   unstable con quattro condizioni: licenza libera passata dal gate di
   `rumblingstone-edizione` (MIT, BSD, Apache-2.0, MPL, GPL/AGPL solo per uso
   interno come pymupdf); una misura prima e dopo scritta col comando che la
   rifà; un guadagno nominato (bug trovati, secondi risparmiati, righe tolte,
   un rischio chiuso); l'ok del DM sulla PR.
3. **stable**: bloccante in CI, versione nel registro (e nel lock, quando A3
   di AMBIENTE c'è), uguale sulle piattaforme di ADR-0081. Sale da testing
   quando sono vere tutte e quattro:
   - almeno **14 giorni e 10 run della CI su `main`** in testing;
   - **zero falsi allarmi non spiegati** in quei run (ogni rilievo letto e
     classificato in una riga del piano);
   - **nessuna misura della piattaforma peggiora** oltre la soglia: tempo del
     job principale non più di +5%, nessun test in meno, nessun passo verde che
     diventa rosso;
   - l'ok del DM, come il congelamento di una release Debian.
4. **Si scende senza discussione.** Un componente stable che boccia a torto o
   rompe una pipeline torna testing con una PR il giorno stesso; si riparla di
   promuoverlo con una misura nuova.
5. **La stable si congela.** Dentro una versione della piattaforma entrano
   solo correzioni di sicurezza (il gruppo di sicurezza di Dependabot, subito)
   e correzioni di bug che servono. Gli aggiornamenti di versione entrano con
   una ragione scritta nella PR, mai «perché è uscito» (lo dice già §4 di
   AMBIENTE; qui vale per ogni componente).
6. **La migrazione della versione maggiore segue Debian.** Python, il runner
   Ubuntu e l'immagine Docker salgono quando sale Debian stable: Python 3.14
   quando esce Debian 14. Prima del salto la versione nuova passa da testing
   (un job CI non bloccante sulla nuova versione per almeno un mese). Dopo il
   salto la vecchia resta **oldstable**: un job non bloccante per tre mesi, poi
   esce. Un'eccezione sola, che decide il DM: se una libreria stable lascia la
   nostra Python prima che Debian salga (con SPEC 0 numpy e scipy lasciano
   3.13 intorno a ottobre 2027), si sceglie fra fermare la libreria
   all'ultima versione compatibile (solo sicurezza) e anticipare la
   migrazione.
7. **Python resta 3.13**, ed è una versione esatta, non un minimo:
   `PYTHON_MINIMO` diventa `PYTHON` e un test boccia la CI se `ci.yml`,
   `dipendenze.yml`, il Dockerfile o `binari.py` ne dichiarano un'altra (A2 di
   AMBIENTE, che lo prevedeva).
8. **La piattaforma si misura intera.** Le misure di
   [MISURE](../esperimenti/piattaforma-2026-10-23/MISURE.md) sono il punto di
   partenza; ogni promozione cita la differenza. Il lotto P2 del piano le
   rende un comando che la CI esegue a ogni run.
9. **`converters/` entra nella piattaforma** (D6, DM: *«D6 b»*), e supera
   PRATICHE D9. Python 3.13 anche lì, i tre bug trovati da ruff corretti,
   Dependabot con una voce e gruppi suoi, ruff sul codice come altrove, e un
   job CI in testing che installa le sue dipendenze vere e prova che ogni
   modulo si importi. I suoi test leggono PDF che non stanno nel repo e
   restano fuori dalla CI.

## Conseguenze

- Una domanda sola per tutto («in che canale è, e cosa dice la misura?») al
  posto di un ADR per componente. Gli ADR 0084, 0085 e 0086 restano validi:
  sono le misure con cui tcod, scipy, fonttools e torch sono entrati.
- La prima applicazione: ruff entra in testing (passo non bloccante, otto
  gruppi di regole che cercano bug e non stile, 0,08 s); mypy resta fuori; uv e
  pytest-xdist si propongono al DM con le misure (D3, D4); la seconda
  esecuzione della suite di test con `unittest` si propone di toglierla (D2),
  perché la parità la controlla già un test e costa 222 s su 914.
- Si paga: un registro dei canali da tenere aggiornato (il lotto P1 lo mette
  in `binari.py`, non in un file nuovo); due settimane di attesa prima che uno
  strumento utile possa bocciare; un job CI in più nei mesi prima di una
  migrazione di Python.
- Diventa più difficile adottare qualcosa perché va di moda, ed è voluto. Uno
  strumento che non porta una misura resta in unstable anche se lo usa mezzo
  mondo.
- La regola copre le pipeline del DM (mappe, prosa, stampa, sessione) solo per
  i componenti di terzi che usano. Le regole del contenuto (norme, soglie di
  qualità, standard dei master) hanno i loro ADR e non cambiano.

**Da rivedere se**: un componente resta in testing più di tre mesi senza che
nessuno lo promuova o lo tolga (allora la soglia di promozione è sbagliata o
nessuno guarda il registro); oppure una migrazione di Python fatta con questa
regola rompe il portatile del DM la sera di una sessione; oppure Debian
cambia ciclo di rilascio.
