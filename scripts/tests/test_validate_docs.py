"""Test di comportamento per validate_docs.py (gate anti-deriva doc<->filesystem).

Copre i casi che rendono il gate affidabile: deve **trovare** un percorso
inventato e deve **tacere** su citazioni legittime (abbreviazioni ADR, modelli
di nome, segnaposto, direttive di esclusione). Un validatore che dà falsi
positivi viene disattivato dopo due settimane: i casi negativi qui sotto sono
quelli che ne difendono la credibilità.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import validate_docs as vd  # noqa: E402


class TestTreeParsing(unittest.TestCase):
    def test_ricostruisce_i_percorsi_annidati(self):
        text = "```\ncampaign/\n├── state.md\n└── lore/\n    └── house-rules.md\n```\n"
        got = [p for _, p in vd.paths_from_tree_blocks(text)]
        self.assertIn("campaign/state.md", got)
        self.assertIn("campaign/lore/house-rules.md", got)

    def test_ignora_i_commenti_a_destra(self):
        text = "```\ncampaign/                 # commento con parole/slash\n```\n"
        self.assertEqual([p for _, p in vd.paths_from_tree_blocks(text)], ["campaign"])


class TestFalsiPositivi(unittest.TestCase):
    """Ogni caso qui è una citazione legittima: il gate NON deve segnalarla."""

    def test_abbreviazione_adr_accettata(self):
        # `plans/adr/ADR-0003` designa senza ambiguità un solo file.
        self.assertTrue(vd._exists("plans/adr/ADR-0003"))

    def test_prefisso_ambiguo_rifiutato(self):
        # `plans/adr/ADR-00` corrisponde a molti file: ambiguità = errore.
        self.assertFalse(vd._exists("plans/adr/ADR-00"))

    def test_modelli_di_nome_non_sono_percorsi(self):
        for tmpl in ("campaign/sessions/YYYY-MM-DD_session-N.md",
                     "campaign/npcs/[name-kebab-case].md"):
            self.assertTrue(
                vd.PLACEHOLDER.search(tmpl) or vd.NAME_TEMPLATE.search(tmpl),
                f"{tmpl} dovrebbe essere riconosciuto come modello",
            )

    def test_mirror_generati_esclusi(self):
        self.assertTrue(vd._is_generated_mirror(".claude/skills/x"))
        self.assertFalse(vd._is_generated_mirror(".github/workflows/ci.yml"))


class TestDirettiveDiEsclusione(unittest.TestCase):
    def test_ignore_su_singola_riga(self):
        text = "a\n`campaign/inesistente/` <!-- validate-docs: ignore -->\nb\n"
        self.assertEqual(vd.ignored_lines(text), {2})

    def test_ignore_a_blocco(self):
        text = ("a\n<!-- validate-docs: ignore-begin -->\nx\ny\n"
                "<!-- validate-docs: ignore-end -->\nb\n")
        self.assertEqual(vd.ignored_lines(text), {2, 3, 4, 5})


class TestGateReale(unittest.TestCase):
    def test_il_repo_e_pulito(self):
        """Il gate deve essere verde sul repo: è la condizione per tenerlo in CI."""
        tops = vd._toplevel_dirs()
        problems = []
        for d in vd.DEFAULT_DOCS:
            problems.extend(vd.check_doc(d, tops))
        self.assertEqual(problems, [], f"percorsi citati e inesistenti: {problems}")

    def test_trova_un_percorso_inventato(self):
        """Caso negativo: un documento che asserisce una cartella inesistente fallisce."""
        doc = ROOT / "scripts" / "tests" / "fixtures" / "_tmp_validate_docs.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("```\ncampaign/\n└── npcs/\n```\n", encoding="utf-8")
        try:
            problems = vd.check_doc(str(doc.relative_to(ROOT)), vd._toplevel_dirs())
            self.assertTrue(any(p["path"] == "campaign/npcs" for p in problems))
        finally:
            doc.unlink()


class TestLinkDentroBacktick(unittest.TestCase):
    """Lotto 4b: un link citato dentro i backtick e' sintassi, non un rimando.

    Nove hit su ventisei erano di questa forma — fra cui, per intero, la riga di
    `plans/CHANGELOG.md` che descriveva proprio questo difetto nel convertitore
    Typst. Il rischio della correzione e' l'opposto: spegnere il controllo. I due
    test vanno letti in coppia.
    """

    def _link(self, riga: str) -> list[str]:
        doc = ROOT / "plans" / "FINTO.md"
        return [p for _, p in vd.paths_from_links(riga + "\n", doc)]

    def test_link_dentro_backtick_non_conta(self):
        self.assertEqual(self._link("il convertitore non gestisce `![alt](path)` e"), [])
        self.assertEqual(self._link("usciva stampato come `![Stemma](non/esiste.png)`"), [])

    def test_link_fuori_backtick_conta_ancora(self):
        """La correzione non deve spegnere il controllo: stesso link, senza backtick."""
        self.assertEqual(self._link("vedi [la spec](adr/ADR-9999-inventato.md)"),
                         ["plans/adr/ADR-9999-inventato.md"])

    def test_backtick_riaperti_sulla_stessa_riga(self):
        """Due span di codice: quel che sta *in mezzo* resta un link vero."""
        got = self._link("`![a](x)` poi [vero](adr/ADR-9999-inventato.md) poi `![b](y)`")
        self.assertEqual(got, ["plans/adr/ADR-9999-inventato.md"])

    def test_la_lunghezza_della_riga_e_conservata(self):
        """Si svuota, non si toglie: i numeri di colonna devono restare veri."""
        riga = "prima `![alt](path)` dopo"
        self.assertEqual(len(vd.senza_code_span(riga)), len(riga))


class TestLinkDentroCommentiHtml(unittest.TestCase):
    """Lotto E1: terza famiglia di falsi positivi, stessa forma delle prime due.

    I tre `URL` rimasti nei booklet dopo la correzione del generatore erano
    tutti dentro un commento HTML che *spiega al DM la sintassi da usare*:

        <!-- Copertina: carica un'immagine sul brew e inserisci qui:
             ![background](URL){position:absolute,...} -->

    Un commento non viene reso da nessun lettore markdown, quindi non puo'
    contenere un riferimento vivo. I due test vanno letti in coppia.
    """

    def _link(self, testo: str) -> list[str]:
        doc = ROOT / "plans" / "FINTO.md"
        return [p for _, p in vd.paths_from_links(testo, doc)]

    def test_link_dentro_un_commento_non_conta(self):
        self.assertEqual(self._link("<!-- usa ![bg](URL) qui -->\n"), [])
        self.assertEqual(
            self._link("<!-- vedi [x](adr/ADR-9999-inventato.md) -->\n"), [])

    def test_commento_su_piu_righe(self):
        testo = ("<!-- Copertina: carica un'immagine\n"
                 "     e inserisci ![bg](adr/ADR-9999-inventato.md) -->\n")
        self.assertEqual(self._link(testo), [])

    def test_link_fuori_dal_commento_conta_ancora(self):
        """La correzione non deve spegnere il controllo."""
        self.assertEqual(self._link("vedi [x](adr/ADR-9999-inventato.md)\n"),
                         ["plans/adr/ADR-9999-inventato.md"])

    def test_quel_che_sta_dopo_il_commento_conta(self):
        testo = "<!-- ![bg](URL) --> poi [vero](adr/ADR-9999-inventato.md)\n"
        self.assertEqual(self._link(testo), ["plans/adr/ADR-9999-inventato.md"])

    def test_i_numeri_di_riga_restano_veri(self):
        """Si svuota, non si toglie: la riga 3 deve restare la riga 3."""
        testo = "<!-- a\nb -->\n[x](adr/ADR-9999-inventato.md)\n"
        righe = [n for n, _ in vd.paths_from_links(testo, ROOT / "plans" / "FINTO.md")]
        self.assertEqual(righe, [3])

    def test_le_direttive_restano_leggibili_altrove(self):
        """`ignored_lines` legge il testo GREZZO: svuotare i commenti nei link
        non deve renderla cieca alle proprie direttive."""
        testo = "a\n`x/y/z` <!-- validate-docs: ignore -->\nb\n"
        self.assertEqual(vd.ignored_lines(testo), {2})


class TestPercorsiAssoluti(unittest.TestCase):
    def _scrivi(self, testo: str) -> str:
        doc = ROOT / "scripts" / "tests" / "fixtures" / "_tmp_assoluti.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text(testo, encoding="utf-8")
        return str(doc.relative_to(ROOT))

    def test_boccia_un_checkout_personale(self):
        # Il fixture contiene il difetto per costruzione: la direttiva vale anche
        # per questo file.  validate-docs: ignore
        rel = self._scrivi("cd /home/tizio/Scrivania/RumblingStone/campaign\n")  # validate-docs: ignore
        try:
            self.assertEqual(len(vd.percorsi_assoluti(rel)), 1)
        finally:
            (ROOT / rel).unlink()

    def test_la_direttiva_lo_lascia_passare(self):
        """Chi *descrive* il difetto invece di commetterlo deve poterlo scrivere."""
        rel = self._scrivi("cd /home/tizio/RumblingStone <!-- validate-docs: ignore -->\n")
        try:
            self.assertEqual(vd.percorsi_assoluti(rel), [])
        finally:
            (ROOT / rel).unlink()

    def test_le_home_di_servizio_non_sono_un_difetto(self):
        """Il primo giro ne segnalo' undici in `converters/`, tutte corrette.

        Unit systemd, Dockerfile, il path standard di Homebrew su Linux: sono
        destinazioni di deploy, non la scrivania di chi scrive. Il segno che
        distingue le due cose e' il nome del repo dentro il percorso.
        """
        rel = self._scrivi(
            'WorkingDirectory=/home/htmlconverter/tools/html-converter\n'
            'export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"\n'
            'ENV PATH="/home/converter/.local/bin:${PATH}"\n'
        )
        try:
            self.assertEqual(vd.percorsi_assoluti(rel), [])
        finally:
            (ROOT / rel).unlink()


class TestSorgenti(unittest.TestCase):
    def test_esclude_generati_e_vendored(self):
        for rel in ("07_arco/homebrew/X.hb.md", "build/out.md",
                    "scripts/typst/packages/preview/droplet/0.3.1/README.md",
                    ".claude/skills/x/SKILL.md"):
            self.assertTrue(vd._e_generato(rel), f"{rel} andrebbe escluso")

    def test_tiene_i_sorgenti(self):
        for rel in ("plans/CHANGELOG.md", "docs/guides/GUIDA-MAPPE.md",
                    ".github/workflows/ci.yml"):
            self.assertFalse(vd._e_generato(rel), f"{rel} andrebbe tenuto")

    def test_enumera_dal_repo_non_da_un_elenco_a_mano(self):
        """Quarta regola di ADR-0045: l'insieme si conta, non si dichiara."""
        md = vd.sorgenti(".md")
        self.assertIn("plans/CHANGELOG.md", md)
        self.assertGreater(len(md), 400)
        self.assertFalse([f for f in md if f.endswith(".hb.md")])


