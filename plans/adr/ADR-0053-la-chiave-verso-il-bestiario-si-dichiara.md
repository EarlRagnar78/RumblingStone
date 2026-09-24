# ADR-0053 — La chiave verso il Bestiario si dichiara, non si deduce

- **Stato**: accettata (2026-09-17), **attuata**
- **Decide**: come si passa dallo stato vivo di un PNG alla sua scheda
- **Chiude**: **D17** (i due villain senza scheda: si scrivono, si contano o
  escono da §3?)
- **Segue**: ADR-0052, che aveva dichiarato questo limite e rimandato qui

---

## Contesto

ADR-0052 ha chiuso la domanda di cosa è dato e cosa è prosa, e ha lasciato
scritto il proprio limite: *«un LLM che parte dallo stato vivo e vuole la scheda
di un PNG non ha una chiave»*. La misura di allora diceva 11 villain su 13 e 23
righe di §4 su 31 agganciabili per somiglianza di stringa.

**Rimisurando prima di costruire, quel numero si è rivelato ottimista in un modo
che conta più del numero.** Il primo confronto era severo — pretendeva tutte le
parole del nome della cartella — e produceva solo silenzi. Allentandolo, le
righe agganciate salgono; ma le nuove risposte sono **sbagliate**:

| Riga in `state.yaml` | Cosa aggancia un confronto permissivo | |
|---|---|---|
| `Zalkatar (Illithid Warlock)` | `Xal_thor` **oppure** `Zarim` | due illithid diversi |
| `Wyrmlord Saarvith + Regiarix` | `Wyrmlord_Karruk` | un altro wyrmlord |
| `Zalkatar (via Sethrax)` | `Sethrax_il_Velato` | ma chi *sa* è Zalkatar: il tramite non è il soggetto |
| `Druid Circle of the Sacred Forest` | `druid-bear-ally-cr12.md` | l'orso alleato di un druido |

🔴 **È la scoperta che decide l'architettura.** Un matcher più generoso non
riduce l'ignoranza: la **traveste**. Trasforma «non lo so» in un errore sicuro
di sé, e il quarto caso mostra perché è la forma peggiore — «Sethrax» è un PNG
che esiste davvero, quindi il collegamento sbagliato supera qualunque controllo
di esistenza. È esattamente il modo in cui sbaglia un LLM.

Una seconda cosa emersa misurando: il `Bestiario/` **non ha un file per
persona**. La scheda canonica sta in `X/X/X.md` o `X/X.md`, il `*-crN.md` in
cima è spesso un puntatore, e alcune persone (Brenna Sorvane, Sertieren, Norro
Wiston) vivono come **sezione dentro un file di gruppo**. Nessuna regola di
derivazione dal nome può sapere questo.

## Decisione

**Una sezione `png` in `campaign/state.yaml`: l'anagrafica, con la chiave
dichiarata.** Ventotto voci, una per soggetto nominato in §3 o §4:

```yaml
- id: sonjak                      # chiave stabile
  nome: Sonjak (Matrona Sajak)    # nome canonico
  tipo: persona                   # persona | gruppo | divinita
  scheda: Bestiario/villain/Sonjak/Sonjak.md
```

E `png_id` sulle righe di §3 (13) e §4 (31), che vi puntano.

Tre regole la tengono vera, e sono tutte provate a mordere:

- **R10** — ogni `png_id` risolve a una voce, gli `id` sono unici, e un
  `scheda: null` porta sempre il proprio `perche_senza_scheda`. Un id rotto
  sarebbe invisibile: il nome per esteso resta leggibile nella riga, quindi il
  documento *sembra* sano e solo la macchina inciampa.
- **R11** — ogni `scheda` dichiarata punta a un file che **esiste**. È ciò che
  rende la chiave una chiave: senza, sarebbe una stringa plausibile, cioè la
  stessa cosa di prima scritta meglio. Le schede si spostano e si rinominano;
  questa regola se ne accorge il giorno stesso, non sei settimane dopo al tavolo.
- **R12** — le voci senza scheda si **contano** a ogni esecuzione, come R7 (il
  tempo non dichiarato) e R8 (gli stati ignoti). Forma di ADR-0041.
- **R13** — 🐛 **nata da un errore mio, e lo dice.** Un buco dichiarato è
  un'affermazione forte: dice «ho cercato e non c'è». Questa regola la mette
  alla prova a ogni esecuzione contro **tutto** il repo scritto a mano, non solo
  contro il `Bestiario/`. Se emergono file che portano quel nome, o uno di essi
  è la scheda, o va detto in `candidati_esclusi` perché non lo è. Provata
  all'indietro **sullo stato in cui l'anagrafica è nata**: rimettendo `zalkatar`
  a «senza scheda», il cancello diventa rosso.

### D17 — e la premessa della domanda era falsa

🐛 **La prima stesura di questo ADR diceva che quattro voci non avevano una
scheda. Tre di quelle quattro ce l'avevano, e il DM me l'ha fatto notare.**

