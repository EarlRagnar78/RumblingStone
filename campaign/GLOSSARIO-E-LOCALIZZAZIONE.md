# Glossario bloccato e localizzazione

> **A cosa serve.** Fissare **una volta sola** come si scrive ogni nome proprio
> della campagna, e cosa succede a quel nome se un giorno esisterà un'edizione
> inglese. È il *loc kit* previsto da [ADR-0016](../plans/adr/ADR-0016-lingua-sorgente-e-edizioni.md):
> costa poco adesso, costa settimane a farlo dopo.
>
> **Regola d'uso**: se un nome è in questa tabella, si scrive **così** in ogni
> file nuovo. Se non c'è, aggiungilo tu la prima volta che lo inventi.

**Lingua sorgente: italiano** (ADR-0016). L'inglese in tabella è la resa
**prevista**, non un testo esistente: serve a impedire che fra due anni lo
stesso nome esca in tre modi diversi.

---

## 1. La regola dei nomi misti (perché non si uniforma)

Il repo mescola nomi inglesi e italiani, e **va bene così**: è Faerûn, dove il
Comune convive con le lingue razziali. La regola che ci sta sotto, resa
esplicita:

| Categoria | Lingua | Perché |
|---|---|---|
| **Nomi propri di persona e di luogo canonici FR** | come in FR | *Hammerfist*, *Rethmar*, *Dauth*: sono già canone di ambientazione |
| **Artefatti nominati in Comune** | inglese | *Aegis Fang* è un nome proprio, non una descrizione |
| **Artefatti nominati in nanico/descrittivi** | italiano | *Corona di Adamantio*, *Bracieri Gemelli di Moradin* |
| **Soprannomi e epiteti** | **italiano** | *Barbadiferro*, *Fuocospento*, *il Velato*, *Seta-Argento* — sono **parlanti**, e in italiano parlano |
| **Termini di regolamento** | italiano al tavolo | **CD** non DC, **TS**, **Lotta**, **azione veloce** |

⚠️ **Non uniformare i nomi esistenti.** Sono già in centinaia di file, nelle
mappe, nelle immagini e nelle schede dei giocatori. Il costo supera di molto il
beneficio estetico.

---

## 2. Personaggi giocanti

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Thorik | Thorik | invariato |
| Tordek Durinheart | Tordek Durinheart | invariato |
| Hella Oakenshield | Hella Oakenshield | invariato |
| Artemis | Artemis | invariato |
| Durik | Durik | compagno di Hella, **maschio** |

## 3. Artefatti

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Aegis Fang | Aegis Fang | **DNT** — già inglese |
| Corona di Adamantio | Crown of Adamantine | tradurre: è descrittivo |
| Ring of Chaotic Illumination | Ring of Chaotic Illumination | **DNT** — già inglese in tutte le schede |
| Bracieri Gemelli di Moradin | Twin Braziers of Moradin | tradurre |
| Collana dei Semi Eterni | Necklace of Eternal Seeds | tradurre |
| Cuore di Moradin | Heart of Moradin | tradurre |
| Cintura della Devastazione | Belt of Devastation | oggetto custom del PG (D17) |
| Smeraldo della Forza · Topazio del Tempo · Rubino della Leggenda | Emerald of Strength · Topaz of Time · Ruby of Legend | le tre gemme della Corona |
| Frequenza della Confusione | Frequency of Confusion | conoscenza, non oggetto |
| Diapason Armonico | Harmonic Tuning Fork | **speso** sulla Sentinella |
| Seme-Mercato (di Varis) | Market-Seed | innesto planare |

## 4. Antagonisti e PNG

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Terros l'Antico | Terros the Ancient | GS 15, **sconfitto** |
| Skullcrusher il Nero | Skullcrusher the Black | **DNT** sul nome |
| Fauci di Palude | Swamp Maw | drago nero, ARC-08 |
| Balvar Fuocospento | Balvar Quenchfire | *Fuocospento* è parlante: la resa deve restare parlante |
| Zog'tar Deatheye | Zog'tar Deatheye | **DNT** |
| Thorgrim Barbadiferro | Thorgrim Ironbeard | parlante |
| Re Thorek I / Re Thorek Hammerfist | King Thorek | |
| Durin Rocciadura | Durin Hardstone | parlante |
| Il Collezionista | The Collector | |
| Varis «Seta-Argento» | Varis "Silversilk" | parlante |
| Sethrax il Velato | Sethrax the Veiled | |
| Sonjak · Xal'thor · Zalkatar · Vatore · Therysol | invariati | **DNT** |
| Sentinella Silenziosa / di Mithral | Silent Sentinel | **sconfitta** |
| Madre Cristallo | Crystal Mother | |
| Custode delle Radici | Root Warden | psicopompo, ARC-07 #3 |

## 5. Luoghi e concetti della campagna

| Italiano (sorgente) | Inglese previsto | Note |
|---|---|---|
| Valle di Channath / Cannath Vale | Cannath Vale | equivalente dell'Elsir Vale |
| Palio di Channathgate | Palio of Channathgate | ⚠️ *Palio* **DNT**: è un prestito culturale, non si traduce |
| Hammerfist Holds | Hammerfist Holds | **DNT** |
| Rethmar · Dauth · Drellin's Ferry | invariati | **DNT** |
| Sala della Forgia Eterna | Hall of the Eternal Forge | |
| Portale della Forgia Eterna | Portal of the Eternal Forge | titolo dell'ARC-07 |
| Stanza della Corona | Crown Chamber | |
| Tempio di Mithral | Mithral Temple | |
| Oceano di Roccia | Ocean of Stone | Piano della Terra |
| Incudine del Mondo | Anvil of the World | anche l'epiteto di Terros |
| La Cronaca Vivente · «La Forgia Ricorda» | The Living Chronicle · "The Forge Remembers" | |
| Trinità Divina | Divine Trinity | sinergia S4 |
| Colpo dell'Alba Oscura | Dark Dawn Strike | sinergia S3 |
| Orologio di Hammerfist | Hammerfist Clock | il countdown |
| Custodi Eterni · Cerimonia delle 100 Asce | Eternal Wardens · Ceremony of the Hundred Axes | ARC-08 |

## 6. Lista «non tradurre» (DNT) — categorie

Oltre alle voci marcate DNT sopra, **non si traducono mai**:

1. **Nomi di divinità**: Moradin, Abbathor, Lathander, Mask, Shar, Tiamat.
2. **Nomi propri di persona** senza componente descrittiva.
3. **Toponimi canonici dei Forgotten Realms.**
4. **Nomi di incantesimi 3.5**, che restano in inglese corsivo anche nel testo
   italiano: *black tentacles*, *dispel magic*, *righteous might*. È già la
   prassi del repo e va mantenuta.
5. **Sigle di sistema** nei file tecnici: CR, HD, DR, SR. *(Nel testo da tavolo
   valgono invece gli equivalenti italiani — vedi §1.)*

## 7. Quando aggiungi un nome nuovo

Tre domande, in ordine:

1. **È parlante?** (*Fuocospento*, *Barbadiferro*, *il Velato*) → **italiano**,
   e annota accanto una resa inglese che resti parlante.
2. **È un nome proprio secco?** → come viene, e finisce in **DNT**.
3. **È canone FR?** → esattamente come in FR, mai reinventato.

Poi aggiungilo qui. La riga costa dieci secondi; ritrovarsi lo stesso PNG con
tre grafie costa una giornata di *grep*.
