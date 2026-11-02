# La pipeline migliora_prosa: scegliere una riscrittura e misurare se è migliore

Il DM ha chiesto se la pipeline può restituire una prosa migliore e misurare il
miglioramento. Il giudice di «migliore» resta il suo voto cieco (ADR-0093):
nessuna misura automatica lo prevedeva ([ricerca](../../../RICERCA-QUALITA-MISURABILE-2026-10.md) §3).
Questa cartella prova a costruirne una sui voti già dati, e prepara il voto che
dice se la pipeline vince.

Lo script è [`scripts/migliora_prosa.py`](../../../../scripts/migliora_prosa.py). Le
candidate le scrive un agente seguendo `rumblingstone-narrative-style` e
`read-aloud-adulti.md` §2-ter; lo script non chiama modelli linguistici.

## I file

| File | Cosa contiene | Nel repo |
|---|---|---|
| `SOGLIA.txt` | modello, tratti e soglia, scritti prima di addestrare | sì |
| `VOTI.json` | le 55 coppie votate alla cieca (giro 2: 16, giro 3: 9, prova del 21: 13, riscrittura del 22: 17, di cui una pari), con testo vincente, perdente, originale ed etichette | sì |
| `MODELLO.txt` | l'uscita di `migliora_prosa.py modello` | sì |
| `prova-1/BOX.json` | i sei box scelti per la prima prova, col testo originale | sì |
| `cieco/SCHEDA-CIECA.md` | la scheda per il DM: sei coppie, vincitrice della pipeline contro originale | sì |
| `prova-1/candidate/P0N.md` | le quattro candidate scritte per ogni box | **dopo il voto** |
| `prova-1/SCELTE.json` | filtro e punteggio di ogni candidata, e la vincitrice | **dopo il voto** |
| `chiave/CHIAVE.json` | quale lettera è la pipeline | **dopo il voto** |

Le candidate e le scelte dicono quale testo è nuovo, quindi aprono la chiave
quanto la chiave stessa: entrano col commit che registra il voto.

## Il modello

Regressione logistica senza intercetta sulle differenze di undici tratti fra le
due versioni di una coppia, penalità L2 fissa. I tratti sono le misure del repo
(dettagli sensoriali, gerundi in coda e avverbi in -mente di `misura_craft
--stile`, Gulpease, possessivi, `livelli_max` di `misura_sintassi`, MATTR,
lunghezza) e quattro regole di §2-ter misurate rispetto all'originale: frase
finale tolta, subordinata spezzata, nomi propri tolti, monologo spezzato.

Validazione in leave-one-out sulle 54 coppie decise (con spaCy):

| | giuste | accuratezza | Wilson 95% |
|---|---:|---:|---|
| modello | 33 su 54 | 0,611 | 0,478-0,730 |
| «vince la più lunga» | 28 su 54 | 0,519 | 0,389-0,646 |
| caso | | 0,500 | |

**Il modello non supera la soglia**: il limite inferiore di Wilson resta sotto
0,50 (test del segno p = 0,13). Fa meglio della regola banale, ma con 54 coppie
la differenza dal caso non è dimostrata. Quindi ordina le candidate solo come
suggerimento; la pipeline vale come filtro di non regressione e come
raccoglitore di voti, e ogni voto nuovo rientra nel modello.

Che cosa preferisce, coi pesi addestrati su tutte le coppie: la versione con
più possessivi (il peso più forte, lo stesso segnale della calibrazione), più
gerundi in coda e avverbi in -mente, più Gulpease, più dettagli sensoriali e più
livelli di subordinate; perde la versione che spezza una subordinata o un
monologo. Le regole di §2-ter vengono in parte da questi stessi voti, quindi i
loro pesi sono letti sui dati che le hanno suggerite.

⚠️ Il peso sui possessivi va contro `italiano-nativo.md` §1 (niente possessivo
sul corpo). Nella prima prova ha dato punteggi bassissimi a tutte le
riscritture di P05, il box di ARC-08 pieno di «la sua armatura», «le sue
teste»: la pipeline ha scelto la candidata che ne toglieva meno. Il voto dirà
chi ha ragione.

## La prima prova

Sei box di ARC-07 e ARC-08 scelti con `scegli --seme 20261023`: almeno 25
parole, non note di regola, non fra i 25 congelati del giro 3, non nel campione
della riscrittura, non già votati. Per ognuno quattro candidate con fatti, nomi
e numeri invariati. Il filtro ne ha scartate due (P04, regola 4: subordinata
spezzata); fra le altre il modello ha scelto la vincitrice, e `campione --seme
20261024` ha scritto la scheda. Tutte e sei le coppie vanno al DM: la misura
non ne decide nessuna.

