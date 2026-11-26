# Promozioni da testing a stable del 2026-11-25 (ADR-0099)

> Le candidate del rilascio 1.1.0 ([MS-0171](../../MEMORIA-STORICA.md): il
> rilascio aspetta le promozioni previste per il 22-24/11) e il lotto P4 di
> [PIANO-PIATTAFORMA-DI-SVILUPPO](../../PIANO-PIATTAFORMA-DI-SVILUPPO.md).
> La regola: si sale dopo 14 giorni e 10 run su `main` senza falsi allarmi non
> spiegati e senza peggiorare il job principale di oltre il 5%, poi con l'ok
> del DM. Le misure e le proposte sono state scritte prima dell'ok; il DM ha
> scelto «Tutti e sei, con il codice» sulla card del 2026-11-25 (D8 del piano),
> e le promozioni sono nella stessa PR di questo file.
>
> Misurato su `main` a 14085a37 (2026-11-21 17:31, l'ultimo push su `main`).

## Esito

| Candidata | In testing dal (primo run su `main`) | Run su `main` | Rossi del passo | Falsi allarmi | Oggi su `main`, in locale | Proposta |
|---|---|---|---|---|---|---|
| pytest-xdist 3.8.0 (job `testing`) | 2026-11-08 11:36, 29056bf (#342), la stessa suite | 168 | 0 su `main`; su PR nessuno che il job principale non abbia avuto | 0 | 3.445 passate e 18 saltate in 362 s (in CI 3.447 e 16) | **sale a stable**, al posto del passo pytest del job principale |
| Cancello dei numeri (ADR-0118) | 2026-11-10 00:17 | 146 | 0 su `main`; 3 su 384 run di PR | 0 non spiegati: 2 veri, 1 del lettore, spiegato | verde, 0 scarti in baseline, 73 file non coperti, 8,6 s | **sale a stable** |
| 14 conti PF1e `in_prova` (ADR-0119) | 2026-11-10 00:38 | 145 (158 col passo, 13 di prima) | 0 avvisi su `main` e su 420 run di PR | 0 | `--cancello-moduli --severo` verde | **sale a stable**, ma non è un cambio di soli dati: 31 prove rosse (sotto) |
| D eufonica (ADR-0120) | 2026-11-10 06:23 | 141 | 0 su `main`; 0 su 369 run di PR | 0 | verde, 701 file, nessun refuso | **sale a stable** |
| Avvisi della scheda, `check_schede` (ADR-0114) | 2026-11-08 08:59 (31 avvisi), a zero dalle 11:36 | 168 a zero | 0 avvisi su `main` e su 523 run di PR dopo le 12 | 0 | `validate_skills`: 0 errori, 0 avvisi | **sale a stable**, è codice: chiede `sviluppatore` |
| Marche sulle righe cambiate (ADR-0109) | 2026-11-07 10:28, gira solo sulle PR | 0 per costruzione | 3 su 510 run di PR | 0: le 3 sono marche senza domanda e base, corrette | non si prova su `main` | **sale a stable**, con la nota che i «10 run su `main`» qui sono run di PR |

ADR-0109 rientra perché fissa «dopo due settimane» dal 2026-11-07: la data è
il 2026-11-21, scaduta.

Il tempo in testing è di 15-17 giorni di calendario per tutte. Va detto però
che su `main` non c'è stato nessun push dopo il 2026-11-21 17:31: i run
coprono dall'8 al 21 novembre, 12 giorni con almeno un run.

## pytest-xdist

Ogni run di `main` dal 2026-11-08 11:36 (29056bf, #342) ha le stesse prove
passate e saltate nel job principale e nel job xdist: **168 su 168**, nessuna
fallita né nell'uno né nell'altro
([conteggi-prove.tsv](conteggi-prove.tsv), colonna `uguali`). I 5 run
«DIVERSI» sono tutti dell'8 novembre mattina, prima della #342, quando il job
xdist non aveva typst; 2 di questi non hanno il conteggio del job principale
perché quel run è fallito prima di pytest.

Sulle PR, 543 run dal 2026-11-07: 468 verdi in tutti e due, 24 rossi in tutti
e due, 48 in cui il passo pytest principale è saltato perché un passo prima
era fallito (non si confrontano), e 3 rossi solo nel principale, tutti dell'8
novembre alle 8:22-8:24 e tutti per `test_pacchetti_typst.py`
(`PermissionError: 'typst'`), la prova che xdist allora saltava. Sulle teste
delle cinque PR aperte i conti tornano: per esempio #507 3.290 + 158 = 3.448
passate e 16 saltate, come il job principale.

| Tempi in secondi, mediana | pytest nel job principale | i due giri xdist | job «Validate» | job xdist |
|---|---|---|---|---|
| i primi 10 run dal 2026-11-08 | 258 | 158 | 576 | 213 |
| tutti i 168 run | 699 | 392 | 983 | 426 |
| gli ultimi 10 run (dal 2026-11-19 16:27) | 1.127 | 477 | 1.442 | 521 |

Promuovere toglie dal job principale circa 650 s (mediana degli ultimi 10:
1.127 → 477). Il criterio «non peggiora oltre il 5%» è quindi rispettato con
margine, da riscontrare sul run della PR.

**Riscontro sul run della #516** (testa c1ef61d9, job 139067587639): passo
pytest 761 s (giro parallelo 731 s, 3.161 passate e 16 saltate; giro in serie
29 s, 297 passate), job «Validate» 1.108 s. Rispetto alla mediana degli ultimi
10 run di `main`: −366 s sul passo (−32%), −334 s sul job (−23%). La stima di
477 s era ottimista: il job xdist misurato girava da solo, senza il resto del
job accanto. Comando: `gh api repos/gsamuele78/RumblingStone/actions/jobs/139067587639`.

**Un peggioramento che non viene da xdist.** In 13 giorni il passo pytest del
job principale è passato da 258 a 1.127 s di mediana (×4,4) mentre le prove
crescevano da 2.494 a 3.447 (+38%). I tempi degli ultimi run sono bimodali,
attorno a 860 s e a 1.370 s, con le stesse prove: c'è rumore del runner, ma
la crescita resta. Il job «Validate» è a 1.442 s contro i 914 s di §4 del
piano. È una misura della piattaforma peggiorata, e non ha un responsabile
misurato: è il lavoro di P2.

Cosa cambia in `ci.yml` per promuovere:

- righe 516-517, il passo «Unit tests — pytest» del job `validate`: il comando
  diventa i due giri delle righe 581-582
  (`python -m pytest scripts/tests -q -n auto -m "not scrive_nel_repo"` e
  `python -m pytest scripts/tests -q -m scrive_nel_repo`), e il commento sopra
  (509-515) dice che xdist è stable da quel giorno;
- righe 549-582: il job `testing` esce intero;
- `requirements-dev.txt:107` ha già `pytest-xdist==3.8.0`: niente da cambiare.

`test_i_test_girano_in_ci.py` conta le prove senza eseguirle e non legge il
comando di `ci.yml`; `gate_locale.py` legge i passi da `ci.yml` e prende il
comando nuovo da solo.

## Cancello dei numeri

146 run su `main` dal 2026-11-10, 146 verdi, nessuna riga `##[error]` nel
passo ([passi-main.tsv](passi-main.tsv)). La baseline ha 0 scarti; i file non
coperti sono scesi da 75 a 73. Il passo dura 3,4 s di mediana.

Sulle PR, 3 rossi su 384 ([passi-pr.tsv](passi-pr.tsv)):

- 43719288546 e 43719659462 (ramo `84sweg`, 2026-11-15):
  `Arco-Post-Hammerfist-P2B-Torneo-Tordek-BATTLE-STATS-e-VILLAIN-ICONICI.md`,
  «numeri di combattimento che nessun conto legge». È il caso per cui il
  cancello esiste (file nuovo con numeri non calcolati): allarme vero.
- 43629329432 (ramo `u8xojz`, 2026-11-14): l'hobgoblin bladebearer,
  «attacco +1, atteso +10». Il commit dopo (0a6c4281) toglie il `+1` da
  «doppia ascia orchesca +1 (una testa +1, l'altra perfetta)» negli `attributi`:
  il lettore aveva preso il bonus dell'arma per il bonus d'attacco. È un falso
  allarme del lettore, spiegato, e aggirato riscrivendo il dato, non
  correggendo il lettore. Su `main` lo stesso file oggi passa.

Per promuovere, in `ci.yml` righe 205-210: il commento dice stable dal giorno
della PR, il nome del passo perde «non bloccante fino al 2026-11-23» e la
riga `continue-on-error: true` (210) esce. Nessun dato cambia.

## I 14 conti PF1e in prova

Stanno in `sistemi/pf1e/dati/conformita.toml`, righe 22-27: `fatti` ne ha
7 (pf, CA, prosa, iniziativa, attacco, CD, ereditate), `in_prova` ne ha 14
(BMC, DMC, BAB, TS, contatto_sprovvista, iniziativa_recinto, schivare,
scurovisione, visione_crepuscolare, corrompere_acqua, incanalare, pf_bonus,
pf_misti, cd_incantesimi). Il cancello `--cancello-moduli` (ci.yml 202-203,
già bloccante) stampa uno scarto di un conto in prova come `⚠` e non esce 1;
con `--severo` esce 1. I conti si fanno su 14 schede: 7 nel Giardino, 7 nel
Drappo.

Dal 2026-11-10 00:38, primo run senza «saltati perché manca la regola», in
145 run su `main` e in 420 run di PR (con quelli di prima) il passo non ha mai stampato un avviso
dei conti in prova. Oggi in locale `--cancello-moduli --severo` esce 0.

Promuovere vuol dire spostare i 14 nomi da `in_prova` a `fatti`. **Non basta
il dato**: simulato in memoria su `test_conformita_pf1e.py`, 31 rossi su 14
prove (30 fallimenti, quasi tutti sottocasi di
`test_ogni_numero_sbagliato_e_bocciato_sul_suo_conto`, più un errore in
`test_un_conto_promosso_blocca_anche_senza_severo`, che fa
`in_prova.remove("BMC")`). La ragione è in
`conformita_statblocchi.py:969-972`: il nome del conto finisce nello scarto
solo come chiave `prova`, quindi un conto promosso non dice più quale conto
è. Serve una modifica di `sviluppatore` (lo scarto porta sempre il suo conto,
le prove leggono quella chiave) nella stessa PR del dato.

## D eufonica

141 run su `main` dal 2026-11-10 06:23, tutti con «nessun refuso»; 369 run di
PR, nessun rosso. Il passo dura 8,1 s di mediana, perché riesegue tutto
`validate_lingua.py`. In locale oggi: 701 file, nessun refuso. Nessuna
misura dice se la regex abbia mai preso un errore vero in CI: zero rossi
valgono come zero falsi allarmi, non come prova che morde. Che morda lo dice
`test_lingua.py`.

Per promuovere, la via minima è in `ci.yml` righe 279-287: `continue-on-error`
(287) esce e il nome perde «non bloccante fino al 2026-11-24». La via che il
commento stesso descrive («--d-eufonica diventa il comportamento di sempre»)
è codice: `validate_lingua.py:230-243` con la d eufonica sempre errore, e il
passo separato esce, risparmiando 8 s. Quella la fa `sviluppatore`.

## Avvisi della scheda (ADR-0114)

`check_schede` sta in `scripts/validate_skills.py:375-400` e i suoi rilievi
vanno nella lista `warnings` (riga 416): il passo «Validate skill trees»
(ci.yml 74-75) non fallisce per loro. Gli avvisi sono 31 nei run dell'8
novembre dalle 8:59 alle 11:36, poi 0 in 168 run su `main` e in tutte le PR
dopo le 12 di quel giorno. Su `main` oggi: 18 skill, 0 errori, 0 avvisi.

L'audit dice «bloccante dal 22/11», ma ADR-0114 (righe 47-49) fissa una
proposta dell'audit due settimane dopo il secondo lotto, non una data. Per
promuovere non c'è niente da cambiare in `ci.yml`: `check_schede` deve finire
negli errori (riga 416), e `test_prove_skill.py:112-116` va riletto. È codice,
quindi `sviluppatore`.

## Marche sulle righe cambiate (ADR-0109)

Il passo ha `if: github.event_name == 'pull_request'` (ci.yml 164): su
`main` non gira mai, e la regola dei 10 run su `main` non si applica alla
lettera. Sulle PR dal 2026-11-07 10:28: 510 run su 46 rami, 3 rossi, tutti del
ramo `84sweg` (2026-11-15 e 2026-11-17): marche `[INFERRED]` senza domanda e
base in Azarr Kul, Zarim, Ghostlord e il Collezionista. Su `main` oggi quelle
righe hanno la forma `[INFERRED — domanda?; base: …]`: difetti veri, corretti.

Per promuovere, `ci.yml` righe 160-166: `continue-on-error` (165) esce, il
nome perde «non bloccante», il commento dice stable.

## Le PR aperte

Ultimo run di CI di ognuna, sola lettura: su #507 (fe6a5b49), #508
(c34cd59b), #512 (ad28ee72), #515 (2bc81b89) e #459 (2b9379c4) i passi del
cancello dei numeri, della d eufonica, delle marche e dei moduli sono verdi,
`validate_skills` ha 0 avvisi, nessun avviso dei conti in prova, e le prove
del job xdist sono le stesse del job principale. Nessuna promozione le
farebbe diventare rosse su quel commit. Due limiti: #508 e #512 sono in
conflitto con `main` (stato `dirty`) e il loro run è di prima, quindi vanno
rimisurate dopo il rebase; e la promozione di xdist non si vede su un run
vecchio, perché cambia solo dove gira la stessa suite.

## Gli altri lotti del piano

| Lotto | Stato | In questa PR? |
|---|---|---|
| P1 · il canale nel registro | non iniziato: `binari.py` (503 righe) non ha il campo `canale`, nessun `--canali`, nessun test | no: codice e test, una PR sua |
| P2 · `misura_piattaforma.py` | lo script non esiste | no: script nuovo, e serve prima di tutto per spiegare il ×4,4 del passo pytest |
| P5 · il lock di A3 | la parte che installa è stable dall'8/11; nessun lock nel repo, A3 di AMBIENTE non iniziato | no: A3 ha la scelta `.in`/`.lock` e la prova con Dependabot ancora da fare |
| P6 · una Python sola | i workflow hanno `3.13` ovunque tranne il job 3.14 voluto (P8); manca il test che li confronta col registro (A2) | no: è il test di A2, codice |
| P7 · le skill sanno la regola | non fatto: nessuna riga su ADR-0099 in `rumblingstone-automation` e `rumblingstone-debugging` | **sì**, è piccolo: una riga per skill e `validate_skills` verde |

## Come si rifà

Le liste dei run, dei job e i log vengono dall'API di GitHub (con `gh api`):

- run di `main`:
  `repos/gsamuele78/RumblingStone/actions/workflows/ci.yml/runs?branch=main&event=push&created=>=2026-11-08`
  (173 run, 170 verdi); di PR: stesso indirizzo con `event=pull_request&created=>=2026-11-07` (543);
- per ogni run `actions/runs/{id}/jobs`, poi `actions/jobs/{id}/logs` del job
  «Validate skills & scripts» e del job xdist;
- un passo con `continue-on-error` risulta `success` nell'API anche quando
  fallisce, quindi il log si taglia fra la riga `##[group]Run <comando>` e la
  successiva `##[group]Run`, e nel pezzo si cerca `##[error]`. I conteggi delle
  prove sono le righe `N passed, M skipped … in S s` dentro i passi pytest; i
  due giri xdist si sommano.

I risultati sono in [conteggi-prove.tsv](conteggi-prove.tsv) (un run per
riga), [passi-main.tsv](passi-main.tsv) e [passi-pr.tsv](passi-pr.tsv) (un
passo per riga, con l'esito letto dal log).

In locale, su 14085a37 (dopo la promozione `--d-eufonica` non esiste più:
la *d* eufonica è un errore di `validate_lingua.py` senza opzioni):

```bash
python3 scripts/conformita_statblocchi.py --cancello-numeri
python3 scripts/conformita_statblocchi.py --cancello-moduli --severo
python3 scripts/validate_lingua.py
python3 scripts/validate_skills.py
python3 -m pytest scripts/tests -q -n auto -m "not scrive_nel_repo"   # 3.287 + 18 saltate, 340 s
python3 -m pytest scripts/tests -q -m scrive_nel_repo                 # 158, 21 s
```

La simulazione dei 14 conti promossi carica `conformita_statblocchi`, sposta
in memoria `in_prova` dentro `fatti` nel dizionario di
`regole_conformita("pf1e")["conti"]` e lancia `test_conformita_pf1e` con
`unittest`: 14 prove, 30 fallimenti, 1 errore.
