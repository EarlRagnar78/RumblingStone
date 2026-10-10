# ADR-0083 — L'asse delle chiusure si ricava dai vicini

- **Stato**: **accettata** e attuata (il DM, il 2026-10-08, sera: D13, D14, D15 di [PIANO-COLLAUDO-E-GENERAZIONE-MAPPE](../PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md))
- **Data**: 2026-10-08
- **Decisori**: DM (Gianfranco Samuele), agente
- **Rapporti**: completa [ADR-0082](ADR-0082-la-mappa-si-collauda-come-grafo-prima-che-come-immagine.md) §8 (la regola di posa diceva *dove* sta una chiusura, non *come*); legge la legenda di [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md); rispetta [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) e la regola 5 di `rumblingstone-mapmaking` (niente arte di terzi); [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) per le mappe già decise dal DM

## Contesto

Il DM, la sera della #226: *«gli oggetti tipo porte e grate o celle devono
essere orientati nel modo giusto. C'è un algoritmo che può controllarle […]
in maniera deterministica, migliorando la resa e risolvendo i problemi che
trova?»*. Nello stesso messaggio: guardare gli asset di *Battle for Wesnoth*
per la legenda, e usarli solo se sono migliori.

Una griglia emoji non dice in che verso sta una porta. `🚪` è lo stesso
carattere in un muro est-ovest e in uno nord-sud. Misurato il 2026-10-08 sulle
44 mappe del corpus (`plans/esperimenti/orientamento-e-dipendenze-2026-10/`),
le 125 chiusure (tutte `🚪`: i simboli nuovi della #226 non li usa ancora
nessuna mappa) si dividevano così, e tre programmi davano tre risposte:

| Chi | Come decideva | Sbagliate |
|---|---|---|
| `render_map_svg.py` | non decideva: ogni glifo disegnato come in un muro est-ovest | **36 su 96** chiusure con un asse, disegnate di traverso |
| `export_uvtt.py` | «muro sopra *o* sotto» = muro nord-sud | **13 portali su 96** girati in Foundry e Roll20: tutti in file di porte, dove un muro sta da un lato solo |
| `collaudo_mappe.py` | calcolava l'asse in `_nel_muro` per sapere se la porta stava nel muro, poi lo scartava | nessuna, ma il dato non usciva |

Le altre 29 chiusure: 27 senza muro intorno (le viste d'insieme di Hammerfist
e i portoni del Drappo, già noti ad ADR-0082) e 2 ambigue, un portone 2×2 sul
bordo nord del Portale.

**Wesnoth.** Guardato file per file prima di proporre: il codice è GPL-2.0+,
l'arte vecchia GPL-2.0+ e quella nuova CC BY-SA 4.0, senza un elenco dei
crediti per immagine (`copyrights.csv` copre 396 file audio e nessuna
immagine), quindi la licenza di un PNG si ricostruirebbe dalla storia git.
Tecnicamente sono PNG 72×72 in vista obliqua per una griglia di esagoni, con
l'orientamento nel nome del file (`gate-rusty-se`, `gate-rusty-sw`): non si
innestano su una griglia quadrata zenitale vettoriale. E il corpus non ne
chiede: le 13 legende locali inventano stalagmiti, cristalli e i PG, niente che
Wesnoth abbia e la legenda no. La cosa che Wesnoth fa meglio non è un'immagine:
le sue regole di terreno scelgono la variante di un muro o di un cancello
guardando le tessere vicine. È la stessa domanda dell'orientamento.

## Decisione

1. **Una funzione, tre lettori.** `scripts/dmcore/chiusure.py` dà l'asse di
   ogni tessera con `posa: nel_muro` o `recinto` (porte, grate, finestre,
   sbarre). Il collaudo lo riporta, il renderer gira il glifo, l'export UVTT
   mette il portale lungo il muro. Nessuno dei tre ha più una regola sua.

