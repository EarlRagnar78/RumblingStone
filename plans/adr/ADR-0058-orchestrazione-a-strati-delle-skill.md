# ADR-0058 — Le skill si orchestrano a strati, e la precedenza è un dato

- **Stato**: accettata (2026-09-19), **attuata** (`skills/ORCHESTRAZIONE.md`,
  `check_orchestrazione()` in `validate_skills.py`)
- **Decisore**: DM — *«fai un ordine gerarchico delle skill nelle golden rule
  che eviti di far saltare le skill e le usi in modo intelligente, non
  omettendo ma usandole quanto serve. C'è un metodo/algoritmo che ottimizza
  l'utilizzo? Verificare se ci sono skill che si sovrappongono e orchestrarle
  in maniera smart eliminando i contrasti, con meccanismi davvero misurabili»*
- **Rapporti**: estende [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md)
  (l'instradamento aveva un gate, la **precedenza** no) · applica
  [ADR-0056](ADR-0056-una-norma-senza-misura-non-esiste.md) alla gerarchia
  stessa · formalizza [ADR-0035](ADR-0035-due-prose-due-norme.md)

---

## Contesto: la gerarchia c'era già, sparsa in cinque punti di prosa

Misurando `AGENTS.md` e le skill, le regole di precedenza **esistevano tutte**,
e tutte come frasi:

| Dove | Cosa diceva |
|---|---|
| regola 8 | *«la coerenza batte lo stile»* |
| tabella per compito | *«`indagine` sopra `narrative-style`, che resta il fondo»* |
| tabella per compito | *«⚠️ regole opposte alla riga sopra: non mescolarle»* |
| avvertenze | *«le righe si sommano»* |
| regola 11 | *«with the read-aloud ceilings winning any conflict»* |

Cinque affermazioni corrette, in cinque posti, **nessuna verificabile**. E
`validate_skills.py` presidiava l'**instradamento** (ADR-0041: ogni skill è
citata, nessun puntatore morto) ma **non la precedenza**: una skill nuova
poteva nascere senza che nessuno decidesse dove sta nella gerarchia.

## 🔎 Le sovrapposizioni, misurate prima di progettare

Contate sui trigger dichiarati nel frontmatter delle diciotto skill:

| Coppia | Trigger condivisi |
|---|---:|
| `indagine` ↔ `narrative-style` | **5** — *indagine, indizio, mistero, ricomposizione, chi è stato* |
| `automation` ↔ `narrative-style` | 2 — *handout, recap* |
| `art-direction` ↔ `editoria` · `automation` ↔ `mapmaking` · `mapmaking` ↔ `narrative-style` | 1 ciascuna |

**Cinque coppie in tutto**, e la più grossa aveva già la sua precedenza scritta.
La sovrapposizione non era il problema: il problema era che **non si poteva
verificare** che una precedenza esistesse.

## Decisione

**Cinque strati più uno di consultazione, dichiarati come dato**, e un
algoritmo a cinque domande in `skills/ORCHESTRAZIONE.md`:

| Strato | Domanda | Composizione |
|---|---|---|
| **L0 · canone** | «È vero in questa campagna?» | batte tutti |
| **L1 · chi legge** | «Un giocatore o il repo?» | **mutuamente esclusive** |
| **L2 · che cosa è** | «Che genere di contenuto?» | sopra L1, additive fra loro |
| **L3 · come esce** | «In che forma arriva?» | additive |
| **L4 · come si lavora** | «Che gesto sto facendo?» | ortogonali al contenuto |
| **LR · consultazione** | «Qual è il fatto?» | non prevalgono mai |

🔎 **Diciotto skill, diciotto caselle, nessuna in due strati.** Il modello non è
stato inventato: è la struttura che il repo già usava, e il fatto che copra
tutto esattamente una volta è la prova che era lì.

Gli **otto conflitti** hanno ognuno un vincitore dichiarato — e la tabella dice
anche la cosa meno ovvia: **i conflitti veri sono quattro**. Gli altri quattro
sono sovrapposizioni che **non** sono conflitti (una copertina vuole
`editoria` *e* `art-direction`), e stanno nella stessa tabella per non
ridiscuterle ogni volta.

### Il gate

`check_orchestrazione()` dentro `validate_skills.py` — **non** un secondo
script, perché la cosa da presidiare è la stessa: la relazione fra le skill e
il documento che le governa.

1. **Copertura**: ogni skill su disco sta in **esattamente uno** strato.
2. **Onestà**: gli strati e i conflitti non nominano skill inesistenti.
3. **Risoluzione**: ogni conflitto porta un vincitore scritto.

## ⚠️ Perché «massimizzare l'uso» è il bersaglio sbagliato

Il DM ha chiesto un metodo che **massimizzi** l'utilizzo delle skill. Su questo
la decisione va contro la richiesta letterale, e vale la pena dirlo:

**caricarle tutte e diciotto sempre sarebbe il danno.** `narrative-style` e
`prosa-documenti` dettano regole **opposte** sullo stesso italiano (ADR-0035):
applicarle insieme non dà il doppio della qualità, dà un testo che sbaglia in
entrambi i modi. E le quattro di consultazione, caricate quando non servono,
aggiungono contesto che nessuno userà.

> **Il bersaglio misurabile è: *zero omissioni di ciò che è obbligatorio*.**
> Non «quante ne uso».

E il complemento è dichiarato: **L4 e LR non si caricano per sicurezza**. Un
elenco di obblighi senza il suo contrario diventa un rito, e un rito lo si
salta appena si ha fretta.

## Conseguenze

**Buone.**
- Una skill nuova **non può nascere fuori dalla gerarchia**: il gate è rosso
  finché non la si colloca, e collocarla è una decisione di dieci secondi.
- Le cinque frasi sparse diventano una tabella sola, e le precedenze si
  leggono senza cercarle.

**Costi, dichiarati.**
- ⚠️ **Il gate verifica la forma, non la saggezza.** Può dire che ogni skill
  ha uno strato; non può dire che sia lo strato **giusto**. Se qualcuno
  mettesse `editoria` in LR, il gate resterebbe verde.
- ⚠️ **L'algoritmo non è eseguibile da una macchina.** Le cinque domande le
  risponde chi scrive; nessuno script sa se il testo che stai per produrre lo
  leggerà un giocatore o il repo. Il presidio vero resta la domanda 2 di
  `AGENTS.md`, e questo documento la rende **esplicita e ordinata**, non
  automatica.
- 🔴 **Restano otto conflitti dichiarati oggi.** Se domani nascono
  sovrapposizioni nuove e nessuno le aggiunge, il gate **non se ne accorge**:
  controlla che le righe presenti siano oneste, non che siano complete. La
  completezza è un giudizio, e sta in questa riga invece che in un falso verde.

## Alternative scartate

1. **Una priorità numerica piatta** (skill 1 > skill 2 > …). Scartata: il repo
   non funziona così. `editoria` e `art-direction` non si ordinano, si sommano;
   `narrative-style` e `prosa-documenti` non si ordinano, si escludono. Una
   lista piatta avrebbe costretto a inventare precedenze dove non servono.
2. **Caricare sempre tutte le skill.** Scartata: vedi sopra — è il danno.
3. **Un orchestratore che sceglie le skill a runtime.** Scartata per ADR-0012
   (gate verificabili, zero token) e perché la scelta dipende da
   un'informazione che solo chi scrive ha: **chi leggerà il testo**.
