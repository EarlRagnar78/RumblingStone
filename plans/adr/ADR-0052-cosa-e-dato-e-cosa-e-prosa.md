# ADR-0052 — Cosa è dato e cosa è prosa: il criterio, non la categoria

- **Stato**: accettata (2026-09-16), **attuata** per §1, §2.1 e §3
- **Decide**: dove vive un fatto di campagna, quando `state.yaml` e `state.md`
  contengono tutti e due qualcosa di vero
- **Chiude**: **D14** (dove va la riga del March Clock) e **D16** (i villain
  hanno bisogno di un campo `stato`?)
- **Precede**: ADR-0050 (un master, mai due) — questo ne è la regola d'uso

---

## Contesto

ADR-0050 ha dato ai fatti tabellari un master (`campaign/state.yaml`) e ha reso
le tabelle di `campaign/state.md` una vista generata. Ha detto **che** esistono
due file. Non ha detto **come si decide** in quale dei due finisce un fatto
nuovo, e la domanda si è presentata subito, due volte:

- **D14** — «`**Current March Day:** **19**`» è un numero che la macchina
  aggiorna, ma nel canone di oggi è la **prima riga di un paragrafo di cinque**
  che spiega perché il Giorno 19 è un bersaglio e non un passato. Numero e
  spiegazione erano la stessa riga, e per questo `state_apply --migrate` si
  **rifiutava** di marcarla: sostituendola avrebbe lasciato orfane a metà frase
  le altre quattro righe.
- **D16** — «Regiarix killed» è un fatto che il log di sessione dichiara, ma i
  record `villain` non avevano un campo per riceverlo. Il tool proponeva al DM
  di scriverlo dentro `dove` o `agenda`, cioè di infilare un dato strutturato
  dentro una frase — il difetto che ADR-0050 aveva appena chiuso altrove.

Il DM ha posto la domanda nella sua forma generale: *«in state.yaml ci sono gli
stati di tutte le tabelle, tutto il necessario per PNG e villain in modo da
poter essere recuperato da un LLM o da un algoritmo deterministico; in state.md
la parte che può leggere il DM. Ha senso questa visione? E può essere attuata?»*

## Decisione

**Il criterio non è «dato vs prosa». È: si può sbagliare in silenzio?**

Un fatto va in `state.yaml` quando **un attore diverso da chi l'ha scritto lo
rileggerà per deciderne un altro** — uno script, un agente, il DM sei settimane
dopo. Lì l'errore non si vede: nessuno rilegge un numero per controllarlo, lo
usa. Un fatto resta prosa in `state.md` quando **serve a capire perché** un
altro fatto è quello che è: lì l'errore lo vede chiunque legga, perché il testo
smette di avere senso.

Ne seguono tre regole operative.

1. **Il numero è dato, il ragionamento è prosa, e non condividono una riga.**
   Il March Day va in `march_clock.giorno_corrente`; la nota del DM sta sotto,
   fuori dalla regione generata. Separati, ognuno cambia senza toccare l'altro.
2. **Quel che un trigger di sessione può dichiarare, dev'essere un campo.**
   Se `state_sync` riconosce «X killed», allora esiste un campo che riceve
   quella dichiarazione. Un trigger senza campo è una proposta che il DM deve
   tradurre a mano ogni volta, e tradurre a mano significa tradurre diverso.
3. **Un valore derivabile non si scrive due volte.** «Days remaining» si
   calcola da `giorno_arrivo − giorno_corrente`. Scriverlo è crearne una
   seconda copia che diverge al primo aggiornamento saltato.

### Il campo `stato`, e perché ha un compagno

Enumerazione chiusa: `attivo · latitante · neutralizzato · morto · ignoto`.

- `neutralizzato` copre il caso più frequente al tavolo — sconfitto ma non
  morto: prigioniero, smascherato, privato del suo asso. Senza, il DM sarebbe
  costretto a scrivere `morto` per non scrivere `attivo`.