class TestIndiceADR(unittest.TestCase):
    """Lotto 4b: un elenco a mano accanto a una cartella si sfasa.

    `docs/INDEX.md` §4 si era fermato ad ADR-0020 mentre `plans/adr/` era a 0048:
    ventotto assenze, invisibili al controllo sui percorsi perche' nessun link
    era rotto. Stessa forma delle 13 skill su 18 di ADR-0041.
    """

    def test_il_repo_e_allineato(self):
        self.assertEqual(vd.indice_adr(), [], "ADR esistenti e non elencati")

    def test_conta_dalla_cartella_non_dall_elenco(self):
        """Quarta regola di ADR-0045: l'insieme si conta dalla fonte."""
        su_disco = {f.name for f in (ROOT / vd.CARTELLA_ADR).glob("ADR-*.md")}
        citati = set(vd.LINK_ADR.findall((ROOT / vd.INDICE_ADR).read_text(encoding="utf-8")))
        self.assertGreater(len(su_disco), 40)
        self.assertEqual(su_disco - citati, set())


class TestGateSorgentiSulRepoVero(unittest.TestCase):
    def test_zero_link_rotti_e_zero_percorsi_assoluti(self):
        """La condizione per tenere `--sorgenti` in CI. Lotto 4b."""
        tops = vd._toplevel_dirs()
        problemi = []
        for d in vd.sorgenti(".md"):
            problemi.extend(vd.check_doc(d, tops, solo_link=True))
        for d in vd.sorgenti(".md", ".py"):
            problemi.extend(vd.percorsi_assoluti(d))
        problemi.extend(vd.indice_adr())
        self.assertEqual(problemi, [], f"il repo non e' pulito: {problemi}")


