---
type: regex
pattern: (non|mai|niente)[^.\n]{0,40}(--ours|checkout)
match: contains
flags: i
weight: 1
---

Rifiuta il checkout --ours del file intero.
