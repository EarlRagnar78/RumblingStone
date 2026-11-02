# Giro 3 di ARC-07: le norme nuove applicate ai cinque master

Il DM ha chiesto di riscrivere ARC-07 con tutte le norme diventate standard
con la #246 (`read-aloud-adulti.md` §2-ter, `verdetto_misurato`,
`box_impoveriti`) e di misurare il miglioramento contro le versioni
precedenti. Questo giro parte da main dopo la #251 e tocca 34 box su 120,
più i paragrafi per il DM che `ciclo_prosa segnala` marcava.

## Come si è lavorato

1. **Il campione del cieco è stato congelato prima di riscrivere**
   (`misure/CIECO-CAMPIONE.json`, seme 20261019, cinque box per master). Ne
   sono esclusi i 16 box già votati dal DM nel giro 2, perché il DM li ha
   già visti.
2. **I 16 box votati restano parola per parola** (`misure/CONGELATI.json`,
   estratti da `congelati.py`). Sono la scelta del DM, e questo giro non la
   riapre.
3. **Ogni master è passato da un cancello** (`cancello.py`) che boccia il
   file se un box qualunque perde dettagli sensoriali o spezza un monologo
   rispetto a main (`verdetto_misurato`), se compare un box impoverito
   rispetto a prima della #249 (`box_impoveriti`), se una norma del ciclo o
   il punteggio MQM peggiorano, se cambia un fatto (nomi, numeri, CD) o se un
   box supera le 12 righe. I cinque passano (`misure/CANCELLO-E-VERSIONI.txt`).
4. Il brief chiedeva di lasciare un box com'era quando non si sa dire quale
   norma migliora. Così è andata: 86 box su 120 sono identici. Le note box
   per box di chi ha riscritto sono in `note/`.

## Cosa è cambiato

- **Antitesi «non X: è Y» e trattini lunghi come respiro**, nei box e nei
  paragrafi per il DM: le segnalazioni di `ciclo_prosa` scendono da 37 a 13.
  Le 13 rimaste sono nomi che il tavolo conosce (che §2-ter dice di non
  cambiare in perifrasi) e due tic dentro box votati dal DM.
- **P1 e la frase che spiega**: tolti «vi vede entrare», «l'avete sentita nei
  denti», «lo hanno visto tutti», «Avete riconquistato una testa di ponte»,
  «e nessuno di voi sa dire perché», «capiscono di essere dentro una storia».
- **Monologhi riuniti**: Moradin in A1 e Aegis Fang in A7 (DEF-2), Re Thorek
  al passaggio di consegne (DEF-5) e Thorgrim nella Scena 4 (DEF-4), l'unico
  impoverito che restava contro la versione prima della #249.
- **Mestiere e registro**: «metallo temprato» era sbagliato (la tempra
  raffredda di colpo); via «carta moschicida», «click», «Benvenuti».

## Le cinque versioni a confronto

Misura sui box read-aloud di tutti e cinque i master (`versioni.py`).

| versione | box | parole | mediana | sens. | sens. ‰ | -mente ‰ | 30-70 % | segnalazioni | MQM medio | impoveriti |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| prima del rifacimento | 108 | 7852 | 66,5 | 398 | 50,7 | 0,4 | 48 | 91 | 99,14 | 0 |
| #249 | 128 | 6971 | 54 | 488 | 70,0 | 0,6 | 54 | 23 | 99,98 | 15 |
| #251 | 120 | 7702 | 61 | 509 | 66,1 | 0,5 | 52 | 37 | 99,69 | 1 |
| **giro 3** | 120 | 7710 | 61,5 | **526** | 68,2 | 0,6 | 51 | **13** | 99,70 | **0** |

«Impoveriti» conta i box che, contro la versione prima della #249, hanno meno
dettagli sensoriali o un monologo spezzato. La #249 aveva le segnalazioni più
basse e 15 box impoveriti, e al cieco ha pareggiato: per questo il giro 3 non
scende sotto la #251 sui dettagli e non insegue le segnalazioni a ogni costo.

## Cosa non è migliorato

- **Gli avverbi in -mente restano fuori dalla fascia umana italiana**
  (0,6‰ contro 3,8-13,4‰ del corpus Gruppo Chimera). Il brief chiedeva di
  rimetterli solo dove un autore italiano li scriverebbe, e chi ha riscritto ne
  ha trovato un punto solo. È il limite che resta più lontano dal corpus, e un
  giro che li inserisse per fare numero inseguirebbe l'indicatore.
- **Gulpease e ritmo** scendono di poco in DEF-2 (64,7 → 63,6 e 0,63 → 0,59),
  dove i monologhi riuniti hanno allungato i periodi.
- Il miglioramento è di frase, non di immagine. Chi ha riscritto si aspetta un
  cieco in buona parte pari.

## Il voto cieco

Dei 25 box del campione, 16 sono rimasti identici e non si votano. Delle 9
coppie che restano, la misura ne decide 3 (tutte a favore della versione
nuova, per un dettaglio sensoriale in più) e le manda al cieco come
controllo; le altre 6 le decide il DM. La scheda è `misure/CIECO-SCHEDA.md`;
la chiave, da non aprire prima del voto, è `misure/CIECO-CHIAVE.json`. Si
vota scrivendo `misure/CIECO-VOTI.txt` (una riga per coppia: `N A`, `N B` o
`N =`) e si scioglie con:

```
python3 scripts/cieco_versioni.py esito --chiave plans/esperimenti/giro3-arc07-2026-10-19/misure/CIECO-CHIAVE.json --voti plans/esperimenti/giro3-arc07-2026-10-19/misure/CIECO-VOTI.txt
```

Nove coppie sono poche. Un esito favorevole dice che il giro non ha
peggiorato, non che ha migliorato in modo dimostrato.

## Da rifare

`python3 plans/esperimenti/giro3-arc07-2026-10-19/versioni.py` dalla radice
del repo rifà la tabella sulle versioni nel repo; con una cartella come
argomento aggiunge la riga di quella cartella.

## L'esito del cieco

Il DM ha votato le nove coppie (`misure/CIECO-VOTI.txt`): la versione nuova
ne vince 5, la vecchia 4, nessun pari. La soglia era 7 su 9, quindi il
miglioramento **non è dimostrato**. Dei tre controlli decisi dalla misura,
due sono confermati; il terzo (la Corona che si completa, DEF-5) il DM lo ha
dato alla versione vecchia anche se la nuova aveva un dettaglio sensoriale in
più. Sulle sei coppie indecise è finita 3 a 3.

Come dopo il giro 2, le quattro vecchie vincitrici sono tornate intatte nei
master (l'Affresco A5 in DEF-1, A7 in DEF-2, l'apparizione e la Corona in
DEF-5), e tutti e nove i box votati sono entrati in `misure/CONGELATI.json`:
un giro futuro non li riapre.

La lezione è la stessa della #251: una riscrittura che toglie tic senza
aggiungere immagini arriva al pari. Il controllo perso dice anche che un
dettaglio sensoriale in più non basta, da solo, a far vincere un box.