if __name__ == "__main__":
    unittest.main()


class TestIFileNuoviNonSonoInvisibili(unittest.TestCase):
    """🐛 Il cancello era cieco ai file non ancora in stage (2026-09-16).

    `sorgenti()` enumerava da `git ls-files`, che elenca i **tracciati**: un
    documento appena creato non veniva guardato finche' qualcuno non lo
    aggiungeva. Chi scriveva un ADR nuovo con un link rotto dentro vedeva
    **verde in locale e rosso in CI** un minuto dopo, al primo `git add`.

    E' successo davvero: `ADR-0050`, creato nel lotto 4d-1, citava un nome di
    file inventato per ADR-0041, e il giro completo dei sedici cancelli —
    eseguito apposta prima di spingere — l'aveva dato verde **due volte**. Il
    difetto non era la disattenzione di chi scriveva: era che il controllo
    locale **non poteva** vederlo.
    """

    def test_un_file_nuovo_entra_nell_enumerazione(self):
        nuovo = ROOT / "plans" / "adr" / "ZZZ-prova-file-nuovo.md"
        nuovo.write_text("[x](ADR-9999-che-non-esiste.md)\n", encoding="utf-8")
        try:
            self.assertIn("plans/adr/ZZZ-prova-file-nuovo.md", vd.sorgenti(),
                          "un file nuovo non tracciato deve essere gia' guardato")
        finally:
            nuovo.unlink()

    def test_e_il_gate_lo_boccia(self):
        """L'altra meta': vederlo non basta, deve anche diventare rosso."""
        nuovo = ROOT / "plans" / "adr" / "ZZZ-prova-file-nuovo.md"
        nuovo.write_text("[x](ADR-9999-che-non-esiste.md)\n", encoding="utf-8")
        try:
            esito = subprocess.run(
                [sys.executable, "scripts/validate_docs.py", "--sorgenti"],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(esito.returncode, 1)
            self.assertIn("ZZZ-prova-file-nuovo", esito.stdout + esito.stderr)
        finally:
            nuovo.unlink()

    def test_i_file_ignorati_restano_fuori(self):
        """`--exclude-standard` e' la meta' che impedisce al gate di esplodere.

        Senza, l'enumerazione si mangerebbe `build/`, le cache e tutto cio'
        che `.gitignore` tiene fuori — e un gate che boccia troppo viene
        spento al primo giro.
        """
        sorgente = (ROOT / "scripts" / "validate_docs.py").read_text(encoding="utf-8")
        self.assertIn("--exclude-standard", sorgente)
        for f in vd.sorgenti():
            self.assertFalse(f.startswith("build/"), f)


class TestIlNumeroDiUnAdrEUnico(unittest.TestCase):
    """🐛 `ADR-0049` e' stato dato DUE VOLTE in due giorni (2026-09-16).

    Prima all'edizione commerciale (PR #138), poi al margine del bosco
    (PR #141), perche' chi scriveva il secondo — io — non ha guardato la
    cartella. **Nessun controllo poteva vederlo**: nessun link era rotto e
    nessun ADR mancava dall'indice, che si limitava a mostrare due righe con
    lo stesso numero.

    Il numero di un ADR e' la sua identita': si cita nei commit, nei piani, nel
    codice e nei changelog. Due decisioni che lo condividono rendono ambigua
    ogni citazione **all'indietro**, sui documenti gia' scritti — e il repo ne
    ha centinaia.

    ⚠️ Il limite: il gate vede la collisione **dopo** che il file esiste. La
    meta' preventiva e' `--prossimo-adr`, ed e' per quello che la regola d'oro
    dice di eseguirlo PRIMA di scrivere.
    """

    def test_sul_repo_vero_nessun_numero_e_doppio(self):
        self.assertEqual(vd.adr_duplicati(), [])

    def test_il_gate_morde(self):
        """Ricreata la collisione vera, non una inventata."""
        gemello = ROOT / "plans" / "adr" / "ADR-0051-ZZZ-prova-collisione.md"
        gemello.write_text("# prova\n", encoding="utf-8")
        try:
            duplicati = vd.adr_duplicati()
            self.assertTrue(duplicati, "due file con ADR-0051 devono dare rosso")
            self.assertEqual({p["path"] for p in duplicati}, {"ADR-0051"})
            esito = subprocess.run(
                [sys.executable, "scripts/validate_docs.py", "--sorgenti"],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(esito.returncode, 1)
        finally:
            gemello.unlink()

    def test_il_prossimo_numero_e_quello_giusto(self):
        """La meta' che rende la regola seguibile invece che solo esigibile."""
        usati = vd.numeri_adr()
        atteso = f"ADR-{max(int(n) for n in usati) + 1:04d}"
        self.assertEqual(vd.prossimo_adr(), atteso)
        esito = subprocess.run(
            [sys.executable, "scripts/validate_docs.py", "--prossimo-adr"],
            cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(esito.returncode, 0, esito.stderr)
        self.assertIn(atteso, esito.stdout)

    def test_il_comando_segnala_le_collisioni_gia_presenti(self):
        gemello = ROOT / "plans" / "adr" / "ADR-0051-ZZZ-prova-collisione.md"
        gemello.write_text("# prova\n", encoding="utf-8")
        try:
            esito = subprocess.run(
                [sys.executable, "scripts/validate_docs.py", "--prossimo-adr"],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(esito.returncode, 1)
            self.assertIn("ADR-0051", esito.stderr)
        finally:
            gemello.unlink()
