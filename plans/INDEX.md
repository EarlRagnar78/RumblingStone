# 📚 ARCHIVIO PIANI — INDICE

> **Cos'è**: la vista d'insieme di tutti i piani di lavoro della campagna
> (revisioni, infrastruttura), con stato, % di completamento, lotti
> rimanenti e gate. Creato dal Lotto **K-A** del piano DM-TOOLKIT (K-D3).
>
> **Regola di manutenzione** (regola d'oro 4 dei piani): *chi chiude un
> lotto aggiorna — nello stesso commit — (1) la checklist del piano,
> (2) la riga qui sotto, (3) una riga in `plans/CHANGELOG.md`.*
>
> Le decisioni architetturali (il "perché" delle scelte di struttura)
> vivono in `plans/adr/`.

## Stato dei piani

| Piano | Ambito | Stato | % | Lotti/task rimanenti | Gate |
|---|---|---|---|---|---|
| [PIANO-REVISIONE-ARC07](PIANO-REVISIONE-ARC07-COERENZA-E-QUALITA.md) | Arco 07 — Portale della Forgia Eterna | 🟡 quasi completo | ~95% | B1 parziale: date/XP/loot **reali** dei log ricostruiti | sessioni giocate al tavolo |
| [PIANO-REVISIONE-ARC08](PIANO-REVISIONE-ARC08-COERENZA-E-QUALITA.md) | Arco 08 — Battaglia di Hammerfist | ✅ completo | 100% | — | — (l'arco resta ⬜ da giocare: il *piano* è chiuso, il *gioco* no) |
| [PIANO-REVISIONE-ARC09](PIANO-REVISIONE-ARC09-COERENZA-E-QUALITA.md) | Arco 09 — post-Hammerfist | ✅ completo | 100% | — | — (idem) |
| [PIANO-REVISIONE-TRASVERSALE](PIANO-REVISIONE-TRASVERSALE-COERENZA-E-QUALITA.md) | Rituale P3B · Mappe · Artefatti (tutta la campagna) | 🟡 gated dal tavolo | ~95% | T8 (sinergie Collana) · chiusura T9 (esito P3B in state.md §8) · SVG dei 16 narrativi (opzionale/estetico) | T8: quest ARC-09 giocata · T9: P3B giocato |
| [PIANO-DM-TOOLKIT](PIANO-DM-TOOLKIT-HYPE-E-ARCHIVIO-PIANI.md) | Infrastruttura: CLI dm.py · hype Homebrewery · questo archivio | ✅ completo | 100% | — | — (code da tavolo: verifica visiva dei brew al collaudo del container; piloti lettera/avviso-torneo quando il DM fornisce testo canone) |
| [RICERCA-GENERATORI-MAPPE](RICERCA-GENERATORI-MAPPE-QUALITA-RHOD.md) | Infrastruttura: pipeline mappe qualità AP — renderer "pergamena", import Watabou, export PNG, skill `rumblingstone-mapmaking` | 🟡 completo + follow-up in review | ~100% | Ultra-Clear P4 Piano Terra (PR #42 **aperta**, non mergiata) | — (hero map ComfyUI: opzionale, macchina DM con GPU; giudizio a occhio caso per caso) |
| [INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ](PIANO-INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITA.md) | Infrastruttura: 3 modalità mappa, contratto JSON+validatore (Mod. 3), export UVTT/dd2vtt (Foundry/Roll20), infra container ComfyUI su Bazzite, **overlay professionale mappe** (bussola/movimenti/callout/zone, ADR-0006), direzione artistica IP-safe | 🟡 M1-M5 implementati, collaudo al tavolo | ~92% | collaudo DM: import `.uvtt` in Foundry, setup container ComfyUI su GPU; opz.: convertire Campo Drow 2/3 in JSON | collaudo al tavolo/macchina DM |
| [PIANO-AUTOMAZIONE-STATO-SESSIONI](PIANO-AUTOMAZIONE-STATO-SESSIONI-BRANCH-GRUPPO.md) | Infrastruttura: `dm.py session` — wizard fine-sessione, apply engine `state.md` (regioni marcate), visibilità per-PG, brief prossima sessione, branch-per-gruppo con guardia su `main` | 🟢 implementato (A-F ✅, LLM E-bis escluso per decisione DM; [ADR-0007](adr/ADR-0007-scritture-canone-triplo-vincolo.md); wizard, per-PG, hook ❓, 31 test in CI; Quick Guide nuovi DM) | ~98% | — | collaudo al tavolo del flusso `session end` alla prima sessione reale |
| [PIANO-REINTEGRAZIONE-PNG-AP-RHOD](PIANO-REINTEGRAZIONE-PNG-AP-RHOD.md) | Contenuto: reintegrazione PNG dell'AP originale (Guado di Drellin, Rethmar 2° anello, Witchwood/Tiri Kitor, Wyrmlord) + proposta PNG caotico Lirien | 🟡 R1+R5+R7 fatti e **canonizzati** (2026-07-20), R2-R4 preparazione | ~65% | R2 (Rethmar 2° anello) · R3 (Witchwood/Tiri Kitor) · R4 (Wyrmlord, decisione DM) | R4: decisione DM |
| VERIFICA LEGALE-IP (P2D "Palio") — [ADR-0005](adr/ADR-0005-confini-ip-uso-non-commerciale.md) · [rapporto](../09_Continuazione%20Arco%20Narrativo%20dopo%20Battaglia%20di%20Hammerfist/Arco-Post-Hammerfist-P2D-PALIO-VERIFICA-LEGALE-IP.md) | Conformità IP: Regolamento/Consorzio Palio di Siena + blocco WotC/Forgotten Realms | ✅ verifica completata (PR #47) | 100% | bonifica §7 (rinomina contrade/livree/motti, "Piazza il Campo", riambientazione fuori FR) — **solo se** si punta a edizione commerciale | decisione DM su uso commerciale (non presa) |

## Prossimi passaggi (volutamente in bianco — si riempiono al tavolo / su decisione DM)

### PIANO-REVISIONE-ARC07
- ⬜ _(da definire al tavolo: date/XP/loot reali per chiudere B1)_

### PIANO-REVISIONE-ARC08
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-ARC09
- ⬜ _(nessuno pianificato — eventuali emergenze dal gioco dell'arco)_

### PIANO-REVISIONE-TRASVERSALE
- ⬜ _(T8: quando la quest ARC-09 di Hella è giocata)_
- ⬜ _(chiusura T9: quando il P3B è giocato — esito reale in state.md §8)_

### PIANO-DM-TOOLKIT
- 🟡 _(K-B3.9 — tavole di Channathgate ricollocate in `immagini/` + ridimensionate con Pillow: **PR #46 aperta**, non mergiata; le tavole PNG del DM sono già su main via `ed56aa6`)_
- ⬜ _(riapertura estetica K-B0 solo se il DM indicherà template specifici del pack)_
- ⬜ _(collaudo al tavolo: container + brew I-V; piloti lettera/avviso-torneo quando arriva testo canone)_

### RICERCA-GENERATORI-MAPPE
- 🟡 _(P4 Piano Terra → griglie Ultra-Clear, dall'agguato Xorn al boss Terros: **PR #42 aperta**, non mergiata — quando merge, tracciare qui e in CHANGELOG)_
- ⬜ _(opzionale/estetico: portare a griglia Ultra-Clear le altre mappe KO del censimento — Torre P2A, Torneo P2B, Battaglia Finale P3 — ora che il renderer c'è)_
- ⬜ _(mappa regionale Cannath Vale/Dalelands con Azgaar FMG — `.map` master + export in rendered/)_
- ⬜ _(hero map ComfyUI sulle 2-3 mappe chiave — solo su macchina DM, vedi skill mapmaking)_

### INTEGRAZIONE-PIPELINE-MAPPE-3-MODALITÀ
- ⬜ _(collaudo DM: generare una mappa Mod. 3 reale da JSON per un incontro ARC-08/09 e renderla)_
- ⬜ _(collaudo DM: importare un `.uvtt` in Foundry e verificare muri/luci)_
- ⬜ _(collaudo DM: setup container ComfyUI su Bazzite con GPU + hero map su una mappa chiave)_

### PIANO-AUTOMAZIONE-STATO-SESSIONI
- ⬜ _(collaudo al tavolo: primo `dm.py session end` — wizard incluso — su una sessione reale del gruppo, sul branch `campaign-group-rumblingstone-dm-gianfranco`)_
- ⬜ _(opzionale, decisione DM futura: lotto E-bis LLM per evoluzioni narrative — oggi escluso)_

### VERIFICA LEGALE-IP (P2D "Palio")
- ⬜ _(bonifica §7 — rinomina contrade, cambio livree, riscrittura motti da zero, rimozione "Piazza il Campo", riambientazione fuori Forgotten Realms: **gated** su una decisione DM di puntare a un'edizione commerciale, non ancora presa — vedi ADR-0005)_
- ⬜ _(debito documentale a bassa priorità: correggere la nota IP interna che dichiara i motti "originali" — sono parafrasi §3.3; documentare provenienza/licenza delle 2 tavole PNG del DM)_

### PIANO-REINTEGRAZIONE-PNG-AP-RHOD
- ⬜ _(R2 — secondo anello di Rethmar: Tredora Goldenbrow, Immerstal il Rosso, Capitano Ulverth, Teyani Sura)_
- ⬜ _(R3 — Witchwood/Tiri Kitor: Vecchio Warklegnaw, Trellara Nightshadow + mini-dossier cross-link per Sellyria/Killiar/Illian)_
- ⬜ _(R4 — Wyrmlord mancanti: Ulwai Stormcaller; decisione DM su Hravek Kharn vs Karruk)_
- ✅ _(R6 — canonizzazione DM di R1+R5 avvenuta il 2026-07-20: flag sciolti, righe applicate a state.md §1/§3/§7/§8)_
- ✅ _(R7 — Mira Serani «l'Aranea»: reintegrata + twist figlia-di-Lorana; statblock **canon CR 8** calibrato PG 8-9 (ramo APL-13 CR 11/13-14 nel dossier); collisione risolta: «Mira del Traghetto» → «Nania Seriv del Traghetto»)_
