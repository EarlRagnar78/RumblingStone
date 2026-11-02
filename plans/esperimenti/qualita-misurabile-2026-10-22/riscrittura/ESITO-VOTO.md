# Esito del voto cieco (2026-10-22, 07:15)

> Correzione delle 11:25: B08 l'ha vinto la catena nuova, non la vecchia (la tabella diceva 9 a 4, il conto giusto è 8 a 5). Lo spezzare le subordinate quindi non ha perso 2 su 2, ma 1 a 1.

Voti del DM in `cieco/VOTI-1.txt` e `cieco/VOTI-2.txt`, sciolti con `cieco_versioni.py esito`.

- **Parte 1, catena vecchia (V) contro nuova (N)**: V 8, N 5, pari 1 su 14 (soglia 10). La catena nuova **non** è migliore. Etichette: N perde 2 volte per «ritmo», V 1 volta.
- **Parte 2, fusione (F) contro originale (O)**: F 2, O 1 su 3. Non dimostrato.

## Box per box, con ciò che ciascun arm ha cambiato

| Box | Vince | V ha cambiato | N ha cambiato |
|---|---|---|---|
| B01 | V (N «ritmo») | «c'è una colonna che geme» | complemento spostato per un falso del parser |
| B02 | V (N «ritmo») | «ci sono piattaforme» | avverbio spostato per un falso del parser |
| B03 | V | «c'è» | stare+gerundio tolto, soggetto chiarito |
| B04 | pari | niente (nomi rimessi da `confronta_fatti`) | niente |
| B05 | N (V «ritmo») | solo «c'è» | niente: N è l'originale |
| B06 | V | solo «c'è» | niente: N è l'originale |
| B08 | N | niente: V è l'originale | subordinata spezzata in frase sua |
| B09 | V | gerundi in coda, «c'è» | gerundi in coda, subordinata spezzata, tolta una frase («spiega») |
| B10 | V | stare+gerundio | soggetto dopo il verbo ×2, stare+gerundio, quattro ritocchi LAMP |
| B11 | N | niente: V è l'originale | soggetto dopo il verbo ×2 |
| B12 | N | maiuscole, stare+gerundio, dislocazione | maiuscole, stare+gerundio, «potete vedere» tolto (inglese) |
| B13 | N | possessivo, gerundio, dislocazione | gerundio, «disperatamente» tolto (ricercata), «ora nell'ora» (goffo) |
| B14 | V | stare+gerundio, gerundio, «ci sono» | gli stessi più tolta la frase «terrificante e magnifico» («spiega») |
| B16 | V (= originale) | niente | soggetto dopo il verbo, tolta la chiusa sull'eroe leggendario («spiega») |

## Cosa dice per ogni intervento

I casi sono pochi (da 1 a 4 per intervento): sono indizi, non prove.

| Intervento | Catena | Esito nei voti | Decisione |
|---|---|---|---|
| Riscrivere su un falso del parser (spaCy) | N | perso 3 su 3 (B01, B02, B10) | ogni rilievo di `misura_sintassi` si conferma a occhio prima di riscrivere |
| Spezzare le subordinate oltre due livelli | N | vinto B08 puro, perso B09 insieme ad altro | non è un rimedio automatico: si spezza solo dove al terzo livello l'orecchio si perde (calibrazione: la versione con più subordinate vince 11 su 12) |
| LAMP «spiega»: tagliare la frase che spiega | N | perso 4 su 4 (B09, B10, B14, B16) | tolta dalla checklist di riscrittura: il DM tiene le chiuse enfatiche |
| LAMP «goffo», «inglese», «ricercata» | N | vinto 2 su 3 (B12, B13; perso B10) | si tiene come checklist |
| Soggetto dopo il verbo (calco vero) | N | vinto B11 puro; perso B10 e B16 insieme a «spiega» | si tiene come norma di riscrittura |
| «c'è» presentativo (`--costrutto-italiano`) | V | vinto B06 puro, perso B05 puro, presente in 6 vincitori | resta com'è: non è dannoso |
| Dislocazione | V | perso 2 su 2 (B12, B13), insieme ad altro | da rivedere al prossimo giro |
| Tetto dei nomi distinti | V | nessun effetto: 6 riscritture su 6 annullate da `confronta_fatti` | da togliere (decisione del DM, `specifiche-qualita.yaml`) |
| Stare+gerundio, gerundio in coda | V e N | entrambi gli arm, nessuna differenza | si tengono |

## La catena che diventa standard

È la fusione: la catena vecchia, più il soggetto dopo il verbo e le etichette LAMP «goffo», «inglese», «ricercata», meno il tetto dei nomi. Restano fuori dalla riscrittura: i rilievi di spaCy non confermati, lo spezzare le subordinate come rimedio automatico, il taglio delle frasi che «spiegano».
