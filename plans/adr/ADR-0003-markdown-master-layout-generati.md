# ADR-0003 — Markdown è il MASTER; i layout (SVG, Homebrewery, PDF) sono artefatti generati

**Stato**: accettata
**Data**: 2026-07-10
**Decisione-fonte**: T-D2 (DM 2026-07-03, mappe) esteso da K-D2 (DM 2026-07-10, hype Homebrewery)

## Contesto

La campagna produce materiale in più vesti: griglie tattiche (markdown
emoji → SVG), recap per i giocatori (markdown → PDF), e ora materiale
hype/handout in stile Manuale del Giocatore via Homebrewery V3. Ogni
veste "bella" tenta di diventare il posto dove si edita — e a quel punto
canone e layout divergono.

## Decisione

Il file markdown del repo è **sempre** la fonte di verità; ogni layout
(SVG in `rendered/`, `.hb.md` per Homebrewery in `*/homebrew/`, PDF) è un
**artefatto generato**, marcato "Auto-generated — do not edit by hand",
che si **rigenera** e non si corregge a mano. I generatori ereditano il
filtro spoiler-safe di `session_recap.py`: le sezioni DM-private non
entrano mai negli artefatti player-facing.

## Conseguenze

- Correzioni in un posto solo; gli artefatti non divergono dal canone.
- Si può cambiare stile (o abbandonare Homebrewery) senza perdere contenuto.
- Costo: la resa estetica è vincolata a ciò che il generatore sa fare;
  ritocchi estetici una-tantum vanno codificati nel generatore, non
  nell'artefatto.
