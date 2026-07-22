Arco-Post-Hammerfist-P2-RHEST-FASE3-INTRUSIONE-EDIFICI-RHEST.md
===============================================================

# Rhest Fase 3 – Intrusione negli edifici sommersi

> **Versione**: v2 (2026-07-02) — espansa a standard "pacchetto Palio" (Lotto B,
> task B1.3): read-aloud, mappa in scala **1,5 m/quadretto**, regole subacquee
> SRD complete, tre approcci di infiltrazione (furtività / diplomazia coi
> prigionieri lucertoloidi / assalto), intel quantificato per l'assedio.
> **HUB Rhest**: `Arco-Post-Hammerfist-P2-RHEST-OVERVIEW.md`.
> **Statblock nemici boss**: `...-ENCOUNTER-SAARVITH-REGIARIX-STATBLOCCHI.md` (Fase 4).

---

## 0. Read-aloud d'apertura

> *Il cuore di Rhest galleggia su se stesso: tre edifici ancora in piedi legati
> da passerelle marce sopra l'acqua nera, e sotto di essi un intero piano di
> città **sommerso**, sale e corridoi dove la luce arriva verde e obliqua. Su una
> passerella, torce della Mano Rossa. Sotto, nel buio liquido, porte spalancate
> aspettano. Da qualche parte lì dentro, Wyrmlord Saarvith tiene i suoi ordini e
> i suoi prigionieri — e sotto tutto, paziente, respira il drago.*

**Obiettivo**: capire cosa c'è al centro (forze, legame Saarvith↔Regiarix,
documenti d'assedio), liberare/reclutare eventuali prigionieri, e **preparare il
terreno** per il boss di Fase 4 — idealmente arrivandoci di sorpresa.

---

## 1. Mappa in scala (1,5 m/quadretto)

```
         ══════ passerella nord ══════
        ║                              ║
   ┌────╨────┐                    ┌────╨─────┐
   │  TORRE  │                    │ DEPOSITO │
   │  /FARO  │····acqua bassa····│ /TEMPIO  │
   │ (12×12) │                    │ (16×12)  │
   └────╥────┘                    └────╥─────┘
        ║                              ║
        ╚═══════╗            ╔═════════╝
                ║            ║
            ┌───╨────────────╨───┐
            │   SALA DEL CONSIGLIO │   ← QG di Saarvith
            │      (24×20)         │      piano alto asciutto,
            │  ▓▓ piano inferiore  │      piano inferiore sommerso
            │  ▓▓ SOMMERSO ▓▓▓▓▓▓ │
            └──────────╥──────────┘
                       ║
              acqua profonda (Regiarix)
```

- **Scala**: 1 quadretto = **1,5 m**. Distanze fra edifici: 6–10 quadretti di
  acqua bassa/passerella.
- **Acqua bassa** (fra gli edifici): terreno difficile, guado; Nuotare non
  richiesto se si resta sulle passerelle.
- **Acqua profonda** (attorno alla Sala del Consiglio, sotto tutto): dominio di
  Regiarix. Chi ci entra applica le **regole subacquee** (§2).
- **Piano inferiore sommerso** della Sala: corridoi allagati che collegano gli
  edifici **sott'acqua** (rotta di infiltrazione alternativa, §3).

---

## 2. Regole subacquee (SRD 3.5) — riferimento della quest

> Questo è il blocco-regole a cui rimandano Fase 2 e Fase 4.

**Trattenere il fiato**
- Un personaggio può trattenere il fiato per **2 × il punteggio di Costituzione**
  in round **se resta inattivo**. Se compie **azioni faticose** (combattere,
  nuotare vigorosamente), la riserva scende a **Costituzione (punteggio) round**.
- Esaurita la riserva: ogni round **Costituzione CD 10, +1 cumulativo** per round.
  Al fallimento cade a **0 pf** (morente), poi −1, poi affoga.

**Combattimento subacqueo (senza velocità di nuoto né *Freedom of Movement*)**
- Armi da **taglio o impatto**: **−2 al tiro per colpire** e **danni dimezzati**.
- Armi da **perforazione**: colpiscono e danneggiano **normalmente**.
- **A distanza**: le balestre funzionano (gittata ridotta a un incremento); le
  armi da lancio **non** funzionano. Movimento a nuoto = prove di **Nuotare**.
- **Appigli/spinte**: senza appoggio, chi è in acqua è instabile (nessuna carica,
  nessun attacco in arco completo se deve nuotare nello stesso round).

**Incantesimi sott'acqua**
- Descrittore **fuoco**: inefficace sott'acqua a meno di una prova di **Sapienza
  Magica CD 20 + livello incantesimo** (crea una bolla di vapore).
- Descrittore **elettricità/fulmine**: colpisce **tutte** le creature entro l'area
  in acqua (attenzione al fuoco amico).
