# Il ripiego senza PyYAML in `compress_skills.py`: si fa?

Domanda del DM (2026-11-08): misurare se vale la pena e decidere in base alla
misura. Era l'ultima casella opzionale di PIANO-AUDIT-SCRIPTS, ripresa da
RECUPERO D5.

## Cosa si è misurato

1. **Il ripiego funziona?** `misura_ripiego.py` (da eseguire dalla radice del
   repo) prova un parser minimo del frontmatter (`chiave: valore`, blocchi
   `>` e `|`) e un'uscita JSON al posto di `yaml.dump` (il JSON è YAML valido).
   Su 18 skill su 18 `name` e `description` coincidono con PyYAML, e su 18 su 18
   `structured.yaml` dà gli stessi dati. Tecnicamente si può fare.
2. **Chi lo userebbe?** Il ripiego serve solo dove PyYAML manca:
   - la CI installa `requirements.txt`, dove c'è `pyyaml>=6.0.3`;
   - il bundle offline (`bundle_offline.py`) porta le wheel di `requirements.txt`.
     PyYAML 6.0.3 ha la wheel cp313 per linux x86_64 e aarch64, macOS arm64 e
     Windows amd64 (scaricate con `pip download --only-binary` il 2026-11-08);
   - senza `pip install -r requirements.txt`, oltre a `compress_skills.py`
     falliscono altri 17 script che importano `yaml`, fra cui `validate_skills`,
     `validate_state`, `state_apply` e `riscontro_srd`. Con PyYAML nascosto,
     `build-skills.sh` si ferma al passo 2 con
     `ERROR: PyYAML required (pip install pyyaml)` e codice 2, che è il
     messaggio giusto.
3. **Cosa costerebbe?** Circa 30 righe di parser YAML fatto in casa, con i
   suoi test. Si romperebbe al primo frontmatter con una lista, una chiave
   annidata o due punti dentro un valore senza virgolette. In più
   `structured.yaml` cambierebbe forma (stile JSON invece dello stile a
   blocchi) secondo l'ambiente, quindi lo stesso commit darebbe due pacchetti
   diversi.

## Decisione

**Non si fa.** Il ripiego copre un solo caso, l'installazione saltata, in cui
il repo è comunque rotto in altri 17 posti e lo script lo dice già in modo
chiaro. Costa un parser non standard e un'uscita che dipende dall'ambiente.
Vale la regola del 2026-11-08: si parte dallo standard di fatto (PyYAML,
dentro il pacchetto come le altre librerie), e il fatto in casa entra solo se
la misura boccia lo standard. Qui la misura non lo boccia.

**Da rivedere se** una piattaforma del bundle resta senza wheel di PyYAML, o se
`compress_skills.py` deve girare in un posto dove non si installa niente.
