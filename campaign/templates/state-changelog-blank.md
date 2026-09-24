# Changelog dello stato di campagna — append-only

> Lo storico di `campaign/state.md` per questo gruppo. Lo copia
> `scripts/azzera_partita.py` quando un gruppo nuovo parte (ADR-0050 §7).
>
> 🔴 **Append-only.** Ogni riga e' un fatto gia' successo al tavolo. Non si
> cancella, non si riordina e non si ricompatta: quando una voce risulta
> sbagliata si **aggiunge** la correzione con la sua data.
>
> Ci scrive `scripts/state_apply.py`, dentro la regione `changelog` qui sotto.

<!-- auto:begin key=changelog -->
```
YYYY-MM-DD  Gruppo nuovo: stato azzerato dal template (sessione 0).
```
<!-- auto:end key=changelog -->
