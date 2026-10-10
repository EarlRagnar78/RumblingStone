# Il collaudatore a freddo su M7-C — prima esecuzione vera (2026-10-09)

Il ruolo di V11-bis di [COLLAUDO-MAPPE](../../PIANO-COLLAUDO-E-GENERAZIONE-MAPPE.md)
([`collaudo-mappe.md`](../../../skills/rumblingstone-mapmaking/references/collaudo-mappe.md)),
lanciato in un subagente che non aveva visto né il piano né la conversazione.
Materiali, e nient'altro:
- `ARC07-MAPPE-M7C-TENDA-DEL-COMANDO.md` e il suo `.json`;
- `ARC07-DEF-4-VIAGGIO-MILLE-ANNI.md`, righe 1440-2013 (il campo, Scene 7 e 8)
  e 3201-3240 (Appendice D);
- il rapporto di `collaudo_mappe.py`: **0 errori, 0 avvisi**;
- il PNG della mappa.

**Perché M7-C.** Lo stesso giorno l'audit della #226 aveva trovato che Grask e
il sacerdote dell'orda, presenti nella bozza D28 ritirata, mancano dalla mappa
su `main`, mentre DEF-4 li mette alla tenda. Al collaudatore non è stato detto.
Li ha trovati tutti e due (righe 4 e 5), insieme ad altri 16 rilievi che lo
strumento non può vedere. Il criterio di qualità del lotto è soddisfatto: *trova
almeno uno di ciò che lo strumento non può trovare*.

