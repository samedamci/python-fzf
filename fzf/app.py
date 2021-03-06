from __future__ import annotations
from subprocess import Popen, PIPE
from collections import namedtuple
from typing import Iterable, Optional, List
import sys

Result = namedtuple("Result", ["index", "output"])
EXE = "fzf.exe" if sys.platform == "win32" else "fzf"
ENC = sys.getdefaultencoding()


def fzf(
    iterable: Iterable,
    prompt: Optional[str] = None,
    query: Optional[str] = None,
    multi: bool = False,
    cycle: bool = False,
    mouse: bool = True,
    sort: bool = False,
    reverse: bool = False,
    ansi: bool = True,
    bold: bool = True,
    options: Optional[str] = None,
) -> List[Result]:
    cmd = [EXE, "--with-nth=2.."]
    if prompt:
        cmd.append(f"--prompt={prompt.strip()} ")
    if query:
        cmd.append(f"--query={query}")
    if multi:
        cmd.append("--multi")
    if cycle:
        cmd.append("--cycle")
    if not mouse:
        cmd.append("--no-mouse")
    if not sort:
        cmd.append("--no-sort")
    if reverse:
        cmd.append("--tac")
    if ansi:
        cmd.append("--ansi")
    if not bold:
        cmd.append("--no-bold")
    if options:
        cmd += options.split(" ")

    proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=None)
    stdin = proc.stdin
    stdout = proc.stdout

    for i, el in enumerate(iterable):
        line = f"{i} {el}"
        stdin.write(line.encode(ENC) + b"\n")

    stdin.flush()
    stdin.close()
    proc.wait()

    results = []
    for ln in stdout.readlines():
        sel = str(ln.strip(), encoding=ENC).split(" ", 1)
        results.append(Result(int(sel[0]), sel[1]))

    return results
