"""Controller Models of Comments."""

from datetime import datetime

from pydantic import BaseModel, RootModel

from server.model_utils import ObjectIdRaw, SelfIdRaw


class DbComment(BaseModel):
    """Comment database schema."""

    id: SelfIdRaw
    content: str
    author: ObjectIdRaw
    post: ObjectIdRaw
    creation_time: datetime
    modification_time: datetime


class DbCommentNotFoundError(Exception):
    """Comment does not exist in the database."""


DbCommentList = RootModel[list[DbComment]]
"""List of database comments."""
