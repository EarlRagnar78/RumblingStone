# Promozioni da testing a stable del 2026-11-08 (ADR-0099)

> Lotti P3, P4 (xdist), P5 (uv) e P9 di
> [PIANO-PIATTAFORMA-DI-SVILUPPO](../../PIANO-PIATTAFORMA-DI-SVILUPPO.md).
> Ok del DM del 2026-11-08: *«Ok anche per la migrazione a stabile deglinstrumenti eptoseguire ?»* (testo
> com'è). La regola: si sale dopo 14 giorni e 10 run su `main`
> senza falsi allarmi e senza peggiorare il job principale di oltre il 5%. Si
> chiude solo ciò che la misura dimostra.

## Esito

| Componente | Run su `main` dal 2026-10-23 | Falsi allarmi | Tempo | Esito |
|---|---|---|---|---|
| ruff 0.16.9 (passo in «validate») | 81: 76 puliti, 5 rossi il 2026-11-07 | 0: i 5 rossi sono due F841 veri (`fine` in `abbina_incantesimi.py:100`, `val` in `misura_tabelle.py:74`), corretti con la #319 | < 1 s | **stable** |
| uv 0.11.32 (installazione) | 81, «Stessi pacchetti di pip» verde 81 su 81 | 0 | 6 s (uv + installazione) contro 24 s di `pip install` | **stable** nel job principale |
| `converters/` (job «Convertitori») | 81 verdi su 81 | 0 | 52 s in media, in parallelo a «validate» | **stable** |
| pytest-xdist 3.8.0 | 81 verdi su 81, ma con la stessa suite solo negli ultimi 11 | 0 fallimenti in parallelo | 132 s contro 205 s del passo pytest | **resta in testing**, non prima del 2026-11-22 |

Su 81 run il job principale «Validate» dura in media 540 s (mediana 558,
massimo 859) ed è rosso 2 volte (typst 504 su GitHub Releases, 2026-11-08, non
per questi strumenti). La promozione lo accorcia (−18 s di installazione, −1 s
di `compileall`): nessun peggioramento possibile oltre il 5%, da riscontrare
sul run della PR.

Riscontro sul run della PR #353 (020e2fe): «Validate» 584 s, con
installazione 8 s e pytest 274 s. La media di 540 s non è il confronto giusto,
perché la suite è cresciuta in questi 16 giorni (pytest da 205 s in media a
267-270 s oggi). Contro i tre run di `main` dello stesso giorno (590, 572 e
532 s, media 565 s) è +3%: dentro il 5%, e nel rumore fra un runner e
l'altro. L'installazione passa da 26-34 s a 8 s.

## Perché i «success» non nascondevano niente, e dove sì

- Un passo con `continue-on-error: true` che fallisce risulta `success` nell'API
  dei job. Per ruff e pip-audit l'API non basta: si è letto il log del job
  «Validate» di ognuno degli 81 run e si è cercato `##[error]` nella sezione
  del passo ruff ([ruff.tsv](ruff.tsv)). Così sono usciti i 5 rossi del 7/11
  che il «success» copriva.
- I job «testing» e «convertitori» hanno `continue-on-error` sul job, non sui
  passi: un passo fallito si vedrebbe come `failure`. Nessuno su 81.
- **Il buco vero**: dal 23/10 al 2026-11-08 mattina il job xdist eseguiva 9
  prove in meno e ne saltava 9 in più del job principale (per esempio
  2.311 + 23 saltate contro 2.320 + 14), perché non aveva typst: «validate» lo
  installava in un passo suo. Dalla #342 (29056bf, typst da `requirements.txt`)
  i conteggi combaciano: 11 run su 11 ([conteggi-prove.txt](conteggi-prove.txt),
  «DIVERSI» = conteggi diversi). Il verde di xdist era quindi su una suite più
  piccola per 70 run su 81, e i 14 giorni con la suite intera partono dal
  2026-11-08.

## Chi scrive nel repo vero: la misura rifatta

La lista `SCRIVONO_NEL_REPO` di `scripts/tests/conftest.py` veniva dalla misura
del 23/10 su 2.035 prove; oggi sono 2.545. Rifatta con lo stesso metodo (un
audit hook di Python su `open` in scrittura, `os.remove`, `os.rename`,
`os.mkdir`, caricato come `sitecustomize`, [sitecustomize_scritture.py](sitecustomize_scritture.py)),
su tutta la suite in serie: 2.529 passate, 16 saltate.

Scrivono fuori dalle cartelle temporanee i cinque moduli già in lista e **due
nuovi**:

- `test_migliora_prosa.py`: il file provvisorio _testi-provvisori.md nella
  cartella del cieco della pipeline di qualita-misurabile-2026-10-22
- `test_misura_stampa.py`: _tmp_appendice.typ, _tmp_appendice.pdf e la
  cartella _tmp_misura_stampa dentro scripts/tests

Entrano nella lista. In CI non hanno mai fatto fallire il giro parallelo (81
su 81), ma lo stesso schema ha già dato un falso rosso il 23/10
(`test_validate_docs`). I rilievi su `test_new_group` e `test_gruppo_nuovo`
sono un falso positivo del hook: cancellano i symlink della loro copia
temporanea, e `realpath` li risolve nel repo.

Dopo il cambio, in locale su 4 core: giro parallelo 2.398 passate e 14
saltate in 57 s (due giri uguali), giro in serie 131 passate e 2 saltate in
11 s; insieme 2.529 + 16, come la suite in serie. Un primo giro parallelo era
fallito in `test_verifica_sezione6` perché in quel momento l'albero conteneva
questo stesso file con percorsi assoluti, che il cancello vero boccia: rifatto
con l'albero pulito, verde due volte.

## Cosa cambia in `ci.yml`

- «Install dependencies» installa con `uv pip install --system` (uv fissato a
  0.11.32). pip-audit legge ancora `requirements-dev.txt`.
- Il passo ruff perde `continue-on-error`; il passo `compileall` esce (gli
  errori di sintassi li vede E9). Un'avvertenza: `compileall` guardava anche
  `scripts/Old`, che ruff esclude; oggi `scripts/Old` ha solo due script
  shell, quindi non si perde niente.
- Il job `convertitori` perde `continue-on-error` e si chiama «Convertitori
  (import su 3.13)».
- Il job `testing` si chiama «pytest-xdist in prova» e non confronta più uv
  con pip: uv è il riferimento.

Fuori da questa PR: shellcheck (`|| true`), il riscontro SRD, il ratchet
INFERRED, `check_schede` (non prima del 2026-11-22), il resto di P5 (il lock
con hash di A3) e gli altri job che installano con pip.

**Da fare dal DM**: nel ruleset di `main` i check richiesti sono solo
«Validate skills & scripts» e «Build skill packages». «Convertitori (import su
3.13)» stable fa diventare rosso il run, ma blocca il merge solo se lo si
aggiunge ai check richiesti (Impostazioni → Rules).

## Come si rifà

I dati (`lista.tsv`, i job e i log) si scaricano dall'API REST di GitHub:
`/repos/gsamuele78/RumblingStone/actions/workflows/ci.yml/runs?branch=main&event=push`,
poi `/actions/runs/{id}/jobs` e `/actions/jobs/{id}/logs` per ogni run. Le
tabelle [durate.txt](durate.txt), [ruff.tsv](ruff.tsv) e
[conteggi-prove.txt](conteggi-prove.txt) vengono da quei file.
