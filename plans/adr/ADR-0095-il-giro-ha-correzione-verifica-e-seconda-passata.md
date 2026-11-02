# ADR-0095 — Il giro delle letture ha correzione, verifica e seconda passata

**Stato**: proposta
**Data**: 2026-10-18
**Decisione-fonte**: richiesta del DM del 2026-10-18 nel thread di PIANO-MASTER-DEF («controlla cosa hanno aggiunto ai vari giri che non è ancora diventato standard»); audit in `plans/esperimenti/a3-arc08/AUDIT-GIRI-STANDARD-2026-10-18.md`

> Il numero 0093 è preso dalla PR #246 senza prenotazione; questo ramo prende
> 0094.

## Contesto

I due giri su ARC-07 del 2026-10-18 (PR #245 e #249) hanno fatto più di quanto
dice «Il giro» di `rumblingstone-module-standard`. Dopo le quattro letture c'era
un correttore con esiti scritti, un verificatore nuovo che rileggeva il master
corretto, e una seconda passata. Il verificatore ha trovato 25 correzioni
parziali e 3 🟠 nuovi. Le stesse sessioni hanno usato domande del developer che
la rubrica non ha, e due di queste hanno trovato i 🔴 del secondo giro. Niente
di questo era scritto, quindi il giro su ARC-08 lo avrebbe rifatto solo chi
ricordava.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| Scrivere nelle skill le pratiche che hanno trovato difetti veri | il giro dopo le fa senza che nessuno le ricordi; le norme entrano nel registro | il giro costa due letture in più per master |
| Lasciarle nei README dei giri | nessuna modifica alle skill | è il caso che AGENTS.md G3 descrive: una norma che nessuno legge sparisce |
| Renderle cancelli | si misurerebbero | sono giudizi di un agente, e un cancello su un giudizio è rumore (ADR-0073) |

## Decisione

Il giro ha otto passi invece di cinque: correzione con quattro esiti, verifica
di un agente nuovo e seconda passata. Il canone giocato si legge dal ramo di
gruppo, e le mappe si correggono in tutte le loro copie. Il developer ha le
quattro domande della §17 e un codice fisso per i rilievi. I numeri dei master
si verificano sui mirror dell'SRD con il criterio di `RULES-VERIFICATION.md`.

Le norme stanno in `rumblingstone-module-standard/SKILL.md` («Il giro»),
`rumblingstone-playtest/SKILL.md` §7-bis, `sviluppo-degli-incontri.md` §17 e
«Come si scrive un rilievo», `campaign-coherence.md`, `collaudo-mappe.md` e
`RULES-VERIFICATION.md`. Sono registrate come 🔴 con la ragione.

## Conseguenze

- Il giro su ARC-08 è il primo che parte con lo standard scritto.
- Ogni master costa due letture di agente in più per giro.
- Le norme restano non misurate. Lo strumento più vicino è
  `registro_letture.py`, che oggi non registra né le letture sul master intero
  né il developer.

**Da rivedere se**: dopo il giro su ARC-08 la verifica non trova parziali né
nuovi in nessun master. Allora il passo costa più di quanto rende.
