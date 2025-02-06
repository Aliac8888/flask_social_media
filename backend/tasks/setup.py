#!/usr/bin/env python
"""Setup/reset the database for initial use."""

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

_logger = getLogger(__name__)


def setup() -> None:
    """Setup/reset the database for initial use."""
    if not maintenance:
        _logger.critical("Cannot setup the database without maintenance mode.")
        _logger.warning("Set SOCIAL_BE_MAINTENANCE=1 before running this task.")
        _logger.info(
            "Maintenance mode will allow the backend to use the root password when "
            "authenticating with the database."
        )
        _logger.info(
            "This means that certain operations, like creating users, defining roles, "
            "or accessing all collections are allowed."
        )
        _logger.info(
            "These operations are necessary when setting up the database, therefore "
            "the setup task requires the maintenance mode."
        )
        sys.exit(1)

    if db_backend_user == db_root_user:
        _logger.critical(
            "During setup, backend username should not be the same as the root "
            "username."
        )
        _logger.warning("Set SOCIAL_BE_DB_USER and SOCIAL_BE_DB_PASS accordingly.")
        _logger.info(
            "During setup, the root username and password are used for database "
            "authentication."
        )
        _logger.info(
            "The setup task will create a user with the regular username and password."
        )
        _logger.info(
            "Ideally, we would want the backend user to have as minimal access to the "
            "database as possible."
        )
        _logger.info("But, the root username and password always has full permissions.")
        _logger.info("Therefore, the setup task disallows the two to be the same.")
        sys.exit(2)

    _logger.info("Dropping the social media database...")
    client.drop_database(db, comment="Setup")
    _logger.info("\tDone.")

    try:
        _logger.info("Dropping the backend user...")

        client.admin.command("dropUser", db_backend_user, comment="Setup")

        _logger.info("\tDone.")
    except OperationFailure as e:
        if e.code != USER_NOT_FOUND:
            raise

        _logger.info("\tBackend user did not exist.")

    _logger.info("Creating the backend user...")

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

    _logger.info("\tDone.")
    _logger.info("Creating database indexes...")

    db.users.create_index("email", unique=True)

    _logger.info("\tDone.")
    _logger.info("Creating the admin user...")

    signup(
        name="Admin",
        email=admin_email,
        password=admin_pass,
    )

    _logger.info("\tDone.")


if __name__ == "__main__":
    setup()
