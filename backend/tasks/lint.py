from os import chdir, execv
from pathlib import Path
from sys import argv

chdir(Path(__file__).parent.parent)
execv(".venv/bin/ruff", ["ruff", "check", *argv[1:]])
