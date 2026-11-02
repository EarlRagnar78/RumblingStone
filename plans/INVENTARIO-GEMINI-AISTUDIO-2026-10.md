# Inventario di Gemini e Google AI Studio contro il repo

> **Richiesta del DM, 2026-10-23**: *«vedere se ci sono dei contenuti su gemini
> o Google ai studio che sono stati persi relativi a rumblingstone e che non
> sono presenti sul repo»*.
> **Cosa c'è qui**: per ogni file di Drive legato alla campagna, la versione più
> recente, quanto ne sta già nel repo e cosa manca. **Cosa non c'è**: il
> contenuto dei file. Restano privati su Drive e qui se ne scrive solo una
> descrizione breve. Nessuna voce è decisa: il canone del repo vince, e ogni
> divergenza la valuta il DM.

## 1 · Cosa si è guardato e cosa no

| Fonte | Guardata | Note |
|---|---|---|
| Cartella Drive «Google AI Studio» | sì, tutti i 182 file elencati | Circa 45 riguardano RumblingStone. Gli altri sono lavoro BIOME e di sistema (codice R, Nginx, Proxmox, i «Paste» di maggio 2026) e una campagna diversa (`applet_access_history.json`, PF2e). |
| Documento «Encanced with data scient rumblingstone repos» (Google Doc e `.odt`, 2026-09-16) | sì | Vedi §4. |
| Documento «Red Hand of Doom 3.5 Conversion» (2026-03-21) | sì | Vedi §4. |
| `RedHandOfDoom.zip` (8 MB) | **no** | Non aperto. |
| Le chat dell'app Gemini (gemini.google.com) | **no, non si può** | Non stanno su Drive. Si vedono solo se il DM le esporta (Google Takeout, «Le mie attività nelle app Gemini»), e allora si ripete questo confronto. |
| Le chat di AI Studio con immagini (10-53 MB) | **no** | Il connettore di Drive non scarica file sopra i 10 MB circa. L'elenco è in §5. |

**Metodo.** Ogni file è stato scaricato e decodificato (le chat di AI Studio
sono JSON: si tiene il testo dei turni, non i «pensieri» del modello). Per le
chat, la versione più recente è l'ultimo turno del modello su quell'argomento.
Ogni riga lunga almeno 40 caratteri, normalizzata, è cercata in tutti i `.md`
tracciati dal repo (`git ls-files`); la percentuale è la quota di righe
trovate. Dove la percentuale è bassa ho cercato a mano i termini più
riconoscibili (nomi, titoli di sezione). Una percentuale alta non dice che il
testo è identico, dice che le righe ci sono; una bassa può voler dire anche
che il repo ha la stessa cosa riscritta.

## 2 · I file `.md` di Hammerfist (settembre-ottobre 2025)

| File su Drive | Versione presa | Nel repo | Cosa manca |
|---|---|---|---|
| `00_Final_hammerfist_battle-…-Guida_Completa_del_DM.md` | 2025-10-03, `1hdLUigR7k601skVCfaZqb2i0xNxbLG4p` | 97% | Niente di sostanza: sta in `ARC08-01-GUIDA-DM.md` e nella revisione D13. |
| `hammerfist_battle-…-Guida_Completa_del_DM.md` (67 KB) | `1MagkBsGtgRjKoh9Ptk5mSagNqvgAwBbM` | 61% | Bozze precedenti di statblocchi e sessioni, superate dalla versione `00_Final`. |
| `hammerfist_encounters-…-final.md` | `1aJPudqU7i1EG5WuTxARfxVO_4S17oDNu` | 99% | Niente. |
| `hammerfist_armies_update_to_be_finished.md` | `1S9JVEBVhTsOZd88sg_NIX2gcr8g7mNgO` | 86% | L'indice dell'esercito e alcune sezioni di unità: Hobgoblin Warrior 3, cavalieri di worg, sacerdoti di guerra della Mano del Destino, adepti di guerra, appendice C dei PE. |
| `hammerfist_maps.md` | `197bnameFRN9zkUh3GVfoc5fmUy0jc1fm` | 45% | Le versioni «rielaborate» delle mappe 1A-1 e 1A-2, con viste dall'alto, di lato e di fronte. |
| **`battle_stats_maps.md`** | `17qMbTQO_4iNvCuZRPYSUbPUej8rfFLrG` | **quasi assente** | Gli «Spaventadraghi» (*Dragon Scarers*); la scala della magia nel combattimento di massa (un livello d'incantesimo = un'unità); le tabelle dei punti ferita di mura e strutture (1.800 pf); le statue ancestrali; le conversioni danno → unità; le fasi da boss di Gorthak, Grimjaw e Fauci. ⚠️ `ARC08-90-DEPRECATO-battle-stats-maps.md` nel repo ha un nome simile ma è un altro atlante. |
| `hammerfist_battle_timeline.md` (4 KB) | `1OBQ1XONtvdJXOypOpXTX_xn1-NfSFT_E` | in parte | Gli schemi ASCII dello schieramento (900 attaccanti, 300 difensori), il combattimento aereo, i cavalieri di worg, i giganti. I cavalieri di worg goblin ci sono (`ARC08-01`, `ARC08-02`); il «contatto stimato al round 9» e la sezione «Mappe aggiornate con layout» no. |
| `00_ATLANTE VISIVO DELLA BATTAGLIA DI HAMMERFIST-complete.md` | 2025-10-03 | probabile | Stessa dimensione dell'atlante v3 in archivio (32.821 contro 33.170 byte). Non confrontato riga per riga. |
| `mass_combat_guide_Dm.md` | — | probabile | Su Drive 16,5 KB, nel repo 20,4 KB: il repo ha la versione più lunga. Non confrontato riga per riga. |
| `hammerfist_armies_update.md` (6,8 KB) | — | **non scaricato** | Da fare. |

