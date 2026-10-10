#!/usr/bin/env bash
# avvia_languagetool.sh: un server LanguageTool LOCALE per il secondo lettore.
#
#   scripts/avvia_languagetool.sh [PORTA]        # default 8081, resta in primo piano
#   python3 scripts/ciclo_prosa.py segnala FILE --languagetool http://127.0.0.1:8081
#
# Perche' esiste (ADR-0079): LanguageTool trova qualche difetto che i rilevatori del
# repo non vedono (genere dei nomi propri, parentesi troncate, parole ripetute), ma
# vuole Java e 250 MB di jar. Per questo e' un passo FACOLTATIVO, fuori dalla CI.
#
# Il server ascolta solo su 127.0.0.1 (nessun --public) e ciclo_prosa.py rifiuta un
# indirizzo che non sia locale: il testo della campagna non esce dalla macchina.
# Non usare mai api.languagetool.org.
#
# Licenza: LanguageTool e' LGPL-2.1. Qui si scarica da Maven Central in una cache
# fuori dal repo e si usa come servizio: nessun suo file entra nel repo.
set -euo pipefail

VERSIONE="6.8"
PORTA="${1:-8081}"
CACHE="${RS_LT_CACHE:-$HOME/.cache/rumblingstone/languagetool-$VERSIONE}"

command -v java >/dev/null || { echo "serve Java 17 o superiore (java non trovato)" >&2; exit 1; }
command -v mvn  >/dev/null || { echo "serve Maven per scaricare i jar la prima volta (mvn non trovato)" >&2; exit 1; }

if [ ! -d "$CACHE/lib" ]; then
  mkdir -p "$CACHE"
  cat > "$CACHE/pom.xml" <<POM
<project xmlns="http://maven.apache.org/POM/4.0.0"><modelVersion>4.0.0</modelVersion>
<groupId>rumblingstone</groupId><artifactId>lt</artifactId><version>1</version>
<dependencies>
<dependency><groupId>org.languagetool</groupId><artifactId>languagetool-server</artifactId><version>$VERSIONE</version></dependency>
<dependency><groupId>org.languagetool</groupId><artifactId>language-it</artifactId><version>$VERSIONE</version></dependency>
</dependencies></project>
POM
  (cd "$CACHE" && mvn -q -B dependency:copy-dependencies -DoutputDirectory=lib)
fi

echo "LanguageTool $VERSIONE su http://127.0.0.1:$PORTA (solo locale). Ctrl+C per fermarlo."
exec java -cp "$CACHE/lib/*" org.languagetool.server.HTTPServer --port "$PORTA"
