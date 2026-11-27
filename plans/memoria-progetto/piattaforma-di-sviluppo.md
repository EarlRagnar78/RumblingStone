---
name: piattaforma-di-sviluppo
description: Regola dei tre canali (unstable/testing/stable) per strumenti e librerie di RumblingStone, ADR-0099, PR #273, misure e decisioni aperte
metadata:
  type: project
  modified: 2026-10-23T09:13:49.732Z
---

Dal 2026-10-23 Jfs vuole una piattaforma di sviluppo unica: una sola Python stabile e supportata scelta come Debian sceglie il kernel, librerie e strumenti standard de facto solo con misura prima/dopo, la stessa regola per CI, test, skill e pipeline (mappe, prosa, stampa), aggiornamento come la migrazione del kernel in Debian.

PR #273 (unita su main il 2026-10-23, 2a509e9; ramo claude/project-thread-8f3s7k): ADR-0099 «la piattaforma ha tre canali come Debian», accettata dal DM il 2026-10-23 (D1-D6 tutte decise: «D1-d5 ok», «D6 b»), plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md (censimento §2, lotti P1-P8, D1-D6), misure in plans/esperimenti/piattaforma-2026-10-23/MISURE.md. ruff in testing (ruff.toml, solo regole-bug).

Numeri chiave: Python 3.13 resta (Debian 13; upstream solo sicurezza da 2026-10 al 2029-10; si sale con Debian 14). CI main 914 s di cui 222 s unittest che riesegue i test di pytest (D2 toglierlo). pytest-xdist 219→67 s (D3). uv 33→4 s a freddo (D4). mypy 328 rilievi 0 bug (no). ruff: 3 bug veri in converters/ (D6).

Applicato: unittest tolto dalla CI (parità resta nel test), job `testing` (uv + pytest -n auto) e `convertitori` non bloccanti, converters/ dentro la piattaforma (Python 3.13, Dependabot, ruff, 3 bug corretti). Promozioni a stable non prima del 2026-11-06; xdist ha test instabili in test_validate_docs (file finti scritti nel repo vero). Jfs vuole che ogni cambio misuri anche la qualità del progetto (prima/dopo).

**Why:** Jfs chiede regola unica e misurata invece di un ADR per componente.
**How to apply:** un componente nuovo entra in unstable, va in testing (CI non bloccante) con misura e ok DM, sale a stable dopo 14 giorni/10 run senza falsi allarmi né peggioramenti >5%. Togliere l'eccezione F841 di misura_craft in ruff.toml quando la #264 è su main.

Rete (2026-10-23): Jfs ha aperto nell'ambiente i domini per pytorch CPU, Hugging Face xethub, SRD (d20srd, d20pfsrd, aonprd), Debian, typst, LanguageTool, Docker; funzionano già nella sessione aperta, senza riavvio. xdist: i 5 moduli che scrivono nel repo vero hanno il marcatore `scrive_nel_repo` (scripts/tests/conftest.py) e in CI girano in serie dopo `-n auto`.

Rilasci: ADR-0100 (accettata), PR #275 unita il 2026-10-23 (6656205). **v1.0.0 pubblicata** il 2026-10-23 (https://github.com/gsamuele78/RumblingStone/releases/tag/v1.0.0): archivio skill riproducibile, SHA256SUMS verificata dal container, attestazione Sigstore. Rilasciare = PR che apre `## [X.Y.Z]` in CHANGELOG.md (radice) e alza `__version__` in scripts/dmcore/__init__.py; ogni PR che cambia la superficie pubblica scrive una riga in «Non rilasciato». Il repo è PUBBLICO. Il CHANGELOG 1.0.0 dice cosa NON promette (canale testing, contenuto di gioco, ADR-0095 proposta, P6). docs/ARCHITETTURA.md: 20 diagrammi Mermaid (verificati con mermaid-cli in scratchpad); README riscritto in italiano con badge. validate_docs ora salta i blocchi ```mermaid/bash come alberi. Sourcery ha esaurito il budget settimanale (fino al ~2026-10-28).
