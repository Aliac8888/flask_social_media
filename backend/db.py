from typing import Any
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor

from config import db_host, db_pass, db_port, db_user

USER_NOT_FOUND = 11
DUPLICATE_KEY = 11000

client = MongoClient(
    f"mongodb://{quote_plus(db_user)}:{quote_plus(db_pass)}@{db_host}:{db_port}/",
)

db = client["social_media"]


def get_one[T: dict[str, Any]](cursor: CommandCursor[T]) -> T | None:
    for result in cursor:
        return result

    return None
