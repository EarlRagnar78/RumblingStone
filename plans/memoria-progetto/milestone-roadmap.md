---
name: milestone-roadmap
description: Milestone della roadmap fissate il 2026-11-10: GitHub Milestones v1.1.0-v1.5.0 con criteri d'uscita misurabili, specchio in DECISIONI-E-ROADMAP.md
metadata:
  type: project
---
Jfs 2026-11-10: fissare le milestone della roadmap con gli standard di fatto della community. Fatto con SemVer + Keep a Changelog (già nel repo) + GitHub Milestones intitolate con la versione (create via `gh api repos/gsamuele78/RumblingStone/milestones`, numeri 1-5).
- 1 v1.1.0 Motore e cancelli (ciò che è su main dopo v1.0.0 + recupero documentazione)
- 2 v1.2.0 Regole complete 3.5/SRD/PF1e (blocco 1-sexies, promozioni 22-24/11)
- 3 v1.3.0 Standard del volume e booklet di serata (ADR-0122)
- 4 v1.4.0 Indice P19-P30 (blocco 2)
- 5 v1.5.0 Piattaforma (blocco 3)
Senza date di consegna: una milestone chiude quando i criteri d'uscita sono misurati veri. Definizione di «fatto» comune = [[documentazione-a-ogni-milestone]]. Il thread padre assegna ogni PR alla milestone al merge (`gh api -X PATCH .../issues/N -f milestone=K`). Da verificare nella PR di rilascio: se c'è una rottura della superficie pubblica (docs/RILASCIO.md) la 1.1.0 diventa 2.0.0. Vedi [[thread-padre-pr]].
