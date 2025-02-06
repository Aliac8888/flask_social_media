"""Database."""

from typing import Any
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor

from server.config import db_host, db_pass, db_port, db_user

USER_NOT_FOUND = 11
"""Database user does not exist."""

DUPLICATE_KEY = 11000
"""This database operation violates a unique index."""

client = MongoClient(
    f"mongodb://{quote_plus(db_user)}:{quote_plus(db_pass)}@{db_host}:{db_port}/",
)
"""Database client."""

db = client["social_media"]
"""Database."""


def get_one[T: dict[str, Any]](cursor: CommandCursor[T]) -> T | None:
    """Get one document from a cursor.

    Args:
        cursor (CommandCursor): Database cursor to be consumed.

    Returns:
        T: Single document entry.

    """
    for result in cursor:
        return result

    return None
