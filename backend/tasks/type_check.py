from os import chdir, execvp
from pathlib import Path
from sys import argv

chdir(Path(__file__).parent.parent)
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
        *Path("controllers").glob("**/*.py"),
        *Path("models").glob("**/*.py"),
        *Path("routes").glob("**/*.py"),
        *Path("server").glob("**/*.py"),
        *Path("tasks").glob("**/*.py"),
        *argv,
    ],
)
