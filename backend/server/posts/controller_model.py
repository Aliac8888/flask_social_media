"""Controller models for Posts."""

from datetime import datetime

from pydantic import BaseModel, RootModel

from server.model_utils import SelfIdRaw
from server.users.controller_model import DbUser


class DbPost(BaseModel):
    """Post database schema."""

    id: SelfIdRaw
    content: str
    creation_time: datetime
    modification_time: datetime
    author: DbUser


class DbPostNotFoundError(Exception):
    """Post does not exist in the database."""


DbPostList = RootModel[list[DbPost]]
"""List of database posts."""
