"""Il server MCP: il protocollo davvero parlato, e le sei difese una per una.

I test di protocollo guidano il server **attraverso stdio** — `initialize` →
`tools/list` → `tools/call` — invece di chiamarne le funzioni interne. Chiamare
le funzioni dà test verdi e un server che non parla.

Le difese hanno un test a testa perché sono la ragione per cui questo processo può
esistere: espone 45 programmi a un agente. Il progetto sta in
`plans/SPEC-SERVER-MCP.md`, le difese si chiamano S-1…S-6 anche lì.

Solo `unittest`: la CI non installa pytest.
"""
from __future__ import annotations

import io
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))

import mcp_server as M  # noqa: E402


def parla(*richieste: dict, scrittura: bool = False, timeout: int = 60) -> list[dict]:
    """Guida il server sul suo trasporto: una riga JSON per messaggio."""
    entrata = io.StringIO("\n".join(json.dumps(r) for r in richieste) + "\n")
    uscita = io.StringIO()
    M.Server(M.carica(), scrittura=scrittura, timeout=timeout).gira(entrata, uscita)
    return [json.loads(r) for r in uscita.getvalue().splitlines() if r.strip()]


def chiama(nome: str, argomenti: dict | None = None, **kw) -> dict:
    return parla({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                  "params": {"name": nome, "arguments": argomenti or {}}}, **kw)[0]


class TestProtocollo(unittest.TestCase):
    def test_initialize_dichiara_versione_e_capacita(self):
        r = parla({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})[0]
        self.assertEqual(r["result"]["protocolVersion"], M.PROTOCOLLO)
        self.assertIn("tools", r["result"]["capabilities"])

    def test_una_notifica_non_riceve_risposta(self):
        # Rispondere a una notifica JSON-RPC è un errore di protocollo: il client
        # non ha nessun `id` a cui appaiare la risposta.
        self.assertEqual(parla({"jsonrpc": "2.0", "method": "notifications/initialized"}), [])

    def test_tools_list_espone_il_catalogo_con_le_annotazioni(self):
        ts = parla({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})[0]["result"]["tools"]
        self.assertEqual(len(ts), len(M.carica()))
        for t in ts:
            self.assertIn("inputSchema", t)
            for chiave in ("readOnlyHint", "destructiveHint", "idempotentHint"):
                self.assertIn(chiave, t["annotations"], t["name"])

    def test_json_malformato_e_un_errore_di_protocollo_e_il_server_non_muore(self):
        u = io.StringIO()
        M.Server(M.carica()).gira(io.StringIO('non json\n{"jsonrpc":"2.0","id":9,"method":"ping"}\n'), u)
        r = [json.loads(x) for x in u.getvalue().splitlines()]
        self.assertEqual(r[0]["error"]["code"], M.PARSE)
        self.assertEqual(r[1]["result"], {})     # la riga dopo funziona ancora

    def test_metodo_ignoto(self):
        r = parla({"jsonrpc": "2.0", "id": 1, "method": "tools/inventati"})[0]
        self.assertEqual(r["error"]["code"], M.METODO)


