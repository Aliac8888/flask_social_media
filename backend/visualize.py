from json import dumps
from sys import stdout

from db import db

stdout.write("digraph U {\n")

for i in db.users.find({}):
    name = dumps(str(i["_id"]))
    label = dumps(f"{i['_id']}\n{i['name']}\n{i['email']}")

    stdout.write(f"{name} [label={label}];\n")

    for j in i["followings"]:
        stdout.write(f"{name} -> {dumps(str(j))};\n")

stdout.write("}\n")
