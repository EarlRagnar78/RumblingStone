# I segreti dell'orda — solo per il DM

> **Per chi**: il DM. I giocatori leggono il libretto (`ARC08-18`), non questo
> file: quello che sta qui lo scoprono sul campo, quando succede.
> **Cosa c'è**: le capacità dei reparti dell'orda, le carte dell'avanguardia, e
> le scelte fatte fra i numeri dell'arco che non si accordavano.
> **Stato**: proposta (ADR-0096). Le capacità sono nelle simulazioni di
> `plans/esperimenti/battaglia-campale-2026-10-21/assedio_v3.py`; le carte
> dell'avanguardia in `avanguardia.py`.

---

## 1. Le capacità dei reparti dell'orda

Vengono dalle schede delle unità di `ARC08-02` §1 e §4, lette con i numeri del
libretto. Il DM le applica senza annunciarle; quando succedono, le racconta.

| Reparto | Capacità | Effetto nel libretto | Fonte |
|---|---|---|---|
| **Orchi** | **Carica selvaggia** | nel round in cui arrivano sul fronte: **+1** AU e **−2** DU | `ARC08-02`, unità orchi (AU +8 e DU 12 al primo round) |
| **Orchi** | **Furia** | a 4 PFU o meno: **+1** AU | `ARC08-02`, unità orchi (AU +8 a ≤4 PFU) |
| **Hobgoblin** | **Formazione tattica** | se sul fronte ci sono due o più reparti di hobgoblin, ognuno ha **+1** DU | `ARC08-02` e `ARC08-01`, unità hobgoblin |
| **Lupi e goblin** | **Sbilanciare** | il reparto nanico che hanno davanti ha **−2** al bianco | `ARC08-02`, unità worg (−2 DU al bersaglio) |
| **Giganti** | **Bombardamento** | il macigno ignora le merlature delle Mura | `ARC08-02`, giganti |

Come si raccontano, la prima volta:

- la Carica selvaggia è il muro di scudi che arretra di un passo sotto l'urto,
  e gli orchi che restano scoperti dopo;
- la Formazione tattica è il suono: gli hobgoblin avanzano al passo, al
  tamburo, e gli scudi si chiudono fra un reparto e l'altro;
- lo Sbilanciare sono i lupi che tirano le caviglie e i goblin che tagliano i
  tendini a chi cade.

## 2. Le carte dell'avanguardia (Sessione 1, libretto §13)

| Round | Carta | Effetto |
|---|---|---|
| 1-2 | **I lupi cavalcati** | un reparto di lupi e goblin per squadra, che sbilancia (§1) |
| 3 | **La pattuglia avanzata** | arrivano gli hobgoblin, il fronte di ogni squadra sale a due, e il **sergente** dà **+1** ad AU e DU di tutta l'avanguardia (`ARC08-02`, sergente hobgoblin) |
| 5 | **Il corno di Grimjaw** | Grimjaw è sulla cresta e non scende. Il corno dà **+1** ad AU e DU di tutta l'avanguardia, che fa +2 col sergente. È il momento dell'orda: va letto ad alta voce, e dice ai giocatori che restare costa |

Il sergente si può **Sfidare**: è il duello della retroguardia (libretto §13).
Il sergente è un hobgoblin guerriero di 6° livello con l'armatura completa;
se cade, il **+1** del sergente esce. Grimjaw non si sfida: guarda e ricorda
chi ha visto.

## 3. Le scelte fra numeri che non si accordavano

La ricerca nell'arco ha trovato fonti che si contraddicono. Il libretto ha
preso queste, e le altre restano dove sono senza correzioni in questo
giro.

| Cosa | Le versioni | Scelta del libretto |
|---|---|---|
| Massi dei giganti | AU +14 (`ARC08-02`), 3d8 a 120 m (`Mappe` L2), 2d8+12 (scontri) | la carta usa **AU +14**, la scheda dell'unità |
| Baliste | 6 con AU +10 (`ARC08-02`), 10 a +18 (`Mappe` L2), 12 (archivio) | una per torre, **d20 + 10**, perché nel libretto le altre stanno sui settori senza giocatore |
| Carica | +2 att/−1 CA, +2 att/+2 danni/+1 morale (due righe di `mass_combat_guide_Dm.md`) | l'ordine **Caricare**: +2 al rosso, −2 al bianco |
| Comandare | Car CD 15 (`ARC08-02`), Diplomazia CD 18 (`ARC08-01`) | il gesto **Comandare** senza prova |
| Trappole | 2d6, +2 danni, 4d6 ×3, −2 CA in quattro file | una trappola **annulla una tacca** del primo giorno |
| Morale | scala ±5 (`ARC08-02`), ±4 (variante 2d6), −6 (`Mappe` L3) | scala ±5, sui dadi al massimo ±2 (libretto §6) |
| Olio bollente | non c'è in nessun file | non c'è nemmeno qui |

Le strutture (mura 1.800 pf in `ARC08-02` contro 240 in `Mappe` L2) restano
fuori dal libretto: la breccia si misura con le tacche, non con i pf delle
mura.