## 3 · Le chat di AI Studio

Le righe in grassetto sono quelle dove manca di più.

| Chat | Modello, data | Nel repo | Cosa manca, e se diverge dal canone |
|---|---|---|---|
| Aggiornare Battlestats e Mappe | gemini-2.5-pro | 76% | Il resto sono passaggi intermedi. |
| Guida Completa Battaglia Hammerfist | — | 73% | **Il «Manuale da campo del DM»** (turno 10): schede rapide di PNG e unità con un «profilo tattico». Assente (4 righe su 92). |
| Hammerfist: Guida DM Unificata | — | 56% | La sezione «Giorno 3: il Soffio della Disperazione» (turno 18), assente (0 su 17). |
| Estratto Battaglia Hammerfist: Mappe Tattiche | — | 65% | Varianti delle mappe tattiche. |
| Player Sheets For Red Hand | — | 75% | Sta negli atlanti deprecati di `_ARCHIVIO` e in `ARC08-02`. Manca la «Mappa 2C, vista frontale» (turno 41). |
| Sistema Combattimento Massa D&D 3.5 | — | 6% | Le prime statistiche delle unità e le «Mappe tattiche rielaborate 1A». In gran parte superate da `mass_combat_guide`. |
| **Branch of Sistema Combattimento Massa** | — | **3%** | Il cambio di patrono da Gruumsh a Tiamat, un esercito di 950, la Legione della Zanna Spezzata, la coorte degli Skullcrusher e **tre mini-boss**: Krusk lo Sfonda-Cancelli (GS 13), Vreek del Volto Fantasma (GS 9), Ur-Vrax Voce del Drago (GS 8). Nessuno dei tre è nel repo. |
| **Organizing D&D Campaign Info** | — | **0%** | Statblocchi alternativi di Fauci di Palude, Gorthak, Orion Pelleorsa e di alcune unità (bugbear infiltratori, cavalieri dei gufi celesti) e una «checklist eroica». ⚠️ Divergono dalle schede canone di ADR-0091. |
| Corona di Adamantio: Rituali Completi e Attivazione | — | 19% | I turni 20-24: conseguenze sullo stratega nemico, la difesa della Forgia contro Grimjaw e poi contro Fauce di Palude, l'«Atto di sfida divina». In parte sta in `Evoluzione_della_Scena-Trial_of_the_Deep_Hall.md`. |
| Corona di Adamantio: Prima rituale e Conseguenze | — | 44% | Varianti della guida al rituale. |
| Branch of Corona di Adamantio: Prima rituale | — | 50% | Le varianti della «Guida onnicomprensiva» sono in `06_Stanza-corona-di-adamantio` e in `PG/Artefatti`. |
| Custom D&D Magic Item Creation | — | 0% | La genesi della Corona dalla fusione con la *Earthcrown*. Superata dal canone. |
| D&D 3.5 Adamantine Crown Quest | — | 0% | Una prima idea ambientata a Undermountain («Gordruld's Crown of Earth's Fury»). Superata dal canone. |
| D&D 3.5 Prestige Class Update · Prestige Class Update Instructions | — | assente | L'HTML della classe di prestigio «Lord of Sun and Shadow» con progressione da stregone e una correzione della RD. Nel repo c'è solo l'analisi del PDF, e nel canone Artemis ha rifiutato questa classe. |
| Battle of the Hammerfist Mountains | gemini-2.0-flash, marzo 2025 | quasi assente | La prima bozza narrativa: re Baruk Barbadipietra, dodici aquile giganti celesti, il grido «Baruk Khazâd!». Superata: il canone ha i gufi e Re Thorek. Il nome Baruk compare in 7 file del repo. |
| Sanctuary Encounter: Dread and Decay | gemini-2.5-flash-image | presente | La traduzione del box della sala del trono di Belkram (il drow coi tentacoli, Urialle) sta in `Descrizioni_finali_italiano.md`. |
| Ottimizzazione Toolchain Sviluppo e Campagna | gemini-3.8-flash, 2026-10-08 | ripreso | Un meta-prompt sull'ambiente di sviluppo; le sue idee sono già in ADR-0099 (PR #273). |
| Ai music generation · Untitled prompt (due) · Cannot Access URLs for Data · Bard/Shadowdancer 15-Point Build · Half-Orc Oracle Battle Build · Pathfinder Rage Prophet Build · Porting PCGen To Python | — | **non aperte** | Potrebbero riguardare la campagna (le build, il porting di PCGen); da guardare in un secondo giro. |

