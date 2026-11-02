# Giro 4 di ARC-07: DEF-4 e DEF-5 per la serata

Il DM gioca stasera da DEF-4 Scena 5 e ha chiesto i booklet aggiornati dopo
un giro di developer, playtester e DM a freddo, con mappe, PNG, villain e
tattiche allineati, la misura del miglioramento anche sugli handout e il
controllo di struttura e ordine dei booklet. È anche la prima prova del
«giro completo» che l'altro thread propone come processo standard.

## Come si è lavorato

1. **Lo stato vero del gruppo** è stato copiato dal ramo
   `campaign-group-rumblingstone` in `stato-del-gruppo/`, in sola lettura: volo,
   acquisti al banco, Doni di Hella, Debito di Thorik, pozioni e pergamene.
2. **Sei letture a freddo** su quello stato: developer, playtester e DM per
   ciascun master, più la coerenza di PNG, villain e mappe
   (`DEF-4/`, `DEF-5/`, `COERENZA-PNG-MAPPE.md`).
3. **Le correzioni**, rilievo per rilievo, con una riga ciascuna in
   `DEF-4/CORREZIONI.md` e `DEF-5/CORREZIONI.md`. Un numero senza fonte non è
   stato inventato: il testo porta la proposta come
   `[INFERRED — needs DM confirmation]` e la domanda è in `DECISIONI-DM.md`
   (DEF-4 e serata) e `DEF-5/DECISIONI-DM.md`.
4. **La misura** contro main prima del giro (8a6b1e1) con
   `ciclo_prosa.py confronta`, su master, regia, echi e handout
   (`misure/CONFRONTO-8a6b1e1.txt`). Il cancello del giro 3, con la base
   spostata, è `cancello.py`.

## I rilievi

| lettura | 🔴 | 🟠 | 🟡 |
|---|---:|---:|---:|
| DEF-4 developer | 0 | 6 | 17 |
| DEF-4 playtester | 0 | 3 | 15 |
| DEF-4 DM e booklet | 1 | 10 | 23 |
| DEF-5 developer | 0 | 5 | 15 |
| DEF-5 playtester | 0 | 2 | 13 |
| DEF-5 DM | 0 | 2 | 16 |
| coerenza PNG, villain, mappe | 0 | 7 | 18 |

L'unico rosso era nella regia della serata: contava le tacche a piedi, e un
gruppo che vola ha ancora un'ora in fortezza. Su DEF-4 e la serata, di 100
rilievi 68 sono corretti, 5 in parte, 3 lasciati e 24 vanno al DM; su DEF-5
gli esiti sono nella tabella di `DEF-5/CORREZIONI.md`.

## La misura

Nessun file peggiora sulla prosa: segnalazioni, punteggio MQM e dettagli
sensoriali restano uguali o salgono, nessun box impoverito. I cinque «✗» del
confronto sono tutti fatti cambiati di proposito (numeri e nomi aggiunti al
testo per il DM, il Rubino che ha un nome solo, la regia riscritta); i box
read-aloud non sono stati toccati. Gli handout dei giocatori sono identici
salvo gli echi, dove la riga privata adesso è dichiarata anche nella stampa.

Il miglioramento di questo giro non è di prosa ma di tenuta al tavolo: un DM
che prepara da questi file sa cosa ha in mano il gruppo, quanto tempo ha e
cosa fanno i nemici nei casi che il gruppo renderà probabili.

## Cosa resta fuori

- Le decisioni del DM: dieci servono stasera (in testa a `DECISIONI-DM.md`),
  le altre possono aspettare. Ognuna ha un consiglio e dice cosa succede se il
  DM non decide.
- La scheda di Skullcrusher resta nel file `-cr12`: il GS 14 è nella riga
  Source, ma rinominare il file vuol dire seguire i rimandi e rigenerare il
  catalogo, fuori dal tempo di stasera. ERRATA §2.3 dice ancora GS 12.
- `ARC08-11-PONTE-ARRIVO.md` ha uno stato del gruppo superato e non scrive la
  scena dopo il portale.
- Le pagine della Corona hanno cambiato testo ma restano alla versione r7.