class TestDifese(unittest.TestCase):
    def test_S1_solo_i_tool_del_manifest(self):
        r = chiama("rm_rf")
        self.assertEqual(r["error"]["code"], M.PARAMETRI)
        self.assertIn("sconosciuto", r["error"]["message"])

    def test_S1_le_cartelle_non_sono_tool(self):
        # Tre voci del manifest sono cartelle con un README: annunciarle
        # significa prometterle e fallire al primo tentativo.
        self.assertNotIn("converters_html_to_markdown", M.carica())

    def test_S2_niente_shell_i_metacaratteri_restano_dati(self):
        argv = M.costruisci(M.carica()["validate_prosa"], {"files": "x; rm -rf /"})
        # Resta **un pezzo solo** della lista argv — cioè un nome di file assurdo,
        # non un comando. (La barra finale la normalizza la risoluzione del
        # percorso, che è S-4 e fa il suo mestiere.)
        self.assertTrue(argv[-1].startswith("x; rm -rf"), argv)
        self.assertEqual(len([x for x in argv if ";" in x]), 1, argv)
        self.assertNotIn(";", argv[0])

    def test_S3_tipo_sbagliato(self):
        self.assertIn("intero", chiama("suggest_encounter", {"el": "sei"})["error"]["message"])

    def test_S3_chiave_sconosciuta(self):
        r = chiama("validate_prosa", {"pippo": 1})
        self.assertIn("non previsti", r["error"]["message"])

    def test_S3_enum_rispettato(self):
        r = chiama("dm", {"prep|post|session|recap|handout|maps|hype|dossier|skills|doctor": "distruggi"})
        self.assertEqual(r["error"]["code"], M.PARAMETRI)

    def test_S4_niente_traversamento(self):
        r = chiama("validate_prosa", {"files": "../../../etc/passwd"})
        self.assertIn("esce dalla radice", r["error"]["message"])

    def test_S4_niente_percorsi_assoluti_fuori(self):
        self.assertIn("esce dalla radice",
                      chiama("validate_prosa", {"files": "/etc/passwd"})["error"]["message"])

    def test_S4_un_percorso_del_repo_passa(self):
        self.assertEqual(M.costruisci(M.carica()["validate_prosa"],
                                      {"files": "README.md"})[-1], "README.md")

    def test_S5_chi_scrive_canone_non_parte_in_sola_lettura(self):
        r = chiama("state_apply")
        self.assertEqual(r["error"]["code"], M.PARAMETRI)
        self.assertIn("ADR-0007", r["error"]["message"])

    def test_S5_ma_resta_elencato(self):
        # Nasconderlo lo trasformerebbe in una richiesta fatta a mano, di nascosto.
        nomi = [t["name"] for t in
                parla({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})[0]["result"]["tools"]]
        self.assertIn("state_apply", nomi)

    def test_S5_con_allow_write_arriva_a_partire(self):
        r = chiama("state_apply", {"check": True}, scrittura=True)
        self.assertNotIn("error", r, "in scrittura non deve essere rifiutato a priori")

    def test_S6_il_timeout_e_un_risultato_non_un_guasto(self):
        r = M.esegui({"id": "finto", "exit_codes": {}},
                     [sys.executable, "-c", "import time; time.sleep(5)"], timeout=1)
        self.assertTrue(r["isError"])
        self.assertIn("entro 1 s", r["content"][0]["text"])

    def test_S6_output_troncato(self):
        r = M.esegui({"id": "finto", "exit_codes": {}},
                     [sys.executable, "-c", "print('x' * 5000)"], tetto=100)
        self.assertIn("troncato", r["content"][0]["text"])


class TestEsitiDeiTool(unittest.TestCase):
    def test_uscita_diversa_da_zero_e_un_risultato_col_significato_del_codice(self):
        # `validate_lingua` esce 1 per progetto. Se il server lo trasformasse in
        # un errore JSON-RPC, il client vedrebbe un guasto dove c'e' un referto.
        # Era `suggest_encounter` senza --el, che dal 2026-09-03 riesce leggendo
        # il Party APL da state.md. Serve un tool che decida ancora di no.
        r = chiama("build_chapter_marks")        # ne' --serie ne' --all: uscita 2
        self.assertNotIn("error", r)
        self.assertTrue(r["result"]["isError"])
        self.assertIn("uscita 2", r["result"]["content"][0]["text"])
        self.assertIn("errore uso", r["result"]["content"][0]["text"])

    def test_un_tool_che_funziona_restituisce_il_suo_stdout(self):
        r = chiama("validate_prosa", {"files": "README.md"})
        self.assertFalse(r["result"]["isError"])
        self.assertIn("validate_prosa", r["result"]["content"][0]["text"])


class TestAderenzaAlManifest(unittest.TestCase):
    def test_il_comando_si_deriva_da_path_non_da_invocation(self):
        # `invocation` e' un esempio per gli umani: mescola il comando con
        # segnaposto e flag di comodo (`MANIFEST.json`, `<cartella>`, `--all`).
        # Passarla verbatim vorrebbe dire lanciare `--all` che nessuno ha chiesto.
        t = M.carica()["export_booklet_typst"]
        self.assertIn("--all", t["invocation"])
        argv = M.costruisci(t, {"manifest": "README.md"})
        self.assertNotIn("--all", argv)
        self.assertNotIn("MANIFEST.json", argv)

    def test_le_chiavi_dello_schema_sono_quelle_dell_emettitore(self):
        # Due regole per lo stesso nome sono due regole, e una invecchia.
        import tools_manifest as TM
        emesso = {t["name"]: set(t["inputSchema"]["properties"])
                  for t in json.loads(TM.emit_mcp(
                      json.loads((REPO / "scripts" / "tools.manifest.json").read_text(
                          encoding="utf-8"))))["tools"]}
        for nome, t in M.carica().items():
            self.assertEqual(set(M.descrittore(nome, t)["inputSchema"]["properties"]),
                             emesso[nome], nome)

    def test_ogni_tool_esposto_esiste_su_disco(self):
        for nome, t in M.carica().items():
            self.assertTrue((REPO / t["path"]).is_file(), f"{nome}: {t['path']}")


if __name__ == "__main__":
    unittest.main()
