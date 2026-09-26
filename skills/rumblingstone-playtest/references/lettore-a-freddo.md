# Il lettore a freddo — rubrica fissa

Il lettore è un DM esperto che **non ha mai visto il modulo** e deve portarlo
al tavolo stasera. Legge dall'inizio alla fine, una volta, e annota ogni punto
in cui dovrebbe **inventare** o **cercare** per andare avanti. Non giudica lo
stile e non propone riscritture: trova i buchi.

Serve perché chi ha scritto il modulo non vede le proprie lacune: sa già che
aspetto ha ogni stanza e chi ci sta dentro, e non si accorge che sulla
pagina non c'è scritto. Il 2026-09-25, al tavolo, il DM ha dovuto inventare sul
momento sette cose che `ARC07-DEF-4` non diceva, fra luoghi e persone. Nessun
validatore le aveva viste.

⚠️ **Gli esempi di questa rubrica non vengono mai dai casi di calibrazione.**
Quelle sette lacune servono a misurare quanto il lettore trova: se la rubrica
le nominasse, il lettore le troverebbe perché gliele abbiamo dette. La prima
stesura ne citava tre, ed è stata fermata prima di dare un numero.

## Le condizioni

- Il lettore riceve **solo il modulo**, e i file che il modulo cita per nome.
  Niente storia di git, niente piani, niente conversazioni: sono proprio le
  cose che il DM al tavolo non ha.
- Legge **nell'ordine di gioco**, non a salti. Un'informazione che arriva tre
  scene dopo il punto in cui serviva è un rilievo.
- Scrive un rilievo per ogni buco, anche piccolo. Il conteggio si fa dopo.

## I sei codici

| Codice | La domanda che fa scattare il rilievo |
|---|---|
| `L-LUOGO` | I PG entrano in un posto, o ci possono andare, e non c'è niente da leggere o da dire su com'è? |
| `L-PNG` | Una persona parla con i PG, vende o combatte, e manca **aspetto**, **come parla** o **cosa vuole**? Vale anche per chi ha solo un ruolo e nessun nome |
| `L-RIFERIMENTO` | Il testo nomina una cosa, una regola o un evento come già noto, e il modulo non lo spiega da nessuna parte? |
| `L-ORDINE` | Un'informazione serve prima del punto in cui compare? |
| `L-AMBIGUO` | Una frase si può leggere in due modi, e le due letture portano a un gioco diverso? |
| `L-NUMERO` | Manca un numero che il DM dovrà dire ad alta voce: una distanza, una durata, un prezzo, quanti sono? |

## L'uscita

Una tabella, niente prosa intorno:

```
| # | Scena | Codice | Cosa manca | Gravità | Prova |
```

- **Gravità**: 🔴 *il DM deve inventare qualcosa di strutturale* · 🟠 *il DM
  perde più di 30 secondi a cercare* · 🟡 *se ne accorge un giocatore attento*.
  Sono le due metriche del debrief (`SKILL.md` §5), usate come soglie.
- **Prova**: la riga del modulo, citata tra virgolette, che rende evidente il
  buco. Senza prova il rilievo non si conta.

In coda, sempre, **cosa questa lettura non ha potuto verificare**: il ritmo, il
divertimento, se una scena regge davanti a sei persone. Lo dice il tavolo, non
il lettore.

## Come si usa il risultato

- Un rilievo 🔴 o 🟠 diventa una correzione nel modulo, scritta con i quattro
  campi del `SKILL.md` §7.
- Un **tipo** di rilievo che torna in due moduli diversi diventa una regola di
  `scripts/copertura_scene.py`: il lettore trova il difetto la prima volta, il
  cancello impedisce che si ripeta. È la strada per cui il contratto
  «In scena» è nato dai rilievi `L-LUOGO` e `L-PNG` di DEF-4.
- Il lettore **non è un cancello**. Due letture dello stesso testo non danno
  lo stesso elenco, e l'affidabilità di un giudice-agente nel repo non è
  ancora misurata: l'unico κ calcolato, quello di MQM, vale 0,0 perché il
  campione non aveva varianza, e quindi non dice niente
  (`PIANO-MISURA-EDITORIALE-STANDARD` F3.3). Il suo compito è trovare; quello
  del cancello è impedire che si ripeta.