## 4 · I due documenti fuori cartella

| Documento | Nel repo | Cosa manca, e se diverge |
|---|---|---|
| «Encanced with data scient rumblingstone repos» (2026-09-16) | ripreso | La pipeline LLM/RAG/Mixer, l'estrattore differenziale, il parser cartografico. Sono già in [PIANO-PIPELINE-IBRIDE-GROUNDING-E-MISURA](PIANO-PIPELINE-IBRIDE-GROUNDING-E-MISURA.md) («Estrattore Differenziale»). |
| **«Red Hand of Doom 3.5 Conversion»** (2026-03-21, ha la forma di un Deep Research di Gemini) | **in gran parte assente** | La mappa del Channath Vale; la «soglia della morte dell'eroe» nell'assalto a Tiere; la deviazione nel Sottosuolo; i frammenti d'anima, il «marciume del Sottosuolo», il Tempio della Città Finale, l'aura della corona del Comando di Ferro, i punti vittoria. ⚠️ Diverge dal canone in più punti (parte dal 8° livello, scrive «Channath» per Cannath). |

## 5 · Le chat che non si sono potute scaricare

Sono chat con immagini, fra 10 e 53 MB: Fantasy Medievale Immagini per PG ·
Fantasy Medievale Mappe D&D · Fortezza Nanica Mappa Tattica · Map Images for
RPG · Mappe Fantasy Medievali: Sentiero Nascosto · Maps: Forgotten Realms
Fantasy · Orchi su Lupi al Crepuscolo · Crown of Adamantio With Gems · D&D
Villains Updated For Level 13 (13 MB) · Hero's Comical Nighttime Crash (39 MB).

La più probabile da contenere testo che conta è «D&D Villains Updated For
Level 13». Per guardarle serve che il DM le esporti (o le scarichi da AI
Studio) e le metta in `/mnt/project-files/`, fuori dal repo.

## 6 · Da decidere al DM

<!-- decisioni-dm: INVENTARIO-GEMINI-AISTUDIO -->
| # | Voce | Proposta |
|---|---|---|
| D1 | `battle_stats_maps.md`: Spaventadraghi, magia nel combattimento di massa, pf delle mura, statue ancestrali, fasi da boss | Si riprende come proposta in ARC-08 (MASTER-DEF), con le regole confrontate con l'SRD; quello che diverge da ADR-0091 resta fuori. |
| D2 | I tre mini-boss di «Branch of Sistema Combattimento Massa» (Krusk, Vreek, Ur-Vrax) e il patrono Tiamat | Restano fuori finché il DM non dice se Tiamat è mai stato canone; i mini-boss possono entrare nel Bestiario come proposta. |
| D3 | Il «Manuale da campo del DM» e il «Giorno 3: il Soffio della Disperazione» | Si confrontano con `ARC08-01` quando si scrive il master definitivo di ARC-08. |
| D4 | Statblocchi alternativi di «Organizing D&D Campaign Info» | Restano fuori: le schede canone sono quelle di ADR-0091. |
| D5 | «Red Hand of Doom 3.5 Conversion» | Si legge come fonte di idee per ARC-09, senza importare nulla. |
| D6 | Le chat non scaricate (§5), le sette non aperte (§3), `RedHandOfDoom.zip`, `hammerfist_armies_update.md`, le chat dell'app Gemini | Secondo giro solo se il DM esporta le chat dell'app Gemini o mette i file grandi in `/mnt/project-files/`. |

## 7 · Note oneste

- La percentuale misura righe uguali, non idee. Un contenuto riscritto nel repo
  con parole diverse risulta «mancante»; per le voci in grassetto l'ho
  controllato a mano con i termini propri, per le altre no.
- Le chat dell'app Gemini sono escluse del tutto: se c'era qualcosa di perso,
  è più probabile che sia lì.
- I file di Drive restano su Drive. Nel repo entra solo questo inventario.
