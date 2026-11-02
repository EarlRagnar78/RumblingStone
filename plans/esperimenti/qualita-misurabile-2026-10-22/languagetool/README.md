# LanguageTool nella pipeline della prosa: la prova del 2026-10-23

Il DM ha chiesto di integrare in `migliora_prosa.py` strumenti che migliorino la
resa in modo misurabile, e di vedere se cambia qualcosa. Qui si prova
LanguageTool italiano in locale, e nello stesso giro i tratti esterni dell'altro
thread (Stanza e la perplessità di Qwen2.5-0.5B). La risposta breve è no:
LanguageTool in italiano non vede quasi niente di vero nei nostri box, non
distingue la versione che il DM preferisce da quella che scarta, e nessuna
variante del modello batte il base di 33 su 54.

## Lo strumento

| | |
|---|---|
| versione | LanguageTool **6.8** (build 2026-05-05, f558ce3), `org.languagetool:language-it` e `languagetool-server` da Maven Central |
| licenza | LGPL-2.1: gira come server separato, non si distribuisce e non entra nel repo. Per ADR-0099 vale come uso interno |
| dove sta | fuori dal repo: 172 jar, 252 MB, risolti con `mvn dependency:copy-dependencies` |
| Java | OpenJDK 21 |
| tempi | avvio del server pochi secondi; 109 testi di VOTI.json in 17 s, 229 box di ARC-07 e ARC-08 in 36 s; tutto il giro, varianti comprese, circa 70 s |

## Come si rifà

Fuori dal repo, in una cartella vuota, un `pom.xml` con le due dipendenze
`org.languagetool:language-it:6.8` e `org.languagetool:languagetool-server:6.8`,
poi:

    mvn -q -B dependency:copy-dependencies -DoutputDirectory=lib
    java -cp "lib/*" org.languagetool.server.HTTPServer --port 8081 &

Dal repo:

    # tutto il giro: conti, precisione, calibrazione, sonda, varianti; --scrivi aggiorna MISURE.txt e TRATTI-LT.json
    python3 scripts/migliora_prosa.py languagetool --tratti-esterni FILE-DEI-TRATTI-ESTERNI --scrivi
    # il campione da leggere a mano (quello di PRECISIONE.json)
    python3 scripts/migliora_prosa.py languagetool --campione 30 --seme 20261023 --uscita campione.json
    # le varianti senza server, coi rilievi già contati
    python3 scripts/migliora_prosa.py modello --varianti --tratti-esterni FILE-DEI-TRATTI-ESTERNI \
        --tratti-esterni plans/esperimenti/qualita-misurabile-2026-10-22/languagetool/TRATTI-LT.json
    # il filtro su un box
    python3 scripts/migliora_prosa.py migliora FILE --box N --candidate C.md --lt

`LANGUAGETOOL_URL` cambia l'indirizzo. Se il server non risponde, `languagetool`
lo dice ed esce 0, e `migliora --lt` filtra come prima.

I tratti esterni sono quelli calcolati dall'altro thread
(`/mnt/project-files/qualita-misurabile/tratti-esterni.json`, Stanza 1.15 e
Qwen2.5-0.5B Apache-2.0). La copia in `pipeline/tratti-esterni.json` è da
fare con l'ok del DM: in questo giro il file è stato letto dal suo posto.

## I file

| File | Cosa contiene |
|---|---|
| `SOGLIA.txt` | le varianti del modello e il criterio di «migliora», scritti prima del leave-one-out |
| `PRECISIONE.json` | il campione fisso di 30 rilievi sui box, con il verdetto letto a mano e una nota per ciascuno |
| `MISURE.txt` | l'uscita di `languagetool --scrivi` |
| `TRATTI-LT.json` | `lt_refusi` e `lt_altri` per ogni versione di VOTI.json, nella forma dei tratti esterni |

## Che cosa trova

Sui 229 box di ARC-07 e ARC-08, 346 rilievi. 335 sono refusi
(`MORFOLOGIK_RULE_IT_IT`), e 11 tutto il resto: 8 maiuscole a inizio frase,
1 «a/ha», 1 d eufonica, 1 parentesi. Stile, ripetizioni e accordi non
compaiono mai.

Il dizionario dei nomi (il registro di `misura_craft`, cioè Bestiario e
`state.md`, più le prime due colonne delle tabelle del glossario, con le
flessioni: «naniche» si riconosce da «nanico») toglie 274 refusi su 335. I 61
che restano sono ancora quasi tutti parole giuste: sigle di regolamento finite
in un box (pf, For, Sag), nomi che il registro non ha (Cantitrici, Passolesto,
Manodura), composti voluti (mezzo-ogre, sacerdotesse-barde), parole italiane
corrette che il vocabolario di LanguageTool non conosce (elfa, guantata,
lisciva, àncora), un'onomatopea (tump).

## Precisione

Il campione fisso (`--campione 30 --seme 20261023`) prende tutti gli 11 rilievi
non refusi e 19 refusi estratti fra quelli che il dizionario lascia, cioè
quelli che il filtro userebbe.

| Gruppo | Veri | Letti | Precisione |
|---|---:|---:|---:|
| grammatica | 0 | 9 | 0,00 |
| punteggiatura | 0 | 1 | 0,00 |
| stile | 1 | 1 | 1,00 (sotto i cinque letti richiesti) |
| refusi dopo il dizionario | 0 | 19 | 0,00 |

Le maiuscole sono puntini di sospensione voluti («Io… dove… respirare è
difficile.») o righe di nota che `box_read_aloud` prende per box. «roso a
morsi» non è «ha morsi». La parentesi si chiude due righe sotto. L'unico vero è
«ad ogni» al posto di «a ogni».

