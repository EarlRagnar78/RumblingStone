---
[riga riservata · sha256:587b19c4]
[riga riservata · sha256:a0775954]
metadata:
  type: feedback
---
[riga riservata · sha256:0fe8129a]

**Why:** il 2026-11-03 Jfs ha contestato lo scarto dell'NLI e delle altre prove. Rifatte (RICERCA-GUARDRAIL §8, PR #308), 2 su 5 sono passate da scartate ad adottate: embedding frase per frase (6 vere invece di 1) e box telecomando al plurale (dal 13% al 50%).

**How to apply:** per ogni tecnica nuova, riporta almeno due configurazioni con la misura, e spiega perché quella scartata non migliora. Vale con [[decisioni-superate-regressione]] e [[usabilita-al-tavolo]].

**Seguito (2026-11-03 sera):** Jfs non vuole indicatori che si limitano a segnalare: quello che un controllo trova va **corretto** nel testo, e il controllo diventa **standard** (cancello con `--check` ed elenco delle eccezioni accettate col perché), misurando prima/dopo. PR #309 (unita il 2026-11-03, 008c07c): NLI fedeltà che rimette l'originale dentro ciclo_prosa (26 coppie etichettate dal DM, F1 0,83 contro 0,62), telecomando 4→2 in CI, ripetizioni 21→19 in locale, Lythiel nel cortile esterno.
