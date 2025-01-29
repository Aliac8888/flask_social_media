#!/usr/bin/env python
import sys
from logging import getLogger

import __init__  # noqa: F401
from pymongo.errors import OperationFailure

from server.auth.controller import signup
from server.config import (
    admin_email,
    admin_pass,
    db_backend_pass,
    db_backend_user,
    db_root_user,
    maintenance,
)
from server.db import USER_NOT_FOUND, client, db

logger = getLogger(__name__)


def setup() -> None:
    if not maintenance:
        logger.critical(
            "Cannot setup the database without maintenance mode. "
            "Set SOCIAL_BE_MAINTENANCE=1 before running this script.",
        )
        sys.exit(1)

    if db_backend_user == db_root_user:
        logger.critical(
            "During setup, backend username should not be the same as the root "
            "username. Set SOCIAL_BE_DB_USER and SOCIAL_BE_DB_PASS accordingly.",
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

    signup(
        name="Admin",
        email=admin_email,
        password=admin_pass,
    )


if __name__ == "__main__":
    setup()
