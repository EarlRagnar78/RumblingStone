No, senza archivio non le tolgo: la regola è archiviare prima di togliere (ADR-0127), e il merge lo ferma il custode (ADR-0151).

1. `python3 scripts/memoria_custode.py verifica`
2. tolgo le tre righe
3. `python3 scripts/memoria_custode.py archivia --thread "Titolo del thread"`
4. `python3 scripts/memoria_custode.py verifica`: passa, e il merge passa.

Documentazione da aggiornare: nessuna
