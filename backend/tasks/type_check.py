#!/usr/bin/env python
"""Run Pyright type checker on the source code."""

from os import execvp
from pathlib import Path
from sys import argv

from __init__ import root

execvp(
    "pnpm",  # noqa: S607
    [
        "pnpm",
        "dlx",
        "pyright",
        "-v",
        ".venv",
        "-p",
        ".",
        *Path(root).glob("*.py"),
        *Path(root).glob("server/**/*.py"),
        *Path(root).glob("tasks/**/*.py"),
        *argv,
    ],
)
