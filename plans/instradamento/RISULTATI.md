# Instradamento delle skill: le frasi vere del DM, misurate

L8 di [`PIANO-AGENT-SKILLS-ESTERNE`](../PIANO-AGENT-SKILLS-ESTERNE.md), 2026-10-01.
Lo strumento è `scripts/instradamento_skill.py`; i casi sono in `casi.json`.

## Il metodo

Trenta frasi del DM, copiate da `plans/`, `skills/` e `AGENTS.md` dove sono
citate fra «». Per ognuna l'insieme delle skill **obbligatorie** secondo
ORCHESTRAZIONE §4: L0 se tocca il canone, una L1, le L2 che si applicano. Le
L3, L4 e LR non contano, perché non sono obbligatorie. Gli insiemi li ha
scritti l'agente e vanno confermati (D10).

Una skill obbligatoria è **raggiunta** se almeno un trigger fra virgolette
della sua descrizione compare nella frase (intero, o per una parola sola al
plurale o al femminile italiano). Le frasi sono divise a metà: con le
«taratura» si sono scelti i trigger nuovi, le «verifica» non sono state
guardate.

## I conti

| | prima | dopo |
|---|---:|---:|
| omissioni, taratura | 19 su 23 | 5 su 23 |
| omissioni, **verifica** | 19 su 23 | **8 su 23** |
| skill obbligatorie raggiunte senza essere attese | 2 | 7 |
| conflitti fra le due L1 | 0 | 0 |

«Prima» e «dopo» usano lo stesso matcher. Le prime misure, con un matcher che
non staccava le elisioni né riconosceva i plurali, davano 42 su 46: due
difetti dello strumento, corretti prima di toccare le descrizioni.

## Cosa dicono

**Le descrizioni erano scritte per un altro lettore.** I trigger di
`campaign` erano cinque, tutti inglesi tranne il nome del repo; quelli di
`module-standard` erano parole del gergo del repo («master definitivo»,
«consolidamento»), non del DM («modulo», «avventura», «stanze»). Il DM scrive
in italiano e nomina i PG: «Trigger on PC names» c'era, ma senza i nomi.

**Il guadagno regge sulle frasi non usate:** in verifica le omissioni scendono
da 19 a 8. Sulle frasi di taratura scendono di più (a 5), ed è la differenza
che ci si aspetta da una taratura.

**Il prezzo sono le skill in più**, da 2 a 7: «arco» e «PNG» fanno scattare
`campaign` anche su frasi generiche, «prosa» fa scattare `narrative-style` su
una frase che parla della prosa degli archi come di un posto dove cercare. Una
skill obbligatoria in più costa contesto, una in meno costa il difetto
silenzioso di ORCHESTRAZIONE §4; il cricchetto conta solo le seconde.

**Un instradamento sbagliato tolto prima che succedesse.** `narrative-style`
aveva il trigger «documento», che voleva dire il documento *in gioco* (ADR,
Eco). Una frase come «deep audit del documento» l'avrebbe fatta scattare,
cioè la L1 sbagliata. Ora è «documento in gioco».

## Cosa resta

Le otto omissioni in verifica sono frasi che non nominano niente del lessico
della skill: «se le carte si danno prima, i PG sanno tutto» è narrativa e
canone senza una parola chiave. Per quelle un controllo lessicale non basta,
e il tetto non va spinto a zero aggiungendo trigger su misura delle frasi:
sarebbe imparare la prova a memoria.
