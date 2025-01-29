#!/usr/bin/env python
from os import execvp
from pathlib import Path
from sys import argv

import __init__  # noqa: F401

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
        *Path().glob("*.py"),
        *Path("server").glob("**/*.py"),
        *Path("tasks").glob("**/*.py"),
        *argv,
    ],
)
