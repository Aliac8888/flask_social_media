import sys
from app import app
from models.user import UserInit
from db import USER_NOT_FOUND, client, db
from config import (
    maintenance,
    db_root_user,
    db_backend_user,
    db_backend_pass,
    admin_email,
    admin_pass,
)
from pymongo.errors import OperationFailure

if not maintenance:
    print(
        "Cannot setup the database without maintenance mode.",
        "Set SOCIAL_BE_MAINTENANCE=1 before running this script.",
    )
    sys.exit(1)

if db_backend_user == db_root_user:
    print(
        "During setup, backend username should not be the same as the root username.",
        "Set SOCIAL_BE_DB_USER and SOCIAL_BE_DB_PASS accordingly.",
    )
    sys.exit(2)

client.drop_database(db, comment="Setup")

try:
    client.admin.command(
        "dropUser",
        db_backend_user,
        comment="Setup",
    )
except OperationFailure as e:
    if e.code != USER_NOT_FOUND:
        raise

client.admin.command(
    "createUser",
    db_backend_user,
    pwd=db_backend_pass,
    roles=[
        {
            "role": "readWrite",
            "db": db.name,
        },
    ],
    comment="Setup",
)

db.users.create_index("email", unique=True)

with app.test_client() as c:
    c.post(
        "/users/",
        json=UserInit(
            name="Admin",
            email=admin_email,
            password=admin_pass,
        ).model_dump(),
    )