- Incantesimi con componente verbale: problematici per un incantatore che
  trattiene il fiato (spesso servono *Silent Spell* o bolle d'aria).

**Visibilità**: l'acqua torbida di Rhest dà **occultamento** oltre i 9 m
(occultamento totale oltre i 18 m). Vale per PG **e** nemici.

---

## 3. I tre edifici e i tre approcci

### 3.1 Gli edifici

| Edificio | Cos'è oggi | Cosa c'è dentro |
|---|---|---|
| **Sala del Consiglio** (24×20) | QG militare di Saarvith | Piano alto asciutto (uffici, ordini, arena del boss di Fase 4); piano inferiore sommerso (celle, corridoi allagati). |
| **Torre/Faro** (12×12) | Punto d'osservazione | 1–2 vedette lucertoloidi; da qui si controllano le passerelle (Osservare +alto). Spegnere il faro = infiltrazione più facile. |
| **Deposito/Tempio** (16×12) | Magazzino + altare minore a Tiamat | Rifornimenti, un chierico minore (EL 11–12), e i **prigionieri lucertoloidi** (§3.3). |

**Guarnigione tipica** (scala a piacere): pattuglie lucertoloidi (EL 10–11),
1–2 ufficiali Mano Rossa (hobgoblin/chierici di Tiamat, EL 11–12). Non è ancora
il boss: è la **rete** che, se allertata, mette Saarvith in guardia (Fase 4).

### 3.2 Approccio A — Furtività / infiltrazione

- **Via passerelle** (notturna): Muoversi Silenziosamente / Nascondersi contro
  Osservare/Ascoltare delle vedette. Spegnere il **faro** (Torre) → **−2** alle
  prove di Osservare dei difensori per il resto della fase.
- **Via corridoi sommersi** (piano inferiore): si aggira la guarnigione di
  superficie **del tutto**, ma serve gestire fiato e regole subacquee (§2). Un
  incantesimo di respirazione (*Water Breathing*) o oggetti anfibi lo rendono
  l'ingresso d'élite.
- **Ricompensa furtività**: se i PG raggiungono la Sala del Consiglio **senza
  allertare** la rete, entrano in Fase 4 **con la sorpresa** (Saarvith non è
  preparato: −1 alla sua iniziativa di gruppo, niente buff pre-cast).

### 3.3 Approccio B — Diplomazia (i prigionieri lucertoloidi)

Nel Deposito/Tempio, Saarvith tiene prigionieri i **capi lucertoloidi** che si
sono rifiutati di servire (o le loro famiglie come ostaggi — è così che tiene
in riga le tribù).

- **Liberarli** (combattere il chierico o aggirarlo) + **Diplomazia CD 22** →
  la banda lucertoloide **defeziona**: guide interne, una porta lasciata aperta,
  o un diversivo durante il boss (Fase 4: −2 alle forze di Saarvith).
- Se il party ha già **parlamentato** con una pattuglia in Fase 1 (§3.1 di FASE1),
  **−2 alla CD** qui (fama di liberatori).
- **Intuizione CD 18** per capire che gli ostaggi sono la **leva**: liberarli
  spezza la lealtà forzata dell'intero avamposto.

### 3.4 Approccio C — Assalto frontale

- Piattaforme e passerelle, combattimento su più quote. Rumoroso: la rete si
  allerta, il faro chiama Regiarix, **Saarvith è preparato** in Fase 4 (posizione
  da tiratore già scelta, pozioni bevute). Legittimo, ma paga in Fase 4.

---

## 4. Intel e ricompense

- **Documenti d'assedio** (Sala del Consiglio, Cercare CD 20): mappe di marcia e
  ordini della Mano Rossa. **Ricompensa di campagna**: consegnati al Consiglio di
  Rethmar, valgono **−1 al CR effettivo di una fase dell'assedio a scelta**
  (i difensori sanno dove colpirà l'Orda). Vedi CONSEGUENZE §intel.
- **Legame Saarvith↔Regiarix** (lettere/ordini): rivela che il drago **obbedisce**
  a un patto, non è un semplice mostro — utile per la tattica di Fase 4 (rompere
  il morale dell'uno spezza l'altro).
- **Chiavi/passaggi** verso la sala di Saarvith (accesso diretto al boss senza
  altra guarnigione).
- **Oggetti**: pozioni/scrolls di supporto per il boss (Cura, *Water Breathing*,
  resistenza all'acido — tema Regiarix).

---

## 5. Conseguenze di Fase 3 (verso Fase 4)

| Come è andata l'intrusione | Effetto in Fase 4 (boss) |
|---|---|
| **Furtività riuscita** (rete non allertata) | Sorpresa sul boss: Saarvith non preparato, niente buff pre-cast. |
| **Prigionieri liberati** (diplomazia) | −2 alle forze di Saarvith; possibile diversivo lucertoloide. |
| **Assalto rumoroso** | Saarvith **in allerta e preparato**; Regiarix già chiamato in posizione. |
| **Documenti d'assedio recuperati** | Sblocca il bonus **−1 CR** a una fase di Rethmar (CONSEGUENZE). |

---

## 6. Checklist DM (Fase 3)

- [ ] Mostrata la **mappa in scala** e chiarite le quote (passerelle / acqua bassa / sommerso)?
- [ ] Regole **subacquee** pronte per chi sceglie i corridoi allagati (§2)?
- [ ] Offerti **tutti e tre gli approcci** (furtività / diplomazia / assalto)?
- [ ] Presentati i **prigionieri lucertoloidi** come leva diplomatica?
- [ ] Piazzati i **documenti d'assedio** (bonus −1 CR a Rethmar) da trovare?
- [ ] Registrato lo **stato di allerta di Saarvith** per Fase 4 (sorpresa sì/no)?
