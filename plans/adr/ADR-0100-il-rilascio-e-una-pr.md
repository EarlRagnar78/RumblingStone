# ADR-0100 — Il rilascio è una PR: tag e rilascio li crea il merge

**Stato**: accettata dal DM il 2026-10-23 (D7 di [PIANO-PIATTAFORMA](../PIANO-PIATTAFORMA-DI-SVILUPPO.md): *«1.0.0, solo le skill»*)
**Data**: 2026-10-23
**Decisione-fonte**: il DM, 2026-10-23: *«diventa std per tutto il resto […] aggiornando la documentazione, changelog, gli ADR, e iniziare il tag e release come fatto ad esempio nel progetto iemod-fetch»*.
**Rapporti**: estende [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (la piattaforma ha una versione, e la versione si rilascia); riprende ADR-0027 di iemod-fetch (stesso autore, MIT), adattato a un repo senza pacchetto Python.

## Contesto

Il repo non ha mai avuto un rilascio. `scripts/dmcore/__init__.py` dice
`__version__ = "0.1.0"` da quando esiste, nessuno l'ha mai alzato, e i soli
tag sono quelli d'archivio dei rami chiusi. `plans/CHANGELOG.md` è il diario
dei piani, non dice cosa cambia per chi usa gli strumenti. Con ADR-0099 la
piattaforma ha una regola per ogni componente, ma nessun punto fermo a cui
dire «questa è la versione X, costruita così».

iemod-fetch risolve lo stesso problema con un meccanismo che il DM conosce: un
CHANGELOG.md in formato Keep a Changelog, il numero di versione nel codice, e
un workflow che al merge della PR di rilascio crea il tag e il rilascio da
solo. Nessuno etichetta a mano, nessun segreto a lunga vita.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Il merge della PR di rilascio crea tag e rilascio** (scelta, come iemod-fetch) | un solo passo umano, la revisione della PR; il tag cade sul commit giusto; note e CHANGELOG non divergono | un workflow in più da tenere; GITHUB_TOKEN non può etichettare un commit i cui workflow differiscono da main (caso raro, documentato) |
| Tag a mano (`git tag && git push`) e rilascio dall'interfaccia | niente da costruire | dimenticabile; il tag finisce sul commit sbagliato; le note si riscrivono ogni volta |
| Rilascio a calendario (CalVer, ogni mese) | prevedibile | un rilascio senza niente dentro non dice niente; il DM ha chiesto il modello di iemod-fetch |
| release-please o semantic-release | strumenti diffusi | vogliono commit convenzionali in inglese che il repo non usa; un'azione di terzi con permessi di scrittura in più |

## Decisione

1. **Versionamento semantico** sulla superficie pubblica del progetto: la CLI
   `dm.py` (comandi e opzioni), i contratti dei file (JSON delle mappe,
   `campaign/group.yaml`, regioni `auto` di `state.md`), nomi e formato dei
   pacchetti delle skill, la versione di Python.
   - **maggiore**: un comando o un'opzione tolti o cambiati di senso, un
     contratto che non legge più i file di prima, un salto di Python (ADR-0099 §6);
   - **minore**: uno strumento, una skill, un arco o un modulo nuovi;
   - **correzione**: bug, errata, documenti.
2. **Il numero sta in un posto**, `__version__` in `scripts/dmcore/__init__.py`;
   `dm.py --version` lo legge. Un test boccia la CI se la sezione più recente
   di `CHANGELOG.md` dice un altro numero.
3. **`CHANGELOG.md` alla radice** in formato Keep a Changelog, in italiano, con
   la sezione `## [Non rilasciato]` in cima. Chi cambia qualcosa della
   superficie pubblica ci aggiunge una riga nella stessa PR.
   `plans/CHANGELOG.md` resta il diario dei piani.
4. **Rilasciare è unire una PR** che sposta «Non rilasciato» sotto
   `## [X.Y.Z] - AAAA-MM-GG` e alza `__version__`. Al push su main il
   workflow `release.yml`:
   - sceglie il commit con `scripts/release_plan.py` (l'unione in cui la
     versione è diventata X.Y.Z, o la testa di main se i pacchetti non sono
     cambiati da allora);
   - riesegue tutta la CI su quel commit;
   - costruisce i pacchetti delle skill (`build-skills.sh`) in un archivio
     riproducibile con `SHA256SUMS`;
   - crea il tag `vX.Y.Z` e il rilascio GitHub, con le note prese dalla
     sezione del CHANGELOG (`scripts/release_notes.py`).
5. **Note e CHANGELOG non divergono**: a ogni push su main che tocca il
   CHANGELOG, una sezione corretta riscrive le note del suo rilascio.
6. **Esce solo ciò che è già nel repo**: i pacchetti delle skill e i sorgenti
   del tag. Niente PDF dei booklet né asset esterni finché il DM non lo
   decide passando dal gate di `rumblingstone-edizione`. Il repo è pubblico
   (verificato il 2026-10-23), quindi anche il rilascio lo è: non aggiunge
   niente che chi legge il repo non veda già.
7. **Un rilascio sbagliato non si sposta**: se ne fa uno di correzione. Il tag
   non si muove.
8. **Primo rilascio: 1.0.0**, con la piattaforma di ADR-0099 come base. Lo 0.1.0
   scritto nel codice non è mai stato rilasciato.

Diverge da iemod-fetch in tre punti. Non c'è PyPI, perché il repo non è un
pacchetto Python. Non c'è il back-fill di versioni vecchie, perché non ne
esistono. E la prova generale su una PR non riesegue la CI, che la PR esegue
già. Come in iemod-fetch, l'archivio ha un'attestazione di provenienza
firmata con Sigstore senza chiavi (`actions/attest-build-provenance`): dice
quale workflow, su quale commit, ha prodotto quei byte.

## Conseguenze

- Un rilascio costa una PR di due righe più le note. Le note si scrivono una
  volta, nel CHANGELOG, e il rilascio le copia.
- Ogni PR che cambia la superficie pubblica scrive una riga in «Non
  rilasciato». Il template della PR lo ricorda.
- Il workflow Release è un componente della piattaforma: entra in testing.
  Sale a stable dopo tre rilasci senza interventi a mano (ADR-0099 §3, con il
  conto in rilasci invece che in run).
- Si paga: un secondo CHANGELOG da tenere, e una CI intera in più a ogni
  rilascio (circa 8 minuti).

**Da rivedere se**: il repo diventa privato (allora le attestazioni di
provenienza richiedono GitHub Enterprise e vanno tolte); oppure
un rilascio richiede un intervento a mano due volte di fila; oppure il DM
vuole distribuire i PDF dei booklet.
