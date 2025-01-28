from json import dumps
from sys import stdout

import __init__  # noqa: F401

from controllers.user import get_all_users

stdout.write("digraph U {\n")

for i in get_all_users().root:
    name = dumps(str(i.id))
    label = dumps(f"{i.id}\n{i.name}\n{i.email}")

    stdout.write(f"{name} [label={label}];\n")

    for j in i.followings:
        stdout.write(f"{name} -> {dumps(str(j))};\n")

stdout.write("}\n")