Dopo il voto (righe `N A`, `N B` o `N =` in `cieco/VOTI.txt`):

    python3 scripts/migliora_prosa.py esito \
        --scelte plans/esperimenti/qualita-misurabile-2026-10-22/pipeline/prova-1/SCELTE.json \
        --chiave plans/esperimenti/qualita-misurabile-2026-10-22/pipeline/chiave/CHIAVE.json \
        --voti plans/esperimenti/qualita-misurabile-2026-10-22/pipeline/cieco/VOTI.txt

Registra le sei coppie in `VOTI.json`, rifà il modello e dice quante volte la
pipeline vince, con Wilson. Con sei coppie l'intervallo resta largo: la prova
dice se la pipeline peggiora, non ancora se migliora.

## Una correzione all'esito della riscrittura

Ricostruendo i voti dalla chiave, la coppia B08 della parte 1 (V contro N)
l'ha vinta **N**: `CHIAVE-V-N.json` dà N in A e il voto è `8 A`, e il testo A
della scheda è quello di N («Provi a girare la testa: di chi sono?»). Il conto
8 a 5 di [`ESITO-VOTO.md`](../riscrittura/ESITO-VOTO.md) torna con B08 a N, ma
la tabella la dà a V, e la riga «spezzare le subordinate: perso 2 su 2 (B08
puro, B09)» diventa 1 su 2. È anche la regola 4 di `read-aloud-adulti.md`
§2-ter («ha perso tutte e due le volte»). Qui `VOTI.json` segue la chiave; la
correzione dei due documenti è da decidere.

## LanguageTool, Stanza e perplessità (2026-10-23)

La prova di [`../languagetool/`](../languagetool/README.md) ha aggiunto alla
pipeline LanguageTool 6.8 in locale, come filtro facoltativo (`migliora --lt`),
e ha confrontato in leave-one-out le varianti del modello con i tratti di
LanguageTool, di Stanza e della perplessità. Nessuna batte il base (McNemar
appaiato, soglia scritta prima): il modello resta quello di undici tratti, e
il filtro LT non scarta nulla perché nessun gruppo di rilievi arriva a 0,70 di
precisione.

## Il voto della prima prova (2026-10-23)

Il DM ha votato le sei coppie: `1 B`, `2 =`, `3 A`, `4 A`, `5 A`, `6 B`
(`cieco/VOTI.txt`). Con la chiave:

| Coppia | Box | Vince | Il modello, addestrato prima sui 55 voti vecchi |
|---|---|---|---|
| 1 | P01, ARC-07 DEF-4, il bosco al tramonto | pipeline | pipeline, 0,61 |
| 2 | P02, le rune di Hald | pari | — |
| 3 | P03, la Corona e i due draghi | pipeline | pipeline, 0,88 |
| 4 | P04, l'Aura della Forgia | pipeline | pipeline, 0,59 |
| 5 | P05, ARC-08, l'alba dell'assedio | **originale** | originale, 0,94 |
| 6 | P06, Borin Ferropugno | pipeline | pipeline, 0,67 |

La pipeline vince 4, l'originale 1, pari 1: Wilson 95% [0,30-0,90], sotto la
soglia di `cieco_versioni` (5 su 6). **Che la pipeline migliori la prosa non è
dimostrato.**

Il modello, invece, ha passato due prove. **In prospettiva**: addestrato sui 55
voti di prima, senza vedere questi, ha indovinato 5 coppie decise su 5, compresa
l'unica che il DM ha dato all'originale (p = 1/32 = 0,03 sotto il caso). **In
leave-one-out** sulle 59 coppie decise: 39 giuste, 0,661, Wilson [0,534-0,769],
contro 0,508 della più lunga. Supera la soglia di `SOGLIA.txt`, scritta prima
di addestrarlo, senza cambiare né tratti né parametri.

Conseguenza, come dice `SOGLIA.txt`: il modello diventa misura automatica.
`migliora` ora tiene l'originale quando anche la migliore candidata ha meno di
0,5 contro di lui; con questa regola P05 non sarebbe andata al cieco.

Tre cautele restano vere:

- le regole 1-4 di §2-ter vengono in parte da questi stessi voti, e il
  leave-one-out non lo corregge (la prova in prospettiva sì, ma sono 5 coppie);
- il limite basso di Wilson è a 0,534: altri dieci voti sfortunati lo
  riportano sotto. `esito` lo rimisura a ogni voto;
- **il peso più forte resta quello dei possessivi** (+0,76), e P05 è proprio il
  box pieno di «la sua armatura», «le sue teste» che il DM ha preferito alle
  riscritture che li toglievano. È la seconda volta (dopo la calibrazione,
  p = 0,057) che i voti ciechi vanno contro `italiano-nativo.md` §1 sul
  possessivo. Se la norma vada ammorbidita lo decide il DM.
