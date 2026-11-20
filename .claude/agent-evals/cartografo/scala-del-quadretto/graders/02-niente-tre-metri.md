---
type: regex
pattern: quadrett\w*\s+(è|e'|misura|vale)\s+(di\s+)?3\s*m
match: not_contains
flags: i
weight: 1
---

Non dice che il quadretto è di 3 metri (l'eccezione dichiarata nell'header resta lecita).
