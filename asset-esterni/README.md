# asset-esterni

Qui stanno gli asset di terzi che il DM scarica sulla sua macchina. Git ignora
tutto tranne questo file: la licenza di 2-Minute Tabletop chiede di mandare chi
vuole i file al sito, non di ridistribuirli.

Si installano con `python3 scripts/dm.py asset installa <zip> --categoria base`
(o `premium`). La procedura, le due categorie e cosa si può fare con ciascuna
stanno in `docs/guides/GUIDA-MAPPE.md`, §5.2.

`oggetti-cc0/` tiene i modelli 3D CC0 da cui `build_oggetti_cc0.py` rende le
tessere degli oggetti di scena del tema texture (R4-ter): i glTF di Poly Haven,
ognuno con la sua `fonte.json` (URL e MD5 di ogni file), e i modelli estratti
dallo zip Standard di Quaternius. Le tessere stanno in `scripts/oggetti-cc0/` e
si committano; i modelli no. Procedura: `docs/guides/GUIDA-MAPPE.md`, §5.1.1.