- `ignoto` è la risposta onesta quando i PG non sanno l'esito, e **si conta**
  (regola R8): un buco contato vale più di un valore indovinato — è la forma
  di ADR-0041, la stessa delle 58 righe senza `tempo`.

E un secondo campo obbligatorio, `reversibile`, appena `stato` non è `attivo`
(regola R9). **In questa campagna un morto torna**: il Ghostlord nasce da un
morto, Sal è protetto da un paradosso auto-consistente, Hella è morta in attesa
del rito. Registrare «morto» senza dire se è definitivo è registrare **meno di
quel che il canone sa**, e chi rilegge il dato non ha modo di accorgersene.

⚠️ **`state_apply` scrive `stato` ma non `reversibile`**, ed è voluto: il primo
è la lettura letterale del log, il secondo è una decisione narrativa. R9 la
chiede al DM alla prima esecuzione successiva, che è il posto giusto per
chiederla.

## Alternative scartate

| | Perché no |
|---|---|
| **Tutto in `state.yaml`, `state.md` solo generato** | La spiegazione del Giorno 19 è di 5 righe con tre riferimenti incrociati e una citazione del DM. Modellarla vorrebbe dire inventare uno schema per contenuto che cambia forma ogni sessione — e il DM smetterebbe di scriverla |
| **Tutto in `state.md`, `state.yaml` derivato** | Non esiste un parser onesto della prosa di canone. È il senso che 4d-1 ha già scartato |
| **`stato` anche su §4 (chi sa cosa)** | Misurato: **tre righe non sono persone** («Druid Circle of the Sacred Forest», «Lathander + Mask», «Tiri Kitor wild elves») e **tre persone compaiono sotto due nomi** (Sonjak, Varis, Zalkatar/Sethrax). `stato` lì vorrebbe dire un valore privo di senso in tre casi e due copie divergenti in altri tre |
| **Duplicare gli statblock in `state.yaml`** | Esistono già, meglio fatti, in `Bestiario/`: **115 statblock validati** e un catalogo di **305 voci**. Copiarli qui ricrea il difetto C2 — due master — che ADR-0050 ha appena chiuso |

## Conseguenze

**Quel che si guadagna.** Il flusso di fine sessione scrive nel master quattro
cose invece di una: March Clock, clock dei villain, morte e fuga. La morte di
Hella esce da una frase (`hp: «n/d finché non torna»`) e diventa un dato che uno
script può leggere — §1 e §6 si erano già contraddetti su questo nel lotto 4c, e
nessun cancello se n'era accorto.

**Quel che si perde.** Due campi in più da tenere veri a ogni sessione. R9 li
pretende, quindi il costo si paga; ed è il punto — un campo che nessuno
controlla è un campo che mente.

🔴 **Il limite dichiarato, e va guardato in faccia.** Un LLM che parte dallo
stato vivo e vuole la scheda di un PNG **non ha una chiave**: si è misurato che
**11 villain su 13** e **23 PNG su 31** si agganciano a `Bestiario/` solo
indovinando la stringa, e che **Zalkatar** e **Saarvith/Regiarix** lì non
esistono affatto. Finché quella chiave non è dichiarata, la visione del DM è
attuata a metà: i fatti sono strutturati, il collegamento fra i due archivi no.
Il lotto successivo è quello — un campo `scheda:` con un cancello che verifica
che il percorso esista — e dovrà anche decidere cosa fare dei due villain senza
scheda, che è contenuto e non infrastruttura.

## Riferimenti

- `plans/PIANO-RIPRESA-PR-ABBANDONATE.md` §4.8.9 — il lotto, misure e validazione
- [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) — un master, mai due
- [ADR-0041](ADR-0041-instradamento-delle-skill-con-un-gate.md) — contare invece di indovinare
- `scripts/dmcore/masters.py` · `scripts/validate_state.py` (R8, R9)
