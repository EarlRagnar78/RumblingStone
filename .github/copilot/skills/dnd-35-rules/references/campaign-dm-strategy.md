# Masterizzare per Adulti (Over 40) - Profilo Giocatori e Design della Campagna

Questa analisi è strutturata su misura per un gruppo di giocatori adulti, professionisti affermati, che investono ore di viaggio per giocare. Per un gruppo simile l'esperienza deve essere **Premium**: meno railroading, meno combattimenti "vuoti", maggiore "agency" (potere decisionale) e trame che stimolino l'intelletto, la morale e il problem-solving.

Essendo tu un Senior System Engineer, affrontiamo il design della campagna come un **Design a Sistemi Reattivi**, non come una trama lineare fissa.

---

## 1. PROFILAZIONE DEI GIOCATORI E SOTTOTRAME (SHINE TIME)

### 📌 ARTEMIS (Warlock 13) - *Il Senior Developer*

**Profilo Giocatore:** Mente ipercritica e analitica. Cerca di "craccare" il gioco, scova gli intrighi nascosti. Orientato al loot/soldi insieme a Tordek. Vuole usare magia furtiva, tattica e trovare sbocchi per vendere i tesori del Sottosuolo per il *Mantello dei Tiri Salvezza*.

* **Problema:** Poco spazio per l'infiltrazione e intrighi, ridotto ad artigliere ripetitivo in combattimento.
* **La Soluzione (Sottotrama e Roleplay):**
  * **Il Mercante Opportunista:** Crea **Maestro Varis "Seta-Argento"**, un mercante planare senza scrupoli che gestisce un mercato nero in un porto palesemente neutrale o nascosto. Artemis contratta con lui, vende il bottino del Sottosuolo e compra il Mantello. *MA* Varis scambia informazioni: propone ad Artemis accordi sottobanco per sabotare corporazioni rivali.
  * **L'Intrigo dell'Artefatto:** L'anello di Artemis ("Ring of Chaotic Illumination") attira l'attenzione della Fratellanza dei Mercanti Oscuri o seguaci di Mask. Vogliono assoldarlo... o rubarglielo.
  * **Furtività e Tattica:** Progetta incontri in cui le difese avversarie hanno "Falle di Sistema" che Artemis può individuare e sfruttare (es: bypassare barriere magiche per disattivare trappole ed evitare un massacro al party).

### 📌 THORIK (Guerriero 13) - *Il Manager Strategico*

**Profilo Giocatore:** Gestore di clienti complessi nella vita vera, usa mente strategica, ama avere scelte di peso e ama l'humor tagliente. Vuole fare roleplay risolvendo conflitti, non solo menando fendenti.

* **Problema:** Trovarsi intrappolato in piani elementali o situazioni meccaniche fisse lo frustra (nessuna interazione, è solo un sacco da boxe lento).
* **La Soluzione (Sottotrama e Roleplay):**
  * **Scelte di Comando:** Thorik deve essere il generale. Mettilo davanti a scelte militari (es: la difesa o rilocazione delle popolazioni di Hammerfist). Fagli posizionare le truppe NPC sulla mappa. Se le truppe muoiono a causa della sua tattica, la conseguenza è cruda e reale; se vincono, ne raccoglie l'epica gloria.
  * **La Faccia Diplomatica:** Fagli intimidire/coordinare capitani o despoti locali sbattendogli sul tavolo verità logiche e brute. Intrighi politici spiccioli da "risolvere" con arguzia manageriale e prese di posizione chiare.

### 📌 TORDEK (Guerriero 4/Monaco 9) - *Il Buyer / Ingegnere Meccanico*

**Profilo Giocatore:** Anti-autoritario, geniale "out of the box", baciato dai dadi. Adora distruggere la fisica o usare l'ingegneria in modo creativo. Carica a testa bassa e ama scovare loot.

* **Problema:** Manca interazione fisica con l'ambiente e vuole rompere le "regole" dei preconcetti fantasy.
* **La Soluzione (Sottotrama e Livellamento Terreno):**
  * **Ambienti Distruttibili:** Disegna stanze con argani, crolli di colonne, paranchi e dighe sotterranee che possono essere allagati/distrutti se manipolati fisicamente per spazzare via i nemici. Permetti a Tordek di trasformare la mappa tattica in un'arma sfruttando prove libere ed "ingegneristiche" di Conoscenze/Forza.
  * **Il Loot "Sporco":** Essendo attratto dai tesori, inserisci Golem o Macchinari nanici corrotti con Cuori Elettromeccanici rarissimi. Vuoi loot? Tordek deve "smontare" il costrutto sfidando l'autorità degli antichi ingegneri gnomici/nanici.

### 📌 HELLA (Ranger/Druido) - *La Responsabile Didattica*

**Profilo Giocatore:** È la Bussola Morale ed Epica del gruppo. Cerca significato e coesione, si appassiona alla storia e... le mancano tantissimo lei che si trasforma in rinoceronte e la carica del suo amico animale, il cane da galoppo morto tempo fa in mischia.

