"""Scelta del rasterizzatore in export_map_png.py (Inkscape / browser).

Il test non ha bisogno di Inkscape ne' di Chromium installati: usa due binari
finti che scrivono un PNG minimo e registrano gli argomenti ricevuti. Quello
che si vuole bloccare e' il *contratto* — quale motore vince in `auto`, quali
flag riceve Inkscape (dimensioni in uscita, non viewport), e la degradazione
pulita quando non c'e' niente da usare (ADR-0012).
"""
import contextlib
import importlib.util
import io
import os
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOOL = REPO / "scripts" / "export_map_png.py"

spec = importlib.util.spec_from_file_location("export_map_png", TOOL)
emp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(emp)

# PNG 1x1 valido: basta che il file esista e sia scrivibile dal binario finto.
PNG_1PX = bytes.fromhex(
    "89504e470d0a1a0a0000000d494844520000000100000001080600000"
    "01f15c4890000000a49444154789c6300010000050001"
    "0d0a2db40000000049454e44ae426082"
)

SVG_MIN = '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"></svg>'


def stub_binary(path: Path, log: Path, out_flag: str) -> Path:
    """Finto rasterizzatore: scrive gli argv in `log` e un PNG dove gli e' detto."""
    path.write_text(
        f"#!{sys.executable}\n"
        "import sys, pathlib\n"
        f"log = pathlib.Path({str(log)!r})\n"
        "log.write_text('\\n'.join(sys.argv[1:]), encoding='utf-8')\n"
        "out = None\n"
        "for a in sys.argv[1:]:\n"
        f"    if a.startswith({out_flag!r}):\n"
        f"        out = a[len({out_flag!r}):]\n"
        "if out:\n"
        f"    pathlib.Path(out).write_bytes({PNG_1PX!r})\n"
        "sys.exit(0)\n",
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


class TestRendererChoice(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp = Path(tempfile.mkdtemp())
        self.svg = self.tmp / "mappa.svg"
        self.svg.write_text(SVG_MIN, encoding="utf-8")
        self.out = self.tmp / "mappa.png"
        self.log = self.tmp / "argv.txt"

    def run_tool(self, *extra, env_extra=None):
        env = dict(os.environ)
        # niente ereditarieta' accidentale dai binari veri della macchina
        env.pop("MAP_PNG_BROWSER", None)
        env.pop("MAP_PNG_INKSCAPE", None)
        env["PATH"] = str(self.tmp)  # solo i finti sono raggiungibili
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [sys.executable, str(TOOL), str(self.svg), "-o", str(self.out), *extra],
            capture_output=True, text=True, env=env,
        )

    def test_auto_prefers_inkscape(self):
        ink = stub_binary(self.tmp / "inkscape", self.log, "--export-filename=")
        stub_binary(self.tmp / "chromium", self.tmp / "browser.txt", "--screenshot=")
        res = self.run_tool(env_extra={"MAP_PNG_INKSCAPE": str(ink)})
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("motore inkscape", res.stdout)
        self.assertFalse((self.tmp / "browser.txt").exists(),
                         "in auto il browser non deve essere invocato se c'e' Inkscape")

    def test_inkscape_gets_output_size_not_viewport(self):
        ink = stub_binary(self.tmp / "inkscape", self.log, "--export-filename=")
        res = self.run_tool("--scale", "3", env_extra={"MAP_PNG_INKSCAPE": str(ink)})
        self.assertEqual(res.returncode, 0, res.stderr)
        argv = self.log.read_text(encoding="utf-8").splitlines()
        self.assertIn("--export-type=png", argv)
        self.assertIn(f"--export-filename={self.out}", argv)
        # 100x50 nell'SVG, scala 3 -> 300x150 in uscita
        self.assertIn("--export-width=300", argv)
        self.assertIn("--export-height=150", argv)

    def test_browser_forced_even_with_inkscape_present(self):
        ink = stub_binary(self.tmp / "inkscape", self.log, "--export-filename=")
        blog = self.tmp / "browser.txt"
        stub_binary(self.tmp / "chromium", blog, "--screenshot=")
        res = self.run_tool("--renderer", "browser",
                            env_extra={"MAP_PNG_INKSCAPE": str(ink),
                                       "MAP_PNG_BROWSER": str(self.tmp / "chromium")})
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("motore browser", res.stdout)
        self.assertIn("--headless", blog.read_text(encoding="utf-8").splitlines())


class TestCleanDegradation(unittest.TestCase):
    """Con le liste di candidati vuote nessun motore e' raggiungibile.

    In-process e non via subprocess: sulla macchina di CI un Chromium a
    percorso assoluto (`/opt/pw-browsers/chromium`) esiste comunque, e il
    test misurerebbe la macchina invece del codice.
    """

    def _no_binaries(self):
        return unittest.mock.patch.multiple(
            emp, INKSCAPE_CANDIDATES=[], BROWSER_CANDIDATES=[]
        )

    def test_auto_without_any_rasterizer(self):
        err = io.StringIO()
        with self._no_binaries(), contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as cm:
                emp.pick_renderer("auto", None, None)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("nessun rasterizzatore", err.getvalue())

    def test_missing_inkscape_names_the_binary(self):
        err = io.StringIO()
        with self._no_binaries(), contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as cm:
                emp.pick_renderer("inkscape", None, None)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Inkscape non trovato", err.getvalue())

    def test_missing_browser_names_the_binary(self):
        err = io.StringIO()
        with self._no_binaries(), contextlib.redirect_stderr(err):
            with self.assertRaises(SystemExit) as cm:
                emp.pick_renderer("browser", None, None)
        self.assertEqual(cm.exception.code, 1)
        self.assertIn("Chromium/Chrome", err.getvalue())


if __name__ == "__main__":
    unittest.main()
