No, mai `git checkout --ours` sul file intero: perderei le correzioni di main. Risolvo blocco per blocco: nei record del giocato (PF e risorse dopo la sessione 5) vince il ramo, nella sezione png e nelle correzioni di canone approvate su main vince main, e se lo stesso record è cambiato dai due lati mi fermo e lo chiedo al DM. Dopo il merge: `python3 scripts/sincronia_giocato.py --dopo-merge`, `python3 scripts/validate_state.py`, `python3 scripts/render_state.py --check`, `python3 scripts/dm.py doctor`; se uno fallisce non spingo.

Documentazione da aggiornare: nessuna
