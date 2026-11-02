# Come si rilascia RumblingStone

La regola è [ADR-0100](../plans/adr/ADR-0100-il-rilascio-e-una-pr.md). Il
meccanismo è quello di iemod-fetch.

## Cos'è un rilascio

Un tag `vX.Y.Z` e il rilascio GitHub che lo accompagna. Dentro ci sono i
pacchetti delle skill in un archivio riproducibile, le impronte `SHA256SUMS`
e le note prese dal [CHANGELOG](../CHANGELOG.md). Il tag è l'unica cosa che
conta, e non lo crea nessuno a mano.

## I numeri

Versionamento semantico sulla superficie pubblica: la CLI `dm.py`, i contratti
dei file (JSON delle mappe, `campaign/group.yaml`, le regioni `auto` di
`state.md`), nomi e formato dei pacchetti delle skill, la versione di Python.

- **Maggiore**: un comando o un'opzione di `dm.py` tolti o cambiati di senso;
  un contratto che non legge più i file di prima; il salto di Python a ogni
  rilascio di Debian (ADR-0099).
- **Minore**: uno strumento, una skill, un arco o un modulo nuovi.
- **Correzione**: un bug, un'errata, un documento.

## Fare un rilascio

È una PR come le altre:

```bash
# 1. CHANGELOG.md: le righe di «Non rilasciato» vanno sotto
#    ## [1.1.0] - AAAA-MM-GG, e «Non rilasciato» resta in cima vuota.
# 2. La versione, nello stesso commit:
$EDITOR scripts/dmcore/__init__.py      # __version__ = "1.1.0"
# 3. Verde in locale, poi la PR.
python3 -m pytest scripts/tests -q
```

Unirla è il rilascio. Il push su main cambia `CHANGELOG.md`, e il workflow
Release:

1. con `scripts/release_plan.py` sceglie il commit: l'unione in cui
   `__version__` è diventato 1.1.0. Se da allora i pacchetti non sono cambiati
   (solo piani, CI, contenuti), sceglie la testa di main;
2. riesegue tutta la CI su quel commit;
3. controlla che `dm.py --version` dica il numero del tag;
4. costruisce i pacchetti con `build-skills.sh --no-deploy` e li chiude in
   `rumblingstone-skills-v1.1.0.tar.gz`. L'archivio è riproducibile: con
   `SOURCE_DATE_EPOCH` alla data del commit, ordine dei nomi, proprietario e
   data sono fissi, e tre costruzioni dello stesso commit hanno dato la stessa
   impronta;
5. firma l'archivio con un'attestazione di provenienza (Sigstore);
6. crea il tag `v1.1.0` e il rilascio, con la sezione del CHANGELOG come note
   e le impronte in fondo.

Una versione che ha già il tag si salta. Rieseguire il workflow o correggere
una sezione vecchia del CHANGELOG non fa danni.

## Correggere le note

Si corregge la sezione nel CHANGELOG e si unisce. A ogni push su main il job
«Note dei rilasci allineate al CHANGELOG» riscrive il testo dei rilasci che non
corrisponde più. Il blocco delle impronte resta quello originale.

## Prova senza pubblicare

Non c'è un avvio a mano del workflow: eseguirebbe con i permessi di main il
codice di un commit scelto da chi lo lancia (CodeQL lo segnala come cache
poisoning). Per rifare un rilascio fallito si rilancia il run da Actions.

- Una PR che cambia `release.yml`, `release_plan.py` o `release_notes.py`
  prova la catena sul proprio commit: piano e costruzione, mai tag né rilascio.

## Quando il token non basta

GITHUB_TOKEN non può creare un tag su un commit i cui file in
`.github/workflows/` differiscono da quelli di main. Succede solo se, fra
l'unione della PR di rilascio e il run, è entrata un'altra PR che cambia i
workflow e anche le skill. Il workflow si ferma al piano e lo dice. Si esce
spingendo il tag a mano:

```bash
git tag -a v1.1.0 -m "1.1.0" <sha> && git push origin v1.1.0
```

Il push del tag fa partire il workflow, che rilascia esattamente quel commit.

## Verificare uno scaricamento

```bash
sha256sum -c SHA256SUMS
# chi l'ha costruito: quale workflow, su quale commit (Sigstore, senza chiavi)
gh attestation verify rumblingstone-skills-v1.1.0.tar.gz --repo gsamuele78/RumblingStone
# e, dal sorgente, lo stesso archivio:
git checkout v1.1.0
export SOURCE_DATE_EPOCH=$(git log -1 --format=%ct)
./scripts/build-skills.sh --no-deploy
tar --sort=name --owner=0 --group=0 --numeric-owner --mtime="@$SOURCE_DATE_EPOCH" \
    -C build -cf - . | gzip -n -9 | sha256sum
```

## Se un rilascio è sbagliato

Se ne fa uno di correzione. Il tag non si sposta: qualcuno ha già scaricato
ciò a cui puntava.

## Cosa non esce

I PDF dei booklet, gli asset esterni e tutto ciò che non sta nel repo. Per
farli uscire serve una decisione del DM che passi dal gate d'uscita di
`rumblingstone-edizione` (ADR-0100 §6).
