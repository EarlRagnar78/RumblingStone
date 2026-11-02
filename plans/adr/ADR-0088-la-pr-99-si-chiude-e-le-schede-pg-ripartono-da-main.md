# ADR-0088 — La PR #99 si chiude: le schede PG ripartono da `main`, i gruppi restano rami

**Stato**: accettata il 2026-10-24 (scelta A del DM: *«Vai di a per la 99»*). 4g-1 è su `main` (#278); la #99 è chiusa; i tre pezzi che nessun lotto copriva sono ripresi (punto 5); resta 4g-2
**Data**: 2026-10-23 (proposta scritta il 2026-10-10, rimisurata oggi)
**Decisione-fonte**: il compito del thread «Piano per la PR 99 abbandonata»: chiudere la #99 oppure recuperarne il lavoro in PR nuove piccole, con un ADR breve. Il 2026-10-23 il DM ha dato la regola del lavoro: i thread figli sviluppano e provano, il merge lo fa il thread padre.
**Rapporti**: chiude la FASE 4 di [PIANO-RIPRESA-PR-ABBANDONATE](../PIANO-RIPRESA-PR-ABBANDONATE.md); conferma [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) e [ADR-0090](ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md) (un gruppo è un ramo); applica [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) alle schede PG (un master e una vista, mai due master).

## Contesto

La #99 è una bozza ferma dal 2026-08-10: 15 commit, 88 file, +14.078 / −4.931.
Il 2026-10-23 è **863 commit indietro** rispetto a `main` (384 il 2026-09-16).
Non si ribasa: è un archivio di idee, non un ramo.

Il piano l'ha già svuotata lotto per lotto: **4a-4f sono su `main`**. Le
correzioni di canone dei commit `da8bd281` (−2 DES della Corona) e `dd8306b2`
(il pegno del Rituale 3 è di Thorik) stanno in `campaign/state.yaml`, blocco
`party`. L'ADR-0017 della #99 è su `main` come ADR-0050, con lo stesso testo.

Restano due lotti, di natura diversa.

**4g, schede PG a dati.** Nessun file del lotto era su `main`. Due fatti lo
cambiano rispetto ad agosto: le schede della #99 hanno le caratteristiche a
`null` (il repo non le conosce, e non le hanno inventate), e classe, PF e stato
stanno già in `state.yaml` → `party`. Copiare le schede avrebbe creato una
seconda copia di quei fatti.

**4h, `groups/<slug>/`.** La #99 proponeva un gruppo per cartella invece che
per ramo. Da agosto `main` ha fatto e costruito la scelta opposta: ADR-0007
tiene le scritture di canone sui rami di gruppo, `scripts/gruppo_nuovo.py`
crea il ramo, ADR-0090 fa ripartire la partita su un ramo nuovo. Portare 4h
non recupererebbe lavoro: rovescerebbe una decisione attuata.

## La decisione

1. **4g esce in due PR piccole, da `main`, non dal ramo.**
   - **4g-1, lo strumento** (attuato qui): `validate_pg.py`, `render_pg.py`,
     lo schema `pg_scheda.schema.json`, `scripts/data/pg_modificatori_ignorati.yaml`
     e quattro schede con i soli modificatori permanenti già attestati, ognuno
     con la sua fonte. La scheda **non porta** classe, PF, stato e artefatti:
     il gate li rifiuta e dice dove stanno.
   - **4g-2, i valori**: le caratteristiche dalle schede del DM, confermate da
     un modulo (D19: il DM non scrive YAML). Classe **K**.
2. **4h non si porta.** L'ADR-0018 della #99 si registra come alternativa
   respinta. Si riapre solo se due gruppi devono giocare in contemporanea e
   vedersi a vicenda da `main`.
3. **La #99 si chiude** dal thread padre, col sì del DM, con un commento che
   rimanda qui. Il ramo resta finché 4g-2 non è su `main` (D8).
4. **Il resto della #99 è storico**: gli audit di agosto, il piano di agosto,
   `validate_links.py` (superato da `validate_docs.py`), `dmcore/frontmatter.py`
   (superato da `dmcore/delta_sessione.py`). Restano leggibili nel ramo.
5. **Tre pezzi non stavano in nessun lotto**, misurati riga per riga il
   2026-10-24 (le righe aggiunte dalla #99 cercate su `main`): il DM ha scelto
   di riprenderli tutti e tre prima di chiudere.
   - `scripts/inventory_inferred.py`, il ratchet dei `[INFERRED]` aperti (lotto
     G4): su `main` nessuno li contava. Entra nel canale testing (ADR-0099):
     `--check` non bloccante in CI, baseline 260 in
     `docs/audit/inferred-baseline.json`; l'inventario si genera a richiesta.
   - La regola del cambio d'autore delle echi (`consequence-echoes.md` §1-bis,
     commit `f580bc1d`): su `main` c'era la metà meccanica (`validate_state` R6),
     non la guida per chi scrive.
   - La serie di stemmi Golarion nella verifica legale del Palio (§4): IP di
     Paizo, non portabile in un'edizione commerciale (`c019d7ef`).

## Conseguenze

- Il −2 DES della Corona ha un posto dove la sua assenza si vede: togliendolo
  dalla scheda il gate diventa rosso (il test che vale tutti gli altri).
- Il gate ha corretto tre falsi positivi della versione di agosto, misurati sul
  repo di oggi: «Nessun −2 COS» letto come affermazione, il totale «−4 DES» non
  riconosciuto come somma dei due −2, e i resoconti in `plans/esperimenti/` che
  citano un PG per un costo di un altro.
- **Il CAR di Thorik è 12, non 16.** P1 dà alla Corona «+4 Carisma» (8 → 12),
  DEF-1 (D84) dà +4 CAR al rito: è lo stesso punto scritto due volte. Il DM
  (2026-10-23): il canone è quello giocato dal gruppo e dagli artefatti rivisti.
  Lo `state.yaml` del ramo `campaign-group-rumblingstone` conta «+4 CAR» in
  tutto, la scheda giocatore della Corona scrive «8 → 12». Resta una differenza
  di sola attribuzione: la scheda della Corona lo mette sulla Corona, `state.yaml`
  e DEF-1 sul rito. La scheda PG segue `state.yaml`, che è il master.
- Le caselle `[INFERRED]` sono 22 su 24: lo strumento esiste, i valori quasi
  tutti no.

## Validazione

| Cosa | Come |
|---|---|
| il gate è vero anche sul canone giocato | `validate_pg.py` e `render_pg.py --check` escono 0 su `campaign-group-rumblingstone` con questo ramo fuso sopra (prova del 2026-10-23) |
| il gate è vero sul repo | `python3 scripts/validate_pg.py` esce 0; `render_pg.py --check` esce 0 |
| il gate morde | 14 mutazioni dello strumento, 14 rosse in `scripts/tests/test_validate_pg.py` |
| nessuna seconda copia | una scheda con `classe`, `hp`, `stato` o `artefatti` è rifiutata |
| niente si perde chiudendo la #99 | le righe della #99 di almeno 30 caratteri cercate su `main` (2026-10-24): fuori dai lotti restavano solo i tre pezzi del punto 5 |
| niente si perde chiudendo la #99, sul registro | `python3 scripts/contenuti_nei_rami.py --fetch --check` dopo la chiusura |
