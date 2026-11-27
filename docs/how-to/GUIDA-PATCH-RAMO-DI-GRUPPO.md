# Guida: applicare una patch al ramo di gruppo

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

> **A chi serve.** Al DM che deve portare sul ramo della partita
> (`campaign-group-rumblingstone`) le correzioni di canone preparate nei thread.
> Il ramo di gruppo lo tocca solo il DM, a mano: è il triplo vincolo di
> [ADR-0007](../../plans/adr/ADR-0007-scritture-canone-triplo-vincolo.md), e il
> ramo è quello di [ADR-0090](../../plans/adr/ADR-0090-la-partita-riparte-su-un-ramo-di-gruppo-nuovo.md).
> Chi prepara le patch non fa mai push su quel ramo.

---

## §0 · In breve

```bash
cd ~/RumblingStone                                   # la tua copia del repo
git fetch origin
git switch campaign-group-rumblingstone
git pull --ff-only
git status                                           # deve dire «nothing to commit»
git am --3way ~/patch-gruppo/*.patch                 # applica le patch in ordine
python3 scripts/render_state.py --check              # state.md uguale a state.yaml
python3 scripts/validate_state.py
git log --oneline -6                                 # controlla i commit nuovi
git push origin campaign-group-rumblingstone
```

---

## §1 · Cosa ti arriva

Una cartella con file numerati `0001-….patch`, `0002-….patch`, … nella Library
del progetto (sotto `/mnt/project-files/`). Ogni file è un commit completo, con
autore, data e messaggio, preparato con `git format-patch`. Il numero dice
l'ordine: vanno applicati tutti e nell'ordine dato.

Prima di consegnarle, chi le prepara le prova su una copia pulita del ramo di
gruppo (`git am` più `render_state.py --check`). Se una serie dice di essere
stata provata, a te serve solo applicarla.

## §2 · I passi, uno per uno

1. **Scarica la cartella.** Dalla Library del progetto, salva tutti i file
   `.patch` in una cartella tua, per esempio `~/patch-gruppo/`. Non rinominarli.
2. **Porta il ramo all'ultima versione.**
   ```bash
   cd ~/RumblingStone
   git fetch origin
   git switch campaign-group-rumblingstone
   git pull --ff-only
   ```
   Se `pull --ff-only` rifiuta, hai commit locali non spinti: spingili prima
   (`git push origin campaign-group-rumblingstone`), oppure chiedi nel thread.
3. **Controlla che non ci sia lavoro a metà.** `git status` deve dire «nothing
   to commit, working tree clean». Se ci sono modifiche, fai commit o
   `git stash` prima di andare avanti.
4. **Applica la serie.**
   ```bash
   git am --3way ~/patch-gruppo/*.patch
   ```
   `--3way` risolve da solo i piccoli spostamenti di righe. Ogni patch diventa
   un commit sul ramo, con il suo messaggio.
5. **Controlla lo stato della campagna.** `state.yaml` è il master e
   `state.md` si genera da lì:
   ```bash
   python3 scripts/render_state.py --check
   python3 scripts/validate_state.py
   ```
   Entrambi devono finire con ✓. Se `render_state --check` dice «fuori sync»,
   lancia `python3 scripts/render_state.py` e fai un commit in più con il file
   rigenerato.
6. **Guarda cosa è entrato.**
   ```bash
   git log --oneline -6
   git show --stat HEAD
   ```
7. **Spingi.**
   ```bash
   git push origin campaign-group-rumblingstone
   ```
   Se il push chiede un utente sbagliato (per esempio un vecchio account
   salvato nel portachiavi), lancia una volta `gh auth setup-git` e riprova.

## §3 · Se qualcosa va storto

| Cosa vedi | Cosa fare |
|---|---|
| `git am` si ferma con «patch does not apply» o un conflitto | `git am --abort` riporta il ramo com'era. Scrivi nel thread quale file si è fermato: la serie va rifatta sul ramo aggiornato. |
| `git am` si ferma, il conflitto è piccolo e lo sai risolvere | correggi il file, poi `git add <file>` e `git am --continue` |
| «previous rebase directory … still exists» | c'è un `git am` lasciato a metà: `git am --abort`, poi ricomincia dal passo 4 |
| `render_state --check` fallisce dopo l'applicazione | `python3 scripts/render_state.py`, poi `git commit -am "state.md rigenerato"` |
| Vuoi tornare indietro **prima** del push | `git reset --hard origin/campaign-group-rumblingstone` |
| Vuoi tornare indietro **dopo** il push | `git revert <commit>` per ogni commit da annullare, poi push |

## §4 · Per chi prepara le patch

- Parti dall'ultimo `origin/campaign-group-rumblingstone`, mai da `main`: i due
  rami non hanno più la stessa storia (ADR-0090).
- Cambia `campaign/state.yaml` e rigenera `state.md` con `render_state.py`.
  Una patch che tocca solo `state.md` lascia il ramo fuori sync.
- Prova la serie intera su una copia pulita (`git worktree add`, `git am`,
  `render_state.py --check`, `validate_state.py`) prima di consegnarla.
- Consegna una sola cartella per serie, con i file di `git format-patch`
  numerati. Se una serie nuova ingloba patch vecchie, dillo, così le vecchie
  non vengono applicate due volte.
