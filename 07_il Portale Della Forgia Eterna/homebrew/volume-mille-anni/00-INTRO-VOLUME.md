# Il viaggio a mille anni fa — il volume

> *Il portale non vi trasporta: vi rifà. Per un istante lunghissimo siete
> scomposti nei vostri mille anni, e quando vi ricomponete dall'altra parte le
> ferite che avevate non ci sono più.*
>
> *C'è odore di calcare appena tagliato. Le mura sono bianche. Su una targa di
> bronzo, alle porte, qualcuno ha inciso il vostro destino stamattina.*

**Cos'è questo volume.** Tutto il beat del viaggio a ≈372 DR in un solo libro,
da stampare o da tenere sul tablet: il master `ARC07-DEF-4`, lo statblocco di
Balvar, la tabella B4 che porta le ferite del duello fino a Fauci di Palude, e i
due handout, le Cronache e il piano di battaglia.

**<!-- storico -->Dal 2026-09-25 <!-- /storico -->Il master si legge in avanti.** Tre atti, tredici scene, dal
tramonto all'alba: ogni PNG entra con la sua **scheda d'entrata** nella scena in
cui i PG lo incontrano, e in fondo ci sono quattro appendici su pagine A4 a una
colonna: le **statistiche** (A), il **Sigillo di Ossidiana** (B), le **versioni
veloci** (C) e le **mappe** a pergamena, fra cui la <!-- storico -->nuova <!-- /storico -->M7-C della tenda del
comando (D).<!-- storico --> Il capitolo separato del cast e quello delle mappe non ci sono
più: erano una seconda copia di quello che adesso sta nel master.<!-- /storico -->

<!-- storico -->
**Sostituisce il Fascicolo V** (`homebrew/ARC07-BOOKLET-FASCICOLO-5-P5-MILLE-ANNI.hb.md`),
un riassunto di luglio che non conosce Balvar, l'orologio della notte, Zeth, il
Rituale 4 e l'Aura della Forgia Eterna: tutto è arrivato dopo, con le
riscritture di settembre. Il fascicolo resta nel repo come storia; al tavolo si
usa questo.
<!-- /storico -->

**Come si gioca, in due sessioni**<!-- storico --> *(decisione S1 del DM, 2026-09-24)*<!-- /storico -->:

| Sessione | Da dove a dove | Nel master |
|---|---|---|
| **2026-09-25**, insieme alla resurrezione | l'arrivo, la targa, Durin, il consiglio di Re Thorek I, la notte con le sue otto tacche, Zeth, Balvar, Zog'tar, Vatore. **Ci si ferma al primo ariete sulle mura** | Atto I e Atto II, Scene 1-9 |
| **la successiva** | le mura all'alba, il duello con Skullcrusher, il Rituale della Forgia Eterna, il ritorno | Atto III, Scene 10-13, e §9 → `ARC07-DEF-5` |

La regia minuto per minuto della prima metà sta nel booklet della serata
(`homebrew/sessione-resurrezione-mille-anni/`, capitolo I, Atto IV). Qui c'è il
materiale completo, per entrambe le sessioni.

**Cosa annotare, per la sessione dopo.** Le tacche spese all'uscita dalla tenda,
come è morto Zog'tar (in silenzio, in modo spettacolare, umiliato), se
qualcuno ha letto la runa sulla scaglia del drago, cosa hanno promesso a
Balvar, e l'esito con Vatore. Decidono come comincia il duello.

<!-- storico -->
**Cosa è stato corretto nel master il 2026-09-24**, per allinearlo al canone
giocato dopo la sua ultima riscrittura:

- i «3 semi di treant» da piantare la notte: dopo il rito stanno nella
  Collana. All'alba Hella evoca **due Treant di Adamantio** (Scena 5);
- il **Marchio di Varis** era scritto come probabile: nel canone giocato **non è
  attivo**, e la risonanza con Vatore non scatta (§1, Artemis);
- **Durik** entra nel viaggio e nel duello, con la sua vulnerabilità all'acido
  (§1, e una battuta nella regia dei round della Scena 11);
- il **dono a metà** di `DEF-3` §9 si incassa qui, al primo uso (§1, Hella);
- l'immagine del portale era la foto di un testo (§9).

**Quattro contraddizioni, decise dal DM il 2026-09-24** e già scritte nei
file che le contenevano:

| | Cosa dicevano i file | Cosa vale adesso |
|---|---|---|
| 1 | **Chi ha perso la Corona.** Re Thorek I diceva *«suo nonno»*, Thorgrim *«mio nonno»* | sono **cugini**, nipoti dello stesso re caduto contro Skullcrusher (`DEF-4` Scena 4, scheda di Thorgrim) |
| 2 | **Frostcleaver.** In mano a Re Thorek I in `DEF-4`, a Thorgrim nell'affresco A3 | è **del re**. Nell'affresco Thorgrim tiene **Aegis Fang**, mille anni fa (`DEF-2` A3, `PortaleForgia-P2`) |
| 3 | **Zeth.** La scheda del Ghostlord diceva ottocento anni fa, un'invasione phaerimm, un lich di epoca Netherese | **mille anni fa, durante l'assedio dell'orda**; il cultista di Shar è la mano del Collezionista. Riallineati il Ghostlord, due file di ARC-09 e il Consiglio di Rethmar |
| 4 | **Balvar.** INT 9 e SAG 18 nella riga generata, INT 16 e SAG 20 nel testo | vale il testo: la riga dello statblocco è stata corretta |

E due dettagli: l'**Occhio di Ossidiana** di Zog'tar è un occhio vero, al posto
dell'occhio destro (statblocco in `DEF-4` Appendice A.2).
<!-- /storico -->

<!-- storico -->
**Come si rigenera**, dalla radice del repo:

- volume completo, schermo e stampa:
  `python3 scripts/dm.py volume "07_il Portale Della Forgia Eterna/homebrew/volume-mille-anni/ARC07-MILLE-ANNI-VOLUME.manifest.json" --stampa`
- solo le pagine ✉, un PDF ciascuna:
  `python3 scripts/dm.py booklet <lo stesso manifest> --pdf`
<!-- /storico -->
