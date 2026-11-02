# ADR-0101 — La prosa ha una catena sola, e la chiude il DM

**Stato**: proposta (2026-10-23, PR #264)
**Data**: 2026-10-23
**Decisione-fonte**: il DM, 2026-10-23: *«se ci sono tools skills pipeline plugin e tools che non sono presenti nel repo aggiungili ed integrali così come per tutti gli altri strumenti in un flusso coerente»*; prima, il 2026-10-22: *«rendere obsoleti le versioni peggiori […] e introdurre le versioni migliori»*.
**Rapporti**: applica [ADR-0093](ADR-0093-la-prosa-migliora-se-la-sceglie-il-dm-alla-cieca.md) (giudice è il cieco del DM) e [ADR-0099](ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md) (canali); riprende [ADR-0002](ADR-0002-cli-unica-dm-orchestratore.md) (`dm.py` orchestra, mai logica), [ADR-0079](ADR-0079-un-secondo-rilevatore-per-la-prosa.md) (LanguageTool locale) e [ADR-0089](ADR-0089-un-llm-locale-per-la-prosa-si-misura-prima.md) (modello locale).

## Contesto

Gli strumenti della prosa sono cresciuti per lotti. `misura_craft`,
`validate_prosa` e `punteggio_mqm` misurano; `ciclo_prosa` corregge e
rimisura; `cieco_versioni` fa decidere il DM; `domande_developer` controlla
l'architettura delle scene. Il lotto 7 di AVVENTURE-COMMUNITY ne ha aggiunti
tre: `coerenza_campagna` (fatti fra scene e archi), `misura_sintassi` (spaCy)
e `migliora_prosa` (filtro e modello di preferenza sui voti ciechi). Con la
#234 è arrivato `banco_prosa_locale`, che fa votare le corse di un modello
locale a `voto_scrittura`.

Ognuno aveva la sua porta. Un agente che riscriveva un box doveva sapere da sé
quali dieci script esistono e in che ordine si usano; le due dipendenze
esterne (spaCy e il suo modello, LanguageTool) non stavano nel registro di
`binari.py`, quindi `dm.py doctor` non le vedeva; la documentazione
d'architettura non nominava cinque dei dieci script.

Le misure del lotto 7 dicono anche cosa questa catena **non** fa. Nessuna delle
17 misure di prosa della letteratura prevede il voto cieco del DM; il modello di
preferenza di `migliora_prosa` arrivava a 0,611 in leave-one-out, sotto la
soglia scritta prima di addestrarlo (sale a 0,661 e la supera col voto del
2026-10-23, vedi sotto); LanguageTool ha dato un rilievo vero su 30 letti;
Stanza non batte spaCy (PR #270). La coerenza invece ha trovato contraddizioni
vere fra ARC-07 e ARC-08 ed è diventata un cancello.

## Alternative considerate

| Opzione | A favore | Contro |
|---|---|---|
| **Un ingresso `dm.py prosa <azione>` con l'ordine della catena, strumenti esterni nel registro, il DM chiude** (scelta) | un posto solo da ricordare; `doctor` vede le dipendenze; nessuna logica nuova; gli script restano chiamabili per nome | dieci azioni sono tante; l'ordine è una convenzione, non un vincolo |
| Un orchestratore che esegue tutta la catena da solo su un file | un comando invece di quattro | sceglierebbe al posto del DM: contraddice ADR-0093, e le misure dicono che nessun punteggio automatico ne prevede il voto |
| Lasciare gli script sciolti e documentarli soltanto | niente codice | è già lo stato di oggi, e gli agenti saltavano la coerenza e la sintassi |
| Un servizio esterno di revisione (Sourcery, LanguageTool in rete) | niente da installare | il testo della campagna uscirebbe dalla macchina (ADR-0079 lo vieta); a pagamento o a quota; e i rilievi di stile in inglese non valgono per l'italiano |

## Decisione

1. **Un ingresso.** `dm.py prosa <azione>` passa i flag allo script e ne
   restituisce il codice d'uscita, come `dm.py bestiario`. Le azioni, in
   ordine d'uso:

   | Fase | Azione | Script | In CI |
   |---|---|---|---|
   | misurare | `misura` | `misura_craft` | sì, cancelli e tetti |
   | | `ciclo` | `ciclo_prosa` | sì, `box_impoveriti` e verdetto |
   | | `mqm` | `punteggio_mqm` | sì, contro la baseline |
   | | `sintassi` | `misura_sintassi` | no: spaCy è facoltativo |
   | controllare | `coerenza` | `coerenza_campagna` | sì, `fatti --check` sui residui dichiarati |
   | | `domande` | `domande_developer` | sì, sui master nuovi |
   | riscrivere | `migliora` | `migliora_prosa` | solo `--help` |
   | decidere | `cieco` | `cieco_versioni` | no: è il DM |
   | banco | `banco` | `banco_prosa_locale` | solo `--dry-run` |
   | | `voto` | `voto_scrittura` | i test |

2. **Le candidate le scrive un agente o una persona**, mai lo script.
   `migliora` filtra (fatti cambiati, box impoverito, le regole misurabili di
   `read-aloud-adulti.md` §2-ter) e ordina col modello. Dal 2026-10-23 il
   modello supera la sua soglia (0,661 in leave-one-out su 59 coppie, Wilson
   basso 0,534; 5 coppie nuove su 5 previste prima del voto), quindi fa una
   cosa sola in più: se anche la migliore candidata ha meno di 0,5 contro
   l'originale, resta l'originale e la coppia non va al cieco. Una candidata
   che il modello dà vincente va comunque al cieco, che resta l'unico giudice
   di ciò che entra; ogni voto torna in `pipeline/VOTI.json` e `esito`
   rimisura la soglia.
3. **Le dipendenze esterne sono nel registro.** `binari.py` conosce `spacy`
   (facoltativa, in `requirements-completo.txt` col modello `it_core_news_md`,
   CC BY-NC-SA: nel `.venv`, mai nel repo) e le catene «sintassi della prosa»
   e «secondo lettore LanguageTool»; `dm.py doctor` le mostra. LanguageTool
   resta locale (`avvia_languagetool.sh`, porta 8081) e `migliora --lt` lo
   usa come filtro solo per i gruppi di regole con precisione ≥ 0,70: oggi
   nessuno, quindi non scarta niente.
4. **Canali (ADR-0099).** In stable restano le misure che erano già cancelli.
   Il cancello di coerenza entra in testing. spaCy, LanguageTool e il banco del
   modello locale stanno in unstable: si usano a mano e salgono solo con una
   misura sui voti del DM che li dica utili. Stanza aspetta la #270.
5. **`voto_scrittura` resta.** Il lotto 7e voleva toglierlo; la #234 lo usa per
   votare le corse del modello locale. Prende il rilevatore del «sembra» da
   `validate_prosa`, così la regola ha un posto solo.

## Conseguenze

- Un agente che riscrive un box ha un promemoria (`dm.py prosa` senza azione)
  e una riga in più nella checklist di `rumblingstone-narrative-style`.
- `docs/ARCHITETTURA.md` §10 disegna la catena, i casi d'uso in sequenza e le
  dipendenze fra gli script.
- Un test (`test_dm_prosa.py`) tiene l'ordine delle azioni uguale a questa
  tabella: cambiare la catena vuol dire cambiare l'ADR.
- Si paga: un sottocomando in più in `dm.py`, e `requirements-completo.txt`
  scarica 45 MB di modello per chi vuole la sintassi.

**Da rivedere se**: il modello torna sotto la soglia (allora smette di
scartare); il DM decide che il modello può anche far entrare una candidata
senza cieco, sopra una probabilità da fissare prima; il progetto diventa commerciale (il modello spaCy non è più
installabile); un modello locale vince il cieco contro il generatore di oggi
(ADR-0089).
