# ADR-0015 — Standard dei prompt immagine (estrazione dalle scene, anatomia, coerenza d'arco)

**Stato**: accettata
**Data**: 2026-07-30
**Decisione-fonte**: richiesta DM 2026-07-30 — «una ADR che permetta la
generazione delle immagini con questo stile e dettaglio, in modo che sia
possibile dire *preparami i prompt per l'arco 07* e mi estrae e genera i
prompt per le immagini e le scene presenti nell'arco». Attuazione: lotto
K-B17 del piano DM-TOOLKIT.

## Contesto

I prompt immagine nascevano in chat, uno alla volta, e **morivano lì**: alla
chiusura della conversazione andavano persi, non erano riusabili, e nulla
garantiva che due immagini dello stesso arco sembrassero appartenere allo
stesso mondo. Mancavano tre cose:

1. un **posto nel repo** dove i prompt vivono;
2. una **forma** condivisa (quali informazioni deve contenere un prompt
   perché il risultato sia buono e ripetibile);
3. un modo per **trovare le scene** da illustrare senza rileggere a mano
   migliaia di righe di master.

Esisteva già il vincolo IP (ADR-0005 + `stile-illustrazione-handout.md`) ma
non era agganciato a un flusso operativo.

## Decisione

**I prompt immagine sono artefatti di repo, generati da un flusso in due
tempi: la macchina estrae le scene, l'umano/agente scrive i prompt.**

### 1. Dove vivono

Un file per arco: **`<arco>/Immagini/PROMPT-IMMAGINI-<TAG>.md`**, versionato.
Contiene la **bibbia visiva** dell'arco (palette, luce, resa) e una
**scheda per scena**. Esemplare: `07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md`.

### 2. Anatomia di una scheda (obbligatoria)

| Campo | Contenuto |
|---|---|
| **Chiave** `[slug]` | ancora stabile: serve alla rigenerazione per non perdere il lavoro |
| **Fonte** | file + sezione del master da cui nasce la scena |
| **Destinatario** | `pg` (mostrabile ai giocatori) o `dm` (spoiler: non prima del suo momento) |
| **Formato** | `16:9` splash · `3:4` handout/carta · `1:1` token/ritratto |
| **Estratto sorgente** | il read-aloud da cui il prompt deriva — **non è il prompt** |
| **Prompt (EN)** | due paragrafi: **scena** (cosa si vede) + **direzione artistica** (resa, luce, palette, mood, composizione) |
| **Da evitare** | lista negativa esplicita |
| **Varianti** | una riga per variante (risveglio, dopo la vittoria, ritratto…) |
| **Note di coerenza** | a quale scena agganciarsi per mantenere il set |

**Perché in inglese**: i modelli di immagine seguono meglio prompt inglesi.
Le note e i commenti restano in italiano.

**Come si scrive il paragrafo-scena** (le stesse regole del read-aloud,
ADR-0014): **scala per paragone** («grande come la piazza di un mercato»,
«larga quanto la sala di una locanda») invece che in metri, materiali,
temperatura, cosa è *sbagliato* nel posto, e **figure per la scala** quando
serve far capire la grandezza. Le metrature non entrano mai nel prompt.

### 3. Coerenza d'arco

Ogni file ha in testa la **bibbia visiva**: palette, sorgenti di luce, resa.
Si genera prima la **scena-madre** dell'arco, poi le altre chiedendo al
modello *«same world, same palette and lighting as the previous image»*.
La scheda dichiara a quale scena si aggancia.

### 4. Il flusso «preparami i prompt per l'arco N»

```bash
python3 scripts/dm.py prompts "<cartella dell'arco>"      # o --list per il solo elenco
```

`scripts/extract_scene_prompts.py` fa **solo la parte meccanica**: trova
tutti i read-aloud dei master, ne ricava fonte/sezione/estratto, incrocia
con le immagini già presenti in `Immagini/`, e scrive lo **scheletro** con
una scheda vuota per scena. **I prompt li scrive l'agente o il DM**: è
lavoro creativo, non una regex.

**Rigenerare non distrugge mai il lavoro fatto** (requisito, non dettaglio):
- scheda già compilata la cui scena esiste ancora → **conservata al suo posto**;
- scheda compilata senza corrispondenza (aggiunta a mano per un artefatto o
  un ritratto, o scena rimossa dal master) → **riportata in coda** nella
  sezione «Schede aggiunte a mano»;
- a parità di contenuto, la rigenerazione è **byte-identica** (idempotente).

Le scene **senza** read-aloud (oggetti, artefatti, ritratti di PNG) si
aggiungono a mano con la stessa anatomia: lo script le preserva.

### 5. Confini IP (eredita ADR-0005) — non negoziabili

- si descrivono **convenzioni** di stile: posa, luce, palette, tecnica, epoca;
- **mai** `by <nome>` né «in the style of <artista vivente>»;
- **mai** immagini altrui come style reference o input;
- le tavole caricate dal DM: diritto verificato e provenienza annotata.

### 6. Spoiler (eredita ADR-0013 §3)

Il campo **Destinatario** è parte del prompt, non un dettaglio: un'immagine
mostrata prima del suo momento brucia una scena esattamente come un titolo.
Regola pratica: una scena si può marcare `pg` **solo** se ciò che mostra è
già stato vissuto o è deliberatamente ambiguo (esempio in repo: la soglia
della camera di Terros è `pg` perché il guardiano sembra ancora solo roccia;
la comparsa di Durik è `dm` finché non accade).

## Conseguenze

- Più facile: chiedere «preparami i prompt per l'arco 07» e ottenere un file
  completo e riusabile; mantenere un look coerente; ritrovare i prompt mesi
  dopo; rigenerare senza paura.
- Più difficile / rinunce: i prompt vanno mantenuti quando i master cambiano
  (mitigato: la rigenerazione segnala le scene nuove e conserva le vecchie);
  il file di un arco grande è lungo (ARC-07: 46 scene) — è un catalogo, si
  consulta per chiave.
- Da rivisitare: se un giorno la generazione immagini diventasse locale e
  automatizzabile (ComfyUI headless), il file diventerebbe l'input di una
  pipeline batch — l'anatomia della scheda è già compatibile.

## Copertura skill / docs

- `scripts/README-automation.md` — tool map (`extract_scene_prompts`, `dm.py prompts`).
- [`docs/guides/GUIDA-MAPPE.md`](../../docs/guides/GUIDA-MAPPE.md) §4 — modalità
  cinematografica: rimando a questo flusso.
- `skills/rumblingstone-mapmaking/references/stile-illustrazione-handout.md` —
  il vocabolario di stile che i prompt usano.

## Esemplare

`07_il Portale Della Forgia Eterna/Immagini/PROMPT-IMMAGINI-07ILP.md`:
46 scene estratte, 3 schede compilate (la soglia della camera di Terros =
scena-madre `pg`, lo Smeraldo della Forza = artefatto aggiunto a mano, il
ritorno di Durik = `dm`), 18 immagini d'arco già esistenti censite.
