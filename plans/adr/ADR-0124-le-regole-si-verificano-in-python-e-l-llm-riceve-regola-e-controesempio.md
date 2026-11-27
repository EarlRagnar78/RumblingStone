# ADR-0124 — Le regole si verificano in Python, e l'LLM riceve la regola violata e il controesempio via MCP

**Stato**: proposta (2026-11-11); punti 3-5 scelti dal DM il 2026-11-11 («Strumento talenti in Python via MCP»)
**Data**: 2026-11-11
**Decisione-fonte**: il DM (Jfs), 2026-11-11: valutare lo stack «grafo di eventi + regole in Prolog + regola che fallisce o controesempio restituiti all'LLM perché si corregga», chiamato via server MCP, e misurare se l'adozione nel repo è possibile.
**Rapporti**: applica [ADR-0067](ADR-0067-il-confine-dichiarato-fra-codice-e-llm.md) (l'LLM è client, i verificatori sono deterministici) e [ADR-0030](ADR-0030-server-mcp-sui-tool.md) (server MCP); segue la regola dello standard di fatto del 2026-11-08. Misure in [plans/esperimenti/prolog-verificatore-2026-11-11/ESITO.md](../esperimenti/prolog-verificatore-2026-11-11/ESITO.md).

## Contesto

La proposta separa chi genera (l'LLM) da chi verifica (un motore logico), e
rimanda all'LLM la regola esatta che fallisce. La separazione c'è già:
ADR-0067 tiene l'LLM fuori dagli script, e `mcp_server.py` espone 137 tool. La
domanda vera era se un motore logico (Prolog, lo standard di fatto della
programmazione logica; clingo come alternativa ASP impacchettabile) verifica
meglio del Python che c'è.

Banco: i prerequisiti dei talenti sulle 74 schede del Bestiario che li
elencano, gli stessi fatti dati a tre motori, più 141 difetti iniettati.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Python, regole come dati TOML, uscita strutturata via MCP** (scelta) | trova 141/141 difetti iniettati e le stesse 30 violazioni vere; 0,8 ms; nessuna dipendenza nuova; un solo linguaggio per le regole | le regole ricorsive o temporali vanno scritte a mano |
| SWI-Prolog (BSD-2) | regole dichiarative e leggibili; ricorsione e ricerca del controesempio gratis | stessi 141/141 e 30, **0 difetti in più** dalla chiusura transitiva; binario di sistema che non entra nel bundle offline; ponte janus solo da 9.1 (Ubuntu 24.04 ha 9.0.4); 70× più lento per il processo |
| clingo (ASP, MIT) | ruota PyPI per Python 3.13, si porta nel pacchetto; 14 righe di regole | stessi risultati; seconda lingua nel repo, con 3 falsi positivi introdotti al primo giro dalla traduzione dei fatti (costanti contro stringhe) |

## Decisione

1. **Nessun motore logico nel repo per ora.** La misura boccia lo standard
   (Prolog) e l'alternativa (clingo) non perché sbaglino, ma perché non trovano
   niente in più e costano un secondo linguaggio e, per Prolog, un binario
   fuori dal pacchetto.
2. **Si adotta il pattern, non il motore**: ogni verificatore di regole che
   l'LLM chiama via MCP restituisce per ogni violazione `regola`, `atteso`,
   `ha` e `file:riga`, in JSON, oltre al testo per il DM.
3. Il primo verificatore così è `scripts/verifica_talenti.py`: i
   **prerequisiti dei talenti sulle schede esistenti**, che prima nessun
   cancello controllava. È nel manifest, quindi nel server MCP, in sola
   lettura, e in canale testing (ADR-0099): misura, non cancello. La regola è
   `dmcore.talenti.violazioni`, la stessa di `manca` e del generatore. Esclude
   i talenti bonus senza prerequisiti (monaco, stili del ranger) e le
   competenze della classe; senza classi dichiarate, livello d'incantatore e
   classe vanno fra i non verificabili. Sul Bestiario: da 30 violazioni in 19
   schede (banco) a **21 in 11** (tolti 9 falsi positivi). Le 21 vanno al DM.
4. D1 e D2 sono corretti in `talenti.manca`: una classe 3.5 vale col nome
   inglese e italiano, e `character` sono i dadi vita totali (`Stato.dv`).
   Nell'impronta delle creature cambiano solo i talenti che la correzione
   vuole: Autorità ai comandanti, Arma Specializzata e Arma Focalizzata
   Superiore ai guerrieri, Padronanza degli Incantesimi al mago.
5. Il giro di correzione ha un test (`test_verifica_talenti.py`): scheda
   segnalata, corretta come dice la violazione, `--check` passa da 1 a 0.

6. **Ordine delle fonti (DM, 2026-11-12): SRD d20 → D&D 3.5 → PF1e.** Una
   scheda 3.5 si verifica prima sull'SRD 3.5 (base, mostri, epici, psionici,
   divini: 363 talenti), poi sui manuali 3.5 fuori SRD
   (`sistemi/dnd35/dati/talenti_manuali.toml`, 2.193 talenti con i
   prerequisiti dai dati PCGen di BahamutDragon/pcgen e dalle tabelle dei
   manuali su srd.dndtools.org, solo nome e soglie; dove le due fonti
   divergono vince la tabella del manuale),
   poi sul PRD PF1e. Ogni voce dell'uscita porta `fonte`. Un nome dell'SRD
   vince sempre su un manuale, e il generatore continua a scegliere solo dai
   libri base. Un talento di cui il repo ha solo il nome (1.715 su 3.998), o
   una scheda con classi che la lettura non conosce, va fra i **non
   verificabili**: non passa per buono e non viene segnato come sbagliato.

7. **Una chiamata per scheda**: `scripts/verifica_scheda.py` (manifest, server
   MCP, sola lettura, canale testing) restituisce nella stessa forma i
   prerequisiti dei talenti e i numeri di `conformita_statblocchi.giudica`
   (pf, BAB, tiri salvezza, lotta, attacco, iniziativa), più i **gradi delle
   abilità**: capacità nuova `creature.gradi` nei plugin `dnd35` (dall'SRD) e
   `pf1e` (dal PRD), con massimo per abilità e punti disponibili calcolati sui
   gradi minimi che il bonus scritto chiede. Sulle schede vere 0 segnalazioni;
   con errori inseriti vede 18 su 29 abilità gonfiate di 8 e 3 su 29 gonfiate
   di 4: il margine è largo per non segnalare schede giuste.
   Misura con errori messi apposta: 666 su 1.278 visti (52%); il resto e
   l'ordine in cui chiudere il divario dei plugin stanno in
   [plans/esperimenti/verifica-scheda-2026-11-12/ESITO.md](../esperimenti/verifica-scheda-2026-11-12/ESITO.md).

8. **Classi dei manuali 3.5 fuori SRD** (DM, 2026-11-12: «solo nomi e
   numeri» dalle fonti non OGL). `sistemi/dnd35/dati/classi_manuali.toml`, 658
   classi da srd.dndtools.org e PCGen. Entrano nei conti (`dmcore.progressione`)
   solo quelle con numeri regolari e su cui le due fonti non divergono; le
   altre restano «non verificabili». Un nome dell'SRD vince sempre, e un nome
   dei manuali vale solo scritto intero. Misura: numeri sbagliati visti da 666
   a 701 su 1.278, non verificabili da 82 a 76, 4 schede del Bestiario ora
   leggibili (ESITO §2-ter).

9. **Prerequisiti fisici letti dalla scheda** (DM, 2026-11-12: tipi,
   movimenti, ambienti). Volo, nuoto, scalare, scavare, taglia, tipo, attacchi
   naturali, armatura naturale, soffio e tiri salvezza base si leggono dalla
   scheda e si confrontano col prerequisito del talento (regola `fisico`).
   Senza la riga nella scheda il prerequisito resta non verificabile. Non
   verificabili da 76 a 47, nessuna violazione nuova (ESITO §2-quater).

10. **Incantesimi contro le liste di classe.** Capacità nuova
    `creature.liste_incantesimi` (dnd35 dall'SRD, pf1e dal PRD che c'era già).
    `verifica_scheda` segnala l'incantesimo fuori dalla lista della classe
    (`incantesimo.lista`) e quello scritto sotto il suo livello
    (`incantesimo.livello`); un nome che le liste non hanno resta non
    verificabile. 6 violazioni sulle schede vere; errori messi apposta visti
    167 su 170 (ESITO §2-quinquies).
11. **Chiusura delle violazioni e liste dei manuali** (DM, 2026-11-12:
    «correggi gli errori», e prima di chiuderli finire le classi).
    - Liste di incantesimi dei manuali 3.5 da PCGen, solo nomi e livelli:
      `sistemi/dnd35/dati/liste_incantesimi_manuali.toml` (3.969 incantesimi,
      84 classi, 102 domini, 62 classi che pescano da liste altrui). L'SRD
      vince dove c'è; le voci con una condizione (divinità) restano fuori; un
      dominio dei manuali vale solo dove la scheda segna l'incantesimo come di
      dominio.
    - La classe che lancia si legge anche quando l'intestazione non la nomina
      (l'unica classe incantatrice scritta con il livello più sopra): le righe
      fuori dal controllo scendono da 94 a 16.
    - Razza, sottotipo e allineamento come prerequisito, letti dalla riga del
      tipo. Sulle schede di oggi non cambiano nessun esito.
    - Tre regole che tolgono falsi positivi: il talento bonus «(B)» della
      creatura con dadi vita razziali (SRD, *Monster Feats*), il talento che la
      classe del manuale concede (`talenti_concessi` in `classi_manuali.toml`,
      19 classi), il talento che ne vale un altro come prerequisito
      (`talenti_equivalenti.toml`). Dove le due fonti di un talento dei manuali
      divergono, o il file porta più schede, la voce passa fra i non
      verificabili con il motivo.
    - Violazioni 34 → 7: 12 erano falsi positivi dello strumento, 16 corrette
      in 9 schede (ogni scheda ha la nota «correzione 3.5 da
      verifica_scheda.py»), 1 nuova trovata dalle righe prima non lette. Le 7
      rimaste sono vere anche con i dati delle classi dei manuali e vanno al DM
      (ESITO §2-sexies).


## Conseguenze

- L'LLM riceve la regola esatta e il controesempio senza imparare un motore
  nuovo, e il server MCP che c'è basta.
- Il pacchetto resta senza binari di sistema nuovi.
- Si rinuncia alla ricorsione e alla ricerca dichiarativa: una regola come «chi
  sa cosa, attraverso chi, entro quale giorno» va scritta in Python.
- Il giro di autocorrezione (messaggio libero contro uscita strutturata) **non è
  misurato**: resta da fare col protocollo di ESITO §5.

- I dati PCGen non dichiarano una licenza e srd.dndtools.org riporta manuali
  non OGL: si tengono solo fatti di regola (nome, soglie), e il file si può
  togliere senza toccare il codice. Le due fonti divergono su 353 talenti su
  1.156: una violazione da manuale si rilegge sul libro prima di correggere.

**Da rivedere se**: arriva un dominio con regole davvero ricorsive o temporali
su fatti già strutturati (per esempio §4 «chi sa cosa» di `state.yaml` con una
colonna Tempo), oppure le regole Python di un dominio superano le 300 righe e un
banco di mutanti mostra che la versione dichiarativa trova difetti che il
Python perde.
