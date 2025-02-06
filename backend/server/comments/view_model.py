"""Models of Comments API."""

from pydantic import BaseModel, RootModel

from server.model_utils import Instant, ObjectIdStr, SelfIdStr
from server.users.view_model import User


class Comment(BaseModel):
    """Comment."""

    id: SelfIdStr
    content: str
    author: User
    post: ObjectIdStr
    creation_time: Instant
    modification_time: Instant


class CommentInit(BaseModel):
    """Comment to be created."""

    content: str
    author: ObjectIdStr
    post: ObjectIdStr


class CommentPatch(BaseModel):
    """Comment modification."""

    content: str | None


class CommentId(BaseModel):
    """Id of a comment."""

    comment_id: ObjectIdStr


class CommentNotFound(BaseModel):
    """Request refers to a comment which does not exist."""

    type: str = "CommentNotFound"
    message: str = "Comment not found"


CommentsList = RootModel[list[Comment]]
"""List of comments."""
