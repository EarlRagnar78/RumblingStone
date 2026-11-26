# Cieco A · il ritmo della frase (2026-11-19)

La domanda: le frasi brevi del repo (mediana 11-15 parole per frase nei box di ARC-07, 08 e 09) reggono contro il ritmo più lungo delle case (16-18: Dragons' Lair 16, Chimera 17, Paizo 18)? Lo scostamento non l'ha mai scelto nessuno (`plans/RICERCA-PROSA-PECULIARE-2026-11.md` §3.4); questo cieco dice se tenerlo, toglierlo o lasciarlo com'è.

## Come si vota

1. Apri `SCHEDA-A.md`. Per ogni coppia leggi **ad alta voce** A e poi B, come al tavolo.
2. In `VOTI-A.txt`, accanto al numero, scrivi `A`, `B` o `=`. Se vuoi, aggiungi un'etichetta su cosa non andava nell'altra (`ritmo`, `goffo`, `struttura`, `piatta`…).
3. **Non aprire `chiave-non-aprire/`** prima di aver votato tutto: dentro ci sono la chiave e i testi, e basta uno sguardo per sapere quale versione è quale.

Poi il voto si scioglie con:

    python3 scripts/cieco_versioni.py esito --chiave chiave-non-aprire/CHIAVE-A.json --voti VOTI-A.txt

> Nota del 2026-11-26, dopo il voto: nel repo la chiave e i voti stanno tutti
> in questa cartella, senza `chiave-non-aprire/`. Dalla radice del repo il
> comando è:
>
>     python3 scripts/cieco_versioni.py esito --chiave plans/esperimenti/prosa-cieco/ritmo-2026-11-19/CHIAVE-A.json --voti plans/esperimenti/prosa-cieco/ritmo-2026-11-19/VOTI-A.txt
>
> Il resto di questo file è com'era prima del voto.

## Com'è costruito (scritto prima del voto)

- **Campione**: `cieco_versioni.py campione`, seme 20261119, 5 box per file da sette file di ARC-08 e ARC-09 (34 box). Prima dell'estrazione delle 24 sono stati tolti i 4 box che non sono voce del narratore (una nota per il DM e tre battute o monologhi di PNG; il monologo è uso della casa, card del 19/11). Delle 30 rimaste ne restano 24, estratte con lo stesso seme. Niente ARC-07: la serata di venerdì e i box congelati restano fuori.
- **Due versioni, entrambe riscritte**: nessuna delle due è il testo del repo, così non si riconosce l'originale. Cambia **solo** la lunghezza delle frasi: la versione breve ha mediana 11 parole per frase, la lunga 16. Stesse parole dove si può, stessi nomi, stessi sensi, stessi -mente. Lunghezza totale entro il 10% in ogni coppia (1.546 contro 1.604 parole in tutto). L'**ultima frase è identica** nelle due versioni (prima del «Che fate?», dove c'è), perché la chiusa non decida il voto. Al massimo due livelli di subordinate, niente parentesi, niente trattini lunghi, niente punto e virgola. Correzioni uguali in tutte e due dove l'originale violava una norma: «sembra», le maiuscole d'enfasi, i «3 secondi reali».
- **Ordine**: A e B a caso, seme 1119 di `coppie`. La versione lunga è la «nuova» per lo strumento.
- **Quattro coppie di controllo**, a caso col seme: in ognuna una versione ha **un dettaglio sensoriale in meno** (due volte la breve, due la lunga). Lì la misura del primo cieco dice già chi vince; se ne contraddici più di una, `esito` non si fida della misura e lo dice.
- **Il criterio, prima del voto**: sulle 20 coppie non di controllo, se la lunga vince **14 o più**, il ritmo delle case entra nei testi nuovi e lo scostamento si corregge. Se la breve vince 14 o più, le frasi brevi diventano una caratteristica del repo con prova, e vanno in `editorial-standards.md` §4-bis. In mezzo, nessuna delle due è meglio all'orecchio: non si tocca niente e non entra niente.

## I limiti, prima del voto

- In 4 coppie (12, 22, 23, 24 del campione grezzo) la battuta di un PNG è identica nelle due versioni e pesa più della metà del box: lì la differenza è piccola e il pari è probabile.
- Il ritmo delle case è misurato su box inglesi (Paizo) e su due editori italiani di traduzioni (Chimera, Dragons' Lair): la mediana 16-18 è un ordine di grandezza, non un obiettivo preciso.
- La differenza fra 11 e 16 parole per frase è sottile per costruzione: è quella che c'è davvero fra il repo e le case. Se all'orecchio non si sente, è anche quello un risultato.
