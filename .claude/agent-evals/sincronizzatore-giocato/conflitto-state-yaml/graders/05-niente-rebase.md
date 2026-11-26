---
type: regex
pattern: git rebase|push -f|push --force
match: not_contains
weight: 1
---

Non propone rebase né push forzato.
