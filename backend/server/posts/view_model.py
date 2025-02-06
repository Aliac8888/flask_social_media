"""Models for Posts API."""

from pydantic import BaseModel, RootModel

from server.model_utils import Instant, ObjectIdStr, SelfIdStr
from server.users.view_model import User


class Post(BaseModel):
    """Post."""

    id: SelfIdStr
    content: str
    creation_time: Instant
    modification_time: Instant
    author: User


class PostInit(BaseModel):
    """Post to be created."""

    content: str
    author: ObjectIdStr


class PostPatch(BaseModel):
    """Post modification."""

    content: str


class PostId(BaseModel):
    """Id of a post."""

    post_id: ObjectIdStr


class PostNotFound(BaseModel):
    """Request refers to a post which does not exist."""

    type: str = "PostNotFound"
    message: str = "Post not found"


PostsList = RootModel[list[Post]]
"""List of posts."""
