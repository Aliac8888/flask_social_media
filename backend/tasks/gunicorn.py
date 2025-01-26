import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from os import chdir, execv
from pathlib import Path
from sys import argv

from server.config import be_host, be_port

chdir(Path(__file__).parent.parent)
execv(
    ".venv/bin/gunicorn",
    [
        "gunicorn",
        "-b",
        f"{be_host}:{be_port}",
        *argv[1:],
        "server.app:create_app()",
    ],
)
