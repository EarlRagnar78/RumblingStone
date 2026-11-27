# Vedere il lavoro in sviluppo fuori da main

> Forma: **guida pratica** ([Diátaxis](../../plans/adr/ADR-0123-la-documentazione-segue-diataxis.md)).

Il lavoro già arrivato su `main` sta in [`MEMORIA.md`](../../MEMORIA.md). Quello
ancora in sviluppo (PR in bozza, rami, prove nelle cartelle condivise dei
thread) sta in [`plans/LAVORO-IN-CORSO.md`](../../plans/LAVORO-IN-CORSO.md),
una pagina generata dal registro curato
[`plans/lavoro-in-corso.json`](../../plans/lavoro-in-corso.json). Il perché è in
[ADR-0157](../../plans/adr/ADR-0157-il-lavoro-fuori-da-main-ha-una-pagina-dal-vivo.md).

## 1. Leggere la pagina

La pagina ha cinque parti:

- **Filoni**: un filone per riga, con stato, PR, rami, cartelle condivise,
  thread, che cosa aspetta e il passo dopo. Lo stato `aspetta-jfs` è quello
  che chiede qualcosa al DM;
- **Senza filone**: PR aperte, rami `claude/*` recenti e cartelle condivise
  recenti che il registro non nomina. Vanno attaccati a un filone o chiusi;
- **Da aggiornare o ferme**: PR del registro non più aperte, PR ferme da oltre
  30 giorni, filoni con l'ultimo aggiornamento più vecchio di 14 giorni;
- **Canali della piattaforma (ADR-0099)**: quanti componenti stanno in ogni
  canale e la tabella di quelli in `testing` e `unstable` (sezione 1-bis);
- **Dove guardare**: gli altri posti del lavoro.

La data in testa dice quando è stata fatta. Se è vecchia, si rigenera.

## 1-bis. I canali della piattaforma

Un componente nuovo (libreria, binario, cancello di CI) entra in `unstable`,
passa a `testing` con la versione fissata, la CI non bloccante e la misura
prima e dopo, e sale a `stable` dopo 14 giorni e 10 run su `main` con l'ok del
DM ([ADR-0099](../../plans/adr/ADR-0099-la-piattaforma-ha-tre-canali-come-debian.md)).
La pagina legge il canale dall'ultima colonna delle tabelle di §2 di
[`PIANO-PIATTAFORMA-DI-SVILUPPO.md`](../../plans/PIANO-PIATTAFORMA-DI-SVILUPPO.md):
la prima parola della cella dà il canale, la data «dal AAAA-MM-GG» l'ingresso,
e ogni riga della tabella porta il link alla sua riga del piano. Quelle
tabelle sono scritte a mano: per spostare un componente di canale si corregge
il piano, poi si rigenera la pagina. Quando il lotto P1 del piano porterà il
canale in `binari.py`, la fonte cambierà in una funzione sola
(`canali_piattaforma`).

Un filone può dichiarare il suo canale nel registro, con il campo facoltativo
`canale` (`stable`, `testing` o `unstable`); `--check` rifiuta gli altri valori.

## 2. Rigenerarla dal PC del DM

Dalla radice del clone, con Claude Code CLI o con OpenCode aperti nel repo:

```bash
/lavoro-in-corso
```

Il comando è lo stesso nei due strumenti: Claude Code lo legge da
`.claude/commands/lavoro-in-corso.md`, OpenCode da
`.opencode/commands/lavoro-in-corso.md`. Rigenera la pagina e ne fa un
riassunto in poche righe. Senza agente, da un terminale:

```bash
python3 scripts/lavoro_in_corso.py --fetch     # aggiorna i rami, poi scrive la pagina
python3 scripts/lavoro_in_corso.py --stdout    # la pagina a video, senza scrivere
python3 scripts/lavoro_in_corso.py --offline   # senza rete: niente PR
```

Le PR si leggono dalla REST pubblica di GitHub; un `GITHUB_TOKEN` o `GH_TOKEN`
nell'ambiente alza il limite delle richieste, ma non serve. Se la rete manca,
la pagina si fa lo stesso e lo scrive in testa.

Sul PC la cartella condivisa dei thread (`/mnt/project-files`) non c'è. La
pagina lo dice con una nota in testa: le cartelle che mostra vengono dal
registro, non da una misura, e la sezione delle cartelle recenti resta vuota.
Per vedere le cartelle vere serve la pagina rigenerata in un thread cloud.

## 3. Le sessioni, fuori dalla pagina

La pagina non legge le sessioni. Dove stanno:

- **thread cloud**: in claude.ai/code, nella lista dei thread del progetto. Il
  registro ne scrive il titolo, e una PR aperta da un thread porta nel corpo il
  suo `thread=cmsg_…`;
- **sessioni locali di Claude Code**: `claude --resume` nella cartella del
  clone elenca quelle aperte lì;
- **OpenCode**: tiene le sue sessioni per conto suo; si riprendono
  dall'elenco delle sessioni di `opencode`.

## 4. Aggiungere o aggiornare un filone

Il registro si scrive a mano, la pagina mai. Un filone in
`plans/lavoro-in-corso.json`:

```json
{
  "id": "drappo-flux",
  "titolo": "Immagini FLUX del Drappo (D2) sul portatile 4050",
  "stato": "aspetta-jfs",
  "thread": "Scrivere lo script FLUX per il 4050",
  "thread_id": "cmsg_…",
  "pr": [],
  "rami": [],
  "mnt": ["drappo-flux-2026-11-16"],
  "repo": [],
  "aspetta": "scegliere A o B dopo i confronti",
  "prossimo": "con la scelta, il lotto D2 delle immagini del Drappo",
  "aggiornato": "2026-11-27"
}
```

- `stato` è uno di `in-corso`, `aspetta-jfs`, `in-prova`, `fermo`; il loro
  significato sta nel campo `stati` del registro;
- `mnt` sono cartelle relative a `/mnt/project-files`; `repo` sono percorsi
  del repo, e devono esistere;
- quando un filone cambia, si cambiano insieme `stato`, `aspetta`, `prossimo`
  e `aggiornato`;
- un filone finito, con la PR unita e fuori dal canale testing, si toglie (scelta di Jfs del 27/11):
  da lì in poi lo racconta `MEMORIA.md`. Finché si misura su `main` resta, con
  stato `in-prova`;
- una cartella che non è lavoro (la coda della memoria storica, gli upload)
  va in `servizio`, con il motivo.

Niente dati personali nel registro: né email né nomi dei giocatori. Poi:

```bash
python3 scripts/lavoro_in_corso.py --check     # valida il registro, lo stesso controllo della CI
python3 scripts/lavoro_in_corso.py --fetch     # rigenera la pagina
```

Registro e pagina si portano su `main` con una PR, come ogni file del repo.

## 5. Se qualcosa non torna

| Sintomo | Causa | Cosa fare |
|---|---|---|
| `--check` esce 1 | il registro è malformato: stato sconosciuto, campo mancante, file di `repo` che non esiste | il messaggio dice il filone e il campo; si corregge il JSON |
| un ramo che c'è non compare | il clone non lo conosce | `--fetch` |
| «PR non lette» in testa | rete giù o limite della REST | si riprova, o si esporta con `gh pr list --json number,title,headRefName,isDraft,updatedAt,url,body > prs.json` e si passa `--pr-json prs.json` |
| una cartella vecchia sembra recente | la data è l'mtime del filesystem | si giudica dal titolo del LEGGIMI, non dalla data |
