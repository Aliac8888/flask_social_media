from os import chdir
from pathlib import Path
from sys import path

root = Path(__file__).parent.parent
chdir(root)
path.append(str(root))