L'errore non è stato non trovarle: è stato **come ho concluso**. Ho cercato le
schede **solo dentro `Bestiario/`**, e quando ho allargato la ricerca ho
troncato l'output a sei righe con `head -6` — concludendo «non esistono» da una
lista tagliata. Le tre righe che mancavano dall'output erano proprio i file che
cercavo.

| | Dove la scheda era davvero |
|---|---|
| `zalkatar` | `09_…/Arco-Post-Hammerfist-P2A-Torre-PARTE4-STATBLOCCHI-Zalkatar.md` — **GS 13**, 14d4+70, CA 24, statblocco completo |
| `saarvith-regiarix` | `09_…/Arco-Post-Hammerfist-P2-RHEST-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` — **GS 13**; il file `FASE4` accanto dichiara *«le statistiche sono lì; questo è la regia dello scontro, non le duplica»* |
| `cerchio-sacro` | `Bestiario/mostri/cerchio-druid7-cr7.md` — «Cerchio Sacro Druid 7 (Hella ally) [ACCEPTED — DM-canon 2026-05-05]», `statblocco` validato, e la nota «30 druidi + 5 Treant alleanza» |
| `lathander-mask` | **nessuna, e va bene così**: due divinità non sono una creatura |

**Quindi D17 non aveva bisogno di essere decisa nel modo in cui era posta.** Non
c'era niente da scrivere e niente da togliere: c'era da **cercare meglio**. La
risposta è che le schede si dichiarano dove stanno — e due di esse stanno in un
arco, non nel Bestiario.

Resta un buco su ventotto, ed è corretto.

⚠️ **Una scheda non vive per forza nel `Bestiario/`.** È la conseguenza di
progetto più importante di questa correzione: `scheda` significa «dove stanno le
statistiche», non «dove nel Bestiario». Un cancello tarato sul Bestiario
avrebbe continuato a dare per mancanti due boss da GS 13 che il DM ha scritto.

## Alternative scartate

| | Perché no |
|---|---|
| **Derivare la scheda dal nome a ogni lettura** | È la cosa che questo ADR esiste per non fare. Quattro errori su quattro casi difficili, e il peggiore punta a un PNG reale |
| **`scheda` direttamente sulle righe di §3 e §4** | Tre persone compaiono in due righe di §4 (Sonjak, Varis, Conte Valerius) e quattro anche in §3: il puntatore finirebbe in due o tre posti, che divergono alla prima rinomina |
| **Un `id` derivato dal nome con uno slugger** | «Zin'thara Vel'Ryn «la Voce di Ragnatela»» e «Wyrmlord Saarvith + Regiarix» non hanno uno slug ovvio, e cambiare il nome visualizzato cambierebbe la chiave. L'`id` è stabile *perché* è scritto a mano |
| **Portare `stato` nell'anagrafica adesso** | Sarebbe il refactor giusto (vedi sotto), ma metterebbe `stato` in due posti durante la migrazione — il difetto dei due master. Si fa quando l'anagrafica ha dimostrato di reggere |

## Conseguenze

**Quel che si guadagna.** Da `state.yaml` alla scheda in un passo, verificato:
un algoritmo segue `png_id` → `png[].scheda` e apre un file che c'è. E i due
errori che questo lotto ha attraversato sono **scritti**, quindi non si
ripetono: la conoscenza di Zalkatar messa in conto a Sethrax (R10 la fissa), e
un buco dichiarato senza aver cercato dappertutto (R13 lo mette alla prova).

**Quel che si perde.** Ventotto voci da tenere vere, e un `png_id` in più su 44
righe. Il costo si paga a ogni PNG nuovo: prima si dichiara, poi si nomina.

⚠️ **L'anagrafica è strato macchina e non si vede in `state.md`.** È ADR-0052
applicato a se stesso: un `png_id` non spiega niente a chi legge, quindi non ha
motivo di comparire nella vista. `render_state --check` resta byte-identico
dopo tutto il lotto, ed è la prova che il DM non paga niente per questa chiave.

🔵 **Il passo successivo, già visibile.** Con l'anagrafica in piedi, `stato` e
`reversibile` possono **salire** dalle righe di §3 all'anagrafica — e allora
anche i PNG di §4 ne avranno uno, che è la cosa che D16 aveva chiesto e che si
era dovuta rimandare perché tre righe di §4 non sono persone. Il `tipo`
(`persona` · `gruppo` · `divinita`) esiste già per quel giorno: dice a chi uno
stato vivo si applica e a chi no.

## Riferimenti

- `plans/PIANO-RIPRESA-PR-ABBANDONATE.md` §4.8.10 — il lotto, misure e validazione
- [ADR-0052](ADR-0052-cosa-e-dato-e-cosa-e-prosa.md) — il criterio, e il limite che questo chiude
- [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) — un master, mai due
- `scripts/validate_state.py` (R10, R11, R12) · `scripts/tests/test_anagrafica_png.py`
