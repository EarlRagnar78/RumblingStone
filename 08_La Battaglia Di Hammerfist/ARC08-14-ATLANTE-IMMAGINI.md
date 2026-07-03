# ARC-08 — Atlante delle Immagini (classificazione)

> **Scopo**: rendere usabile a colpo d'occhio il materiale visivo
> dell'arco (~42 file in `immagini/`). Ogni immagine → mappa/scena →
> sessione → prompt d'origine (se rintracciabile) → **quando mostrarla**.
> **Stato**: canonico (indice visivo; piano ARC-08 C3). **Ultima
> revisione**: 2026-07-02.
> **Fonte prompt**: `campaign/ai-media-prompts/09_ARC08_battaglia-
> hammerfist.md` (5 prompt di scena nominati: 3.1 Generale e l'Orda /
> 3.2 Difesa delle Mura / 3.3 Soffio di Fauci / 3.4 Ultima Resistenza /
> 3.5 Ritorno dei Rumbling Stones).
> **Nota rinomina**: la cartella `immage_campaign/` → **`immagini/`**
> (typo corretto, C3). La rinomina dei singoli file allo schema
> `hammerfist-sNN-descrizione.webp` è **proposta** nella colonna
> "nome suggerito" ma **non ancora applicata** (nessun file .md
> referenzia le immagini per nome reale → rinomina a basso rischio ma
> differita a una passata dedicata; qui si fissa la classificazione).

---

## 1. Legenda confidenza

- **✅ Confermata** = immagine vista e identificata.
- **🟡 Variante** = variante evidente di un'immagine confermata (stesso
  soggetto).
- **🔵 Da confermare a vista** = classificata al gruppo (mappa/scena
  generata) ma non pinnata al singolo master senza ulteriore vista.

---

## 2. Immagini illustrate (arte di scena) — root `immagini/`

| File | Confidenza | Mappa/scena | Sessione | Prompt | Quando mostrarla | Nome suggerito |
|---|---|---|---|---|---|---|
| `sentieroNascosto.webp` | ✅ | 1A-1 Sentiero Nascosto (3 worg) | 1 | — | Ricognizione, incontro pattuglia worg | `hammerfist-s1-sentiero-nascosto.webp` |
| `00_PM.webp` | ✅ | 1A-1 recon (pregen B/D/T/N) | 1 | — | Apertura ricognizione, i 4 pregen osservano | `hammerfist-s1-recon-pregen.webp` |
| `torreVedetta.webp` | ✅ | 1A-2 Torrione di Vedetta | 1 | — | Salita al torrione, osservazione | `hammerfist-s1-torrione.webp` |
| `01.webp` | ✅ | 1A-2/1A-3 Dara col cannocchiale | 1 | — | Dara osserva il campo nemico | `hammerfist-s1-dara-cannocchiale.webp` |
| `03.webp` | ✅ | 1A-3/MAPPA 1 Orda + Fauci in volo | 1-2 | 3.1 | Rivelazione dell'orda schierata | `hammerfist-s2-orda-schierata.webp` |
| `02.webp` | ✅ | MAPPA 1 Disposizione + drago + giganti | 2 | 3.1 | Alba del primo giorno d'assedio | `hammerfist-s2-alba-assedio.webp` |
| `05.webp` | ✅ | MAPPA 2 Fortezza + baliste | 2 | 3.2 | Establishing della fortezza | `hammerfist-s2-fortezza.webp` |
| `06.webp` | ✅ | Mura sfondate / breccia + cancello in fiamme | 2 | 3.2 | Breccia alle mura esterne | `hammerfist-s2-breccia.webp` |
| `mure sfondate.webp` | ✅ | Assedio, breccia | 2 | 3.2 | Breccia (variante) | `hammerfist-s2-mura-sfondate.webp` |
| `fauciDiPalude.webp` | ✅ | Fauci di Palude (ritratto/scena) | 2 | 3.3 | Comparsa del drago | `hammerfist-s2-fauci.webp` |
| `07.webp` | ✅ | 2B-Corretta Soffio del Drago (Re Thorek) | 2 | 3.3 | Il soffio acido sui bastioni | `hammerfist-s2-soffio-drago.webp` |
| `09.webp` | ✅ | 3Y Ponte Sospeso (Borin ultima difesa) | 3 | 3.4 | Difesa di retroguardia al ponte | `hammerfist-s3-ponte-sospeso.webp` |
| `sala-interna-hammerfist.webp` | ✅ | 5 Cuore della Montagna (interno) | 3 | 3.4/3.5 | Ritirata al Cuore della Montagna | `hammerfist-s3-cuore-montagna.webp` |
| `10.webp` | ✅ | MAPPA 4 Battaglia Finale (drago+gufi+tempesta) | 4 | 3.5 | Climax aereo-terrestre | `hammerfist-s4-battaglia-finale.webp` |
| `scontro-finale.webp` | ✅ | MAPPA 4 Scontro finale | 4 | 3.5 | Climax (variante) | `hammerfist-s4-scontro-finale.webp` |
| `01-bis.webp` | 🟡 | variante di `01` (Dara/torrione) | 1 | — | alt di 01 | `hammerfist-s1-dara-cannocchiale-alt.webp` |
| `05bis.webp` | 🟡 | variante di `05` (fortezza) | 2 | — | alt di 05 | `hammerfist-s2-fortezza-alt.webp` |
| `07-bis.webp` | 🟡 | variante di `07` (soffio drago) | 2 | 3.3 | alt di 07 | `hammerfist-s2-soffio-drago-alt.webp` |
| `09-bis.webp` | 🟡 | variante di `09` (ponte) | 3 | 3.4 | alt di 09 | `hammerfist-s3-ponte-sospeso-alt.webp` |

