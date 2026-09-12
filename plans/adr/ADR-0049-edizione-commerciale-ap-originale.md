# ADR-0049 — L'edizione commerciale è un Adventure Path **originale autonomo**, mai un'espansione di *Red Hand of Doom*

**Stato**: 🔵 **proposta** — gate: **decisione del DM + verifica di un avvocato IP**

> ⚠️ **Non è accettata, ed è voluto.** Nasceva come ADR-0018 nella PR #72 (26
> luglio 2026) già in stato «proposta», e recuperarla non la promuove: sposta la
> proposta dove si può leggere e decidere. Delle cinque ADR della #72 tre sono
> ora a casa — [ADR-0039](ADR-0039-profili-regole-multisistema.md) (era 0016),
> [ADR-0040](ADR-0040-separazione-prodotto-e-toolkit-estraibile.md) (era 0017) e
> [ADR-0048](ADR-0048-legenda-funzionale-fonte-unica.md) (era 0014). La quarta,
> ex-0015 sulle dipendenze a livelli, **non si recupera**: la contraddice
> [ADR-0037](ADR-0037-stdlib-only-e-le-sue-eccezioni.md), decisa col DM il 3
> settembre.

**Data**: 2026-07-26 (corpo) · 2026-09-11 (recupero e rimisurazione)
**Estende** [ADR-0005](ADR-0005-confini-ip-uso-non-commerciale.md) senza sostituirlo, come ADR-0040 ha fatto per il toolkit.
**Misura**: [`AUDIT-DERIVAZIONE-IP-CAMPAGNA`](../../docs/audit/AUDIT-DERIVAZIONE-IP-CAMPAGNA.md) — **rifatto il 2026-09-11**, perché quello di luglio non era nel repo.

## Contesto

ADR-0005 stabiliva che il repo non è commercializzabile e che il blocco
WotC/Forgotten Realms è **assorbente per tutto il repo**. ADR-0040 ha mostrato
che quella conclusione valeva per il *contenuto*, non per il toolkit. Resta la
domanda vera: **il contenuto può diventare un prodotto?**

La misura dice quello che nessuno aveva quantificato: **la derivazione da RHoD
non è distribuita, è concentrata** — e rimisurata a settembre, su un repo
cresciuto, la tesi regge.

| Arco | Parole | RHoD per 1.000 parole |
|---|---:|---:|
| 04 · 06 | 40.213 | **0,0** |
| 07 | 128.318 | **0,2** |
| 08 | 127.406 | **0,7** |
| 09 | 178.338 | **5,6** |
| 00 (impalcatura) | 7.886 | 21,2 |

Le due spine narrative sono diverse: RHoD va da Guado di Drellin all'assedio di
Brindol; RumblingStone va dalla miniera alla Corona di Adamantio, ai piani
elementali, a Hammerfist, con antagonisti originali (Il Collezionista, Sonjak,
Therysol) e una riscalatura all'8° livello. L'arco 09 è l'eccezione, **per
scelta**: `PIANO-REINTEGRAZIONE-PNG-AP-RHOD`, chiuso il 2026-07-20, vi
reintegrò deliberatamente PNG e luoghi dell'AP originale.

## Decisione proposta

**Se e quando si pubblica, si pubblica un Adventure Path originale autonomo.
Mai un'espansione, un supplemento o un «sequel» di *Red Hand of Doom*.**

### 1. La via esclusa, e perché non ha varianti prudenti

Un'espansione *per* RHoD deve nominarlo: titolo, trama, cast, luoghi. Nessuna
licenza lo copre — l'OGL riguarda le meccaniche dichiarate Open Game Content e
RHoD non lo è; la Community Use Policy di Paizo è **non commerciale** e riguarda
IP Paizo; DMs Guild non licenzia RHoD ed è solo 5e. **La richiesta stessa è il
problema**: non esiste un modo più cauto di formularla.

### 2. La via scelta

AP originale autonomo, meccaniche sotto **OGL 1.0a** (3.5 e/o PF1e), più — per
PF1e — la **Compatibility License** di Paizo. Ambientazione, pantheon, geografia
e fazioni **originali**. I marchi «Dungeons & Dragons», «D&D» e il logo d20
**non sono usabili**: la d20 System Trademark License non è più disponibile.

### 3. Rinominare non basta

