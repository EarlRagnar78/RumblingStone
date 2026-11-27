# ADR-0107 — Chi si incontra sta nel capitolo dove lo si incontra

**Stato**: accettata (2026-11-03, il DM: *«quello che migliora in modo che sia std e non solo ricerca»*)
**Data**: 2026-11-03
**Decisione-fonte**: il DM (Jfs), dopo la serata del 2026-11-02 con il booklet di *Notte e Alba*:
*«per ogni capitolo accanto alla scheda una descrizione, una sua immagine e chi è e cosa vuole credo sia il minimo standard sindacale da adottare, e poi lo leggi da DM»*; e il 2026-11-03: *«voglio che aggiungi anche l'appendice con le schede perché erano fatte bene»*.
**Rapporti**: emenda il punto 7 di [ADR-0105](ADR-0105-ogni-creatura-esce-nello-stesso-riquadro.md) (il riquadro intero solo in appendice); usa la scheda d'entrata di [ADR-0073](ADR-0073-chi-e-dove-sta-scritto-nella-scena.md), il dossier di [ADR-0091](ADR-0091-la-scheda-del-png-ha-una-forma.md) e le piante di stampa di [ADR-0106](ADR-0106-ogni-mappa-si-stampa-in-pianta.md). Ricerca e misure in [RICERCA-USABILITA-AL-TAVOLO-2026-11](../RICERCA-USABILITA-AL-TAVOLO-2026-11.md).

## Contesto

La serata del 2026-11-02 cominciava dal capitolo VII, il barile sulla tenda
di Zog'tar. Il capitolo cita Zog'tar 60 volte e non dice com'è, chi è o cosa
vuole; la sua scheda d'entrata col ritratto sta nel capitolo IV, i suoi numeri
in appendice, le mappe M7-C e M7-H nell'Appendice D del capitolo IV. I
validatori erano verdi. Il DM ha dovuto cercare.

La misura sui dieci booklet del DM (`misura_standard_tavolo.py`, 2026-11-03):
su 145 coppie capitolo × persona, 6 hanno numeri, aspetto, ritratto, chi è,
cosa vuole e tattica insieme; i numeri stampati nel capitolo sono 0 su 145
(tutti in appendice, per ADR-0105 §7); la riga «chi è» c'è nel 6%; la mappa sta
nel capitolo dello scontro in 7 casi su 41.

