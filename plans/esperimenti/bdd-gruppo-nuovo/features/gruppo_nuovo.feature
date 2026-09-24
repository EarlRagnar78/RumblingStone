# language: it
Funzionalità: Un gruppo nuovo parte da un modulo, senza YAML a mano
  Come DM che rigioca la campagna con un altro tavolo
  voglio rispondere a domande invece di scrivere state.yaml
  così che il prodotto resti e la partita del primo tavolo no

  Contesto:
    Dato lo stato di campagna di oggi

  Scenario: Solo le righe che chiedono un giudizio arrivano una alla volta
    Quando derivo lo stato del gruppo nuovo
    Allora le domande una alla volta sono 5 di "villain", 4 di "difensori_rethmar" e 1 di "waypoints"
    E ogni domanda offre "tieni", "svuota" e "rivedi" e mostra il testo

  Scenario: Ciò che è partita si toglie da solo
    Quando derivo lo stato del gruppo nuovo
    Allora restano 12 conoscenze, nessuna sul party o sui PG di prima
    E gli artefatti sono tutti ancora lì, senza portatore
    E gli echi sono vuoti e il March Clock è al giorno 1

  Scenario: I clock ripartono da zero, i trigger restano
    Quando derivo lo stato del gruppo nuovo
    Allora ogni clock numerico è a zero con lo stesso massimo
    E ogni clock che è un trigger è rimasto com'era

  Scenario: Il prodotto resta
    Quando derivo lo stato del gruppo nuovo
    Allora anagrafica dei PNG, scenari di Rethmar, villain e archi sono quelli di prima

  Scenario: L'arco scelto è in corso, i precedenti non giocati
    Quando rispondo arco 8 e livello 13
    Allora l'arco 8 è in corso al livello "13"
    E gli archi prima dell'8 sono "non giocato da questo gruppo"
    E gli archi dopo l'8 sono "da giocare"

  Scenario: I PG diventano il party
    Quando rispondo con un PG "Brunna", "Nana", "Guerriera", livello 5, PF 48
    Allora il party è "Brunna", classe "Guerriera 5 (Nana)", PF "48", attivo

  Scenario: Tieni, svuota, rivedi
    Quando tengo tutte le righe tranne la seconda, che svuoto, e la terza, che rivedo
    Allora la prima riga è com'era
    E la seconda riga porta il segnaposto
    E la terza riga è com'era e c'è una sola domanda aperta, che punta a lei

  Scenario: Una riga senza risposta vale «rivedi»
    Quando rispondo senza scegliere nessuna riga
    Allora ogni riga è diventata una domanda aperta

  Scenario: Lo stato nuovo passa validate_state
    Quando rispondo il minimo indispensabile
    Allora validate_state non trova errori

  Schema dello scenario: Una risposta sbagliata è rifiutata prima di scrivere
    Quando rispondo con <risposta sbagliata>
    Allora la risposta è rifiutata

    Esempi:
      | risposta sbagliata          |
      | nessun PG                   |
      | sette PG                    |
      | livello 0                   |
      | un arco che non esiste      |
      | un gruppo con spazi         |
      | una scelta inventata        |
      | una riga che non esiste     |
      | un PG con zero PF           |

  Scenario: Il modulo esce in JSON anche attraverso dm.py
    Quando chiedo il modulo con "dm.py gruppo nuovo --domande"
    Allora l'uscita è JSON con le righe di "villain", "difensori_rethmar" e "waypoints"

  Scenario: Il modulo in terminale produce le risposte
    Quando compilo il modulo in terminale tenendo tutte le righe tranne l'ultima
    Allora il resoconto dice tutte le righe tenute tranne una da rivedere

  Scenario: Ctrl-D a metà non scrive niente
    Quando interrompo il modulo a metà
    Allora il comando esce 1 e dice che non ha scritto niente

  Scenario: Da capo a fondo su una copia del repo
    Dato una copia del repo sotto git
    Quando lancio "dm.py gruppo nuovo" con il file di risposte
    Allora sono sul ramo "campaign-group-beta" e campaign/ è committato
    E group.yaml dice "group: beta" e render_state --check è verde

  Scenario: Con l'albero sporco non parte
    Dato una copia del repo sotto git con un file non committato
    Quando lancio "dm.py gruppo nuovo" con il file di risposte
    Allora il comando esce 1 e resto sul ramo "main"
