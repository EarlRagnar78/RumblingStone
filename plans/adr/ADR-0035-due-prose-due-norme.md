# ADR-0035 — Due prose, due norme

> **Stato**: accettata · **Data**: 2026-09-03 · **Decide**: G. Samuele (DM)
> **Attua**: `plans/PIANO-PROSA-CHE-NON-SEMBRI-GENERATA.md`
> **Rapporti**: estende ADR-0016 (l'italiano è la lingua sorgente) e la norma di
> `italiano-nativo.md`; il gate è quello aperto dal lotto P della catena
> editoriale.

## Il contesto

I giocatori hanno detto due volte, a un mese di distanza, che la prosa sembra
tradotta dall'inglese. Il DM porta due riferimenti esterni — la skill *the
writing whip* e l'elenco *tropes.fyi* — e chiede se convenga usarli.

## La decisione

**Il repo scrive due prose diverse, e da oggi hanno due norme separate.**

| | Prosa di gioco | Documenti del repo |
|---|---|---|
| Cosa | read-aloud, handout, dialoghi, echi, teaser, iscrizioni | guide, ADR, piani, ricerche, skill, README, corpi delle PR |
| Norma | `rumblingstone-narrative-style` → `italiano-nativo.md` | `rumblingstone-prosa-documenti` |
| Misura | `validate_prosa.py` | `validate_prosa.py --documenti` |
| Chi legge | i giocatori, spesso ad alta voce | chi lavora nel repo, fra sei mesi |

Tenerle separate non è pignoleria: **alcune regole dell'una sono sbagliate
nell'altra.** In un piano il numero annunciato prima dell'elenco è un tic; in un
read-aloud *«tre porte, tre serrature»* è ritmo. In un documento la frase breve
isolata è un tell; in un box è il colpo che chiude.

## Le tre cose che la misura ha deciso al posto mio

**Un tropo inglese non si trapianta.** Le intestazioni con parola interrogativa
sono un tell in inglese; in italiano «Come si usa» è il titolo giusto. La frase
breve isolata è un tic in un saggio e ritmo normale in italiano tecnico dopo un
periodo lungo.

**Un tropo non si trapianta neanche fra generi.** *«Immagina di…»* è nell'elenco
dei difetti, ed è letteralmente cosa fa un read-aloud in seconda persona.

**Quello che non si misura si scrive, non si conta.** Rotazione dei sinonimi,
autocitazione, anafora e gerundio d'analisi sono tic veri e nessuno dei quattro
si distingue dal linguaggio normale con una regex: cercandoli si trovano
descrizioni di mappe, iscrizioni runiche e gerundi italiani corretti. Stanno in
`italiano-nativo.md` §9.2-bis come prescrizione, **con scritto perché non sono
un gate**, così nessuno prova a farne uno fra sei mesi.

## Le soglie, e perché sono quelle

Tarate sulla distribuzione reale dei 177 documenti: mediana 82 trattini ogni
mille righe di prosa, quartile alto 118. La soglia a 150 segnala una trentina di
file su 154. Una soglia a 82 li avrebbe segnalati quasi tutti, e **un rilievo
che compare ovunque è un rilievo che nessuno legge** — poi si spegne il gate, e
con lui i controlli che funzionavano.

Il conteggio esclude tabelle, blocchi di codice, titoli e citazioni. Senza quella
esclusione il file peggiore del repo risultava il `CHANGELOG` con 2.819 trattini
ogni mille righe, che era un artefatto della misura: in una cella `—` vuol dire
«niente», ed è la notazione giusta.

## Le conseguenze

**Quello che si guadagna.** Un documento nuovo si controlla in un comando, e i
54 rilievi aperti dicono da dove cominciare. La skill porta i numeri, non le
opinioni, e chi la legge fra sei mesi sa perché una regola c'è.

**Quello che si paga.**

- **Il gate non blocca.** 54 rilievi non si chiudono in un commit, e un gate
  rosso che resta rosso viene aggirato. Diventerà bloccante quando il lotto D
  avrà ripulito i peggiori, non prima.
- **Una norma in più da tenere allineata.** Due skill di stile possono divergere.
  Il confine è scritto in tutt'e due, ed è la sola difesa.
- **I quattro tic di §9.2-bis restano affidati a un occhio.** Nessuna misura li
  tiene, e quando l'occhio non c'è passano.