**Cosa non è.** I rilievi sono del collaudatore e non sono stati verificati uno
per uno. Correggerli vuol dire toccare una mappa di canone e decidere fra due
testi (il GS di Zog'tar, la quarta runa): decide il DM.

## Il rapporto, com'è uscito

| # | Mappa | Cella | Codice | Cosa non va | Gravità | Prova |
|---|---|---|---|---|---|---|
| 1 | M7-C | nota EVOLUZIONE (riga 81) | M-POSIZIONI | La quarta runa della mappa contraddice il canone: per la mappa è vuota e Balvar la incide durante lo scontro, per il master la quarta è la Catena del drago e la lastra non è una runa attiva | 🟠 | Mappa: «Runa 4: vuota, la incide durante lo scontro.» · Scena 7: «Le rune incise che regge sono **quattro**, e la quarta è la Catena del drago» e «Non è una runa attiva, perché la quinta non la reggerebbe» |
| 2 | M7-C | N12 (`@mark 3`) | M-POSIZIONI | Il GS di Zog'tar è diverso nei due testi | 🟠 | Mappa: «@mark 3 ; N12 ; Zog'tar Deatheye (Grande) (GS 14)» · Scena 7: «Zog'tar (GS 15), Balvar (GS 13), le quattro guardie […] EL 17» |
| 3 | M7-C | M11–N12 contro 👑 M13 | M-POSIZIONI | Zog'tar occupa le quattro celle a nord del seggio e non è seduto. Il testo lo mette sul seggio e lo fa alzare da lì | 🟠 | JSON: `"area": { "rect": [12, 10, 2, 2] }` e `"👑", "at": [12, 12]` · Scena 7: «Zog'tar è sul seggio con le sue guardie» · Scena 8: «Il mezzo-ogre si alza dal seggio» |
| 4 | M7-C | assente | M-POSIZIONI | Il sacerdote dell'orda non è sulla mappa, e nemmeno la sua tenda. Fa parte della scena e del conto dell'EL 17, e la sua entrata ha un punto preciso | 🟠 | Mappa: nella tabella Forze ci sono 8 unità, nessun sacerdote · Scena 8: «Chi: Zog'tar · le quattro guardie · Balvar · il sacerdote dell'orda»; «Dorme nella tenda accanto, a dieci passi […] Dalla soglia lancia *comando*» |
| 5 | M7-C | assente | M-POSIZIONI | Grask, l'araldo col corno, non è segnato. Eppure i PG possono occuparsene prima dello scontro, e il corno suona entro 1d4 round: dove dorme decide il piano | 🟠 | Mappa: nessun `@mark` per Grask · Camp: «L'araldo col corno: dorme fuori dalla tenda, dalla parte del campo»; «lo si lega, lo si addormenta o gli si ruba il corno» |
| 6 | M7-C | K2 (🟢) | M-POSIZIONI | Durik è un PNG che le Scene 7 e 8 non nominano mai. Ha un token suo e la legenda lo legge come «Creatura evocata / bestia». È un'invenzione presentata come canone, senza marca | 🟠 | Mappa: «@mark 2 ; K2 ; Durik» e, nel PNG, la legenda «🟢 — Creatura evocata / bestia» · Scena 7: «Chi: Zog'tar · Balvar · le quattro guardie»; nelle righe 1440-2013 Durik non c'è |
| 7 | M7-C | telo S e telo sopra M13 | M-ACCESSI | Delle tre entrate del testo, la mappa ne segna una sola, la soglia. Non segna il telo est consigliato da Balvar, né il glifo sul telo sopra il seggio: il DM deve ricostruire da solo dove si entra senza far scattare niente | 🟠 | Mappa: solo «"🚪", "at": [12, 3], "label": "La soglia (runa 1…)"» · Camp: «*«Non la soglia. Il telo a sinistra.»* […] cioè il fianco est, non quello sopra il seggio che porta il glifo» |
| 8 | M7-C | 🏮 O6, J11; fondo R13 | M-LETTURA | La regola di luce che decide la scena (soglia illuminata, fondo buio con occultamento) non sta nella tabella AMBIENTE, che elenca solo i due falò fuori dalla tenda. Il raggio dei bracieri non è scritto | 🟠 | Mappa, AMBIENTE: solo «🔥 Falò \| F14» e «🔥 Falò \| V14» · Scena 7: «Il fondo è buio e dà occultamento, la soglia è illuminata e non ne dà» |
| 9 | M7-C | blocco TATTICHE (righe 69-72) | M-LETTURA | Le tattiche della mappa sono rimaste segnaposto del modello, mai compilati | 🟠 | Mappa: «**Round 1-2**: [reazione al contatto]», «**Morale**: [soglia di ripiegamento/resa]» · Scena 8: «**Round 1** (se reagisce): **Ira Barbarica** […] **Soglia 30% pf**» |
| 10 | M7-C | blocco EVOLUZIONE (righe 79-81) | M-LETTURA | Le tre righe di stato B hanno tutte «[trigger]» e «[effetto]», e dentro c'è una nota d'autore («si ricompila»). Mancano gli stati che il testo prevede: palo abbattuto e telo crollato, barriera di lame che divide la tenda, telo scoperchiato dal drago, disposizione in pre-allerta | 🟠 | Mappa: «\| B \| [trigger] \| La tenda e' 18 m x 16,5 m […] la geometria si cambia qui e si ricompila. \| [effetto] \|» · Scena 8: «**abbatte il palo centrale** (Forza **CD 20**…): il telo crolla»; «le quattro guardie davanti al seggio» |
| 11 | M7-C | bordi della griglia | M-ACCESSI | I rinforzi hanno un tempo d'arrivo ma nessun bordo d'entrata: il DM non sa da che lato arrivano | 🟡 | Mappa: nessuna freccia d'entrata, solo `@path` del corridore · Scena 8: «Le ronde di orchi più vicine arrivano alla tenda in **1d4+2 round**, gli squadroni hobgoblin in **2d4+2**» |
| 12 | M7-C | M11–N12 | M-STRUMENTO | Zog'tar è Grande ma manca la direttiva `@taglia`, quindi il controllo `ingombro/grande` non è mai partito. Lo zero del rapporto non lo copre | 🟡 | Griglia: c'è «@mark 3 ; N12 ; Zog'tar Deatheye (Grande)», non c'è un `@taglia N12 ; Grande` · Scena 7: «mezzo-ogre, grande quanto una porta di stalla» |
| 13 | M7-C | M9 (🟪) | M-LETTURA | Il palo della tenda è disegnato e messo in legenda come pilastro di mithral | 🟡 | PNG, legenda: «🟪 — Pilastro / mithral»; JSON: «"Palo centrale, alto 6 m (runa 2: barriera di lame)"» · Scena 7: «sul **palo centrale** — *blade barrier*» |
| 14 | M7-C | F14, V14 (🔥) | M-LETTURA | Il simbolo del falò ha due funzioni diverse: per la legenda fa danno, per l'AMBIENTE è solo una luce. In più la «CD» di Nascondersi non è SRD, perché Nascondersi è una prova contrapposta | 🟡 | PNG, legenda: «🔥 — Fuoco (1d6 fuoco/round)» · Mappa: «luce fioca a 3 m: Nascondersi CD +4 nei quadretti vicini» · Scena 7: «si evitano con **Nascondersi** contro il loro **Osservare**» |
| 15 | M7-C | I5, R9 (🦴) | M-POSIZIONI | Le ossa appese ai tiranti sono disegnate dentro la tenda. Il read-aloud le vede da fuori, sui tiranti, nel vento | 🟡 | JSON: «"🦴", "at": [8, 4], "label": "Ossa di nani appese ai tiranti"» · Scena 7: «di pelle nera, con ossa appese ai tiranti che battono piano nel vento» |
| 16 | M7-C | R13 contro N12 | M-POSIZIONI | Fra Balvar e la cella più vicina di Zog'tar ci sono 4 quadretti (6 m), e in mezzo c'è la guardia in P12. Il testo vuole il dialogo «a tre passi dal generale» | 🟡 | Mappa: «@mark 4 ; R13», «@mark 3 ; N12», «@mark 6 ; P12» · Scena 7: «La conversazione con Balvar si fa **a tre passi dal generale**» |
| 17 | M7-C | L5, N5 | M-POSIZIONI | Due guardie stanno alla soglia, a 10 m da Zog'tar, mentre il read-aloud le fa ascoltare il generale che racconta. Va bene come scelta, ma non è scritta: chi entra dalla soglia passa fra due guardie | 🟡 | Mappa: «@mark 7 ; L5», «@mark 8 ; N5» · Scena 7: «Sta raccontando alle guardie come impalerà il re […] Quattro hobgoblin […] stanno di guardia, le mani sulle armi, e ascoltano» |
| 18 | M7-C | telo nord (riga 4) | M-POSIZIONI | L'etichetta dà un tempo di taglio che il testo non dice, senza la marca `[PROPOSTA]`. Il testo regola il rumore, non il tempo | 🟡 | JSON: «"Telo nord della tenda […] (pelle nera: si taglia in un round)"» · Scena 7: «il taglio fa rumore: le guardie tirano Ascoltare contro il Muoversi Silenziosamente di chi taglia» |

**Verificato senza rilievi**: lo strumento è stato eseguito e dà 0 errori e 0
avvisi, senza deroghe. `@north N` è dichiarato e il testo dice «I PG entrano da
nord»; la soglia in M4 sta nel telo nord. Il «telo a sinistra», per chi arriva
da nord, è davvero il fianco est (colonna S). Le misure tornano: i teli da H a S
e dalla riga 4 alla 14 fanno 12×11 quadretti, cioè 18 m × 16,5 m come
nell'Appendice D. Il palo è in M9, al centro; la tavola con la mappa di
Hammerfist è in J8. Le guardie sono 4 sulla mappa e 4 nel testo. Balvar è
nell'angolo in fondo (sud-est, R13), lontano da tutti e due i bracieri (O6 e
J11). Non ci sono scale né botole, quindi M-LETTURA sui livelli e M-LIVELLI
non si applicano. La mappa è compilata da un contratto JSON scritto a mano e
non ha deroghe: M-GENERATA non ha niente da giudicare. Dalla soglia a Zog'tar
ci sono 7 quadretti, quindi il contatto arriva in 1 round per chiunque abbia
velocità 9 m.

**Cosa il collaudo non ha potuto verificare**:
- La versione per i giocatori non c'è (nessun `@vista giocatori`). Non è stato
  possibile controllare D9 né il rischio che il PNG del master riveli
  l'«angolo buio» o la posizione dei PG invisibili.
- Il percorso del corridore (Z7 → U3 → N3) e la sua provenienza dipendono dalla
  complicazione 6 della Scena 6, fuori dalle righe assegnate.
- Il GS giusto di Zog'tar (14 o 15) sta nell'Appendice A, che non è stata letta.
- Il raggio di luce dei bracieri, e quindi se R13 è davvero al buio, nel testo
  non c'è.
- Restano fuori dal collaudo il divertimento, i tempi reali al tavolo e la resa
  della trattativa sottovoce con Balvar come scena sociale sulla mappa.