La ricerca dice la stessa cosa da fuori: Paizo mette la scheda intera di un PNG
unico dove si combatte la prima volta, col ritratto accanto; l'Alexandrian
chiede una scheda della persona a voci (aspetto, come si interpreta, cosa sa,
statistiche) proprio perché il dettaglio sepolto in un paragrafo si perde al
tavolo; Questing Beast chiede che tutto quello che serve per un argomento stia
su una doppia pagina.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Nel capitolo i sei elementi della persona e la mappa dello scontro; l'appendice con tutti i riquadri resta** (scelta, come ha chiesto il DM) | al tavolo non si gira pagina; il capitolo si può stampare da solo; l'appendice resta l'indice di tutte le creature, «fatta bene» | più pagine; lo stesso riquadro stampato due volte |
| Solo l'appendice, come oggi (ADR-0105 §7, modello WotC) | pagine corte, un riquadro solo | è quello che al tavolo non ha funzionato |
| Scheda intera alla prima comparsa nel volume, poi «vedi p. N» (modello Paizo) | meno ripetizioni | i nostri capitoli si riusano in più volumi (il DEF-4 è in tre booklet) e la serata parte dal capitolo che serve, non dal primo: «la prima comparsa» cambia da un volume all'altro e il rimando torna a far girare pagina |
| Un capitolo «cast» con tutte le persone (la lista avversari dell'Alexandrian, la cassetta del Drappo) | una pagina da tenere aperta | è un'altra appendice: il problema era cercare fuori dal capitolo |

Il rischio della copia doppia è che le due copie divergano. Non succede se il
riquadro del capitolo e quello dell'appendice escono dallo stesso recinto
` ```statblocco ` del master: il generatore li stampa, nessuno li riscrive.

## Decisione

1. **In ogni capitolo dove una persona si incontra** (un PNG o un cattivo con
   un nome: ci parla, ci combatte, ci si nasconde), accanto alla sua scheda
   stanno:
   - **Chi è**: una riga, il suo ruolo in questa storia;
   - **Aspetto**: una o due frasi, da leggere quando la vedono;
   - **Vuole**: cosa vuole, e cosa teme;
   - **Ritratto**: la sua immagine, con la regola di quando mostrarla;
   - **Numeri**: il riquadro intero di ADR-0105;
   - **Tattica**: quella di questo incontro.

   La scheda d'entrata di ADR-0073 prende la riga **Chi è** come prima voce;
   le altre (Suona, Sa, Eco) restano.
2. **L'appendice resta**: tutti i riquadri, in ordine di nome, come la fa oggi
   `appendice-creature`. Il manifest dice `"schede": "entrambe"` (il valore e
   il tema sono quelli della PR #305, dove la stessa creatura in appendice
   esce una volta sola); `"appendice"` e `"qui"` restano per i volumi che li
   vogliono.
3. **La mappa dello scontro sta nel capitolo dello scontro**, in pianta di
   stampa (ADR-0106), con la legenda. Se la stessa mappa serve in due
   capitoli, si stampa in tutti e due.
4. **Le creature senza nome** (guardie, wyvern, mostri) hanno nel capitolo i
   numeri e la tattica; chi è e cosa vuole non servono.
5. **Un capitolo preso da un altro master** porta con sé le persone che ci si
   incontrano: il generatore le prende dal master e le mette nel capitolo,
   così il capitolo del barile ha Zog'tar anche se la sua scheda d'entrata è
   scritta nella Scena 7. Lo fa `dmcore.chi_si_incontra` quando il manifest
   dice `"chi_si_incontra": true`: la riga **Chi è** dal titolo della scheda
   d'entrata se manca, il riquadro (con la tattica) spostato accanto alla
   scheda se sta in un'appendice dello stesso capitolo o copiato se sta in un
   altro master, la scheda portata dove la riga **In scena … Chi:** la nomina
   (o in testa al capitolo, se il capitolo non ha quelle righe e la nomina
   almeno 10 volte), le mappe nominate e stampate lontano copiate dopo il
   paragrafo «**Mappa …**» della scena. Regia e cassetta non si toccano. Il
   master non cambia: cambia solo quello che va in stampa.
6. **La misura** è `scripts/misura_standard_tavolo.py`. Oggi è un indicatore;
   quando il primo booklet è convertito diventa un cricchetto in CI, con tetti
   per booklet che scendono soltanto, come `misura_statblocchi_booklet`.
7. **Prima di consegnare un booklet si legge da DM**, con il PDF e
   nell'ordine della serata: per ogni scontro mappa, scheda, ritratto e tattica
   devono stare entro una voltata di pagina. Il messaggio di consegna dice che
   cosa si è letto.

## Conseguenze

- I booklet si allungano: un riquadro e un ritratto in più per ogni persona e
  capitolo, e le mappe ripetute. I tetti di `misura_stampa` possono salire;
  se succede lo si dice, e lo decide il DM.
- Il generatore c'è (punto 5). Da solo però lavora solo dove il master ha
  già le schede d'entrata: nel repo sono 25, tutte di ARC-07 e ARC-08. Palio,
  Giardino, Drappo e Abbazia descrivono le persone in prosa, e lì la prova
  del 2026-11-03 non ha cambiato niente: servono le schede d'entrata,
  scritte a mano. Anche la riga «Chi è» presa dal titolo («il generale») è
  povera: va scritta nel master, una riga col ruolo in questa storia.
- Le skill `rumblingstone-module-standard` (scheda d'entrata con «Chi è», il
  controllo capitolo per capitolo) e `rumblingstone-playtest` (la lettura da
  DM con il PDF) vanno aggiornate.
- La misura conta le voci con l'etichetta, non la loro qualità: la lettura da
  DM resta il giudizio.

## Prova (2026-11-03)

La prova è in [prova-adr0107-2026-11-03/ESITO.md](../esperimenti/prova-adr0107-2026-11-03/ESITO.md).
Sul booklet della serata del 25/09 la misura dà: numeri nel capitolo da 0 a
25 su 151, mappe vicine allo scontro da 4 a 8 su 41, 15 pagine in più. Tutto
il guadagno sta in ARC-07. Nella lettura cieca il DM e il playtester scelgono
tutti e due la versione nuova. La fascia TATTICHE sopra il piede e le
correzioni di DEF-4 (CD del Vecchio, scurovisione di Zog'tar) sono chiuse:
la prima dal tema, le seconde dalla PR #305.

## Adozione (2026-11-03)

`"schede": "entrambe"` e `"chi_si_incontra": true` entrano nei manifest dei
booklet del DM dove la misura migliora e niente peggiora. PDF compilati prima
e dopo, misurati con `misura_distanza_pagine.py` (mediana delle pagine fra
dove la persona agisce e dove stanno CA e pf) e `misura_standard_tavolo.py`:

| booklet | pagine | Zog'tar | Skullcrusher | Balvar | Durin | esito |
|---|---|---|---|---|---|---|
| Notte e Alba | 143 → 158 | 20,5 → 5,5 | 10 → 3,5 | 25 → 6,5 | 53 → 4,5 | adottato |
| Serata Resurrezione | 158 → 172 | 24 → 5 | 15 → 4 | 30 → 7,5 | 51 → 4,5 | adottato |
| Volume Mille Anni | 93 → 105 | 23,5 → 4,5 | 12 → 3 | 29 → 7 | 51 → 4,5 | adottato |
| Ritorno alla Forgia | 28 → 29 | — | — | — | — | adottato: «vuole» da 0 a 20% |
| Drappo (DM) | 86 → 87 | — | — | — | — | adottato: numeri nel capitolo in 2 coppie |
| Abbazia | 41 → 43 | — | — | — | — | adottato: numeri nel capitolo in 4 coppie |
| Sessione Terros | 66 → 68 | — | — | — | — | **non adottato**: Terros da 7 a 8 pagine |

Sui dieci booklet del DM: numeri nel capitolo da 8 a 25 coppie, «vuole» da 51
a 61, aspetto da 45 a 50, ritratto da 34 a 38, mappe vicine allo scontro da 5
a 9 su 42. Palio e Giardino non cambiano (niente schede d'entrata nei master)
e restano come sono.

La prova ha trovato due difetti veri, corretti: dopo la #305 le schede
d'entrata con il segno `<!-- blocco -->` non si riconoscevano più (il booklet
prendeva Zog'tar da una revisione in `plans/`, con l'immagine rotta); e una
tabella larga in fondo alla pagina copriva il riquadro della colonna accanto.
Il tema ora mette in cima la tabella della persona portata, rimisura il
riquadro dove cade e non lascia un titolo da solo in fondo alla colonna.
`validate_corredo --stampa --rigoroso`, `validate_booklets --stampa` e
`misura_stampa --tutti --check`: zero righe sovrapposte, zero fuori margine,
zero schede spezzate. Il tetto delle immagini sotto 300 dpi sale in tre
volumi (52 → 66, 45 → 53, 43 → 51) per mappe e ritratti ripetuti nei capitoli:
per riscendere servono i file a risoluzione più alta.

Un test (`TestAdozioneAdr0107`) tiene i sei manifest adottati: togliere il
modo da uno di loro è rosso.

## Da rivedere se

- al tavolo il DM trova che le pagine in più rallentano più di quanto aiuti
  avere tutto nel capitolo;
- la misura conta troppe persone citate e non incontrate, e serve marcare nel
  master dove una persona si incontra davvero (il *Chi* del contratto «In
  scena» di ADR-0073 lo fa già, dove c'è);
- un booklet per i giocatori ha bisogno dei ritratti senza i numeri.
