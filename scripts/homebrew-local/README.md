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

## Via B — Docker (dal README.DOCKER.md ufficiale)

Per chi preferisce i container (evita l'installazione manuale di MongoDB).

```bash
# 1. clona e prepara l'immagine
git clone https://github.com/naturalcrit/homebrewery.git
cd homebrewery
```

Crea/adatta `config/docker.json` (template ufficiale):

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
docker-compose build homebrewery

# 2. container MongoDB
docker run --name homebrewery-mongodb -d --restart unless-stopped \
  -v mongodata:/data/db -p 27017:27017 mongo:latest

# 3. container Homebrewery (dalla cartella homebrewery/)
docker run --name homebrewery-app -d --restart unless-stopped \
  -e NODE_ENV=docker \
  -v $(pwd)/config/docker.json:/usr/src/app/config/docker.json \
  -p 8000:8000 docker.io/library/homebrewery:latest
```

Note ufficiali: su CPU vecchie senza AVX usare `bitnami/mongo:latest`;
su ARM (es. Raspberry Pi) usare `arm64v8/mongo:4.4`; da CMD di Windows
sostituire `$(pwd)` con `%cd%`. Per aggiornare: `docker rm -f
homebrewery-app`, poi `git pull`, `docker-compose build homebrewery` e
rilanciare il `docker run` dell'app.

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
