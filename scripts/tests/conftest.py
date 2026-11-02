"""Configurazione di pytest per scripts/tests (ADR-0099, lotto P4).

Alcuni test scrivono per un momento dentro il repo vero: un ADR finto con un
numero già usato, una riga in più nel registro delle norme, un file citato come
«futuro». In serie va bene, perché li tolgono alla fine. In parallelo
(pytest-xdist) un altro processo che scandisce il repo nello stesso istante li
vede e boccia a torto: è successo nel job `testing` della CI il 2026-10-23.

Questi moduli prendono il marcatore `scrive_nel_repo`, e la CI li esegue in un
secondo giro, in serie, dopo quello in parallelo. L'elenco viene da una misura,
non da una ricerca nel codice: un audit hook su `open` in scrittura durante
l'intera suite, ricetta in
plans/esperimenti/piattaforma-2026-10-23/MISURE.md.
"""

SCRIVONO_NEL_REPO = {
    "test_archivi_non_indicizzati.py",  # scripts/monster_catalog.yaml
    "test_dm_volume.py",                # l'HTML homebrew dell'abbazia
    "test_norme_editoriali.py",         # skills/REGISTRO-NORME-EDITORIALI.md
    "test_orchestrazione_skill.py",     # skills/ORCHESTRAZIONE.md
    "test_validate_docs.py",            # ADR finti in plans/adr/, fixtures/_tmp_*
}


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "scrive_nel_repo: il test scrive per un momento nel repo vero; "
        "non va eseguito in parallelo con gli altri",
    )


def pytest_collection_modifyitems(config, items):
    import pytest

    for item in items:
        if item.path.name in SCRIVONO_NEL_REPO:
            item.add_marker(pytest.mark.scrive_nel_repo)
