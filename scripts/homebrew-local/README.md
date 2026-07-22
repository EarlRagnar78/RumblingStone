# Homebrewery self-hosted in locale (Lotto K-B4 · decisione K-D5)

> **Cosa ottieni**: lo **stesso identico editor a due pannelli** (markdown a
> sinistra, anteprima stile Manuale del Giocatore a destra) di
> homebrewery.naturalcrit.com, ma su `http://localhost:8000`, tutto sul tuo
> PC: il contenuto della campagna non esce mai di casa. Il software è
> **The Homebrewery** (naturalcrit), licenza **MIT**.
>
> **Fonti ufficiali** (comandi ripresi ALLA LETTERA, recuperati il
> 2026-07-12 — non inventati):
> - `README.md` del repo [naturalcrit/homebrewery](https://github.com/naturalcrit/homebrewery) (sezione *Installation*)
> - `README.DOCKER.md` dello stesso repo (*Offline Install Instructions: Docker*)

---

## Via A — Installazione nativa (consigliata dal progetto per uso/sviluppo locale)

### Prerequisiti (dal README ufficiale)

1. [Node.js](https://nodejs.org/en/) **versione v16 o superiore**
2. [MongoDB Community](https://www.mongodb.com/try/download/community)
   (il database dove Homebrewery salva i brew; su Linux di solito basta il
   pacchetto della distro e avviare `mongod`)
3. [git](https://git-scm.com/downloads)

### Comandi (ufficiali)

```bash
# 1. clona il repo
git clone https://github.com/naturalcrit/homebrewery.git
cd homebrewery

# 2. variabile d'ambiente per l'esecuzione locale
#    Linux / macOS:
export NODE_ENV=local
#    Windows PowerShell:  $env:NODE_ENV="local"
#    Windows CMD:         set NODE_ENV=local

# 3. dipendenze + avvio
npm install
npm start
```

Con `mongod` in esecuzione, al primo avvio il server crea gli indici del
database (pochi secondi su un DB vuoto), poi:
**apri <http://localhost:8000> nel browser** e usi The Homebrewery offline.

**Scorciatoie di questo repo** (wrapper sottili sugli stessi comandi):

```bash
python3 scripts/dm.py hype setup   # = clone + NODE_ENV=local + npm install
python3 scripts/dm.py hype start   # = NODE_ENV=local + npm start (con check mongod)
```

Il clone finisce in `scripts/homebrew-local/homebrewery/` (gitignorato:
è software di terze parti, non contenuto di campagna).

---

## Via B — Container Docker, chiavi in mano (CONSIGLIATA: un comando solo)

> Il repo ufficiale include un **`docker-compose.yml` con entrambi i
> servizi** (MongoDB + Homebrewery, connessione già cablata via
> `MONGODB_URI: mongodb://mongodb/homebrewery`): non serve installare
> né Node né MongoDB sul PC — solo Docker.

### B.0 — Da zero: installare Docker (una volta sola)

- **Linux** (Docker Engine): <https://docs.docker.com/engine/install/>
  (scegli la tua distro: Ubuntu, Debian, Fedora, Arch, ...).
  Post-install raccomandati dal progetto: [uso senza root](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
  e [avvio al boot](https://docs.docker.com/engine/install/linux-postinstall/#configure-docker-to-start-on-boot).
- **Windows / macOS** (Docker Desktop): <https://docs.docker.com/desktop/>
  (dal pannello di Docker Desktop puoi impostare l'avvio automatico).

Verifica: `docker --version` e `docker compose version` devono rispondere.

### B.1 — Creare e avviare il container (il nostro wrapper, 1 comando)

```bash
python3 scripts/dm.py hype docker
```

Fa, nell'ordine (tutti passi della procedura ufficiale):
1. clona `https://github.com/naturalcrit/homebrewery.git` in
   `scripts/homebrew-local/homebrewery/` (se non c'è già);
2. scrive `config/docker.json` col **template ufficiale** del
   README.DOCKER.md (richiesto dal Dockerfile; la `mongodb_uri` del
   template è sovrascritta dalla env del compose ufficiale);
3. `docker compose up -d --build` → costruisce l'immagine e avvia
   **entrambi** i container (app + database) in background, con volume
   `mongodata` persistente per i tuoi brew.

Al termine: **apri <http://localhost:8000>** — editor a due pannelli.

Gestione:

```bash
python3 scripts/dm.py hype docker-stop   # ferma i container (i brew restano)
python3 scripts/dm.py hype docker        # ri-avvia (idempotente)
# log:   (da scripts/homebrew-local/homebrewery/)  docker compose logs -f homebrewery
```

### B.2 — Gli stessi passi a mano (comandi ufficiali, senza wrapper)

```bash
git clone https://github.com/naturalcrit/homebrewery.git
cd homebrewery
# crea config/docker.json col template ufficiale:
```

```json
{
"host" : "localhost:8000",
"naturalcrit_url" : "local.naturalcrit.com:8010",
"secret" : "secret",
"web_port" : 8000,
"mongodb_uri": "mongodb://172.17.0.2/homebrewery"
}
```

```bash
docker compose up -d --build   # → http://localhost:8000
```

In alternativa il README.DOCKER.md documenta anche i container separati
(`docker-compose build homebrewery` + due `docker run` distinti per
mongo e app): utile se vuoi `--restart unless-stopped` gestito a mano.

### B.3 — Note ufficiali (casi particolari)

- CPU vecchie **senza AVX**: MongoDB 5+ non parte → usare l'immagine
  `bitnami/mongo:latest` al posto di `mongo:latest`.
- **ARM** (es. Raspberry Pi): usare `arm64v8/mongo:4.4`.
- Da **CMD di Windows** `$(pwd)` non è valido: usare `%cd%` nei
  `docker run` manuali (col compose il problema non si pone).
- **Aggiornamento** (procedura ufficiale): dentro il clone
  `git pull`, poi ricostruire (`docker compose up -d --build`; o
  `docker rm -f homebrewery-app` + `docker-compose build homebrewery` +
  rilancio, nella variante a container separati).

---

## Flusso di lavoro con la campagna

1. `python3 scripts/dm.py recap --hype` (o `dm.py handout ...`) genera il
   file `.hb.md`;
2. apri `http://localhost:8000` → **New brew** → incolla il contenuto del
   `.hb.md`: pannello sinistro = markdown, pannello destro = anteprima
   PHB in tempo reale;
3. eventuali ritocchi estetici ricorrenti si codificano nel generatore
   (`scripts/hype_homebrew.py`), **non** a mano nel brew (ADR-0003).

## Perché self-hosted (ADR-0004)

- **Qualità identica per costruzione**: è lo stesso codice del sito.
- **Privacy totale**: il materiale (contenuto RHoD privato) resta locale.
- **Offline**: funziona senza rete, anche al tavolo.
