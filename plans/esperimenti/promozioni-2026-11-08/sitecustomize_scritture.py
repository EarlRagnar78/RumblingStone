"""Audit hook: chi scrive nel repo vero mentre gira la suite (ricetta in MISURE.md).

Uso, dalla radice del repo:
    D=$(mktemp -d); cp plans/esperimenti/promozioni-2026-11-08/sitecustomize_scritture.py $D/sitecustomize.py
    SCRITTURE_REPO=$PWD SCRITTURE_LOG=$D/scritture.log PYTHONPATH=$D python -m pytest scripts/tests -q
Ogni riga del log: il test in corso (PYTEST_CURRENT_TEST) e il file scritto.
Falsi positivi noti: chi cancella un symlink che punta nel repo (test_new_group,
test_gruppo_nuovo) e i nomi relativi a un dir_fd che non si risolve (tmpXXXXXXXX).
"""
import os, sys
_REPO = os.path.realpath(os.environ.get("SCRITTURE_REPO", "."))
_LOG = os.environ.get("SCRITTURE_LOG", "/tmp/scritture.log")
_SKIP = (os.path.join(_REPO, ".git"), os.path.join(_REPO, ".pytest_cache"))
def _note(path, dir_fd=None):
    try:
        path = os.fsdecode(path)
        if dir_fd is not None and not os.path.isabs(path):
            path = os.path.join(os.readlink(f"/proc/self/fd/{dir_fd}"), path)
        p = os.path.realpath(path)
    except Exception:
        return
    if not p.startswith(_REPO + os.sep) or p.startswith(_SKIP) or "__pycache__" in p:
        return
    t = os.environ.get("PYTEST_CURRENT_TEST", "?")
    with open(_LOG, "a") as f:  # fuori dal repo, non ricorsivo
        f.write(f"{t}\t{p}\n")
def _hook(ev, args):
    if ev == "open":
        path, mode, flags = args
        if isinstance(path, int): return
        w = (mode and any(c in mode for c in "wax+")) or (flags is not None and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT))
        if w:
            if not os.path.isabs(os.fsdecode(path)):
                t = os.environ.get("PYTEST_CURRENT_TEST", "?")
                with open(_LOG.replace(".log", "-relativi.log"), "a") as f:
                    f.write(f"{t}\t{os.getcwd()}\t{os.fsdecode(path)}\n")
            _note(path)
    elif ev in ("os.rename", "os.replace"):
        _note(args[1])
    elif ev in ("os.remove", "os.rmdir"):
        _note(args[0], args[1])
    elif ev == "os.mkdir":
        _note(args[0], args[2])
    elif ev == "shutil.rmtree":
        _note(args[0], args[1])
sys.addaudithook(_hook)
