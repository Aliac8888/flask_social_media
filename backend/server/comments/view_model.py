from pydantic import BaseModel, RootModel

from server.model_utils import Instant, ObjectIdStr, SelfIdStr
from server.users.view_model import User


class Comment(BaseModel):
    id: SelfIdStr
    content: str
    author: User
    post: ObjectIdStr
    creation_time: Instant
    modification_time: Instant


class CommentInit(BaseModel):
    content: str
    author: ObjectIdStr
    post: ObjectIdStr


class CommentPatch(BaseModel):
    content: str


class CommentId(BaseModel):
    comment_id: ObjectIdStr


class CommentNotFound(BaseModel):
    type: str = "CommentNotFound"
    message: str = "Comment not found"


CommentsList = RootModel[list[Comment]]