Il metro non è «ho cambiato i nomi» ma la **somiglianza sostanziale
dell'espressione protetta**: sequenza degli eventi, personaggi distintivi,
ambientazioni specifiche. Ogni sostituzione deve produrre un elemento che
**starebbe in piedi da solo**. «Mano Rossa» → «Artiglio Cremisi» è un sinonimo
trasparente e non serve a niente.

### 4. Perimetro della v1 — **aggiornato sulla misura di settembre**

| Materiale | Decisione | Numero di oggi |
|---|---|---|
| **Archi 07 + 08** | **dentro** — la base del prodotto | 255.724 parole a **0,2** e **0,7** |
| **Archi 01-05** | **dentro, ma da SCRIVERE originali** | 🔎 **confermato: sono vuoti.** 01, 02, 03 e 05 hanno **zero parole**; il 04 ne ha 2.838. Scriverli originali costa quanto scriverli derivati: è l'unico punto in cui diventare puliti è **gratis** |
| **Arco 06** | ⚠️ **riscrittura** | Undermountain a **3,9** — dimezzata da luglio (era 8,8) ma ancora la più alta del repo per quella fonte |
| **Arco 09** | **fuori dalla v1** | 178.338 parole a 5,6. Rientra solo dopo riscrittura sostanziale |
| **Arco 00** | si **rigenera** originale | impalcatura, 21,2 |
| 🆕 **`Bestiario/`** | **da decidere: la #72 non l'aveva guardato** | **3,0** su 74.978 parole, e **esce col modulo**. Un perimetro che dice «07+08 dentro» e tace sul bestiario lascia fuori il conto una dipendenza vera |
| 🆕 **Moduli autoconclusivi** | **già puliti** | `10-stand-alone` **0,0**, il Drappo **0,0** (3 occorrenze in 63.870 parole). Su quest'asse il prodotto della linea 3 di `PIANO-VENDIBILITA` **è pronto** |
| `campaign/`, `state.md`, i log, i booklet | **privati per sempre** | ed è il corpo più denso di tutti: **7,6** |

### 5. Moradin è un lotto narrativo, non una sostituzione

**1.680 occorrenze** oggi (erano 1.502 a luglio). L'SRD 3.5 esclude
deliberatamente i nomi delle divinità: Moradin è Product Identity. Ma è anche la
spina teologica di una campagna nanica — Cuore di Moradin, Corona di Adamantio,
Forgia Eterna. Va trattato come **riscrittura narrativa**, ed è il singolo lotto
di contenuto più grande dell'intera bonifica.

### 6. La bonifica si verifica in continuo

Un check `ip/forbidden-term` con la lista dei termini vietati come **dato
versionato**, severità `error` sul ramo commerciale e `info` su quello privato.
Una bonifica fatta a mano si erode alla prima sessione; una verificata in CI no.

## Conseguenze

**Cosa diventa più facile**

- esiste un prodotto di contenuto reale: **255.724 parole già scritte e pulite**
  (archi 07+08) più gli archi 01-05 da scrivere, che oggi sono **davvero vuoti**;
- il perimetro è **dichiarato e misurato**, invece di rimandare la domanda a ogni
  file nuovo;
- ogni contenuto nuovo può nascere già pulito, a costo zero.

**Cosa diventa più difficile**

- **si rinuncia all'arco 09 nella v1** — 178.338 parole, il volume maggiore, ed è
  il costo della scelta;
- la sostituzione del pantheon è settimane, non giorni;
- due varianti dello stesso contenuto vanno tenute allineate, o divergono. La
  commerciale **deriva** dalla privata con una trasformazione dichiarata, mai una
  copia a mano;
- 🔴 **questa non è consulenza legale.** La somiglianza sostanziale non è
  autocertificabile, e l'audit di §Misura lo dice di sé: conta i nomi, non la
  struttura.

**Cosa va rivisitato e quando**

- **la lezione della rev. 2 di luglio vale come metodo**: prima di dichiarare
  pulito un arco si cercano **tutte** le fonti che `campaign-history.md`
  dichiara, non solo quella che si ha in mente. Una misura parziale è più
  pericolosa dell'assenza di misura, perché dà fiducia;
- se un avvocato giudicasse insufficiente la trasformazione di 07-08, il
  perimetro si restringe — e la decisione va presa **prima** della produzione
  editoriale;
- la posizione del **bestiario** nel perimetro (§4) è una domanda aperta che la
  #72 non si era posta;
- l'arco 09 si rivaluta a sé, dopo la v1.
