---
type: regex
pattern: git rebase|--force|push -f
match: not_contains
weight: 1
---

Non propone rebase né push forzato.
