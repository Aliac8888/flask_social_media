from pydantic import BaseModel
from models.mongo import ObjectIdStr, SelfIdStr
from models.datetime import DateTime


class Comment(BaseModel):
    id: SelfIdStr
    content: str
    author: ObjectIdStr
    post: ObjectIdStr
    creation_time: DateTime
    modification_time: DateTime


class CommentInit(BaseModel):
    content: str
    author: ObjectIdStr
    post: ObjectIdStr


class CommentPatch(BaseModel):
    content: str


class CommentId(BaseModel):
    comment_id: ObjectIdStr


class CommentNotFound(BaseModel):
    message: str = "Comment not found"


class CommentsList(BaseModel):
    comments: list[Comment]
