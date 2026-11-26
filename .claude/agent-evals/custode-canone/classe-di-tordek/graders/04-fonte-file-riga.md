---
type: regex
pattern: '[\w./-]+\.(md|yaml|yml|py|json)[`*]*(:\d+|,?\s*(alla |r\.\s*|righ?[ea]\s*)\d+)'
match: contains
weight: 1
---

Almeno un fatto porta file e riga: file:riga, «file, riga N» o «file r. N» (ADR-0148).
