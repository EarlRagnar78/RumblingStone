---
name: sistemi-di-gioco-plugin
description: Regolamenti come plugin attivabili (ADR-0111 proposta; L1-L5a unite #317-#334, 2026-11-07): censimento, banco d'invarianza, D1-D5 al DM
metadata:
  type: project
  modified: 2026-11-07T09:09:56.768Z
---

2026-11-07 Jfs chiede plugin per sistema di gioco su tool/generatori/skill/agent, con un file generale tipo INI che attiva i sistemi e mostra i supportati, misurabile e deterministico.

PR #315 unita su main il 2026-11-07 (99337894; ramo claude/project-thread-fuv4c0): ADR-0111 proposta, plans/PIANO-SISTEMI-DI-GIOCO-PLUGIN.md, plans/esperimenti/sistemi-plugin-2026-11-07/ (censimento.py, impronte.py = 12 impronte SHA-256 che ogni lotto deve lasciare identiche). Numeri: 31/202 script dipendono dal sistema (A 17 regole cablate, B 5 termini, C 2 rilevano, D 7 stampa); 3 modi di rilevare il sistema; lista 5e in 2 copie; 24 file per un sistema d20 nuovo.

Numeri ADR: 0109 marcature (ramo ldjnwk), 0110 regole ufficiali (ramo regole-ufficiali, slug i-termini-ufficiali-hanno-una-tabella-e-un-cancello, prenotato nella #315), 0111 plugin.

Vincoli concordati col thread regole ufficiali: le loro tabelle (lessico_it.yaml, lessico_it_pf1.tsv, lessico_regole.py) restano dati loro, puntate per percorso; esiti di controlla_testo() invariati; e_pf1() resta involucro.

PF1e qui è sia sistema base (Drappo, Giardino PF1e) sia rinforzo dei moduli 3.5: per questo pathfinder-1e-srd non si spegne in una campagna solo 3.5.

**Why:** evitare `if pf1e` sparsi e tre fonti del sistema.
**How to apply:** lotti L1-L8 una PR alla volta, `impronte.py --confronta` prima/dopo; aperte D1 formato (consigliato TOML), D2 dichiarazione per cartella, D3 L1+L2 insieme, D4 ambientazione nello stesso file, D5 skill attivi+rinforzo.

L1-L4 (#317 1738547, #320 fe4ca17, #321 144b2bc, #322 b0a74ae): sistemi.toml + sistemi/{catalogo,d20,dnd35,pf1e}, dmcore/sistemi.py, sistemi.py --check in CI, PF1e dal PRD (estrai_prd_pf1e.py --check); rilevamento unico sistema_di(); termini vietati e abilità per sistema; soglie PE e metodo EL nei dati. In questo container 49 test falliscono anche su main.
Vincolo per L5 (thread regole, 2026-11-07 sera): con la PR #327 (65cf254) i talenti sconosciuti sono a 0 e `--massimo-sconosciuti 0` blocca in CI. Quindi ogni nome di talento che cambia rigenerando le creature deve stare nella tabella o in talenti_manuali_35/pf1.tsv, oppure essere marcato. Se si toccano le schede del Bestiario: impronta_creature.py --scrivi.
L5a (PR #329, 8096399): 9 tabelle di dmcore/tabelle.py in sistemi/dnd35/dati/creature.toml, impronte sha256 identiche a b0a74ae (test_sistemi_creature.py); dnd35 codice 5→4. L5b PR #331 unita (34a3081): incantatori, prestigio, profili, taglie, razze; lettura booklet DM spostata a L8 (uscite identiche). L5c #332, L5d #333 (nel codice resta solo fonti.regole), L6 #334 (skill escluse per sistema spento: 18/17/15) unite; L7 #335 (340fae0; stampa.etichette, 13ª capacità; HTML identici, PDF non compilato) e L8 #336 (e06c2cf; plugin finto prova-d20 solo toml, 9 test) unite: piano L0-L8 chiuso. Limiti: sistemi non d20 servono METODI nuovi; derive/conformita ancora 3.5.
2026-11-08: ADR-0112 proposta + PIANO-MOTORE-AGNOSTICO-D20 (PR #337 unita il 2026-11-08, 18f63d7): microkernel e dati, ambito d20, F0 censimento_formule.py (AST) A1 5, A2 6, A3 6, A4 2, A5 6; I1 fatta: simpleeval ristretto (CEL bocciato); I2 fatta: JSON Schema bozza 7, fastjsonschema nella skill (492/503 difetti, oggi 123 e 77 crash; pydantic bocciato, compilato); I3 fatta: importlib spec_from_file_location (12/12 ostili; entry point bocciati, accettano os:system e collidono in sys.modules), I4 fatta: PCGen formulario nuovo 0,39% PF1e (non lasciare due strade); PR #340 (I2-I4 + pydantic generato: stesse 492 prese, bocciato per il pacchetto) unita il 2026-11-08 (4c04629); prossimo F1-F6. Jfs: librerie dentro il pacchetto come iemod-fetch (bundle con tutti i requisiti). Thread figli: «Installare typst e pdfcpu in automatico» (ADR-0113, mise+lock+Renovate), «Standard dei prompt a schede» (ADR-0114).
