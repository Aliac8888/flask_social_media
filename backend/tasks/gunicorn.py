from os import execv
from sys import argv

import __init__  # noqa: F401

from server.config import be_host, be_port

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
