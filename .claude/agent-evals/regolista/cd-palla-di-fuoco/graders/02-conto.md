---
type: regex
pattern: 10\s*\+\s*3\s*\+\s*4|\b10\b[^\n]*\n(?:[^\n]*\n){0,3}[^\n]*\+\s*3\b[^\n]*\n(?:[^\n]*\n){0,3}[^\n]*\+\s*4\b
match: contains
weight: 1
---

Mostra il conto 10 + 3 + 4, in riga o in tabella.