2. **La regola, sui quattro vicini.** Un lato «continua il muro» se è il
   bordo, muratura vera (blocca movimento e vista e non è un varco) o
   un'altra chiusura; «si attraversa» se non blocca il movimento o è una porta.
   - muro a ovest e a est, e un passaggio a nord o a sud → **EO**, il glifo
     com'è disegnato;
   - il caso ruotato → **NS**, il glifo ruotato di 90° sul centro della cella;
   - entrambe le letture valgono → decide da che parti si passa davvero; se
     non decide neanche quello → **ambiguo**;
   - nessun muro → nessun asse (è già l'errore `posa/nel-muro` di ADR-0082).

   La regola non sa dov'è il nord: ruotare la griglia di 90° scambia EO e NS,
   specchiarla li lascia uguali. I test lo provano su 2.000 griglie a caso con
   un seme fisso.

3. **`@verso <cella> ; NS|EO` per i casi che i vicini non decidono.** È una
   direttiva della famiglia di `@north` e `@collega`, che il DM scrive solo
   dove il collaudo dice `posa/asse-ambiguo`. Vince sui vicini. Senza, un caso
   ambiguo si disegna come oggi (EO).

4. **Tre rilievi nuovi nel collaudo.** `posa/asse-ambiguo` (A),
   `posa/verso-contro-muri` (A: la direttiva dice un asse, i muri l'altro, forse
   un errore di battitura), `posa/verso-illeggibile` (E, peso 1: una direttiva
   che non si legge, o su una cella senza chiusura). Il rapporto JSON conta gli
   assi di ogni mappa nel campo `chiusure`.

5. **Wesnoth entra come idea, non come file.** Nessun PNG, nessun simbolo
   nuovo. L'idea delle regole di terreno è riscritta dalla descrizione per una
   griglia quadrata; il codice di Wesnoth non è stato letto né copiato.

6. **Gli SVG derivati si rigenerano, i master no.** Il cambio del renderer
   tocca 13 SVG: 10 del corpus, fra cui 4 delle mappe D28 della #225, e 3
   dell'archivio di Hammerfist. Nessuna griglia cambia: cambia il disegno di una
   porta che era già lì. Per le mappe D28 l'ha deciso il DM (D13) sapendolo.

## Alternative scartate

| Alternativa | Perché no |
|---|---|
| Un simbolo per verso (`🚪` e una porta «verticale») | raddoppia ogni chiusura nella legenda, e chi scrive la griglia deve indovinare il verso a mano, che è proprio l'errore da togliere. Il verso è un dato che i vicini contengono già |
| Importare i PNG di Wesnoth | raster obliqui su esagoni; e la GPL o la CC BY-SA passerebbero allo SVG che li contiene, e al PDF che contiene lo SVG, su mappe derivate da *Red Hand of Doom* che non si possono rilicenziare (ADR-0005) |
| Ridisegnare in casa i concetti di Wesnoth che mancano (pozzo d'acqua, balla di fieno, cerchio rituale, barca) | il DM l'ha scartato (D15): nessuna mappa li chiede oggi. Si riapre quando un master ne inventa uno in una legenda locale |
| Solo il collaudo, senza toccare renderer e UVTT | lascerebbe 36 porte disegnate di traverso e 13 portali girati in un VTT, sapendolo |
| Correggere nel collaudo e scrivere il verso nel master | il master non ha dove scriverlo se non con una direttiva per ogni porta: 125 righe per dire ciò che i vicini dicono già |

## Le conseguenze

**Cosa si ottiene.** Le porte nei muri nord-sud si leggono come porte e non
come travi di traverso nel corridoio (confronto a vista sulla Fucina Grande,
M7-F). In Foundry e Roll20 i 13 portali sbagliati chiudono il muro giusto. Il
collaudatore a freddo ha nel rapporto il conto degli assi, e un caso ambiguo
diventa una domanda al DM invece di un'immagine che sembra sbagliata.

**Quello che si paga.**

- Una direttiva in più nel formato, registrata come norma
  ([`REGISTRO-NORME-EDITORIALI`](../../skills/REGISTRO-NORME-EDITORIALI.md), G3).
- Tredici SVG rigenerati in un colpo, tre dei quali in `_ARCHIVIO/`. È un
  derivato, e il precedente è ADR-0070 (41 SVG rigenerati per una didascalia),
  ma un diff di tredici file grafici in una PR non si rilegge a mano: lo si
  rilegge con `validate_maps.py` e con i ritagli prima e dopo.
- `dmcore/chiusure.py` legge `legend.json` come gli altri, quindi un simbolo
  nuovo con `posa: nel_muro` ha l'asse senza toccare il codice. Un simbolo
  nuovo disegnato in verticale, invece, verrebbe girato al contrario: i glifi
  delle chiusure **si disegnano per un muro est-ovest**, ed è una regola che
  `stile` di `legend.yaml` non dice ancora.

**Cosa resta fuori.** Le scale (`🔼`, `🔽`) hanno anche loro un verso, la
direzione in cui si sale; il DM ha chiesto porte, grate e celle, e le scale
restano come sono. Le 27 porte senza muro restano errori `posa/nel-muro` da
correggere col DM (V3).