## 3. Mappe tattiche (griglia/vista dall'alto) — root `immagini/`

| File | Confidenza | Mappa | Sessione | Scala | Nome suggerito |
|---|---|---|---|---|---|
| `13.webp` | ✅ | 1A-1 Sentiero Nascosto (mappa tattica) | 1 | 3 m/car | `hammerfist-map-1a1.webp` |
| `04.webp` | ✅ | 2A Fortezza vista dall'alto (isometrica) | 2 | iso | `hammerfist-map-2a.webp` |
| `08.webp` | ✅ | 3X Ingresso Passaggi Antichi (evacuazione) | 3 | iso | `hammerfist-map-3x.webp` |
| `11.webp` | ✅ | 4A Disposizione Strategica Finale | 4 | griglia | `hammerfist-map-4a.webp` |
| `12.webp` | ✅ | 4 vista aerea finale (elevazioni 15-60m) | 4 | elevazione | `hammerfist-map-4-aerea.webp` |

## 4. Generazioni "October 2025" — mappe/scene generate

Sample verificato (`5_44PM`=fortezza iso "MONTAGNA"; `6_09PM`=torrione
tattico "Postazione Scout Hobgoblin"; `new_maps/6_14PM`=fortezza iso
tempesta; `new_maps/6_22PM`=Fauci soffio verde su Re Thorek): sono
**mappe e scene generate degli stessi soggetti dell'arco** (fortezza
2A, torrione 1A-2, drago, finale). Le non campionate sono classificate
al gruppo 🔵 (da confermare a vista per il pin esatto).

| File | Confidenza | Gruppo probabile |
|---|---|---|
| `Generated ... 5_44PM.webp` | ✅ | Mappa fortezza 2A (iso, "MONTAGNA") |
| `Generated ... 6_09PM.webp` | ✅ | Mappa 1A-2 Torrione (scout hobgoblin) |
| `Generated ... 5_11PM / 5_46 / 5_48 / 5_54 / 5_57 / 6_03 / 6_03(1) / 6_08PM.webp` | 🔵 | Scene/mappe dell'arco (fortezza/torrione/drago/finale) — pin a vista |
| `new_maps/6_14PM.webp` | ✅ | Mappa fortezza 2A (iso, tempesta) |
| `new_maps/6_22PM.webp` | ✅ | Scena Fauci soffio / difesa Cuore Montagna |
| `new_maps/6_16 / 6_19 / 6_20 / 6_20(1) / 6_22(1) / 6_22(2).webp` | 🔵 | Mappe generate dell'arco — pin a vista |

---

## 5. Copertura

- **Classificate almeno a gruppo**: **42/42 (100%)**.
- **Pinnate a un master preciso (✅/🟡)**: **28/42 (~67%)**; le restanti
  14 (generazioni "October 2025" non campionate) sono al gruppo 🔵 e
  vanno pinnate con una breve passata a vista.
- Ogni master visivo con un'immagine identificata la indica ora in
  testa alla propria voce (vedi `Mappe/Atlante-Hammerfist-Mappe-
  COMPLETE.md`).

## 6. Coda: rinomina file (differita)

La rinomina allo schema `hammerfist-sNN-descrizione.webp` (colonna
"nome suggerito" sopra) è **pronta ma non applicata**: nessun .md
referenzia le immagini per nome reale, quindi si può fare in blocco in
una passata dedicata senza rompere link. Farla **dopo** aver pinnato a
vista le 14 generazioni 🔵.
