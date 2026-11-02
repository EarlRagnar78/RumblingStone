# ADR-0090 — La partita del primo tavolo riparte su un ramo di gruppo nuovo

**Stato**: proposta (da accettare dal DM)
**Data**: 2026-10-11
**Decisione-fonte**: richiesta del DM del 2026-10-11, nel thread sulle pozioni: *«come faccio a mettere queste cose finalmente con la campagna da giocare? è abbastanza stabile il repo per fare una prova di campagna salvando questo?»*
**Rapporti**: applica [ADR-0007](ADR-0007-scritture-canone-triplo-vincolo.md) (il canone vivo si scrive solo su un ramo di gruppo) e [ADR-0050](ADR-0050-stato-di-campagna-dati-e-prosa.md) (lo stato è `state.yaml`, `state.md` si rigenera)

## Contesto

Il tavolo ha giocato il 2026-09-25 la resurrezione di Hella e la prima notte a
Hammerfist ≈372 DR. Nessuna delle due cose è registrata: `state.yaml` dà Hella
morta e il viaggio «da giocare», e in `campaign/sessions/` c'è solo la
sessione 3, che è scritta in anticipo e non è mai stata giocata.

Il ramo del gruppo esiste, `campaign-group-rumblingstone-dm-gianfranco`, ma
non si può usare. Misurato il 2026-10-11:

- ultimo commit il 2026-07-20, con dentro solo la sessione 3 di prova;
- `git merge origin/main` rifiuta con *refusing to merge unrelated histories*:
  il ramo e `main` non hanno più un antenato comune, quindi i 345 commit di
  `main` arrivati dopo (i master DEF, `state.yaml`, il wizard a delta) non ci
  entrano con un merge;
- `campaign_branch.py ensure` cerca il ramo solo fra quelli locali: in un clone
  che ha ancora quel ramo in locale ci passa sopra, in un clone nuovo ne crea uno
  omonimo da `main` che poi non si può spingere sopra il vecchio.

Lo stato vero della partita, fino al Piano della Terra del 2026-07-31, sta oggi
su `main`, scritto a mano prima che ADR-0007 fosse applicato fino in fondo.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Ramo nuovo `campaign-group-rumblingstone` da `main`** | parte dallo stato vero; `dm.py session branch --group rumblingstone` lo fa in un comando; il vecchio ramo resta dov'è | un secondo ramo di gruppo per lo stesso tavolo, finché il vecchio non si cancella |
| Riusare il nome vecchio con un push forzato | un ramo solo | cancella la sessione di prova senza che nessuno l'abbia guardata, ed è un'azione che non si annulla da GitHub |
| Ricucire il vecchio ramo con `--allow-unrelated-histories` | conserva tutto | centinaia di conflitti su file che il ramo non doveva neanche toccare, per salvare una sessione mai giocata |
| Continuare a scrivere la partita su `main` | nessun ramo nuovo | è quello che ADR-0007 vieta, e mescola la partita di un tavolo con il prodotto che serve a tutti |

## Decisione

**Il primo tavolo riparte su `campaign-group-rumblingstone`, creato da `main`
il giorno in cui si registra la sessione del 2026-09-25.** Da lì in poi ogni
serata si chiude con `dm.py session end` su quel ramo, e `main` entra nel ramo
con un merge prima di ogni preparazione.

- Il vecchio ramo `campaign-group-rumblingstone-dm-gianfranco` **non si tocca**:
  si cancella quando il DM lo decide, dopo averlo guardato.
- Le parti della serata che il wizard non sa scrivere (stato dei PG, artefatti,
  echi) si scrivono a mano in `state.yaml` sullo stesso ramo, poi
  `render_state.py` rigenera le tabelle di `state.md`. È il «residuo manuale»
  che il Playbook §4 già prevede.
- Il debito che Thorik si è preso davanti alla Custode delle Radici è un **fatto
  giocato**: va nel log e negli echi del ramo (eco `E-07g`), non nel master. Il
  prezzo resta `[INFERRED — needs DM confirmation]` finché il DM non lo decide,
  prima di ARC-09.

## Conseguenze

- La sessione del 2026-09-25 diventa registrabile domani mattina, con due
  patch già pronte e validate (`validate_state`, `render_state --check`).
- `dm.py session end` stampava «✓ … committate» anche quando `state_apply` era
  fallito. Corretto nella stessa PR, con un test: ora esce con il codice
  dell'errore e lo dice.
- Restano tre limiti, che questa decisione non risolve:
  1. **il ledger dei PE parte da zero**: `update_xp.py` somma le sessioni del
     ramo e non conosce i PE dei PG di livello 13, quindi segna «livello 2». Finché
     non ha un punto di partenza, il ledger non va committato;
  2. **la sessione 3 scritta in anticipo** è ancora in `campaign/sessions/` su
     `main` e il ledger la conta come giocata;
  3. **il wizard registra clock e villain, non i PG**: Hella risorta e i Doni
     restano lavoro a mano (PIANO-CICLO-DI-SESSIONE, Fase 1b).

**Da rivedere se**: il DM vuole tenere il nome vecchio del ramo, oppure il
tavolo gioca una seconda serata senza che il ramo nuovo sia stato creato.
