# 🧭 Orchestrazione delle skill — quali si caricano, in che ordine, chi vince

> **Cos'è**: la gerarchia delle diciotto skill, dichiarata come **dato** invece
> che sparsa in cinque punti di prosa, più l'algoritmo che dice quali caricare
> per un compito e **chi vince** quando due si contraddicono.
>
> **Gate**: `python3 scripts/validate_skills.py` —
> [ADR-0058](../plans/adr/ADR-0058-orchestrazione-a-strati-delle-skill.md)

---

## ⚠️ Prima di tutto: «massimizzare l'uso» non è l'obiettivo

Il DM ha chiesto un metodo che **massimizzi** l'utilizzo delle skill. La
risposta onesta è che il bersaglio giusto è un altro, e vale la pena dirlo
prima di descrivere il meccanismo.

**Caricarle tutte e diciotto sempre sarebbe il danno, non la cura.** Due di
esse — `narrative-style` e `prosa-documenti` — dettano regole **opposte**
sullo stesso italiano (ADR-0035): applicarle insieme non dà il doppio della
qualità, dà un testo che sbaglia in tutti e due i modi. E quattro sono di pura
consultazione: caricarle quando non servono aggiunge rumore, non canone.

> **L'obiettivo misurabile non è «quante ne uso», è: *zero omissioni di ciò
> che è obbligatorio*.** Questo documento serve a non saltarne nessuna delle
> dovute, non a usarne il più possibile.

---

## 1 · I cinque strati *(più la consultazione)*

<!-- orchestrazione: strati -->

| Strato | Che domanda risponde | Skill | Come si compone |
|---|---|---|---|
| **L0 · CANONE** | «È vero, in questa campagna?» | `rumblingstone-campaign` | **batte tutti** |
| **L1 · CHI LEGGE** | «Un giocatore o il repo?» | `rumblingstone-narrative-style` · `rumblingstone-prosa-documenti` | **mutuamente esclusive** |
| **L2 · CHE COSA È** | «Che genere di contenuto?» | `rumblingstone-indagine` · `rumblingstone-module-standard` · `npc-villain-boosting` | **sopra L1**, additive fra loro |
| **L3 · COME ESCE** | «In che forma arriva a chi legge?» | `rumblingstone-editoria` · `rumblingstone-edizione` · `rumblingstone-mapmaking` · `rumblingstone-art-direction` | **additive** a L1 e L2 |
| **L4 · COME SI LAVORA** | «Che gesto di lavoro sto facendo?» | `rumblingstone-plans` · `rumblingstone-automation` · `rumblingstone-playtest` · `rumblingstone-debugging` | **ortogonali** al contenuto |
| **LR · CONSULTAZIONE** | «Qual è il fatto?» | `dnd-35-srd` · `pathfinder-1e-srd` · `forgotten-realms-lore` · `dnd-35-rules` | **non prevalgono mai** |

🔎 **Diciotto skill, diciotto caselle, nessuna in due strati.** Verificato da
`validate_skills.py`: una skill nuova che non trova posto qui **fa fallire il
gate**, ed è il modo di impedire che nasca fuori dalla gerarchia.

---

## 2 · L'algoritmo — cinque domande, in quest'ordine

Non è una tabella da consultare: è una **procedura**, e l'ordine conta.

```
1. Tocco il canone della campagna?        → sì: L0 SEMPRE. Non è negoziabile.
2. Chi leggerà questo testo?              → giocatore: L1 narrative-style
                                          → il repo:   L1 prosa-documenti
                                          → nessuno dei due (codice): nessuna L1
3. Che cosa sto scrivendo, di preciso?    → L2, tutte quelle che si applicano
4. In che forma esce?                     → L3, tutte quelle che si applicano
5. Che gesto di lavoro sto facendo?       → L4, tutte quelle che si applicano
   (LR si consulta quando serve un fatto, mai per decidere)
```

⚠️ **La 2 è l'unica con una risposta sola.** Tutte le altre possono
sommare — è la regola «le righe si sommano» di `AGENTS.md`, resa esplicita.

### Perché l'ordine è questo e non un altro

La 1 viene prima perché **la coerenza batte lo stile** (regola 8): scoprire a
metà che un fatto è falso rende inutile la prosa migliore. La 2 viene prima di
tutto il resto perché sceglie **la norma linguistica**, e le due possibili si
escludono. Dalla 3 in poi l'ordine è comodità, non precedenza.

---

## 3 · I conflitti, e chi vince

<!-- orchestrazione: conflitti -->

| # | Fra | Vince | Perché, e dov'è scritto |
|---|---|---|---|
| C1 | `rumblingstone-campaign` **vs** qualunque skill di stile | **campaign** | `AGENTS.md` regola 8: *«la coerenza batte lo stile»*. Una bella scena che contraddice `state.md` è un errore, non una scelta |
| C2 | `narrative-style` **vs** `prosa-documenti` | **nessuna: si sceglie** | ADR-0035, *due prose due norme*. Decide **chi legge**, non l'argomento. Mescolarle è il difetto, non il compromesso |
| C3 | `indagine` **vs** `narrative-style` | **indagine sopra, narrative-style sotto** | `AGENTS.md`: *«sopra `narrative-style`, che resta il fondo»*. È la sovrapposizione più grossa del repo — **5 trigger condivisi** |
| C4 | `indagine` **vs** i tetti del read-aloud | **i tetti** | `AGENTS.md` regola 11: *«with the read-aloud ceilings winning any conflict»*. Un nodo d'indizio non giustifica un box da quindici righe |
| C5 | `editoria` **vs** `art-direction` (una copertina) | **additive** | `editoria` decide **come sta sulla pagina**, `art-direction` **cosa si vede**. Non si contraddicono: la copertina vuole entrambe |
| C6 | `automation` **vs** `narrative-style` (recap, handout) | **additive** | `automation` è **il gesto** (chi scrive, su che branch, ADR-0007), `narrative-style` è **la voce**. Un recap generato da `dm.py` resta prosa da leggere |
| C7 | `mapmaking` **vs** `narrative-style` (handout) | **additive** | una mappa-handout è un artefatto **e** un testo che un giocatore guarda |
| C8 | qualunque LR **vs** qualunque L0-L4 | **L0-L4** | l'SRD fornisce il fatto, non decide il documento. Una regola 3.5 non sovrascrive una scelta di canone del DM |

🔎 **I conflitti veri sono due, non otto.** C1-C4 sono **precedenze**: qualcuno
vince. C5-C7 sono **sovrapposizioni che non sono conflitti** — due skill
parlano dello stesso oggetto da lati diversi, e la risposta è *tutte e due*.
Tenerle nella stessa tabella serve a non ridiscuterle ogni volta.

---

## 4 · Cosa NON è obbligatorio, e perché dirlo conta

Un elenco di obblighi senza il suo complemento diventa un rito. Le skill di
**L4** e **LR** non si caricano «per sicurezza»:

- **L4** segue il *gesto*: se non stai aprendo un piano, `plans` non serve, e
  aprirla non rende il lavoro più disciplinato.
- **LR** si consulta per un **fatto**. Caricare `forgotten-realms-lore` per
  scrivere un ADR non aggiunge canone: aggiunge contesto che non userai.

⚠️ **L'unica vera regola di completezza è su L0-L2.** Se stai producendo
contenuto di campagna e ne salti una, il difetto è silenzioso — ed è esattamente
il modo in cui `read-aloud-adulti.md` è rimasto inapplicato per tre settimane.
