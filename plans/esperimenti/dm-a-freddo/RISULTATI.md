# Il DM a freddo, primo passo: la vista di chi scorre sui cinque DEF di ARC-07

Prova del 2026-10-01, L5 di
[`PIANO-AGENT-SKILLS-ESTERNE`](../../PIANO-AGENT-SKILLS-ESTERNE.md) (D2: «parti
da skim e poi vediamo»). Per ogni master `vista_di_chi_scorre.py` ha prodotto
la vista (`DEF-n-VISTA.txt`, dal commit `10127b7`); un agente nuovo, con la
sola vista e il divieto di aprire altro, ha risposto alle quattro domande di
[`dm-a-freddo.md`](../../../skills/rumblingstone-playtest/references/dm-a-freddo.md).
Le risposte intere sono in `RISPOSTE.json`.

## I conti

| Master | Parole della vista | Serata | Chi si oppone | Dichiarazione della serata |
|---|---:|---|---|---|
| DEF-1 | 1.194 | ✓ | Terros sì, **cosa vuole no** | primo paragrafo del Quickstart |
| DEF-2 | 782 | ✓ | **non so**: nessuno in scena, solo il countdown | primo paragrafo del Quickstart |
| DEF-3 | 957 | ✓ | **non so**: pressioni, nessun nemico | primo paragrafo del Quickstart |
| DEF-4 | 1.117 | ✓ | ✓ Zog'tar e Skullcrusher | riquadro *La serata in tre frasi* |
| DEF-5 | 630 | ✓ | **non so**: gli orchi, senza un capo | primo paragrafo del Quickstart |

## Cosa dicono

**La serata si capisce sfogliando, in tutti e cinque.** Nessun agente ha
sbagliato la missione. Il primo paragrafo del Quickstart, che a settembre i
lettori a freddo perdevano negli appunti, chi scorre lo legge: è la prima
prosa che incontra.

**Chi si oppone, no: quattro su cinque.** L'unico master senza «non so» è
DEF-4, l'unico col riquadro, e l'agente cita proprio il riquadro come
l'elemento che l'ha fatto rispondere. È un caso solo e la correlazione non
prova la causa. Va detta però la differenza fra i quattro: in DEF-2 e DEF-3
un avversario in scena non c'è, e l'agente lo dice bene («pressioni non
belliche»), quindi lì `D-AVVERSARIO` non è un buco. In DEF-1 Terros c'è e non
si sa cosa voglia; in DEF-5 gli orchi non hanno un capo. Questi due sono
rilievi veri.

**Il difetto più chiaro era della vista, non dei master.** Tre agenti su
cinque hanno scritto, con parole diverse, «le CD non so a cosa servano»: la
prima versione le elencava nude. Corretto dopo la prova, la vista ora stampa le
quattro parole prima di ogni CD (`test_la_cd_porta_le_parole_prima`). Le viste
salvate qui sono quelle lette, cioè la versione di prima.

**I grassetti non li ha citati nessuno.** I primi quindici di ogni master
vengono dall'intestazione d'apparato («MASTER DEFINITIVO», «Sostituisce e
fonde»). Non hanno guidato nessuna risposta: sono rumore, ma rumore della
vista più che del master.

## Cosa non dice

Non dice se un DM vero, con un'ora, prepara bene la serata: quello è il
secondo passo della rubrica (preparazione a scene) e non è stato fatto. Non
dice nemmeno se un DM umano sfoglia così: l'agente riceve la vista già
estratta, il DM sceglie lui dove fermarsi.
