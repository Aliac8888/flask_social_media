from json import dumps
from db import db

print("digraph U {")

for i in db.users.find({}):
    print(
        f'{dumps(str(i["_id"]))} [label={dumps(f"{i["_id"]}\n{i["name"]}\n{i["email"]}")}];'
    )

    for j in i["followings"]:
        print(f'{dumps(str(i["_id"]))} -> {dumps(str(j))};')

print("}")
