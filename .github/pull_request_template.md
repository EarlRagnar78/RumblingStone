<!-- Modello delle PR (D7 di plans/PIANO-RECUPERO-DECISIONI-E-REVISIONI-INCOMPIUTE-2026-10.md).
     Le sezioni che non c'entrano si tolgono, non si lasciano vuote. -->

**Prima:** cosa vedeva il DM (o chi usa il repo) prima di questa PR.

**Dopo:** cosa vede adesso.

## Come

Le scelte che il diff non spiega da solo.

## Piani e decisioni

- [ ] piano, riga in `plans/INDEX.md` e riga in `plans/CHANGELOG.md` nello **stesso commit** (regola d'oro di `rumblingstone-plans`)
- [ ] le decisioni del DM nelle tabelle `<!-- decisioni-dm: … -->`, con l'eco; §4 di STATO rigenerato con `decisioni_dm.py --emit`
- [ ] un ADR nuovo ha il numero prenotato in `plans/adr-prenotati.json` e la prenotazione è tolta in questa PR
- [ ] una norma nuova è registrata in `skills/REGISTRO-NORME-EDITORIALI.md` con chi la misura (G3)

## Controlli eseguiti

I comandi e il loro esito. Un controllo che non è girato si scrive **non eseguito**, mai «passato».

## Come si torna indietro

Il revert basta, o serve altro (file generati, stato di gruppo, una PR che dipende da questa)?

## Note oneste

Cosa resta fuori, cosa non ho potuto verificare, cosa ho dedotto invece di misurare.