Letti fuori campione tutti i 61 refusi che il dizionario lascia, ce n'è uno
vero: **«un'avalanga»** nel box 6 di
`hammerfist_encounters-La Battaglia-di-Hammerfist-Guida-agli-Scontri-final.md`
(«come un'avalanga di ferro e vendetta»), da correggere in «una valanga»
quando si tocca quel file. Precisione dei refusi grezzi: 1 su 335. Fuori dalla
precisione, ma utile: una nota di regola ripetuta in `ARC08-01-GUIDA-DM.md` e
`ARC08-02-SCHEDE-PERSONAGGI-REGOLAMENTO.md` porta l'etichetta «[Private source
— FRCS]», che LanguageTool segnala come parola inglese.

La sonda di richiamo (venti frasi con un errore voluto, in `SONDA_LT`) dice
perché la grammatica non conta: LanguageTool 6.8 ne vede **6 su 20**. Trova
apostrofi («Qual'è», «Un'albero»), accenti («Perchè»), doppia virgola e spazio
prima della virgola; non vede «Le ragazza sono andate», «Io ho andato», «Lui
disse che e bello», «I nani è arrivati», «La spada di il re». Il modulo
italiano ha 193 regole XML, e nessuna di accordo che scatti su questi casi.

Nessun gruppo arriva a 0,70 con almeno cinque letti, quindi **il filtro di non
regressione non usa nessun gruppo**: `migliora --lt` gira, ma non scarta nulla
finché `PRECISIONE.json` non dice altro.

## Calibrazione

Sulle 54 coppie decise, il test del segno per gruppo (la vincente ha meno
rilievi?) non ha quasi coppie da contare: le due versioni hanno gli stessi
rilievi, perché i refusi sono i nomi e le maiuscole stanno nelle stesse frasi.

| Gruppo | Vincente con meno | Con più | p corretto (Bonferroni × 6) |
|---|---:|---:|---:|
| refusi grezzi | 3 | 3 | 1,00 |
| refusi dopo il dizionario | 0 | 1 | 1,00 |
| grammatica | 0 | 1 | 1,00 |
| stile, ripetizioni, punteggiatura | 0 | 0 | 1,00 |

LanguageTool non dice niente su quale versione il DM preferisce.

## Il modello, prima e dopo

Leave-one-out sulle stesse 54 coppie, L2 con lambda 1 come il base, McNemar
esatto contro il base con la soglia di `SOGLIA.txt` (p < 0,0125 e Wilson basso
sopra 0,50).

| Variante | Tratti | Giuste | Accuratezza | Wilson 95% | Solo base | Solo variante | p McNemar |
|---|---:|---:|---:|---|---:|---:|---:|
| base | 11 | 33 | 0,611 | 0,478-0,730 | | | |
| +LT | 13 | 34 | 0,630 | 0,496-0,746 | 2 | 3 | 1,00 |
| +ppl | 13 | 30 | 0,556 | 0,424-0,680 | 5 | 2 | 0,45 |
| +Stanza | 24 | 33 | 0,611 | 0,478-0,730 | 5 | 5 | 1,00 |
| +tutto | 28 | 31 | 0,574 | 0,442-0,697 | 7 | 5 | 0,77 |

Nessuna variante migliora. +LT fa una coppia in più, con due perse e tre
guadagnate: è rumore, e il peso di `lt_refusi` è positivo (vince la versione
con più «refusi»), cioè conta i nomi propri che il dizionario non conosce, lo
stesso segnale di `nomi_tolti`. +Stanza sposta dieci coppie per restare dov'era;
con 24 tratti su 54 coppie il peso di `stanza_pron_soggetto` arriva a −2,3 su
pochissimi casi non nulli, il segno del sovradattamento. +tutto, con 28 tratti,
fa peggio del base.

La perplessità da sola sembrava promettente: la vincente ha la `nll_token` più
bassa in 35 coppie su 54 (p 0,04). Ma le vincenti sono più lunghe, e un testo
più lungo ha una perplessità per token più bassa. Tolta la lunghezza (retta
sulle differenze di log dei token, pendenza −0,27) restano 34 contro 20,
p 0,08; nel modello, che ha già la lunghezza, il suo peso è −0,19 e la
variante perde tre coppie.

## Raccomandazione

- **LanguageTool resta in unstable** (ADR-0099 §1): non entra in testing. La
  condizione di testing chiede un guadagno nominato, e qui non c'è: precisione
  0 su 29 rilievi letti fuori dalla d eufonica, un refuso vero su 335, nessun
  segnale sulle coppie, nessun guadagno nel modello. Se un giorno entrasse,
  sarebbe come server locale con la versione fissata (6.8) e il job non
  bloccante.
- Il modulo resta in `migliora_prosa.py` come **filtro facoltativo** (`--lt`),
  spento di fatto finché nessun gruppo supera 0,70 in `PRECISIONE.json`. I
  tratti LT **non entrano nel modello**.
- Il refuso «un'avalanga» e l'etichetta «[Private source — FRCS]» vanno
  corretti nei file di ARC-08 da chi li tocca (questa prova non tocca i
  master).
- Le righe di nota di regola che `misura_craft.box_read_aloud` prende per box
  (una riga che comincia con un corsivo a metà frase) hanno prodotto 3 dei 9
  rilievi di grammatica: è un difetto del rilevatore dei box, da guardare a
  parte.
- Stanza e perplessità non migliorano il modello a 54 coppie. Si rifà il
  confronto quando i voti nuovi (la prima prova della pipeline e le successive)
  avranno portato le coppie verso il centinaio, con le stesse varianti.
