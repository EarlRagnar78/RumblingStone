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
plans/esperimenti/piattaforma-2026-10-23/MISURE.md. Rifatta il 2026-11-08 sulla
suite di quel giorno (2.529 prove, plans/esperimenti/promozioni-2026-11-08/):
due moduli nuovi scrivono nel repo e sono entrati qui. Il 2026-11-25, quando
xdist è salito a stable nel job principale, ne sono entrati altri tre
(test_ciclo_prosa, test_booklets, test_componenti) per un rosso visto con
-n auto, non con l'audit hook: la misura completa non è stata rifatta
(plans/esperimenti/promozioni-2026-11-25/).
"""

SCRIVONO_NEL_REPO = {
    "test_archivi_non_indicizzati.py",  # scripts/monster_catalog.yaml
    "test_dm_volume.py",                # l'HTML homebrew dell'abbazia
    "test_norme_editoriali.py",         # skills/REGISTRO-NORME-EDITORIALI.md
    "test_orchestrazione_skill.py",     # skills/ORCHESTRAZIONE.md
    "test_validate_docs.py",            # ADR finti in plans/adr/, fixtures/_tmp_*
    "test_migliora_prosa.py",           # pipeline/cieco/_testi-provvisori.md
    "test_misura_stampa.py",            # scripts/tests/_tmp_appendice.*, _tmp_misura_stampa/
    "test_pdfua.py",                    # il PDF delle schede del Drappo, cartelle tmp* in radice
    # tmp*/x.md in radice (cp.RADICE): con -n auto `componenti --check` di
    # test_componenti lo vedeva sparire a meta' lettura (FileNotFoundError, 2026-11-25)
    "test_ciclo_prosa.py",
    # TemporaryDirectory(dir=REPO): cartelle tmp* in radice (2026-11-25)
    "test_booklets.py",
    # TestLeInclusioni scrive in build/ se manca, e il modulo scandisce il repo
    "test_componenti.py",
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