* **Problema:** Attualmente morta/assente come veicolo o priva di mordente offensivo dopo la morte del compagno.
* **La Soluzione (Sottotrama e Rituale del Ritorno):**
  * **La Rinascita Epica:** Quando Thorik finisce il rituale nel piano della terra e resuscita Hella, mandala in rampa di lancio! Quando rinasce, ha assimilato parte della Terra. Il suo vecchio compagno animale non è "sostituito", ma **il suo spirito ritorna, incarnato nella pietra solida infusa di cristalli**. Diventa un costrutto/cane da galoppo vivente di pietra (guadagna DR 5/Adamantio e si fissa al suo Fianco).
  * **L'Ascolto della Storia:** Sarà la persona a cui si rivolgono gli NPC indifesi o le forze della natura. Offri bivi etici dove Thorik penserebbe "Li salviamo perché conviene" ma Hella dice "Li salviamo perché è GIUSTO". Cerca l'intrigo Morale. Le due fazioni avversarie potrebbero avere entrambe le proprie ragioni etiche diserate dal rancore. Lei deciderà da che parte sta la bilancia. Ha una personalita da console come da test di personalità le piace far stare bene i suoi amici anche se si sente molte volte costretta al ruolo di crocerrossina e non sempre è d'accordo con le decisioni del gruppo.

---

## 2. ELIMINARE IL RAILROADING E AGGIUNGERE "INTRIGUE"

Sei un System Engineer. Invece di scrivere uno *script* (Storia Lineare), devi progettare una *State Machine* (Macchina a Stati Reattiva) che reagisca ai Giocatori.

### A. Non Programmare la Storia, Programma "Le Agende"

Non decidere cosa succede nel prossimo villaggio. Decidi COSA vogliono i cattivi e cosa succederà fra 10 giorni *se il party non fa nulla*.
I giocatori arriveranno (saltando le finestre, distruggendo ponti, etc.) ed essendo agenti del caos, altereranno i piani del Villain. Questo non rovinerà la tua "storia", semplicemente aggiornerà la reazione del Nemico. Questa è vera **Vivid Experience** decisionale.

### B. Il "Villain Intoccabile / Manipolatore" (Subdolo)

Per accontentare un Senior Developer (Artemis) e un Manager (Thorik), un mostro con 1000 HP non basta. Hanno bisogno di un avversario **che non possono abbattere con le spade**.

> **Esempio pratico (Il Conte Valerius):**
> Un potente aristocratico/finanziere che sovvenziona legalmente l'orda nemica o nasconde artefatti nanici sfruttando scappatoie legali del patto cittadino. Ucciderlo di botte significa ribellarsi al regno, attivare le guardie antimagia di livello epico e diventare fuggitivi.
> *Come si combatte?*
>
> * Artemis e Tordek fingono un accordo commerciale, usano l'invisibilità per entrare nel suo caveau finanziario, trafugare documenti esatti o prove di corruzione (spionaggio ingegnerizzato e tattico).
> * Thorik usa l'influenza della sua carica/simboli per bloccarlo a livello politico/sociale.
> * Una volta tolto il suo status, si passa al sangue ed esplode la soddisfazione della mischia.

### C. Abbandonare il "Bivio Binario"

"Aprite Porta A e salvate Mario, oppure Porta B e prendete la Spada". -> **ERRATO** (E troppo semplice per dei 40enni intelligenti).

**Design a Dilemma (Triangolo di Rischio):**
Offri problemi e lancia la sfida alla loro fantasia, lasciando che la risolvano usando le risorse dei PG:
> "Siete nel passaggio. C'è l'oro della corona sotto un dispositivo a pressione idraulica malfunzionante (Invito a *Tordek*). Il mercenario prigioniero dietro la cancellata magica sta per affogare e giura di conoscere il piano del Villain (*Artemis/Hella*). Manca pochissimo all'arrivo dell'armata d'assalto in cui *Thorik* deve posizionare le truppe.
> Come ne uscite investendo magia d'evocazione, forza bruta o furtività?"
Loro dovranno rinunciare a qualcosa, oppure inventare un trucco incredibile per prendere tutto. Qualsiasi cosa scelgano, il mondo invecchierà coerentemente per colpa - o per merito - delle loro scelte.

---

### In Breve per la "Next Session"

1. **Paga l'Artefatto della Terra:** Lascia che finiscano l'inferno del Boss (Terros) con il sacrificio di Thorik, facendo rifulgere Hella tramite risonanza narrativa prima del risveglio.
2. **Resurrezione & Shop:** Falli rientrare alla Forgia Eterna, Hella torna portando doni/epicità e riabbracciando il combat.
3. **Il Ritorno Sociale:** Concedi ad Artemis e Tordek l'accesso ad un NPC carismatico (es. Mercante di Artefatti corrotto o informatore) nel mezzo della capitale, per usare dialettica, baratto di oggetti meravigliosi e preparare un'infiltrazione per fermare l'avanzata delle truppe del nemico manipolatore.